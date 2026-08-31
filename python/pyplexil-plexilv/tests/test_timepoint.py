"""Tests for NodeTimepointValue translation.

These tests verify that node timepoint values are correctly translated
with the proper format and parenthesization.
"""

import pytest
from plexil.core.v1.ast import Node, IsKnown


def test_timepoint_with_node_id(translate_xml):
    """Test timepoint with explicit node ID."""
    xml = """
    <IsKnown>
        <NodeTimepointValue>
            <NodeId>myNode</NodeId>
            <NodeStateValue>INACTIVE</NodeStateValue>
            <Timepoint>START</Timepoint>
        </NodeTimepointValue>
    </IsKnown>
    """
    result = translate_xml(xml, IsKnown)
    # Node ID should be wrapped in extra parentheses
    assert result == "isKnown(timepoint(('myNode),inactive,start))"


def test_timepoint_with_self_reference(translate_xml):
    """Test timepoint with self reference."""
    xml = """
    <IsKnown>
        <NodeTimepointValue>
            <NodeRef dir="self"/>
            <NodeStateValue>EXECUTING</NodeStateValue>
            <Timepoint>START</Timepoint>
        </NodeTimepointValue>
    </IsKnown>
    """
    result = translate_xml(xml, IsKnown)
    # self should NOT have extra parentheses
    assert result == "isKnown(timepoint(self,executing,start))"


def test_timepoint_with_parent_reference(translate_xml):
    """Test timepoint with parent reference."""
    xml = """
    <IsKnown>
        <NodeTimepointValue>
            <NodeRef dir="parent"/>
            <NodeStateValue>FINISHED</NodeStateValue>
            <Timepoint>END</Timepoint>
        </NodeTimepointValue>
    </IsKnown>
    """
    result = translate_xml(xml, IsKnown)
    # parent should NOT have extra parentheses
    assert result == "isKnown(timepoint(parent,finished,end))"


def test_timepoint_states(translate_xml):
    """Test various node state values."""
    states = [
        ("WAITING", "waiting"),
        ("EXECUTING", "executing"),
        ("FINISHING", "finishing"),
        ("FAILING", "failing"),
        ("ITERATION_ENDED", "iteration_ended"),
        ("FINISHED", "finished"),
        ("INACTIVE", "inactive"),
    ]

    for xml_state, expected_state in states:
        xml = f"""
        <IsKnown>
            <NodeTimepointValue>
                <NodeRef dir="self"/>
                <NodeStateValue>{xml_state}</NodeStateValue>
                <Timepoint>START</Timepoint>
            </NodeTimepointValue>
        </IsKnown>
        """
        result = translate_xml(xml, IsKnown)
        assert result == f"isKnown(timepoint(self,{expected_state},start))"


def test_timepoint_values(translate_xml):
    """Test START and END timepoints."""
    timepoints = [
        ("START", "start"),
        ("END", "end"),
    ]

    for xml_timepoint, expected_timepoint in timepoints:
        xml = f"""
        <IsKnown>
            <NodeTimepointValue>
                <NodeRef dir="self"/>
                <NodeStateValue>EXECUTING</NodeStateValue>
                <Timepoint>{xml_timepoint}</Timepoint>
            </NodeTimepointValue>
        </IsKnown>
        """
        result = translate_xml(xml, IsKnown)
        assert result == f"isKnown(timepoint(self,executing,{expected_timepoint}))"


def test_timepoint_in_end_condition(translate_xml):
    """Test timepoint used in an end condition."""
    xml = """
    <Node NodeType="Empty">
        <NodeId>timepoint_test</NodeId>
        <EndCondition>
            <IsKnown>
                <NodeTimepointValue>
                    <NodeId>timepoint_test</NodeId>
                    <NodeStateValue>INACTIVE</NodeStateValue>
                    <Timepoint>START</Timepoint>
                </NodeTimepointValue>
            </IsKnown>
        </EndCondition>
    </Node>
    """
    result = translate_xml(xml, Node)

    # Check that timepoint is correctly formatted in the condition
    assert "isKnown(timepoint(('timepoint_test),inactive,start))" in result
    # Check that node name preserves underscore
    assert "'timepoint_test" in result


def test_timepoint_with_named_node_ref(translate_xml):
    """Test timepoint with a named node reference (not self/parent)."""
    xml = """
    <IsKnown>
        <NodeTimepointValue>
            <NodeRef>otherNode</NodeRef>
            <NodeStateValue>EXECUTING</NodeStateValue>
            <Timepoint>END</Timepoint>
        </NodeTimepointValue>
    </IsKnown>
    """
    result = translate_xml(xml, IsKnown)
    # Named node refs should have extra parentheses
    assert result == "isKnown(timepoint(('otherNode),executing,end))"


def test_timepoint_with_underscore_in_node_name(translate_xml):
    """Test timepoint with node name containing underscore."""
    xml = """
    <IsKnown>
        <NodeTimepointValue>
            <NodeId>node_with_underscore</NodeId>
            <NodeStateValue>WAITING</NodeStateValue>
            <Timepoint>START</Timepoint>
        </NodeTimepointValue>
    </IsKnown>
    """
    result = translate_xml(xml, IsKnown)
    # Node names preserve underscore
    assert result == "isKnown(timepoint(('node_with_underscore),waiting,start))"


def test_timepoint_in_arithmetic_expression(translate_xml):
    """Test timepoint used in arithmetic expression (common pattern)."""
    xml = """
    <Node NodeType="Empty">
        <NodeId>WaitNode</NodeId>
        <EndCondition>
            <GE>
                <LookupOnChange>
                    <Name>
                        <StringValue>time</StringValue>
                    </Name>
                </LookupOnChange>
                <ADD>
                    <IntegerValue>1</IntegerValue>
                    <NodeTimepointValue>
                        <NodeRef dir="self"/>
                        <NodeStateValue>EXECUTING</NodeStateValue>
                        <Timepoint>START</Timepoint>
                    </NodeTimepointValue>
                </ADD>
            </GE>
        </EndCondition>
    </Node>
    """
    result = translate_xml(xml, Node)

    # Check that timepoint is correctly used in the expression
    assert "timepoint(self,executing,start)" in result
    # Should be part of an ADD operation
    assert "_+_" in result


def test_timepoint_comparison_multiple_states(translate_xml):
    """Test multiple timepoint comparisons in same expression."""
    xml = """
    <AND>
        <IsKnown>
            <NodeTimepointValue>
                <NodeRef dir="self"/>
                <NodeStateValue>INACTIVE</NodeStateValue>
                <Timepoint>START</Timepoint>
            </NodeTimepointValue>
        </IsKnown>
        <IsKnown>
            <NodeTimepointValue>
                <NodeRef dir="self"/>
                <NodeStateValue>EXECUTING</NodeStateValue>
                <Timepoint>END</Timepoint>
            </NodeTimepointValue>
        </IsKnown>
    </AND>
    """
    from plexil.core.v1.ast import And

    result = translate_xml(xml, And)

    # Both timepoints should be present
    assert "timepoint(self,inactive,start)" in result
    assert "timepoint(self,executing,end)" in result
