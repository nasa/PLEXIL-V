"""Tests for node failure type handling in EQInternal predicates.

This verifies that node failure equality checks translate correctly
with the appropriate isFailure?() format and camelCase conversion.
"""

import pytest
from plexil.core.v1.ast import Eqinternal

# ====================
# Node Failure Equality Tests
# ====================


def test_eq_internal_failure_pre_condition(translate_xml):
    """Test PRE_CONDITION_FAILED translates to preconditionFailed."""
    xml = """<EQInternal>
      <NodeFailureVariable>
        <NodeId>One</NodeId>
      </NodeFailureVariable>
      <NodeFailureValue>PRE_CONDITION_FAILED</NodeFailureValue>
    </EQInternal>"""
    assert translate_xml(xml, Eqinternal) == "isFailure?('One,preconditionFailed)"


def test_eq_internal_failure_post_condition(translate_xml):
    """Test POST_CONDITION_FAILED translates to postconditionFailed."""
    xml = """<EQInternal>
      <NodeFailureVariable>
        <NodeId>TestNode</NodeId>
      </NodeFailureVariable>
      <NodeFailureValue>POST_CONDITION_FAILED</NodeFailureValue>
    </EQInternal>"""
    assert translate_xml(xml, Eqinternal) == "isFailure?('TestNode,postconditionFailed)"


def test_eq_internal_failure_invariant_condition(translate_xml):
    """Test INVARIANT_CONDITION_FAILED translates to invariantConditionFailed."""
    xml = """<EQInternal>
      <NodeFailureVariable>
        <NodeId>MyNode</NodeId>
      </NodeFailureVariable>
      <NodeFailureValue>INVARIANT_CONDITION_FAILED</NodeFailureValue>
    </EQInternal>"""
    assert (
        translate_xml(xml, Eqinternal) == "isFailure?('MyNode,invariantConditionFailed)"
    )


def test_eq_internal_failure_parent_failed(translate_xml):
    """Test PARENT_FAILED translates to parentFailed."""
    xml = """<EQInternal>
      <NodeFailureVariable>
        <NodeId>Child</NodeId>
      </NodeFailureVariable>
      <NodeFailureValue>PARENT_FAILED</NodeFailureValue>
    </EQInternal>"""
    assert translate_xml(xml, Eqinternal) == "isFailure?('Child,parentFailed)"


def test_eq_internal_failure_parent_exited(translate_xml):
    """Test PARENT_EXITED translates to parentExited."""
    xml = """<EQInternal>
      <NodeFailureVariable>
        <NodeId>Node1</NodeId>
      </NodeFailureVariable>
      <NodeFailureValue>PARENT_EXITED</NodeFailureValue>
    </EQInternal>"""
    assert translate_xml(xml, Eqinternal) == "isFailure?('Node1,parentExited)"


def test_eq_internal_failure_exited(translate_xml):
    """Test EXITED translates to exited."""
    xml = """<EQInternal>
      <NodeFailureVariable>
        <NodeId>Test</NodeId>
      </NodeFailureVariable>
      <NodeFailureValue>EXITED</NodeFailureValue>
    </EQInternal>"""
    assert translate_xml(xml, Eqinternal) == "isFailure?('Test,exited)"


def test_eq_internal_failure_with_sibling_ref(translate_xml):
    """Test node failure check with sibling reference.

    EQInternal predicates use 'NodeName format for child/sibling refs,
    unlike node predicates which use child()/sibling() wrappers.
    """
    xml = """<EQInternal>
      <NodeFailureVariable>
        <NodeRef dir="sibling">One</NodeRef>
      </NodeFailureVariable>
      <NodeFailureValue>PRE_CONDITION_FAILED</NodeFailureValue>
    </EQInternal>"""
    assert translate_xml(xml, Eqinternal) == "isFailure?('One,preconditionFailed)"


def test_eq_internal_failure_with_self_ref(translate_xml):
    """Test node failure check with self reference."""
    xml = """<EQInternal>
      <NodeFailureVariable>
        <NodeRef dir="self"/>
      </NodeFailureVariable>
      <NodeFailureValue>INVARIANT_CONDITION_FAILED</NodeFailureValue>
    </EQInternal>"""
    assert translate_xml(xml, Eqinternal) == "isFailure?(self,invariantConditionFailed)"


def test_eq_internal_failure_with_parent_ref(translate_xml):
    """Test node failure check with parent reference."""
    xml = """<EQInternal>
      <NodeFailureVariable>
        <NodeRef dir="parent"/>
      </NodeFailureVariable>
      <NodeFailureValue>EXITED</NodeFailureValue>
    </EQInternal>"""
    assert translate_xml(xml, Eqinternal) == "isFailure?(parent,exited)"


def test_eq_internal_failure_with_child_ref(translate_xml):
    """Test node failure check with child reference.

    EQInternal predicates use 'NodeName format for child/sibling refs,
    unlike node predicates which use child()/sibling() wrappers.
    """
    xml = """<EQInternal>
      <NodeFailureVariable>
        <NodeRef dir="child">ChildNode</NodeRef>
      </NodeFailureVariable>
      <NodeFailureValue>POST_CONDITION_FAILED</NodeFailureValue>
    </EQInternal>"""
    assert (
        translate_xml(xml, Eqinternal) == "isFailure?('ChildNode,postconditionFailed)"
    )


# ====================
# Integration Test - FailureType3 Acceptance Test Pattern
# ====================


def test_failure_type3_acceptance_pattern(translate_xml):
    """Test the exact pattern from FailureType3.plx acceptance test.

    This ensures that the complete AND condition with Finished and EQInternal
    translates correctly with isFailure?() using the correct camelCase format.
    """
    xml = """<StartCondition>
      <AND>
        <Finished>
          <NodeId>One</NodeId>
        </Finished>
        <EQInternal>
          <NodeFailureVariable>
            <NodeId>One</NodeId>
          </NodeFailureVariable>
          <NodeFailureValue>PRE_CONDITION_FAILED</NodeFailureValue>
        </EQInternal>
      </AND>
    </StartCondition>"""
    from plexil.core.v1.ast import StartCondition

    result = translate_xml(xml, StartCondition)
    # Should have both isFinished? and isFailure? with preconditionFailed
    assert "isFinished?('One)" in result
    assert "isFailure?('One,preconditionFailed)" in result
    assert "startc:" in result
    assert "_and_" in result
