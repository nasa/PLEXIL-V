"""PLEXILScript to PLEXIL-V Maude translator."""

from plexil.plexilscript.v1 import PLEXILScript
from plexilv.common import IndentedWriter
from .dispatch import walk

# Import handlers to register them
from . import handlers  # noqa: F401


def translate(script: PLEXILScript, indent_str: str = "  ") -> str:
    """
    Translate a PLEXILScript AST to PLEXIL-V Maude format.

    Args:
        script: The PLEXILScript root node
        indent_str: String to use for each indentation level

    Returns:
        String containing the Maude INPUT module
    """
    writer = IndentedWriter(indent_str=indent_str)
    walk(script, writer)
    return writer.get_output().strip()


__all__ = ["translate"]
