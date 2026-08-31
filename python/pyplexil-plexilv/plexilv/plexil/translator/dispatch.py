"""Base translation infrastructure using singledispatch."""

from functools import singledispatch
from typing import Any
from .state import TranspilerContext
from plexilv.common import IndentedWriter


@singledispatch
def translate(node: Any, writer: IndentedWriter, context: TranspilerContext):
    """
    Base translation dispatcher. Override for specific types.
    Default: do nothing for unknown types.
    """
    # Unknown type - could log a warning or raise an error
    pass


def walk(node: Any, writer: IndentedWriter, context: TranspilerContext):
    """
    Walk the AST, handling None, lists, and single objects.
    Triggers the translate dispatch for non-None single objects.
    """
    if node is None:
        # Safely handle None values
        return

    if isinstance(node, list):
        # Iterate over list elements
        for item in node:
            walk(item, writer, context)
    else:
        # Single object: push to context stack and translate
        context.push_node(node)
        translate(node, writer, context)
        context.pop_node()
