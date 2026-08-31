"""Helper functions for PLEXIL translation."""

from dataclasses import fields
from plexilv.common import IndentedWriter
from ..state import TranspilerContext
from ..dispatch import translate, walk
from ..constants import UNKNOWN
from plexil.core.v1 import *

# Type aliases
Index = ArrayElement.Index


# Naming conventions for PLEXIL-V output
def format_node_name(name: str) -> str:
    """Format a node name for PLEXIL-V output.

    Node names in PLEXIL-V preserve underscores.
    Example: "my_node" → "my_node"

    Args:
        name: The node name from the AST

    Returns:
        The node name unchanged
    """
    return name


def format_var_name(name: str) -> str:
    """Format a variable name for PLEXIL-V output.

    Variable names in PLEXIL-V keep their underscores unchanged.
    Example: "my_var" → "my_var"

    Args:
        name: The variable name from the AST

    Returns:
        The variable name unchanged (documenting the convention)
    """
    return name


def get_node_ref_string(var):
    """Extract node reference string from a NodeVariable with compound fields.

    Used by EQInternal predicates (isStatus?, isOutcome?, isFailure?, cmdHandleIs?).
    For these predicates, node references are formatted as:
    - self for self reference
    - parent for parent reference
    - 'NodeName for all other references (including child and sibling)

    With compound fields, NodeReference has node_id_or_node_ref field instead of
    separate node_id and node_ref fields.
    """
    if hasattr(var, "node_id_or_node_ref") and var.node_id_or_node_ref:
        ref = var.node_id_or_node_ref
        if isinstance(ref, NodeRef):
            if ref.dir and ref.dir.value in ("self", "parent"):
                return ref.dir.value  # Return "self" or "parent" directly
            # For all other cases (child, sibling, or no direction), use 'NodeName
            node_name = format_node_name(ref.value)
            return f"'{node_name}"
        elif isinstance(ref, NodeId):
            node_name = format_node_name(ref.value)
            return f"'{node_name}"
    # Fallback for old structure (shouldn't happen with new AST)
    elif hasattr(var, "node_ref") and var.node_ref:
        node_ref = var.node_ref
        if node_ref.dir and node_ref.dir.value in ("self", "parent"):
            return node_ref.dir.value
        node_name = format_node_name(node_ref.value)
        return f"'{node_name}"
    elif hasattr(var, "node_id") and var.node_id:
        node_name = format_node_name(var.node_id.value)
        return f"'{node_name}"
    return UNKNOWN


def escape_string(value: str) -> str:
    """Escape special characters in string values for Maude output.

    This ensures string literals are properly escaped in the PLEXIL-V format.
    """
    return (
        value.replace("\\", "\\\\")  # Backslash first
        .replace('"', '\\"')  # Double quotes
        .replace("\n", "\\n")  # Newlines
        .replace("\r", "\\r")  # Carriage returns
        .replace("\t", "\\t")
    )  # Tabs


def collect_operands(node):
    """Collect all operands from an operator node in document order.

    With compound fields, operators typically have a 'choice' field containing operands.
    Binary operators have a single choice, n-ary operators have a list choice.
    """
    operands = []

    # Special case: Wildcard operators (GT, LT, GE, LE) use any_element
    if hasattr(node, "any_element") and node.node_id_or_node_ref is not None:
        if hasattr(node.node_id_or_node_ref, "children"):
            return node.node_id_or_node_ref.children
        return []

    # Compound fields: most operators now use 'choice' field
    if hasattr(node, "choice"):
        choice = getattr(node, "choice")
        if choice is not None:
            # Binary/unary operators have a single choice value
            if isinstance(choice, list):
                return choice
            else:
                return [choice] if choice else []

    # N-ary operators use 'expression' field
    if hasattr(node, "expression") and isinstance(node.expression, list):
        return node.expression

    # Fallback for legacy operators without choice field
    try:
        node_fields = fields(node)
        for field in node_fields:
            attr = getattr(node, field.name, None)
            if attr is None:
                continue

            # Handle list attributes (N-ary operators)
            if isinstance(attr, list) and attr:
                operands.extend(attr)
            # Handle single attributes (unary/binary operators)
            elif not isinstance(attr, (str, int, float, bool, type(None))):
                # Check if it's an expression node (has value or is a node type)
                if hasattr(attr, "__class__") and attr.__class__.__module__.startswith(
                    "plexil.core"
                ):
                    operands.append(attr)
    except TypeError:
        pass

    return operands


