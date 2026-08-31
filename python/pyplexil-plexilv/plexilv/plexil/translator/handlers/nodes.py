"""Node structure translation handlers"""

from ..dispatch import translate, walk
from plexilv.common import IndentedWriter
from ..state import TranspilerContext
from ..constants import TranspilationError
from ._helpers import *
from plexil.core.v1 import *


@translate.register(PlexilPlan)
def _(node: PlexilPlan, writer: IndentedWriter, context: TranspilerContext):
    """Translate the root PlexilPlan element.

    Acts as a transparent wrapper - validates the plan has a root node
    and delegates to it. Does not produce wrapper output itself.

    Raises:
        ValueError: If the plan has no root node
    """
    if not node.node:
        raise ValueError("PlexilPlan must have a root node")

    # Global declarations (for future use)
    if node.global_declarations:
        walk(node.global_declarations, writer, context)
        writer.blank_line()

    # Delegate to the node - this produces the actual output
    walk(node.node, writer, context)


@translate.register(Node)
def _(node: Node, writer: IndentedWriter, context: TranspilerContext):
    """Translate an Node (Node implementation) to PLEXIL-V format.

    Format: nodeType('nodeId, vardecls, conditions, body)
    Where nodeType is: empty, assignment, command, list
    """
    # Extract NodeId - format for PLEXIL-V
    node_id = "anonymous"
    if node.node_id and node.node_id.value:
        node_id = format_node_name(node.node_id.value)

    # Determine node type
    node_type = node.node_type.value if node.node_type else "Empty"

    # Route to appropriate node type handler
    if node_type == "Empty":
        translate_empty_node(node, node_id, writer, context)
    elif node_type == "Assignment":
        translate_assignment_node(node, node_id, writer, context)
    elif node_type == "Command":
        translate_command_node(node, node_id, writer, context)
    elif node_type == "Update":
        translate_update_node(node, node_id, writer, context)
    elif node_type == "NodeList":
        translate_list_node(node, node_id, writer, context)
    elif node_type == "LibraryNodeCall":
        translate_library_node(node, node_id, writer, context)
    else:
        # Unsupported node type - raise error
        raise TranspilationError(
            f"Unsupported node type '{node_type}' for node '{node_id}'"
        )


def collect_node_conditions(node: Node):
    """Collect all non-None conditions from a Node.

    In the new AST, conditions are single objects (not lists).
    Returns a list of condition objects.
    """
    conditions = []
    if node.start_condition:
        conditions.append(node.start_condition)
    if node.end_condition:
        conditions.append(node.end_condition)
    if node.pre_condition:
        conditions.append(node.pre_condition)
    if node.post_condition:
        conditions.append(node.post_condition)
    if node.invariant_condition:
        conditions.append(node.invariant_condition)
    if node.repeat_condition:
        conditions.append(node.repeat_condition)
    if node.exit_condition:
        conditions.append(node.exit_condition)
    if node.skip_condition:
        conditions.append(node.skip_condition)
    return conditions


def translate_empty_node(
    node: Node, node_id: str, writer: IndentedWriter, context: TranspilerContext
):
    """Translate an Empty node to PLEXIL-V format.

    Format (multi-line):
    empty(
      'nodeId,
      vardecls,
      conditions
    )
    """
    writer.write("empty(")
    writer.writeln()
    writer.indent()

    # Node ID
    writer.writeln(f"'{node_id},")

    # Variable declarations
    if node.variable_declarations:
        writer.write("")  # Start line at current indent
        walk(node.variable_declarations, writer, context)
        writer.writeln(",")
    else:
        writer.writeln("nilocdecl,")

    # Conditions
    conditions = collect_node_conditions(node)
    if conditions:
        writer.write("(")
        for i, cond in enumerate(conditions):
            if i > 0:
                writer.write(",")
            walk(cond, writer, context)
        writer.writeln(")")
    else:
        writer.writeln("(none)")

    writer.dedent()
    writer.write(")")


