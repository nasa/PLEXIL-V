"""Expression and operator translation handlers"""

from ..dispatch import translate, walk
from plexilv.common import IndentedWriter
from ..state import TranspilerContext
from ._helpers import *
from plexil.core.v1 import *


@translate.register(And)
def _(node: And, writer: IndentedWriter, context: TranspilerContext):
    """Translate AND operator."""
    operands = collect_operands(node)
    write_nary_operator("_and_", operands, writer, context)


@translate.register(Or)
def _(node: Or, writer: IndentedWriter, context: TranspilerContext):
    """Translate OR operator."""
    operands = collect_operands(node)
    write_nary_operator("_or_", operands, writer, context)


@translate.register(Xor)
def _(node: Xor, writer: IndentedWriter, context: TranspilerContext):
    """Translate XOR operator."""
    operands = collect_operands(node)
    write_nary_operator("_xor_", operands, writer, context)


@translate.register(Not)
def _(node: Not, writer: IndentedWriter, context: TranspilerContext):
    """Translate NOT operator."""
    operands = collect_operands(node)
    writer.write("not_(")
    walk(operands[0], writer, context)
    writer.write(")")


# Equality Operators


@translate.register(Eqboolean)
def _(node: Eqboolean, writer: IndentedWriter, context: TranspilerContext):
    """Translate EQBoolean operator."""
    operands = collect_operands(node)
    writer.write("_equ_(")
    walk(operands[0], writer, context)
    writer.write(",")
    walk(operands[1], writer, context)
    writer.write(")")


@translate.register(Neboolean)
def _(node: Neboolean, writer: IndentedWriter, context: TranspilerContext):
    """Translate NEBoolean operator."""
    operands = collect_operands(node)
    writer.write("_nequ_(")
    walk(operands[0], writer, context)
    writer.write(",")
    walk(operands[1], writer, context)
    writer.write(")")


@translate.register(Eqnumeric)
def _(node: Eqnumeric, writer: IndentedWriter, context: TranspilerContext):
    """Translate EQNumeric operator."""
    operands = collect_operands(node)
    writer.write("_equ_(")
    walk(operands[0], writer, context)
    writer.write(",")
    walk(operands[1], writer, context)
    writer.write(")")


@translate.register(Nenumeric)
def _(node: Nenumeric, writer: IndentedWriter, context: TranspilerContext):
    """Translate NENumeric operator."""
    operands = collect_operands(node)
    writer.write("_nequ_(")
    walk(operands[0], writer, context)
    writer.write(",")
    walk(operands[1], writer, context)
    writer.write(")")


@translate.register(Eqstring)
def _(node: Eqstring, writer: IndentedWriter, context: TranspilerContext):
    """Translate EQString operator."""
    operands = collect_operands(node)
    writer.write("_equ_(")
    walk(operands[0], writer, context)
    writer.write(",")
    walk(operands[1], writer, context)
    writer.write(")")


@translate.register(Nestring)
def _(node: Nestring, writer: IndentedWriter, context: TranspilerContext):
    """Translate NEString operator."""
    operands = collect_operands(node)
    writer.write("_nequ_(")
    walk(operands[0], writer, context)
    writer.write(",")
    walk(operands[1], writer, context)
    writer.write(")")


# Comparison Operators


@translate.register(Gt)
def _(node: Gt, writer: IndentedWriter, context: TranspilerContext):
    """Translate GT operator."""
    operands = collect_operands(node)
    writer.write("_>_(")
    walk(operands[0], writer, context)
    writer.write(",")
    walk(operands[1], writer, context)
    writer.write(")")


@translate.register(Lt)
def _(node: Lt, writer: IndentedWriter, context: TranspilerContext):
    """Translate LT operator."""
    operands = collect_operands(node)
    writer.write("_<_(")
    walk(operands[0], writer, context)
    writer.write(",")
    walk(operands[1], writer, context)
    writer.write(")")


@translate.register(Ge)
def _(node: Ge, writer: IndentedWriter, context: TranspilerContext):
    """Translate GE operator."""
    operands = collect_operands(node)
    writer.write("_>=_(")
    walk(operands[0], writer, context)
    writer.write(",")
    walk(operands[1], writer, context)
    writer.write(")")


@translate.register(Le)
def _(node: Le, writer: IndentedWriter, context: TranspilerContext):
    """Translate LE operator."""
    operands = collect_operands(node)
    writer.write("_<=_(")
    walk(operands[0], writer, context)
    writer.write(",")
    walk(operands[1], writer, context)
    writer.write(")")


# Arithmetic Operators


