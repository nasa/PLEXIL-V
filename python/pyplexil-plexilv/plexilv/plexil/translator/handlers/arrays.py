"""Array operation translation handlers"""

from ..dispatch import translate, walk
from plexilv.common import IndentedWriter
from ..state import TranspilerContext
from ._helpers import *
from plexil.core.v1 import *


@translate.register(ArrayElement)
def _(node: ArrayElement, writer: IndentedWriter, context: TranspilerContext):
    """Translate array element access."""
    writer.write("arrayVar(")

    # With compound fields, the array is in node.choice
    if node.choice:
        if isinstance(node.choice, str):
            # Plain string name (from <Name> element)
            # Variable names preserve underscores (unlike node IDs which use hyphens)
            writer.write(f"'{node.choice}")
        elif isinstance(node.choice, ArrayVariable):
            writer.write(f"'{node.choice.value}")
        else:
            # ArrayValue, Lookup, etc.
            walk(node.choice, writer, context)

    writer.write(",")

    # Get the index - Index has a choice field with the numeric expression
    if node.index and node.index.choice:
        walk(node.index.choice, writer, context)

    writer.write(")")


@translate.register(ArraySize)
def _(node: ArraySize, writer: IndentedWriter, context: TranspilerContext):
    """Translate array size operation."""
    writer.write("arraySize(")

    # With compound fields, the array is in node.choice
    if node.choice:
        walk(node.choice, writer, context)

    writer.write(")")


@translate.register(ArrayMaxSize)
def _(node: ArrayMaxSize, writer: IndentedWriter, context: TranspilerContext):
    """Translate array max size operation."""
    writer.write("arrayMaxSize(")

    # With compound fields, the array is in node.choice
    if node.choice:
        walk(node.choice, writer, context)

    writer.write(")")


@translate.register(Index)
def _(node: Index, writer: IndentedWriter, context: TranspilerContext):
    """Translate array index expression."""
    # With compound fields, Index has a choice field with the numeric expression
    if node.choice:
        walk(node.choice, writer, context)
