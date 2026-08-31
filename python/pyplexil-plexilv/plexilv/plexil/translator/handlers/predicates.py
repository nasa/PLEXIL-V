"""Node predicate translation handlers"""

from ..dispatch import translate, walk
from plexilv.common import IndentedWriter
from ..state import TranspilerContext
from ._helpers import *
from plexil.core.v1 import *


@translate.register(Waiting)
def _(node: Waiting, writer: IndentedWriter, context: TranspilerContext):
    """Translate Waiting predicate."""
    ref = format_node_predicate_reference(node.node_id_or_node_ref)
    writer.write(f"isWaiting?({ref})")


@translate.register(Executing)
def _(node: Executing, writer: IndentedWriter, context: TranspilerContext):
    """Translate Executing predicate."""
    ref = format_node_predicate_reference(node.node_id_or_node_ref)
    writer.write(f"isExecuting?({ref})")


@translate.register(Finished)
def _(node: Finished, writer: IndentedWriter, context: TranspilerContext):
    """Translate Finished predicate."""
    ref = format_node_predicate_reference(node.node_id_or_node_ref)
    writer.write(f"isFinished?({ref})")


@translate.register(IterationEnded)
def _(node: IterationEnded, writer: IndentedWriter, context: TranspilerContext):
    """Translate IterationEnded predicate."""
    ref = format_node_predicate_reference(node.node_id_or_node_ref)
    writer.write(f"hasIterationEnded?({ref})")


@translate.register(Inactive)
def _(node: Inactive, writer: IndentedWriter, context: TranspilerContext):
    """Translate Inactive predicate."""
    ref = format_node_predicate_reference(node.node_id_or_node_ref)
    writer.write(f"isInactive?({ref})")


# Outcome Predicates


@translate.register(Succeeded)
def _(node: Succeeded, writer: IndentedWriter, context: TranspilerContext):
    """Translate Succeeded predicate."""
    ref = format_node_predicate_reference(node.node_id_or_node_ref)
    writer.write(f"hasSucceeded?({ref})")


@translate.register(Failed)
def _(node: Failed, writer: IndentedWriter, context: TranspilerContext):
    """Translate Failed predicate."""
    ref = format_node_predicate_reference(node.node_id_or_node_ref)
    writer.write(f"hasFailed?({ref})")


@translate.register(Skipped)
def _(node: Skipped, writer: IndentedWriter, context: TranspilerContext):
    """Translate Skipped predicate."""
    ref = format_node_predicate_reference(node.node_id_or_node_ref)
    writer.write(f"hasSkipped?({ref})")


@translate.register(PostconditionFailed)
def _(node: PostconditionFailed, writer: IndentedWriter, context: TranspilerContext):
    """Translate PostconditionFailed predicate."""
    ref = format_node_predicate_reference(node.node_id_or_node_ref)
    writer.write(f"hasPostconditionFailed?({ref})")


# Composite Predicates


@translate.register(NoChildFailed)
def _(node: NoChildFailed, writer: IndentedWriter, context: TranspilerContext):
    """Translate NoChildFailed predicate."""
    # NoChildFailed always translates to just "noChildFailed" regardless of node ref
    writer.write("noChildFailed")


# Knowledge Tests


@translate.register(AllKnown)
def _(node: AllKnown, writer: IndentedWriter, context: TranspilerContext):
    """Translate AllKnown predicate."""
    writer.write("allKnown(")

    if node.choice:
        walk(node.choice, writer, context)

    writer.write(")")


@translate.register(AnyKnown)
def _(node: AnyKnown, writer: IndentedWriter, context: TranspilerContext):
    """Translate AnyKnown predicate."""
    writer.write("anyKnown(")

    if node.choice:
        walk(node.choice, writer, context)

    writer.write(")")


