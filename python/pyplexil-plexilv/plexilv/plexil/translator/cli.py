#!/usr/bin/env python3
"""plx2maude: Transpile PLEXIL XML to PLEXIL-V format.

Usage: plx2maude <input.plx>

This script parses a PLEXIL XML file and all its library dependencies
(assumed to be in the same directory), then transpiles to PLEXIL-V format.
"""

import sys
import click
from pathlib import Path
from typing import Any
import xml.etree.ElementTree as ET
from xsdata.formats.dataclass.parsers import XmlParser

from plexil.core.v1.ast import PlexilPlan, LibraryNodeCall, Node
from plexilv.common import IndentedWriter, create_parser
from .state import TranspilerContext
from .dispatch import walk


def parse_plexil_plan(xml_content: str, parser: XmlParser) -> tuple[PlexilPlan, str]:
    """Parse PLEXIL XML and properly construct PlexilPlan with Node node.

    The xsdata parser doesn't automatically parse the Node element as Node,
    so we need to extract it and re-parse it.

    Args:
        xml_content: XML content as string
        parser: XmlParser instance to use

    Returns:
        Tuple of (PlexilPlan with properly parsed Node, root node ID)
    """
    # Parse XML with ElementTree to extract the Node element
    root = ET.fromstring(xml_content)
    node_elem = root.find(".//Node")

    if node_elem is None:
        # No node element, return empty PlexilPlan
        return PlexilPlan(), "UNKNOWN"

    # Extract NodeId for module name
    node_id_elem = node_elem.find("NodeId")
    if node_id_elem is not None and node_id_elem.text:
        node_id = node_id_elem.text
    else:
        node_id = "UNKNOWN"

    # Convert Node element to string
    node_xml = ET.tostring(node_elem, encoding="unicode")

    # Parse as Node and wrap in PlexilPlan
    node = parser.from_string(node_xml, Node)
    return PlexilPlan(node=node), node_id


def find_library_dependencies(node: Any) -> set[str]:
    """Recursively find all library names referenced in the AST.

    Args:
        node: Root node to scan for library dependencies

    Returns:
        Set of library names (strings) found in LibraryNodeCall nodes
    """
    library_names = set()
    visited = set()

    def visit(obj):
        """Recursively visit all nodes in the AST."""
        if obj is None:
            return

        # Avoid infinite loops by tracking visited objects
        obj_id = id(obj)
        if obj_id in visited:
            return
        visited.add(obj_id)

        # If this is a LibraryNodeCall, extract the library name
        if isinstance(obj, LibraryNodeCall):
            if obj.node_id and obj.node_id.value:
                library_names.add(obj.node_id.value)

        # Recursively visit all fields
        if hasattr(obj, "__dict__"):
            for value in obj.__dict__.values():
                if isinstance(value, list):
                    for item in value:
                        visit(item)
                else:
                    visit(value)

    visit(node)
    return library_names


def validate_library_name(lib_name: str, plan_dir: Path) -> tuple[bool, str | None]:
    """Validate a library name for security and construct its safe path.

    Ensures library names don't contain path traversal attempts or
    special characters that could be used for injection attacks.

    Args:
        lib_name: The library name to validate
        plan_dir: The directory where libraries are stored

    Returns:
        Tuple of (is_valid, error_message). If valid, error_message is None.
        If invalid, error_message describes the validation failure.
    """
    # Library names should only contain alphanumeric, hyphens, and underscores
    safe_chars = lib_name.replace("-", "").replace("_", "")
    if not safe_chars.isalnum():
        return (
            False,
            f"Invalid library name '{lib_name}' "
            f"(must contain only alphanumeric, hyphens, and underscores)",
        )

    # Construct the library path
    lib_path = plan_dir / f"{lib_name}.plx"

    # Ensure the resolved path is still within plan_dir (prevent directory traversal)
    try:
        resolved_lib_path = lib_path.resolve()
        resolved_plan_dir = plan_dir.resolve()
        if not resolved_lib_path.is_relative_to(resolved_plan_dir):
            return (False, f"Library path '{lib_name}' escapes plan directory")
    except (ValueError, OSError) as e:
        return (False, f"Invalid library path '{lib_name}': {e}")

    return (True, None)