def translate_assignment_node(
    node: Node, node_id: str, writer: IndentedWriter, context: TranspilerContext
):
    """Translate an Assignment node to PLEXIL-V format.

    Format (multi-line):
    assignment(
      'nodeId,
      vardecls,
      conditions,
      assignmentAction
    )
    """
    writer.write("assignment(")
    writer.writeln()
    writer.indent()

    # Node ID
    writer.writeln(f"'{node_id},")

    # Variable declarations
    if node.variable_declarations:
        writer.write("")  # Start line at current indent
        walk(node.variable_declarations, writer, context)
        writer.writeln(",")
    else:
        writer.writeln("nilocdecl,")

    # Conditions
    conditions = collect_node_conditions(node)
    if conditions:
        writer.write("(")
        for i, cond in enumerate(conditions):
            if i > 0:
                writer.write(",")
            walk(cond, writer, context)
        writer.writeln("),")
    else:
        writer.writeln("(none),")

    # Assignment body - extract from NodeBody
    if not node.node_body:
        raise TranspilationError(
            f"Assignment node '{node_id}' is missing node body"
        )
    if not node.node_body.choice:
        raise TranspilationError(
            f"Assignment node '{node_id}' has empty node body"
        )
    if not isinstance(node.node_body.choice, Assignment):
        raise TranspilationError(
            f"Assignment node '{node_id}' has wrong body type: "
            f"{type(node.node_body.choice).__name__}"
        )
    writer.write("")  # Start line at current indent
    walk(node.node_body.choice, writer, context)
    writer.writeln()

    writer.dedent()
    writer.write(")")


def translate_command_node(
    node: Node, node_id: str, writer: IndentedWriter, context: TranspilerContext
):
    """Translate a Command node to PLEXIL-V format.

    Format (multi-line):
    command(
      'nodeId,
      vardecls,
      conditions,
      commandAction
    )
    """
    writer.write("command(")
    writer.writeln()
    writer.indent()

    # Node ID
    writer.writeln(f"'{node_id},")

    # Variable declarations
    if node.variable_declarations:
        writer.write("")  # Start line at current indent
        walk(node.variable_declarations, writer, context)
        writer.writeln(",")
    else:
        writer.writeln("nilocdecl,")

    # Conditions
    conditions = collect_node_conditions(node)
    if conditions:
        writer.write("(")
        for i, cond in enumerate(conditions):
            if i > 0:
                writer.write(",")
            walk(cond, writer, context)
        writer.writeln("),")
    else:
        writer.writeln("(none),")

    # Command body - extract from NodeBody and wrap the command name
    if not node.node_body:
        raise TranspilationError(f"Command node '{node_id}' is missing node body")
    if not node.node_body.choice:
        raise TranspilationError(f"Command node '{node_id}' has empty node body")
    if not isinstance(node.node_body.choice, Command):
        raise TranspilationError(
            f"Command node '{node_id}' has wrong body type: "
            f"{type(node.node_body.choice).__name__}"
        )

    cmd = node.node_body.choice
    # Manually format command with wrapped name
    writer.write("(")
    # Command name - wrap in parentheses for node context
    if cmd.name and cmd.name.choice:
        if isinstance(cmd.name.choice, StringValue):
            writer.write(f"('{cmd.name.choice.value})")
        else:
            writer.write("cmdId(")
            walk(cmd.name.choice, writer, context)
            writer.write(")")
    writer.write(" / ")
    # Arguments
    if cmd.arguments:
        writer.write("(")
        walk(cmd.arguments, writer, context)
        writer.write(")")
    else:
        writer.write("(nilpar)")
    writer.write(" / ")
    # Return variable - now in choice field
    if cmd.choice:
        var = cmd.choice
        writer.write(f"just('{var.value})")
    else:
        writer.write("nothing")
    writer.writeln(")")

    writer.dedent()
    writer.write(")")


