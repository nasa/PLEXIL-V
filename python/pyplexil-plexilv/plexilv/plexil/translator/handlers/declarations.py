"""Declaration translation handlers"""

import sys
from ..dispatch import translate, walk
from plexilv.common import IndentedWriter
from ..state import TranspilerContext
from ..constants import UNKNOWN
from ._helpers import *
from plexil.core.v1 import *


@translate.register(GlobalDeclarations)
def _(node: GlobalDeclarations, writer: IndentedWriter, context: TranspilerContext):
    """Translate global declarations.

    Global declarations (CommandDeclaration, StateDeclaration, LibraryNodeDeclaration)
    are not supported in the PLEXIL-V Maude format. These declarations are used for
    interface specifications in PLEXIL but are not needed for verification in Maude,
    as the semantics are defined directly in the PLEXIL-V module.

    This handler produces no output (empty string) but warns when declarations are
    encountered so users are aware they're being omitted.

    See: PLEXIL Language Reference, Section on Global Declarations
    """
    # Count how many declarations are present
    decl_count = 0
    if hasattr(node, "choice") and node.choice:
        decl_count = len(node.choice)

    if decl_count > 0:
        print(
            f"Warning: GlobalDeclarations with {decl_count} declaration(s) encountered. "
            "Global declarations are not supported in PLEXIL-V format and will be omitted.",
            file=sys.stderr,
        )

    # Produce no output - PLEXIL-V doesn't use global declarations
    pass


@translate.register(CommandDeclaration)
def _(node: CommandDeclaration, writer: IndentedWriter, context: TranspilerContext):
    """Translate command declaration.

    Command declarations are not supported in PLEXIL-V Maude format.
    They define command interfaces but are not needed for verification.

    This handler produces no output (empty string).
    Note: Warnings are issued by the GlobalDeclarations handler when these are
    encountered as part of global declarations.
    """
    # Produce no output - PLEXIL-V doesn't use command declarations
    pass


@translate.register(StateDeclaration)
def _(node: StateDeclaration, writer: IndentedWriter, context: TranspilerContext):
    """Translate state declaration.

    State declarations are not supported in PLEXIL-V Maude format.
    They define lookup interfaces but are not needed for verification.

    This handler produces no output (empty string).
    Note: Warnings are issued by the GlobalDeclarations handler when these are
    encountered as part of global declarations.
    """
    # Produce no output - PLEXIL-V doesn't use state declarations
    pass


@translate.register(LibraryNodeDeclaration)
def _(node: LibraryNodeDeclaration, writer: IndentedWriter, context: TranspilerContext):
    """Translate library node declaration.

    Library node declarations are not supported in PLEXIL-V Maude format.
    They define library node interfaces but are not needed for verification,
    as library nodes are inlined during translation.

    This handler produces no output (empty string).
    Note: Warnings are issued by the GlobalDeclarations handler when these are
    encountered as part of global declarations.
    """
    # Produce no output - PLEXIL-V doesn't use library node declarations
    pass


@translate.register(VariableDeclarations)
def _(node: VariableDeclarations, writer: IndentedWriter, context: TranspilerContext):
    """Translate variable declarations block."""
    # Format: ((declaration1)(declaration2)...) or () for empty
    writer.write("(")

    # All declarations (variables, arrays, mutexes) are in one compound choice field
    for decl in node.declare_variable_or_declare_array_or_declare_mutex:
        walk(decl, writer, context)

    writer.write(")")


@translate.register(DeclareVariable)
def _(node: DeclareVariable, writer: IndentedWriter, context: TranspilerContext):
    """Translate single variable declaration."""
    # Format: ('varName : value) or ('varName : unknown)
    # NOTE: Variable names keep underscores (unlike node names which use hyphens)
    var_name = node.name
    writer.write(f"('{var_name} : ")

    if node.initial_value:
        # Find the populated field in InitialValue
        for field_info in fields(node.initial_value):
            field_name = field_info.name
            if field_name in ("file_name", "line_no", "col_no", "epx"):
                continue
            field_value = getattr(node.initial_value, field_name)
            if field_value is not None:
                # For Values, write val(...) directly without const() wrapper
                if isinstance(
                    field_value, (IntegerValue, RealValue, BooleanValue, StringValue)
                ):
                    if isinstance(field_value, IntegerValue):
                        writer.write(f"val({field_value.value})")
                    elif isinstance(field_value, RealValue):
                        writer.write(f"val({field_value.value})")
                    elif isinstance(field_value, BooleanValue):
                        val_str = "true" if field_value.value else "false"
                        writer.write(f"val({val_str})")
                    elif isinstance(field_value, StringValue):
                        val_str = field_value.value if field_value.value else ""
                        escaped_value = escape_string(val_str)
                        writer.write(f'val("{escaped_value}")')
                else:
                    # For expressions (variables, operators, etc.), use walk
                    walk(field_value, writer, context)
                break
    else:
        writer.write(UNKNOWN)

    writer.write(")")


@translate.register(DeclareArray)
def _(node: DeclareArray, writer: IndentedWriter, context: TranspilerContext):
    """Translate array declaration."""
    # Format: ('arrayName : createArray(size,values)) or ('arrayName : createArray(size,unknownArray(size)))
    # NOTE: Variable names keep underscores (unlike node names which use hyphens)
    arr_name = node.name
    max_size = node.max_size if node.max_size else 0

    writer.write(f"('{arr_name} : createArray({max_size},")

    if node.initial_value and node.initial_value.choice:
        # Array has initial values - in choice field
        if isinstance(node.initial_value.choice, ArrayValue):
            array_val = node.initial_value.choice
            # ArrayValue now has all values in its choice list
            values = array_val.choice

            # Write values as val(x) # val(y) # val(z) with spaces around #
            for i, val in enumerate(values):
                if i > 0:
                    writer.write(" # ")
                # For Values in array initial value, write val(...) directly without const() wrapper
                if isinstance(val, IntegerValue):
                    writer.write(f"val({val.value})")
                elif isinstance(val, RealValue):
                    writer.write(f"val({val.value})")
                elif isinstance(val, BooleanValue):
                    val_str = "true" if val.value else "false"
                    writer.write(f"val({val_str})")
                elif isinstance(val, StringValue):
                    val_str = val.value if val.value else ""
                    escaped_value = escape_string(val_str)
                    writer.write(f'val("{escaped_value}")')
                else:
                    walk(val, writer, context)
        else:
            # Single value (not an array) - shouldn't happen for DeclareArray but handle gracefully
            walk(node.initial_value.choice, writer, context)
    else:
        # No initial values - use unknownArray(size)
        writer.write(f"unknownArray({max_size})")

    writer.write("))")
