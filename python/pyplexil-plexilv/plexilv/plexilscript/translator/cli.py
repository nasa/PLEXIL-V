#!/usr/bin/env python3
"""
PLEXILScript to Maude translator CLI.

Reads a PLEXILScript XML file and outputs the PLEXIL-V Maude INPUT module.
"""

import sys
import click
from pathlib import Path
from xsdata.formats.dataclass.parsers import XmlParser

from plexil.plexilscript.v1 import PLEXILScript
from plexilv.common import create_parser
from . import translate


def parse_plexilscript(xml_content: str, parser: XmlParser) -> PLEXILScript:
    """
    Parse PLEXILScript XML content into AST.

    Args:
        xml_content: The XML content as a string
        parser: The xsdata XML parser

    Returns:
        Parsed PLEXILScript object
    """
    script = parser.from_string(xml_content, PLEXILScript)
    return script


@click.command(name='psx2maude')
@click.argument(
    'input_file',
    type=click.Path(exists=True, dir_okay=False, path_type=Path),
)
@click.option(
    '--indent',
    type=int,
    default=2,
    help='Number of spaces for indentation (default: 2)',
)
def main(input_file: Path, indent: int):
    """Transpile PLEXILScript XML to PLEXIL-V Maude format.

    INPUT_FILE is the path to the PLEXILScript XML file (.psx)

    \b
    Examples:
      psx2maude script.psx > output.maude
      psx2maude --indent 4 script.psx
    """
    # Read input file
    try:
        xml_content = input_file.read_text(encoding="utf-8")
    except Exception as e:
        raise click.ClickException(f"Error reading input file: {e}")

    # Create parser
    xml_parser = create_parser()

    # Parse PLEXILScript
    try:
        script = parse_plexilscript(xml_content, xml_parser)
    except Exception as e:
        raise click.ClickException(f"Error parsing PLEXILScript XML: {e}")

    # Translate to Maude
    try:
        indent_str = " " * indent
        output = translate(script, indent_str=indent_str)
    except Exception as e:
        raise click.ClickException(f"Error translating to Maude: {e}")

    # Output result
    click.echo(output)


if __name__ == "__main__":
    main()