def translate_update_node(
    node: Node, node_id: str, writer: IndentedWriter, context: TranspilerContext
):
    """Translate an Update node to PLEXIL-V format.

    Format (multi-line):
    update(
      'nodeId,
      vardecls,
      conditions,
      updateAction
    )
    """
    writer.write("update(")
    writer.writeln()
    writer.indent()

    # Node ID
    writer.writeln(f"'{node_id},")

    # Variable declarations
    if node.variable_declarations:
        writer.write("")  # Start line at current indent
        walk(node.variable_declarations, writer, context)
        writer.writeln(",")
    else:
        writer.writeln("nilocdecl,")

    # Conditions
    conditions = collect_node_conditions(node)
    if conditions:
        writer.write("(")
        for i, cond in enumerate(conditions):
            if i > 0:
                writer.write(",")
            walk(cond, writer, context)
        writer.writeln("),")
    else:
        writer.writeln("(none),")

    # Update body - extract from NodeBody
    if not node.node_body:
        raise TranspilationError(f"Update node '{node_id}' is missing node body")
    if not node.node_body.choice:
        raise TranspilationError(f"Update node '{node_id}' has empty node body")
    if not isinstance(node.node_body.choice, Update):
        raise TranspilationError(
            f"Update node '{node_id}' has wrong body type: "
            f"{type(node.node_body.choice).__name__}"
        )
    writer.write("")  # Start line at current indent
    walk(node.node_body.choice, writer, context)
    writer.writeln()

    writer.dedent()
    writer.write(")")


def translate_list_node(
    node: Node, node_id: str, writer: IndentedWriter, context: TranspilerContext
):
    """Translate a NodeList (sequence) node to PLEXIL-V format.

    Format (multi-line):
    list(
      'nodeId,
      vardecls,
      conditions,
      (child1 child2 ...)
    )
    """
    writer.write("list(")
    writer.writeln()
    writer.indent()

    # Node ID
    writer.writeln(f"'{node_id},")

    # Variable declarations
    if node.variable_declarations:
        writer.write("")  # Start line at current indent
        walk(node.variable_declarations, writer, context)
        writer.writeln(",")
    else:
        writer.writeln("nilocdecl,")

    # Conditions
    conditions = collect_node_conditions(node)
    if conditions:
        writer.write("(")
        for i, cond in enumerate(conditions):
            if i > 0:
                writer.write(",")
            walk(cond, writer, context)
        writer.writeln("),")
    else:
        writer.writeln("(none),")

    # Children nodes - extract from NodeBody
    if node.node_body and node.node_body.choice:
        if isinstance(node.node_body.choice, NodeList):
            body_choice = node.node_body.choice
            writer.write("(")
            writer.writeln()
            writer.indent()

            # Process each child node
            for i, child_node in enumerate(body_choice.node):
                # The child_node only has NodeId in any_element due to parsing issue
                # We need to create a minimal Node structure
                if (
                    hasattr(child_node, "any_element")
                    and child_node.node_id_or_node_ref
                ):
                    any_elem = child_node.node_id_or_node_ref

                    # If any_element is AnyElement with children, use those
                    if hasattr(any_elem, "children"):
                        # Build Node from children
                        from plexil.core.v1.ast import (
                            Node as AG,
                            NodeActionTypeNodeType,
                        )

                        ag = AG()

                        # Extract components from children
                        import re

                        for child_elem in any_elem.children:
                            elem_type = child_elem.__class__.__name__

                            # Convert PascalCase element name to snake_case attribute name
                            # e.g., NodeId -> node_id, StartCondition -> start_condition
                            attr_name = re.sub(
                                r"(?<!^)(?=[A-Z])", "_", elem_type
                            ).lower()

                            # Try to set the attribute if it exists on Node
                            if hasattr(ag, attr_name):
                                attr = getattr(ag, attr_name)
                                # Most attributes are lists, append to them
                                if isinstance(attr, list):
                                    attr.append(child_elem)
                                else:
                                    # For non-list attributes, set directly
                                    setattr(ag, attr_name, child_elem)

                        # Infer NodeType from NodeBody contents (attributes not captured by xsdata)
                        if ag.node_body:
                            body = ag.node_body[0]
                            if body.assignment:
                                ag.node_type = NodeActionTypeNodeType.ASSIGNMENT
                            elif body.command:
                                ag.node_type = NodeActionTypeNodeType.COMMAND
                            elif body.node_list:
                                ag.node_type = NodeActionTypeNodeType.NODE_LIST
                            elif body.update:
                                ag.node_type = NodeActionTypeNodeType.UPDATE
                            elif body.library_node_call:
                                ag.node_type = NodeActionTypeNodeType.LIBRARY_NODE_CALL
                            else:
                                ag.node_type = NodeActionTypeNodeType.EMPTY
                        else:
                            ag.node_type = NodeActionTypeNodeType.EMPTY

                        walk(ag, writer, context)
                        writer.writeln()
                    elif isinstance(any_elem, NodeId):
                        # Only has NodeId - create minimal empty node
                        from plexil.core.v1.ast import (
                            Node as AG,
                            NodeActionTypeNodeType,
                        )

                        ag = AG()
                        ag.node_id = [any_elem]
                        ag.node_type = NodeActionTypeNodeType.EMPTY
                        walk(ag, writer, context)
                        writer.writeln()
                    else:
                        # Unknown structure
                        walk(child_node, writer, context)
                        writer.writeln()
                else:
                    walk(child_node, writer, context)
                    writer.writeln()

            writer.dedent()
            writer.writeln(")")
        else:
            writer.writeln("()")
    else:
        writer.writeln("()")

    writer.dedent()
    writer.write(")")