def load_libraries(
    plan_dir: Path, initial_plan: PlexilPlan, parser: XmlParser
) -> dict[str, PlexilPlan]:
    """Load all library dependencies recursively.

    Starting from the initial plan, finds all LibraryNodeCall references,
    loads the corresponding .plx files, and recursively processes transitive
    dependencies.

    Args:
        plan_dir: Directory containing the plan and library files
        initial_plan: The main plan to scan for dependencies
        parser: XML parser instance

    Returns:
        Dictionary mapping library names to PlexilPlan ASTs
    """
    libraries = {}
    to_process = find_library_dependencies(initial_plan)
    processed = set()

    while to_process:
        lib_name = to_process.pop()

        if lib_name in processed:
            continue

        processed.add(lib_name)

        # Validate library name for security
        is_valid, error_msg = validate_library_name(lib_name, plan_dir)
        if not is_valid:
            click.echo(f"Warning: {error_msg}", err=True)
            continue

        # Try to load the library file
        lib_path = plan_dir / f"{lib_name}.plx"

        if not lib_path.exists():
            click.echo(f"Warning: Library file not found: {lib_path}", err=True)
            continue

        try:
            with open(lib_path, "r") as f:
                lib_plan, _ = parse_plexil_plan(
                    f.read(), parser
                )  # Ignore NodeId for libraries
                libraries[lib_name] = lib_plan

                # Find transitive dependencies
                transitive_deps = find_library_dependencies(lib_plan)
                for dep in transitive_deps:
                    if dep not in processed:
                        to_process.add(dep)

        except Exception as e:
            click.echo(f"Error loading library {lib_name}: {e}", err=True)
            continue

    return libraries


@click.command(name='plx2maude')
@click.argument(
    'input',
    type=click.Path(exists=True, dir_okay=False, path_type=Path),
)
@click.option(
    '--indent',
    type=int,
    default=2,
    help='Number of spaces for indentation (default: 2)',
)
def main(input: Path, indent: int):
    """Transpile PLEXIL XML to PLEXIL-V format.

    Parses a PLEXIL XML file and all its library dependencies
    (assumed to be in the same directory), then transpiles to PLEXIL-V format.

    INPUT is the path to the PLEXIL XML file (.plx)

    \b
    Examples:
      plx2maude plan.plx > output.maude
      plx2maude --indent 4 plan.plx
    """
    # Validate input file extension
    if input.suffix != ".plx":
        click.echo(f"Warning: Input file does not have .plx extension", err=True)

    # Parse the main plan
    xml_parser = create_parser()

    try:
        with open(input, "r") as f:
            main_plan, root_node_id = parse_plexil_plan(f.read(), xml_parser)
    except Exception as e:
        raise click.ClickException(f"Error parsing input file: {e}")

    # Load all library dependencies
    plan_dir = input.parent
    libraries = load_libraries(plan_dir, main_plan, xml_parser)

    # Translate the plan to PLEXIL-V format
    try:
        from . import translate

        indent_str = " " * indent
        plexilv_code = translate(main_plan, libraries=libraries, indent_str=indent_str).strip()

        # Wrap in Maude module format
        click.echo(f"mod {root_node_id}-PLAN is")
        click.echo()
        click.echo("protecting PLEXIL-V .")
        click.echo()
        click.echo("op rootNode : -> Plexil .")
        click.echo("eq rootNode =")
        click.echo()
        click.echo(plexilv_code)
        click.echo("  .")
        click.echo()
        click.echo("endm")
    except ValueError as e:
        raise click.ClickException(str(e))
    except Exception as e:
        raise click.ClickException(f"Error during translation: {e}")


if __name__ == "__main__":
    main()
