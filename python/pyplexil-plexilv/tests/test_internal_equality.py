import pytest
from plexil.core.v1.ast import Eqinternal, Neinternal

# ====================
# Eqinternal - Node State Equality
# ====================


def test_eq_internal_state_finished(translate_xml):
    xml = """<Eqinternal>
      <NodeStateVariable>
        <NodeRef dir="child">TestVars1</NodeRef>
      </NodeStateVariable>
      <NodeStateValue>FINISHED</NodeStateValue>
    </Eqinternal>"""
    assert translate_xml(xml, Eqinternal) == "isStatus?('TestVars1,finished)"


def test_eq_internal_state_waiting(translate_xml):
    xml = """<Eqinternal>
      <NodeStateVariable>
        <NodeRef dir="child">TestVars1</NodeRef>
      </NodeStateVariable>
      <NodeStateValue>WAITING</NodeStateValue>
    </Eqinternal>"""
    assert translate_xml(xml, Eqinternal) == "isStatus?('TestVars1,waiting)"


def test_eq_internal_state_executing(translate_xml):
    xml = """<Eqinternal>
      <NodeStateVariable>
        <NodeRef dir="child">TestVars1</NodeRef>
      </NodeStateVariable>
      <NodeStateValue>EXECUTING</NodeStateValue>
    </Eqinternal>"""
    assert translate_xml(xml, Eqinternal) == "isStatus?('TestVars1,executing)"


def test_eq_internal_state_finishing_reversed(translate_xml):
    xml = """<Eqinternal>
      <NodeStateValue>FINISHING</NodeStateValue>
      <NodeStateVariable>
        <NodeRef dir="child">TestVars1</NodeRef>
      </NodeStateVariable>
    </Eqinternal>"""
    assert translate_xml(xml, Eqinternal) == "isStatus?('TestVars1,finishing)"


def test_eq_internal_state_failing(translate_xml):
    xml = """<Eqinternal>
      <NodeStateVariable>
        <NodeRef dir="child">TestVars1</NodeRef>
      </NodeStateVariable>
      <NodeStateValue>FAILING</NodeStateValue>
    </Eqinternal>"""
    assert translate_xml(xml, Eqinternal) == "isStatus?('TestVars1,failing)"


def test_eq_internal_state_iteration_ended(translate_xml):
    xml = """<Eqinternal>
      <NodeStateVariable>
        <NodeRef dir="child">TestVars1</NodeRef>
      </NodeStateVariable>
      <NodeStateValue>ITERATION_ENDED</NodeStateValue>
    </Eqinternal>"""
    assert translate_xml(xml, Eqinternal) == "isStatus?('TestVars1,iterationEnded)"


def test_eq_internal_state_inactive(translate_xml):
    xml = """<Eqinternal>
      <NodeStateVariable>
        <NodeRef dir="child">TestVars1</NodeRef>
      </NodeStateVariable>
      <NodeStateValue>INACTIVE</NodeStateValue>
    </Eqinternal>"""
    assert translate_xml(xml, Eqinternal) == "isStatus?('TestVars1,inactive)"


def test_eq_internal_state_with_sibling(translate_xml):
    xml = """<Eqinternal>
      <NodeStateVariable>
        <NodeRef dir="sibling">MyNode</NodeRef>
      </NodeStateVariable>
      <NodeStateValue>EXECUTING</NodeStateValue>
    </Eqinternal>"""
    assert translate_xml(xml, Eqinternal) == "isStatus?('MyNode,executing)"


def test_eq_internal_state_with_self(translate_xml):
    xml = """<Eqinternal>
      <NodeStateVariable>
        <NodeRef dir="self" />
      </NodeStateVariable>
      <NodeStateValue>WAITING</NodeStateValue>
    </Eqinternal>"""
    assert translate_xml(xml, Eqinternal) == "isStatus?(self,waiting)"