def translate_library_node(
    node: Node, node_id: str, writer: IndentedWriter, context: TranspilerContext
):
    """Translate a LibraryNodeCall node to PLEXIL-V format.

    Format (multi-line):
    library(
      'callNodeId,
      aliasVardecls,
      localVardecls,
      conditions,
      callInfo(...),
      libraryNode
    )

    Phase 6a: This implements inline library calls where the library definition
    would be embedded. For now, we output a placeholder for the library definition
    since resolving external libraries requires additional infrastructure.
    """
    writer.write("library(")
    writer.writeln()
    writer.indent()

    # Node ID
    writer.writeln(f"'{node_id},")

    # Extract LibraryNodeCall from NodeBody (needed for alias variables)
    lib_call = None
    if node.node_body and node.node_body.choice:
        if isinstance(node.node_body.choice, LibraryNodeCall):
            lib_call = node.node_body.choice

    # Check what declarations we have
    has_local_vars = (
        node.variable_declarations
        and node.variable_declarations.declare_variable_or_declare_array_or_declare_mutex
    )
    has_alias_vars = lib_call and lib_call.alias

    # Variable declarations field(s)
    # The format varies based on what's present:
    # - Both present: concatenate into one field (localVars)(aliasVars), no comma between
    # - Only alias: field2=(aliasVars), field3=(none)
    # - Only local: field2=(localVars), field3=(none)
    # - Neither: field2=nilocdecl, field3=(none)

    if has_local_vars and has_alias_vars:
        # Both present: concatenate with no comma between them
        # Local vars first
        writer.write("(")
        all_vars = (
            node.variable_declarations.declare_variable_or_declare_array_or_declare_mutex
        )
        for i, var_decl in enumerate(all_vars):
            if i > 0:
                writer.write(" ")
            writer.write(format_var_decl_for_library(var_decl))
        writer.write(")")

        # Alias vars immediately after (no comma!)
        writer.write("(")
        for i, alias in enumerate(lib_call.alias):
            if i > 0:
                writer.write(" ")
            param_name = alias.node_parameter
            writer.write(f"('{param_name} : unknown)")
        writer.writeln("),")

    elif has_alias_vars:
        # Only alias vars: two separate fields
        writer.write("(")
        for i, alias in enumerate(lib_call.alias):
            if i > 0:
                writer.write(" ")
            param_name = alias.node_parameter
            writer.write(f"('{param_name} : unknown)")
        writer.writeln("),")
        writer.writeln("(none),")

    elif has_local_vars:
        # Only local vars: two separate fields
        writer.write("(")
        all_vars = (
            node.variable_declarations.declare_variable_or_declare_array_or_declare_mutex
        )
        for i, var_decl in enumerate(all_vars):
            if i > 0:
                writer.write(" ")
            writer.write(format_var_decl_for_library(var_decl))
        writer.writeln("),")
        writer.writeln("(none),")

    else:
        # Neither: nilocdecl and (none)
        writer.writeln("nilocdecl,")
        writer.writeln("(none),")

    # Conditions (8 types) from call site node
    # NOTE: Only output conditions if present (Haskell omits the field when none)
    conditions = collect_node_conditions(node)

    if conditions:
        writer.write("(")
        for i, cond in enumerate(conditions):
            if i > 0:
                writer.write(",")
            walk(cond, writer, context)
        writer.writeln("),")

    # CallInfo: callInfo('libraryName, ids(param1 . param2 . ...), (expr1 expr2 ...))
    if lib_call:
        library_name = lib_call.node_id.value
        writer.write(f"callInfo('{library_name},")

        # Parameter IDs
        if lib_call.alias:
            writer.write("ids(")
            for i, alias in enumerate(lib_call.alias):
                if i > 0:
                    writer.write(" . ")
                param_name = alias.node_parameter  # Now a string
                writer.write(f"'{param_name}")
            writer.write("),")
        else:
            writer.write("ids(nilq),")

        # Parameter expressions
        if lib_call.alias:
            # Check if any alias uses a variable (needs varForwarding)
            needs_parens = len(lib_call.alias) > 1
            if needs_parens:
                writer.write("(")
            for i, alias in enumerate(lib_call.alias):
                if i > 0:
                    writer.write(" ")

                # Get the value expression
                value_expr = get_alias_value(alias)

                # Check if it's a variable (needs varForwarding wrapper)
                if value_expr and (
                    isinstance(value_expr, IntegerVariable)
                    or isinstance(value_expr, RealVariable)
                    or isinstance(value_expr, BooleanVariable)
                    or isinstance(value_expr, StringVariable)
                ):
                    # Variable forwarding: const(varForwarding('varName))
                    var_name = value_expr.value
                    writer.write(f"const(varForwarding('{var_name}))")
                else:
                    # Regular value - walk it directly (it already wraps with const(val(...)))
                    if value_expr:
                        walk(value_expr, writer, context)
                    else:
                        writer.write("unknown")
            if needs_parens:
                writer.write(")")
        else:
            writer.write("nilpar")

        writer.writeln("),")
    else:
        writer.writeln("callInfo(unknown,ids(nilq),nilpar),")

    # Library definition (inlined node)
    if lib_call:
        library_name = lib_call.node_id.value
        library_plan = context.libraries.get(library_name)

        if not library_plan:
            raise TranspilationError(
                f"Library node '{node_id}' references undefined library '{library_name}'"
            )
        if not library_plan.node:
            raise TranspilationError(
                f"Library '{library_name}' has no root node (empty library)"
            )
        # Recursively translate the library's root node
        # library_plan.node is already a Node, walk it directly
        walk(library_plan.node, writer, context)
        writer.writeln()
    else:
        raise TranspilationError(
            f"Library node '{node_id}' is missing LibraryNodeCall body"
        )

    writer.dedent()
    writer.write(")")


