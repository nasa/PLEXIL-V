"""Action translation handlers (Assignment, Command, Update, LibraryNodeCall)"""

from ..dispatch import translate, walk
from plexilv.common import IndentedWriter
from ..state import TranspilerContext
from ._helpers import *
from plexil.core.v1 import *


@translate.register(Assignment)
def _(node: Assignment, writer: IndentedWriter, context: TranspilerContext):
    """Translate assignment statement."""
    writer.write("(")

    # LHS - Left-hand side (what is being assigned to) - in node.choice
    if node.choice:
        walk(node.choice, writer, context)

    writer.write(" := ")

    # RHS - Right-hand side (the value being assigned) - in node.choice_1
    if node.choice_1:
        walk(node.choice_1, writer, context)

    writer.write(")")


# RHS Types (Right-hand side expression containers)


@translate.register(BooleanRhs)
def _(node: BooleanRhs, writer: IndentedWriter, context: TranspilerContext):
    """Translate BooleanRHS expression."""
    # With compound fields, BooleanRhs has a choice field with the expression
    if node.choice:
        walk(node.choice, writer, context)


@translate.register(NumericRhs)
def _(node: NumericRhs, writer: IndentedWriter, context: TranspilerContext):
    """Translate NumericRHS expression."""
    # With compound fields, NumericRhs has a choice field with the expression
    if node.choice:
        walk(node.choice, writer, context)


@translate.register(StringRhs)
def _(node: StringRhs, writer: IndentedWriter, context: TranspilerContext):
    """Translate StringRHS expression."""
    # With compound fields, StringRhs has a choice field with the expression
    if node.choice:
        walk(node.choice, writer, context)


@translate.register(ArrayRhs)
def _(node: ArrayRhs, writer: IndentedWriter, context: TranspilerContext):
    """Translate ArrayRHS expression."""
    # With compound fields, ArrayRhs has a choice field with the expression
    if node.choice:
        walk(node.choice, writer, context)


@translate.register(Command)
def _(node: Command, writer: IndentedWriter, context: TranspilerContext):
    """Translate command invocation.

    Format: (name/args/returnVar)
    - name: 'cmdName for string literals, cmdId(var('name)) for variables
    - args: (nilpar) for no args, or arguments list
    - returnVar: nothing for no return, just('varName) for return variable
    """
    writer.write("(")

    # Command name
    if node.name and node.name.choice:
        if isinstance(node.name.choice, StringValue):
            # String literal name: 'cmdName
            writer.write(f"'{node.name.choice.value}")
        elif isinstance(node.name.choice, StringVariable):
            # Variable name: cmdId(var('name))
            writer.write("cmdId(")
            walk(node.name.choice, writer, context)
            writer.write(")")
        else:
            # Other name types (concat, lookup, array element)
            writer.write("cmdId(")
            walk(node.name.choice, writer, context)
            writer.write(")")

    writer.write(" / ")

    # Arguments
    if node.arguments:
        writer.write("(")
        walk(node.arguments, writer, context)
        writer.write(")")
    else:
        writer.write("(nilpar)")

    writer.write(" / ")

    # Return variable - now in choice field
    if node.choice:
        var = node.choice
        writer.write(f"just('{var.value})")
    else:
        writer.write("nothing")

    writer.write(")")


@translate.register(Update)
def _(node: Update, writer: IndentedWriter, context: TranspilerContext):
    """Translate update statement.

    Format: (< 'name1 ; expr1 > < 'name2 ; expr2 > ...)
    Each Pair is: < 'name ; expression >
    """
    writer.write("(")

    for i, pair in enumerate(node.pair):
        if i > 0:
            writer.write(" ")

        # Write pair: < 'name ; expression >
        writer.write("< '")
        writer.write(pair.name)
        writer.write(" ; ")

        # Get and translate the value expression
        value = get_pair_value(pair)
        if value:
            # Array variables need special formatting: arrayVar('name)
            if isinstance(value, ArrayVariable):
                writer.write(f"arrayVar('{value.value})")
            else:
                # All other values and expressions translate directly
                # (literal values already get const() wrapper from their handlers)
                walk(value, writer, context)

        writer.write(" >")

    writer.write(")")


@translate.register(LibraryNodeCall)
def _(node: LibraryNodeCall, writer: IndentedWriter, context: TranspilerContext):
    """Translate library node call body element.

    NOTE: This handler is for the LibraryNodeCall body element itself.
    The full library call node translation is handled by translate_library_node.
    This handler should not be called directly in normal translation flow.
    """
    # This should not be reached in normal flow since LibraryNodeCall
    # is translated as part of the Node with NodeType="LibraryNodeCall"
    library_name = node.node_id.value
    writer.write(f"unexpected-library-call-element('{library_name})")