def test_eq_internal_state_with_parent(translate_xml):
    xml = """<Eqinternal>
      <NodeStateVariable>
        <NodeRef dir="parent" />
      </NodeStateVariable>
      <NodeStateValue>FINISHED</NodeStateValue>
    </Eqinternal>"""
    assert translate_xml(xml, Eqinternal) == "isStatus?(parent,finished)"


def test_eq_internal_state_with_node_id(translate_xml):
    xml = """<Eqinternal>
      <NodeStateVariable>
        <NodeId>Task1</NodeId>
      </NodeStateVariable>
      <NodeStateValue>EXECUTING</NodeStateValue>
    </Eqinternal>"""
    assert translate_xml(xml, Eqinternal) == "isStatus?('Task1,executing)"


# ====================
# Eqinternal - Node Outcome Equality
# ====================


def test_eq_internal_outcome_failure(translate_xml):
    xml = """<Eqinternal>
      <NodeOutcomeVariable>
        <NodeRef dir="child">TestVars1</NodeRef>
      </NodeOutcomeVariable>
      <NodeOutcomeValue>FAILURE</NodeOutcomeValue>
    </Eqinternal>"""
    assert translate_xml(xml, Eqinternal) == "isOutcomeFailure?('TestVars1)"


def test_eq_internal_outcome_success_reversed(translate_xml):
    xml = """<Eqinternal>
      <NodeOutcomeValue>SUCCESS</NodeOutcomeValue>
      <NodeOutcomeVariable>
        <NodeRef dir="child">TestVars2</NodeRef>
      </NodeOutcomeVariable>
    </Eqinternal>"""
    assert translate_xml(xml, Eqinternal) == "isOutcome?('TestVars2,success)"


def test_eq_internal_outcome_skipped(translate_xml):
    xml = """<Eqinternal>
      <NodeOutcomeVariable>
        <NodeRef dir="child">TestVars1</NodeRef>
      </NodeOutcomeVariable>
      <NodeOutcomeValue>SKIPPED</NodeOutcomeValue>
    </Eqinternal>"""
    assert translate_xml(xml, Eqinternal) == "isOutcome?('TestVars1,skipped)"


def test_eq_internal_outcome_interrupted(translate_xml):
    xml = """<Eqinternal>
      <NodeOutcomeVariable>
        <NodeRef dir="child">TestVars1</NodeRef>
      </NodeOutcomeVariable>
      <NodeOutcomeValue>INTERRUPTED</NodeOutcomeValue>
    </Eqinternal>"""
    assert translate_xml(xml, Eqinternal) == "isOutcome?('TestVars1,interrupted)"


def test_eq_internal_outcome_with_sibling(translate_xml):
    xml = """<Eqinternal>
      <NodeOutcomeVariable>
        <NodeRef dir="sibling">Task2</NodeRef>
      </NodeOutcomeVariable>
      <NodeOutcomeValue>SUCCESS</NodeOutcomeValue>
    </Eqinternal>"""
    assert translate_xml(xml, Eqinternal) == "isOutcome?('Task2,success)"


def test_eq_internal_outcome_with_self(translate_xml):
    xml = """<Eqinternal>
      <NodeOutcomeVariable>
        <NodeRef dir="self" />
      </NodeOutcomeVariable>
      <NodeOutcomeValue>FAILURE</NodeOutcomeValue>
    </Eqinternal>"""
    assert translate_xml(xml, Eqinternal) == "isOutcomeFailure?(self)"


def test_eq_internal_outcome_with_node_id(translate_xml):
    xml = """<Eqinternal>
      <NodeOutcomeVariable>
        <NodeId>MyTask</NodeId>
      </NodeOutcomeVariable>
      <NodeOutcomeValue>SUCCESS</NodeOutcomeValue>
    </Eqinternal>"""
    assert translate_xml(xml, Eqinternal) == "isOutcome?('MyTask,success)"


# ====================
# Eqinternal - Command Handle Equality
# ====================


