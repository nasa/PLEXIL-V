"""Lookup and node reference translation handlers"""

from ..dispatch import translate, walk
from plexilv.common import IndentedWriter
from ..state import TranspilerContext
from ..constants import UNKNOWN
from ._helpers import *
from plexil.core.v1 import *


@translate.register(LookupNow)
def _(node: LookupNow, writer: IndentedWriter, context: TranspilerContext):
    """Translate LookupNow state query."""
    writer.write("lookup(")

    # Write the lookup name
    walk(node.name, writer, context)

    writer.write(",")

    # Write arguments (or nilpar if none)
    if node.arguments:
        writer.write("(")
        walk(node.arguments, writer, context)
        writer.write(")")
    else:
        writer.write("(nilpar)")

    writer.write(")")


@translate.register(LookupOnChange)
def _(node: LookupOnChange, writer: IndentedWriter, context: TranspilerContext):
    """Translate LookupOnChange state query."""
    writer.write("lookupOnChange(")

    # Write the lookup name
    walk(node.name, writer, context)

    writer.write(",")

    # Write arguments (or nilpar if none)
    if node.arguments:
        writer.write("(")
        walk(node.arguments, writer, context)
        writer.write(")")
    else:
        writer.write("(nilpar)")

    writer.write(",")

    # Write tolerance (or default val(0.0) if none)
    if node.tolerance:
        walk(node.tolerance, writer, context)
    else:
        writer.write("val(0.0)")

    writer.write(")")


@translate.register(Name)
def _(node: Name, writer: IndentedWriter, context: TranspilerContext):
    """Translate Name element (used in lookups and commands)."""
    # With compound fields, Name has a choice field
    if node.choice:
        # Special case: StringValue should be written as a quoted string
        if isinstance(node.choice, StringValue):
            writer.write(f"'{node.choice.value}")
        else:
            walk(node.choice, writer, context)


@translate.register(Arguments)
def _(node: Arguments, writer: IndentedWriter, context: TranspilerContext):
    """Translate Arguments list.

    Arguments now uses a single 'expression' list that preserves document order.
    Literal values are wrapped with const(val(...)).
    Variables and expressions are translated directly.
    """
    # Iterate through expressions in document order (in node.choice list)
    for i, arg in enumerate(node.choice):
        if i > 0:
            writer.write(" ")

        # For literal Values in Arguments, wrap with const()
        if isinstance(
            arg, (IntegerValue, RealValue, BooleanValue, StringValue, ArrayValue)
        ):
            if isinstance(arg, IntegerValue):
                writer.write(f"const(val({arg.value}))")
            elif isinstance(arg, RealValue):
                writer.write(f"const(val({float(arg.value):.1f}))")
            elif isinstance(arg, BooleanValue):
                writer.write(f"const(val({str(arg.value).lower()}))")
            elif isinstance(arg, StringValue):
                escaped_value = escape_string(arg.value)
                writer.write(f'const(val("{escaped_value}"))')
            elif isinstance(arg, ArrayValue):
                # For arrays, still need to format properly
                walk(arg, writer, context)
        else:
            # For variables and expressions, use normal translation (no const wrapper)
            walk(arg, writer, context)


@translate.register(Tolerance)
def _(node: Tolerance, writer: IndentedWriter, context: TranspilerContext):
    """Translate Tolerance expression.

    Note: Tolerance values use val(...) without const() wrapper.
    """
    # Tolerance can contain any numeric expression
    operands = collect_operands(node)
    if operands:
        operand = operands[0]
        # For literal values, write val(...) directly without const() wrapper
        if isinstance(operand, IntegerValue):
            writer.write(f"val({operand.value})")
        elif isinstance(operand, RealValue):
            writer.write(f"val({operand.value})")
        else:
            # For expressions/variables, walk normally
            walk(operand, writer, context)


@translate.register(NodeStateVariable)
def _(node: NodeStateVariable, writer: IndentedWriter, context: TranspilerContext):
    """Translate NodeStateVariable reference."""
    # Extract node_ref or node_id from compound field
    if isinstance(node.node_id_or_node_ref, NodeRef):
        writer.write(format_node_reference(node.node_id_or_node_ref, None))
    elif isinstance(node.node_id_or_node_ref, NodeId):
        writer.write(format_node_reference(None, node.node_id_or_node_ref))
    else:
        writer.write("")