@translate.register(NodeBody)
def _(node: NodeBody, writer: IndentedWriter, context: TranspilerContext):
    """Translate node body."""
    writer.writeln("Body {")
    writer.indent()

    if node.node_list:
        walk(node.node_list, writer, context)
    elif node.command:
        walk(node.command, writer, context)
    elif node.assignment:
        walk(node.assignment, writer, context)
    elif node.update:
        walk(node.update, writer, context)
    elif node.library_node_call:
        walk(node.library_node_call, writer, context)

    writer.dedent()
    writer.writeln("}")


@translate.register(NodeList)
def _(node: NodeList, writer: IndentedWriter, context: TranspilerContext):
    """Translate a list of child nodes."""
    for child_node in node.node:
        walk(child_node, writer, context)


@translate.register(Interface)
def _(node: Interface, writer: IndentedWriter, context: TranspilerContext):
    """Translate interface declaration."""
    writer.writeln("Interface {")
    writer.indent()

    for in_param in node.in_value:
        for var in in_param.declare_variable:
            writer.writeln(f"In: {var.type_value.value} {var.name}")
        for arr in in_param.declare_array:
            writer.writeln(f"In: {arr.type_value.value}[] {arr.name}")

    for inout_param in node.in_out:
        for var in inout_param.declare_variable:
            writer.writeln(f"InOut: {var.type_value.value} {var.name}")
        for arr in inout_param.declare_array:
            writer.writeln(f"InOut: {arr.type_value.value}[] {arr.name}")

    writer.dedent()
    writer.writeln("}")