def test_eq_internal_command_handle_success(translate_xml):
    xml = """<Eqinternal>
      <NodeCommandHandleVariable>
        <NodeRef dir="self" />
      </NodeCommandHandleVariable>
      <NodeCommandHandleValue>COMMAND_SUCCESS</NodeCommandHandleValue>
    </Eqinternal>"""
    assert translate_xml(xml, Eqinternal) == "cmdHandleIs?(self,CommandSuccess)"


def test_eq_internal_command_handle_failed(translate_xml):
    xml = """<Eqinternal>
      <NodeCommandHandleVariable>
        <NodeRef dir="child">CmdNode</NodeRef>
      </NodeCommandHandleVariable>
      <NodeCommandHandleValue>COMMAND_FAILED</NodeCommandHandleValue>
    </Eqinternal>"""
    assert translate_xml(xml, Eqinternal) == "cmdHandleIs?('CmdNode,CommandFailed)"


def test_eq_internal_command_handle_denied(translate_xml):
    xml = """<Eqinternal>
      <NodeCommandHandleVariable>
        <NodeRef dir="child">CmdNode</NodeRef>
      </NodeCommandHandleVariable>
      <NodeCommandHandleValue>COMMAND_DENIED</NodeCommandHandleValue>
    </Eqinternal>"""
    assert translate_xml(xml, Eqinternal) == "cmdHandleIs?('CmdNode,CommandDenied)"


def test_eq_internal_command_handle_accepted(translate_xml):
    xml = """<Eqinternal>
      <NodeCommandHandleVariable>
        <NodeRef dir="child">CmdNode</NodeRef>
      </NodeCommandHandleVariable>
      <NodeCommandHandleValue>COMMAND_ACCEPTED</NodeCommandHandleValue>
    </Eqinternal>"""
    assert translate_xml(xml, Eqinternal) == "cmdHandleIs?('CmdNode,CommandAccepted)"


def test_eq_internal_command_handle_reversed(translate_xml):
    xml = """<Eqinternal>
      <NodeCommandHandleValue>COMMAND_SUCCESS</NodeCommandHandleValue>
      <NodeCommandHandleVariable>
        <NodeRef dir="self" />
      </NodeCommandHandleVariable>
    </Eqinternal>"""
    assert translate_xml(xml, Eqinternal) == "cmdHandleIs?(self,CommandSuccess)"


def test_eq_internal_command_handle_with_sibling(translate_xml):
    xml = """<Eqinternal>
      <NodeCommandHandleVariable>
        <NodeRef dir="sibling">Command1</NodeRef>
      </NodeCommandHandleVariable>
      <NodeCommandHandleValue>COMMAND_SUCCESS</NodeCommandHandleValue>
    </Eqinternal>"""
    assert translate_xml(xml, Eqinternal) == "cmdHandleIs?('Command1,CommandSuccess)"


def test_eq_internal_command_handle_with_node_id(translate_xml):
    xml = """<Eqinternal>
      <NodeCommandHandleVariable>
        <NodeId>MyCommand</NodeId>
      </NodeCommandHandleVariable>
      <NodeCommandHandleValue>COMMAND_SUCCESS</NodeCommandHandleValue>
    </Eqinternal>"""
    assert translate_xml(xml, Eqinternal) == "cmdHandleIs?('MyCommand,CommandSuccess)"


def test_eq_internal_command_handle_sent_to_system(translate_xml):
    """Test COMMAND_SENT_TO_SYSTEM translates to CommandSentToSystem.

    This is from simple-closedloop-command-a1.plx acceptance test.
    The fallback conversion should capitalize all parts: COMMAND_SENT_TO_SYSTEM -> CommandSentToSystem
    """
    xml = """<Eqinternal>
      <NodeCommandHandleVariable>
        <NodeId>Drive</NodeId>
      </NodeCommandHandleVariable>
      <NodeCommandHandleValue>COMMAND_SENT_TO_SYSTEM</NodeCommandHandleValue>
    </Eqinternal>"""
    assert translate_xml(xml, Eqinternal) == "cmdHandleIs?('Drive,CommandSentToSystem)"


# ====================
# Neinternal - Node State Inequality
# ====================