@translate.register(Add)
def _(node: Add, writer: IndentedWriter, context: TranspilerContext):
    """Translate ADD operator."""
    operands = collect_operands(node)
    write_nary_operator("_+_", operands, writer, context)


@translate.register(Sub)
def _(node: Sub, writer: IndentedWriter, context: TranspilerContext):
    """Translate SUB operator."""
    operands = collect_operands(node)
    write_nary_operator("_-_", operands, writer, context)


@translate.register(Mul)
def _(node: Mul, writer: IndentedWriter, context: TranspilerContext):
    """Translate MUL operator."""
    operands = collect_operands(node)
    write_nary_operator("_*_", operands, writer, context)


@translate.register(Div)
def _(node: Div, writer: IndentedWriter, context: TranspilerContext):
    """Translate DIV operator."""
    operands = collect_operands(node)
    writer.write("_/_(")
    walk(operands[0], writer, context)
    writer.write(",")
    walk(operands[1], writer, context)
    writer.write(")")


@translate.register(Mod)
def _(node: Mod, writer: IndentedWriter, context: TranspilerContext):
    """Translate MOD (remainder) operator."""
    operands = collect_operands(node)
    writer.write("_rem_(")
    walk(operands[0], writer, context)
    writer.write(",")
    walk(operands[1], writer, context)
    writer.write(")")


# Unary Numeric Functions


@translate.register(Abs)
def _(node: Abs, writer: IndentedWriter, context: TranspilerContext):
    """Translate ABS function."""
    operands = collect_operands(node)
    writer.write("func(absp,")
    walk(operands[0], writer, context)
    writer.write(")")


@translate.register(Sqrt)
def _(node: Sqrt, writer: IndentedWriter, context: TranspilerContext):
    """Translate SQRT function."""
    operands = collect_operands(node)
    writer.write("func(sqrt,")
    walk(operands[0], writer, context)
    writer.write(")")


@translate.register(Ceil)
def _(node: Ceil, writer: IndentedWriter, context: TranspilerContext):
    """Translate CEIL function."""
    operands = collect_operands(node)
    writer.write("func(ceiling,")
    walk(operands[0], writer, context)
    writer.write(")")


@translate.register(Floor)
def _(node: Floor, writer: IndentedWriter, context: TranspilerContext):
    """Translate FLOOR function."""
    operands = collect_operands(node)
    writer.write("func(floor,")
    walk(operands[0], writer, context)
    writer.write(")")


@translate.register(Round)
def _(node: Round, writer: IndentedWriter, context: TranspilerContext):
    """Translate ROUND function."""
    operands = collect_operands(node)
    writer.write("func(round,")
    walk(operands[0], writer, context)
    writer.write(")")


@translate.register(Trunc)
def _(node: Trunc, writer: IndentedWriter, context: TranspilerContext):
    """Translate TRUNC function."""
    operands = collect_operands(node)
    writer.write("func(trunc,")
    walk(operands[0], writer, context)
    writer.write(")")


@translate.register(RealToInt)
def _(node: RealToInt, writer: IndentedWriter, context: TranspilerContext):
    """Translate RealToInt function."""
    operands = collect_operands(node)
    writer.write("func(real-to-int,")
    walk(operands[0], writer, context)
    writer.write(")")


# N-ary Numeric Functions


@translate.register(Max)
def _(node: Max, writer: IndentedWriter, context: TranspilerContext):
    """Translate MAX function."""
    operands = collect_operands(node)
    write_nary_operator("_max_", operands, writer, context)


@translate.register(Min)
def _(node: Min, writer: IndentedWriter, context: TranspilerContext):
    """Translate MIN function."""
    operands = collect_operands(node)
    write_nary_operator("_min_", operands, writer, context)


# Known Test


@translate.register(IsKnown)
def _(node: IsKnown, writer: IndentedWriter, context: TranspilerContext):
    """Translate IsKnown operator."""
    operands = collect_operands(node)
    writer.write("isKnown(")
    walk(operands[0], writer, context)
    writer.write(")")


@translate.register(Concat)
def _(node: Concat, writer: IndentedWriter, context: TranspilerContext):
    """Translate Concat operator - string concatenation using + operator."""
    operands = collect_operands(node)
    write_nary_operator("_+_", operands, writer, context)


@translate.register(Strlen)
def _(node: Strlen, writer: IndentedWriter, context: TranspilerContext):
    """String length operation is not supported in PLEXIL-V."""
    raise NotImplementedError(
        "String length (Strlen) operation is not currently supported in PLEXIL-V. "
        "Consider tracking string lengths separately if needed."
    )
