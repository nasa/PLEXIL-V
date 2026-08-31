"""Value and variable translation handlers"""

from ..dispatch import translate, walk
from plexilv.common import IndentedWriter
from ..state import TranspilerContext
from ._helpers import *
from plexil.core.v1 import *


@translate.register(IntegerValue)
def _(node: IntegerValue, writer: IndentedWriter, context: TranspilerContext):
    """Translate integer value."""
    writer.write(f"const(val({node.value}))")


@translate.register(RealValue)
def _(node: RealValue, writer: IndentedWriter, context: TranspilerContext):
    """Translate real value."""
    # Format as float, removing unnecessary trailing zeros
    val = float(node.value)
    # Use repr-like formatting to preserve precision but remove trailing zeros
    formatted = f"{val:g}" if "." in f"{val:g}" else f"{val:.1f}"
    writer.write(f"const(val({formatted}))")


@translate.register(BooleanValue)
def _(node: BooleanValue, writer: IndentedWriter, context: TranspilerContext):
    """Translate boolean value."""
    writer.write(f"const(val({str(node.value).lower()}))")


@translate.register(StringValue)
def _(node: StringValue, writer: IndentedWriter, context: TranspilerContext):
    """Translate string value."""
    escaped_value = escape_string(node.value)
    writer.write(f'const(val("{escaped_value}"))')


@translate.register(ArrayValue)
def _(node: ArrayValue, writer: IndentedWriter, context: TranspilerContext):
    """Translate array value.

    When used in assignment RHS, outputs: const(array(val(x)#val(y)#...))
    Note: Variable initialization uses DeclareArray handler which outputs createArray() directly.
    """
    # In compound fields, all values are in the choice list
    values = []

    for v in node.choice:
        if isinstance(v, IntegerValue):
            values.append(f"val({v.value})")
        elif isinstance(v, RealValue):
            values.append(f"val({float(v.value):.1f})")
        elif isinstance(v, BooleanValue):
            values.append(f"val({str(v.value).lower()})")
        elif isinstance(v, StringValue):
            escaped_value = escape_string(v.value)
            values.append(f'val("{escaped_value}")')

    # Format the array for assignment RHS
    if not values:
        # Empty array
        writer.write("const(array(emptyList))")
    else:
        # Array with values - wrap in const(array(...))
        array_content = " # ".join(values)
        writer.write(f"const(array({array_content}))")


@translate.register(IntegerVariable)
def _(node: IntegerVariable, writer: IndentedWriter, context: TranspilerContext):
    """Translate integer variable reference."""
    writer.write(f"var('{node.value})")


@translate.register(RealVariable)
def _(node: RealVariable, writer: IndentedWriter, context: TranspilerContext):
    """Translate real variable reference."""
    writer.write(f"var('{node.value})")


@translate.register(BooleanVariable)
def _(node: BooleanVariable, writer: IndentedWriter, context: TranspilerContext):
    """Translate boolean variable reference."""
    writer.write(f"var('{node.value})")


@translate.register(StringVariable)
def _(node: StringVariable, writer: IndentedWriter, context: TranspilerContext):
    """Translate string variable reference."""
    writer.write(f"var('{node.value})")


@translate.register(ArrayVariable)
def _(node: ArrayVariable, writer: IndentedWriter, context: TranspilerContext):
    """Translate array variable reference."""
    writer.write(f"var('{node.value})")
