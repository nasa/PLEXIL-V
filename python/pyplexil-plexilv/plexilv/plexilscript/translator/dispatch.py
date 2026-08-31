"""Base translation infrastructure for PLEXILScript using singledispatch."""

from functools import singledispatch
from typing import Any
from plexilv.common import IndentedWriter


@singledispatch
def translate(node: Any, writer: IndentedWriter):
    """
    Base translation dispatcher. Override for specific types.
    Default: do nothing for unknown types.
    """
    pass


def walk(node: Any, writer: IndentedWriter):
    """
    Walk the AST, handling None, lists, and single objects.
    Triggers the translate dispatch for non-None single objects.
    """
    if node is None:
        return

    if isinstance(node, list):
        for item in node:
            walk(item, writer)
    else:
        translate(node, writer)