def test_ne_internal_state_finished(translate_xml):
    xml = """<Neinternal>
      <NodeStateVariable>
        <NodeRef dir="child">TestVars1</NodeRef>
      </NodeStateVariable>
      <NodeStateValue>FINISHED</NodeStateValue>
    </Neinternal>"""
    assert translate_xml(xml, Neinternal) == "_not_(isStatus?('TestVars1,finished))"


def test_ne_internal_state_with_self(translate_xml):
    xml = """<Neinternal>
      <NodeStateVariable>
        <NodeRef dir="self" />
      </NodeStateVariable>
      <NodeStateValue>WAITING</NodeStateValue>
    </Neinternal>"""
    assert translate_xml(xml, Neinternal) == "_not_(isStatus?(self,waiting))"


def test_ne_internal_state_reversed(translate_xml):
    xml = """<Neinternal>
      <NodeStateValue>EXECUTING</NodeStateValue>
      <NodeStateVariable>
        <NodeRef dir="child">Task1</NodeRef>
      </NodeStateVariable>
    </Neinternal>"""
    assert translate_xml(xml, Neinternal) == "_not_(isStatus?('Task1,executing))"


# ====================
# Neinternal - Node Outcome Inequality
# ====================


def test_ne_internal_outcome_failure(translate_xml):
    xml = """<Neinternal>
      <NodeOutcomeVariable>
        <NodeRef dir="child">TestVars1</NodeRef>
      </NodeOutcomeVariable>
      <NodeOutcomeValue>FAILURE</NodeOutcomeValue>
    </Neinternal>"""
    assert translate_xml(xml, Neinternal) == "_not_(isOutcomeFailure?('TestVars1))"


def test_ne_internal_outcome_success(translate_xml):
    xml = """<Neinternal>
      <NodeOutcomeVariable>
        <NodeRef dir="child">TestVars2</NodeRef>
      </NodeOutcomeVariable>
      <NodeOutcomeValue>SUCCESS</NodeOutcomeValue>
    </Neinternal>"""
    assert translate_xml(xml, Neinternal) == "_not_(isOutcome?('TestVars2,success))"


def test_ne_internal_outcome_with_self(translate_xml):
    xml = """<Neinternal>
      <NodeOutcomeVariable>
        <NodeRef dir="self" />
      </NodeOutcomeVariable>
      <NodeOutcomeValue>SKIPPED</NodeOutcomeValue>
    </Neinternal>"""
    assert translate_xml(xml, Neinternal) == "_not_(isOutcome?(self,skipped))"


# ====================
# Neinternal - Command Handle Inequality
# ====================


def test_ne_internal_command_handle_success(translate_xml):
    xml = """<Neinternal>
      <NodeCommandHandleVariable>
        <NodeRef dir="self" />
      </NodeCommandHandleVariable>
      <NodeCommandHandleValue>COMMAND_SUCCESS</NodeCommandHandleValue>
    </Neinternal>"""
    assert translate_xml(xml, Neinternal) == "_not_(cmdHandleIs?(self,CommandSuccess))"


def test_ne_internal_command_handle_failed(translate_xml):
    xml = """<Neinternal>
      <NodeCommandHandleVariable>
        <NodeRef dir="child">CmdNode</NodeRef>
      </NodeCommandHandleVariable>
      <NodeCommandHandleValue>COMMAND_FAILED</NodeCommandHandleValue>
    </Neinternal>"""
    assert (
        translate_xml(xml, Neinternal) == "_not_(cmdHandleIs?('CmdNode,CommandFailed))"
    )


def test_ne_internal_command_handle_reversed(translate_xml):
    xml = """<Neinternal>
      <NodeCommandHandleValue>COMMAND_DENIED</NodeCommandHandleValue>
      <NodeCommandHandleVariable>
        <NodeRef dir="child">Task1</NodeRef>
      </NodeCommandHandleVariable>
    </Neinternal>"""
    assert translate_xml(xml, Neinternal) == "_not_(cmdHandleIs?('Task1,CommandDenied))"
