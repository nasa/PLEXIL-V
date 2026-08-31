"""PLEXIL to PLEXIL-V Maude translator."""

from plexil.core.v1 import PlexilPlan
from plexilv.common import IndentedWriter
from .state import TranspilerContext
from .dispatch import walk


def translate(
    plan: PlexilPlan,
    libraries: dict[str, PlexilPlan] | None = None,
    indent_str: str = "  ",
) -> str:
    """
    Translate a PLEXIL plan to PLEXIL-V format.

    Args:
        plan: The main PLEXIL plan to translate
        libraries: Optional dict mapping library names to PlexilPlan ASTs.
                   Used to resolve LibraryNodeCall references.
        indent_str: String to use for each indentation level

    Returns:
        The translated output as a string
    """
    # Import handlers lazily to avoid circular import issues
    from . import handlers  # noqa: F401

    libraries = libraries or {}

    # Create writer and context
    writer = IndentedWriter(indent_str=indent_str)
    context = TranspilerContext(libraries=libraries)

    # Walk and translate the AST
    walk(plan, writer, context)

    # Get output
    return writer.get_output()


__all__ = ["translate"]