def write_nary_operator(
    op_name: str, operands: list, writer: IndentedWriter, context: TranspilerContext
):
    """Write an n-ary operator with left associativity."""
    if len(operands) == 2:
        writer.write(f"{op_name}(")
        walk(operands[0], writer, context)
        writer.write(",")
        walk(operands[1], writer, context)
        writer.write(")")
    else:
        # Left-associate: op(op(a,b),c) for three operands
        for i in range(len(operands) - 1):
            writer.write(f"{op_name}(")
        # Write first operand
        walk(operands[0], writer, context)
        # Write remaining operands with closing parens
        for i in range(1, len(operands)):
            writer.write(",")
            walk(operands[i], writer, context)
            writer.write(")")


# Logical Operators (N-ary)


def format_node_reference(node_ref, node_id):
    """Format a node reference (NodeRef or NodeId) for output."""
    if node_ref:
        if node_ref.dir and node_ref.dir.value in ("self", "parent"):
            # self and parent are written without quotes
            return node_ref.dir.value
        else:
            # Named nodes: format and add quote
            node_name = format_node_name(node_ref.value)
            return f"'{node_name}"
    elif node_id:
        # NodeId: format and add quote
        node_name = format_node_name(node_id.value)
        return f"'{node_name}"
    return ""


def format_node_predicate_reference(node_ref_or_id):
    """
    Format a node reference for predicates.
    Returns 'NodeName for named nodes, self/parent for special refs.
    """
    if isinstance(node_ref_or_id, NodeRef):
        if node_ref_or_id.dir:
            dir_val = node_ref_or_id.dir.value
            if dir_val in ("self", "parent"):
                return dir_val
            elif dir_val in ("child", "sibling"):
                node_name = format_node_name(node_ref_or_id.value)
                return f"{dir_val}('{node_name})"
            else:
                # Shouldn't happen, but handle gracefully
                node_name = format_node_name(node_ref_or_id.value)
                return f"'{node_name}"
        else:
            # No direction, just use name
            node_name = format_node_name(node_ref_or_id.value)
            return f"'{node_name}"
    elif isinstance(node_ref_or_id, NodeId):
        node_name = format_node_name(node_ref_or_id.value)
        return f"'{node_name}"
    else:
        # Handle raw string or other types
        return str(node_ref_or_id)


# State Predicates


def get_pair_value(pair):
    """Extract the expression value from a Pair node.

    Pair has many optional fields for different expression types.
    Returns the first non-None expression field.
    """
    # Check all possible expression fields
    for attr_name in dir(pair):
        if attr_name.startswith("_") or attr_name in (
            "name",
            "file_name",
            "line_no",
            "col_no",
            "epx",
        ):
            continue
        attr_value = getattr(pair, attr_name, None)
        if attr_value is not None:
            return attr_value
    return None


def get_alias_value(alias):
    """Extract the expression value from an Alias node.

    In the compound fields AST, Alias has a choice field that contains the expression.
    Returns the choice value.
    """
    return alias.choice if hasattr(alias, "choice") else None


def format_var_decl_for_library(var_decl):
    """Format a variable declaration for library context (with spaces around :).

    Library context uses format: ('varName : value)
    Regular context uses format: ('varName:value)
    NOTE: Variable names keep underscores (unlike node names which use hyphens)
    """
    var_name = format_var_name(var_decl.name)

    if isinstance(var_decl, DeclareVariable):
        if var_decl.initial_value and var_decl.initial_value.choice:
            # InitialValue now has a choice field
            field_value = var_decl.initial_value.choice
            # For Values, write val(...) directly
            if isinstance(field_value, IntegerValue):
                return f"('{var_name} : val({field_value.value}))"
            elif isinstance(field_value, RealValue):
                return f"('{var_name} : val({field_value.value}))"
            elif isinstance(field_value, BooleanValue):
                val_str = "true" if field_value.value else "false"
                return f"('{var_name} : val({val_str}))"
            elif isinstance(field_value, StringValue):
                val_str = field_value.value if field_value.value else ""
                return f'(\'{var_name} : val("{val_str}"))'
            else:
                # For expressions, would need to walk - not supported in this helper
                return f"('{var_name} : unknown)"
        return f"('{var_name} : unknown)"
    elif isinstance(var_decl, DeclareArray):
        max_size = (
            var_decl.max_size if var_decl.max_size else 0
        )  # Now an int, not object
        return f"('{var_name} : createArray({max_size},unknownArray({max_size})))"
    else:
        return f"('{var_name} : unknown)"


def translate_condition(
    condition_name: str, node, writer: IndentedWriter, context: TranspilerContext
):
    """Helper to translate any condition type."""
    writer.write(f"({condition_name}: (")

    # Find the first non-None field (the actual expression)
    for field_info in fields(node):
        field_name = field_info.name
        # Skip metadata fields
        if field_name in ("file_name", "line_no", "col_no", "epx"):
            continue
        field_value = getattr(node, field_name)
        if field_value is not None:
            walk(field_value, writer, context)
            break

    writer.write("))")
