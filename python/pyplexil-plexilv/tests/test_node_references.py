import pytest
from plexil.core.v1.ast import (
    NodeStateVariable,
    NodeOutcomeVariable,
    NodeCommandHandleVariable,
    NodeStateValue,
    NodeOutcomeValue,
    NodeCommandHandleValue,
)

# ====================
# NodeStateVariable Tests
# ====================


def test_node_state_variable_with_child_ref(translate_xml):
    xml = """<NodeStateVariable>
      <NodeRef dir="child">TestVars1</NodeRef>
    </NodeStateVariable>"""
    assert translate_xml(xml, NodeStateVariable) == "'TestVars1"


def test_node_state_variable_with_sibling_ref(translate_xml):
    xml = """<NodeStateVariable>
      <NodeRef dir="sibling">TestReal__2</NodeRef>
    </NodeStateVariable>"""
    assert translate_xml(xml, NodeStateVariable) == "'TestReal__2"


def test_node_state_variable_with_self_ref(translate_xml):
    xml = """<NodeStateVariable>
      <NodeRef dir="self" />
    </NodeStateVariable>"""
    assert translate_xml(xml, NodeStateVariable) == "self"


def test_node_state_variable_with_parent_ref(translate_xml):
    xml = """<NodeStateVariable>
      <NodeRef dir="parent" />
    </NodeStateVariable>"""
    assert translate_xml(xml, NodeStateVariable) == "parent"


def test_node_state_variable_with_node_id(translate_xml):
    xml = """<NodeStateVariable>
      <NodeId>TestVars1</NodeId>
    </NodeStateVariable>"""
    assert translate_xml(xml, NodeStateVariable) == "'TestVars1"


# ====================
# NodeOutcomeVariable Tests
# ====================


def test_node_outcome_variable_with_child_ref(translate_xml):
    xml = """<NodeOutcomeVariable>
      <NodeRef dir="child">Printer0</NodeRef>
    </NodeOutcomeVariable>"""
    assert translate_xml(xml, NodeOutcomeVariable) == "'Printer0"


def test_node_outcome_variable_with_node_id(translate_xml):
    xml = """<NodeOutcomeVariable>
      <NodeId>callBoolArrayCommand</NodeId>
    </NodeOutcomeVariable>"""
    assert translate_xml(xml, NodeOutcomeVariable) == "'callBoolArrayCommand"


def test_node_outcome_variable_with_sibling_ref(translate_xml):
    xml = """<NodeOutcomeVariable>
      <NodeRef dir="sibling">TestVars2</NodeRef>
    </NodeOutcomeVariable>"""
    assert translate_xml(xml, NodeOutcomeVariable) == "'TestVars2"


def test_node_outcome_variable_with_self_ref(translate_xml):
    xml = """<NodeOutcomeVariable>
      <NodeRef dir="self" />
    </NodeOutcomeVariable>"""
    assert translate_xml(xml, NodeOutcomeVariable) == "self"


# ====================
# NodeCommandHandleVariable Tests
# ====================


def test_node_command_handle_variable_with_self_ref(translate_xml):
    xml = """<NodeCommandHandleVariable>
      <NodeRef dir="self" />
    </NodeCommandHandleVariable>"""
    assert translate_xml(xml, NodeCommandHandleVariable) == "self"


def test_node_command_handle_variable_with_child_ref(translate_xml):
    xml = """<NodeCommandHandleVariable>
      <NodeRef dir="child">CommandNode1</NodeRef>
    </NodeCommandHandleVariable>"""
    assert translate_xml(xml, NodeCommandHandleVariable) == "'CommandNode1"


def test_node_command_handle_variable_with_node_id(translate_xml):
    xml = """<NodeCommandHandleVariable>
      <NodeId>MyCommand</NodeId>
    </NodeCommandHandleVariable>"""
    assert translate_xml(xml, NodeCommandHandleVariable) == "'MyCommand"


# ====================
# NodeStateValue Tests
# ====================


def test_node_state_value_waiting(translate_xml):
    xml = "<NodeStateValue>WAITING</NodeStateValue>"
    assert translate_xml(xml, NodeStateValue) == "waiting"


def test_node_state_value_executing(translate_xml):
    xml = "<NodeStateValue>EXECUTING</NodeStateValue>"
    assert translate_xml(xml, NodeStateValue) == "executing"


def test_node_state_value_finished(translate_xml):
    xml = "<NodeStateValue>FINISHED</NodeStateValue>"
    assert translate_xml(xml, NodeStateValue) == "finished"


def test_node_state_value_inactive(translate_xml):
    xml = "<NodeStateValue>INACTIVE</NodeStateValue>"
    assert translate_xml(xml, NodeStateValue) == "inactive"


def test_node_state_value_failing(translate_xml):
    xml = "<NodeStateValue>FAILING</NodeStateValue>"
    assert translate_xml(xml, NodeStateValue) == "failing"


def test_node_state_value_finishing(translate_xml):
    xml = "<NodeStateValue>FINISHING</NodeStateValue>"
    assert translate_xml(xml, NodeStateValue) == "finishing"


def test_node_state_value_iteration_ended(translate_xml):
    xml = "<NodeStateValue>ITERATION_ENDED</NodeStateValue>"
    assert translate_xml(xml, NodeStateValue) == "iterationEnded"


# ====================
# NodeOutcomeValue Tests
# ====================


def test_node_outcome_value_success(translate_xml):
    xml = "<NodeOutcomeValue>SUCCESS</NodeOutcomeValue>"
    assert translate_xml(xml, NodeOutcomeValue) == "success"


def test_node_outcome_value_failure(translate_xml):
    xml = "<NodeOutcomeValue>FAILURE</NodeOutcomeValue>"
    assert translate_xml(xml, NodeOutcomeValue) == "failure"


def test_node_outcome_value_skipped(translate_xml):
    xml = "<NodeOutcomeValue>SKIPPED</NodeOutcomeValue>"
    assert translate_xml(xml, NodeOutcomeValue) == "skipped"


def test_node_outcome_value_interrupted(translate_xml):
    xml = "<NodeOutcomeValue>INTERRUPTED</NodeOutcomeValue>"
    assert translate_xml(xml, NodeOutcomeValue) == "interrupted"


# ====================
# NodeCommandHandleValue Tests
# ====================


def test_node_command_handle_value_command_success(translate_xml):
    xml = "<NodeCommandHandleValue>COMMAND_SUCCESS</NodeCommandHandleValue>"
    assert translate_xml(xml, NodeCommandHandleValue) == "commandSuccess"


def test_node_command_handle_value_command_failed(translate_xml):
    xml = "<NodeCommandHandleValue>COMMAND_FAILED</NodeCommandHandleValue>"
    assert translate_xml(xml, NodeCommandHandleValue) == "commandFailed"


def test_node_command_handle_value_command_denied(translate_xml):
    xml = "<NodeCommandHandleValue>COMMAND_DENIED</NodeCommandHandleValue>"
    assert translate_xml(xml, NodeCommandHandleValue) == "commandDenied"


def test_node_command_handle_value_command_accepted(translate_xml):
    xml = "<NodeCommandHandleValue>COMMAND_ACCEPTED</NodeCommandHandleValue>"
    assert translate_xml(xml, NodeCommandHandleValue) == "commandAccepted"