@translate.register(NodeTimepointValue)
def _(node: NodeTimepointValue, writer: IndentedWriter, context: TranspilerContext):
    """Translate NodeTimepointValue reference.

    Format: timepoint((node_ref), state, timepoint) or timepoint(self, state, timepoint)
    Example: timepoint(('nodeId),inactive,start) or timepoint(self,executing,start)
    Note: Node reference is wrapped in parentheses except for self/parent
    """
    # Check if this is a self/parent reference
    is_self_or_parent = False
    if isinstance(node.node_id_or_node_ref, NodeRef):
        if node.node_id_or_node_ref.dir and node.node_id_or_node_ref.dir.value in (
            "self",
            "parent",
        ):
            is_self_or_parent = True

    if is_self_or_parent:
        # self/parent without extra parentheses
        writer.write("timepoint(")
    else:
        # Named nodes with extra parentheses
        writer.write("timepoint((")

    # Node reference
    if isinstance(node.node_id_or_node_ref, NodeRef):
        writer.write(format_node_reference(node.node_id_or_node_ref, None))
    elif isinstance(node.node_id_or_node_ref, NodeId):
        writer.write(format_node_reference(None, node.node_id_or_node_ref))
    else:
        writer.write("")

    if is_self_or_parent:
        writer.write(",")
    else:
        writer.write("),")

    # Node state (lowercase)
    if node.node_state_value and node.node_state_value.value:
        state = node.node_state_value.value.value.lower()
        writer.write(state)
    else:
        writer.write(UNKNOWN)

    writer.write(",")

    # Timepoint (lowercase)
    if node.timepoint and node.timepoint.value:
        timepoint = node.timepoint.value.value.lower()
        writer.write(timepoint)
    else:
        writer.write(UNKNOWN)

    writer.write(")")


@translate.register(NodeOutcomeVariable)
def _(node: NodeOutcomeVariable, writer: IndentedWriter, context: TranspilerContext):
    """Translate NodeOutcomeVariable reference."""
    # Extract node_ref or node_id from compound field
    if isinstance(node.node_id_or_node_ref, NodeRef):
        writer.write(format_node_reference(node.node_id_or_node_ref, None))
    elif isinstance(node.node_id_or_node_ref, NodeId):
        writer.write(format_node_reference(None, node.node_id_or_node_ref))
    else:
        writer.write("")


@translate.register(NodeCommandHandleVariable)
def _(
    node: NodeCommandHandleVariable, writer: IndentedWriter, context: TranspilerContext
):
    """Translate NodeCommandHandleVariable reference."""
    # Extract node_ref or node_id from compound field
    if isinstance(node.node_id_or_node_ref, NodeRef):
        writer.write(format_node_reference(node.node_id_or_node_ref, None))
    elif isinstance(node.node_id_or_node_ref, NodeId):
        writer.write(format_node_reference(None, node.node_id_or_node_ref))
    else:
        writer.write("")


@translate.register(NodeStateValue)
def _(node: NodeStateValue, writer: IndentedWriter, context: TranspilerContext):
    """Translate NodeStateValue enum."""
    # Convert UPPER_CASE to camelCase
    value_str = node.value.value
    # Handle special cases
    if value_str == "ITERATION_ENDED":
        writer.write("iterationEnded")
    else:
        # Convert to lowercase
        writer.write(value_str.lower())


@translate.register(NodeOutcomeValue)
def _(node: NodeOutcomeValue, writer: IndentedWriter, context: TranspilerContext):
    """Translate NodeOutcomeValue enum."""
    # Convert to lowercase
    writer.write(node.value.value.lower())


@translate.register(NodeCommandHandleValue)
def _(node: NodeCommandHandleValue, writer: IndentedWriter, context: TranspilerContext):
    """Translate NodeCommandHandleValue enum."""
    # Convert COMMAND_SUCCESS to commandSuccess (camelCase)
    value_str = node.value.value
    # Split by underscore and convert to camelCase
    parts = value_str.split("_")
    if len(parts) > 1:
        # First part lowercase, rest title case
        camel = parts[0].lower() + "".join(p.capitalize() for p in parts[1:])
        writer.write(camel)
    else:
        writer.write(value_str.lower())