@translate.register(Eqinternal)
def _(node: Eqinternal, writer: IndentedWriter, context: TranspilerContext):
    """Translate EQInternal predicate."""
    # With compound fields, Eqinternal has a choice list with Variable and Value elements
    # Extract them into the old structure for compatibility
    node_state_variable = [
        item for item in node.choice if isinstance(item, NodeStateVariable)
    ]
    node_state_value = [
        item for item in node.choice if isinstance(item, NodeStateValue)
    ]
    node_outcome_variable = [
        item for item in node.choice if isinstance(item, NodeOutcomeVariable)
    ]
    node_outcome_value = [
        item for item in node.choice if isinstance(item, NodeOutcomeValue)
    ]
    node_command_handle_variable = [
        item for item in node.choice if isinstance(item, NodeCommandHandleVariable)
    ]
    node_command_handle_value = [
        item for item in node.choice if isinstance(item, NodeCommandHandleValue)
    ]
    node_failure_variable = [
        item for item in node.choice if isinstance(item, NodeFailureVariable)
    ]
    node_failure_value = [
        item for item in node.choice if isinstance(item, NodeFailureValue)
    ]

    # Determine which type of internal equality this is
    if node_state_variable and node_state_value:
        # Node state equality
        var = node_state_variable[0]
        val = node_state_value[0]

        # Get the node reference using helper
        ref_str = get_node_ref_string(var)

        # Get the state value - handle enum or string
        if isinstance(val.value, str):
            value_str = val.value
        else:
            value_str = val.value.value
        if value_str == "ITERATION_ENDED":
            state_value = "iterationEnded"
        else:
            state_value = value_str.lower()

        # Format as isStatus?(ref,stateValue)
        writer.write(f"isStatus?({ref_str},{state_value})")

    elif node_outcome_variable and node_outcome_value:
        # Node outcome equality
        var = node_outcome_variable[0]
        val = node_outcome_value[0]

        # Get the node reference using helper
        ref_str = get_node_ref_string(var)

        # Get the outcome value - handle enum or string
        if isinstance(val.value, str):
            outcome_value = val.value.lower()
        else:
            outcome_value = val.value.value.lower()

        # Special case: FAILURE uses isOutcomeFailure?
        if outcome_value == "failure":
            writer.write(f"isOutcomeFailure?({ref_str})")
        else:
            writer.write(f"isOutcome?({ref_str},{outcome_value})")

    elif node_command_handle_variable and node_command_handle_value:
        # Command handle equality
        var = node_command_handle_variable[0]
        val = node_command_handle_value[0]

        # Get the node reference using helper
        ref_str = get_node_ref_string(var)

        # Convert command handle value to PascalCase
        # COMMAND_SUCCESS -> CommandSuccess
        if isinstance(val.value, str):
            cmd_val = val.value.lower()
        else:
            cmd_val = val.value.value.lower()
        if cmd_val == "command_success":
            cmd_str = "CommandSuccess"
        elif cmd_val == "command_failed":
            cmd_str = "CommandFailed"
        elif cmd_val == "command_denied":
            cmd_str = "CommandDenied"
        elif cmd_val == "command_accepted":
            cmd_str = "CommandAccepted"
        else:
            # Fallback: convert COMMAND_SENT_TO_SYSTEM -> CommandSentToSystem
            parts = cmd_val.split("_")
            cmd_str = "".join(p.capitalize() for p in parts)

        writer.write(f"cmdHandleIs?({ref_str},{cmd_str})")

    elif node_failure_variable and node_failure_value:
        # Node failure equality
        var = node_failure_variable[0]
        val = node_failure_value[0]

        # Get the node reference using helper
        ref_str = get_node_ref_string(var)

        # Convert failure value to camelCase
        # PRE_CONDITION_FAILED -> preconditionFailed
        # POST_CONDITION_FAILED -> postconditionFailed
        # INVARIANT_CONDITION_FAILED -> invariantConditionFailed
        # PARENT_FAILED -> parentFailed
        # PARENT_EXITED -> parentExited
        # EXITED -> exited
        if isinstance(val.value, str):
            failure_val = val.value.lower()
        else:
            failure_val = val.value.value.lower()

        # Special handling for known failure types
        if failure_val == "pre_condition_failed":
            failure_str = "preconditionFailed"
        elif failure_val == "post_condition_failed":
            failure_str = "postconditionFailed"
        elif failure_val == "invariant_condition_failed":
            failure_str = "invariantConditionFailed"
        elif failure_val == "parent_failed":
            failure_str = "parentFailed"
        elif failure_val == "parent_exited":
            failure_str = "parentExited"
        elif failure_val == "exited":
            failure_str = "exited"
        else:
            # Fallback: convert SNAKE_CASE to camelCase
            parts = failure_val.split("_")
            failure_str = parts[0] + "".join(p.capitalize() for p in parts[1:] if p)

        writer.write(f"isFailure?({ref_str},{failure_str})")


@translate.register(Neinternal)
def _(node: Neinternal, writer: IndentedWriter, context: TranspilerContext):
    """Translate NEInternal predicate as negation of EQInternal."""
    writer.write("_not_(")

    # With compound fields, Neinternal has the same structure as Eqinternal
    # Create a temporary Eqinternal node with the same choice list
    eq_node = Eqinternal(choice=node.choice)

    # Translate the EQInternal equivalent
    walk(eq_node, writer, context)

    writer.write(")")
