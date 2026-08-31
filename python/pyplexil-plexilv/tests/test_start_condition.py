"""Tests for StartCondition translation in command nodes.

This test ensures that StartCondition elements within nodes are properly
translated when nodes are children of a NodeList.

This prevents regression of the fix that converts PascalCase condition names
to snake_case when reconstructing Node from AnyElement children.
"""

import pytest
from plexil.core.v1.ast import Node
from tests.conftest import normalize_whitespace


def test_command_node_with_start_condition(translate_xml):
    """Test Command node with StartCondition translates correctly."""
    xml = """
    <Node NodeType="Command">
        <NodeId>TestCommand</NodeId>
        <StartCondition>
            <EQInternal>
                <NodeStateVariable>
                    <NodeId>OtherNode</NodeId>
                </NodeStateVariable>
                <NodeStateValue>FINISHED</NodeStateValue>
            </EQInternal>
        </StartCondition>
        <NodeBody>
            <Command>
                <Name>
                    <StringValue>executeTask</StringValue>
                </Name>
            </Command>
        </NodeBody>
    </Node>
    """
    result = translate_xml(xml, Node)

    # Check that startc condition is present
    assert "startc:" in normalize_whitespace(result), f"StartCondition not found in: {result}"
    assert (
        "isStatus?('OtherNode,finished)" in result
    ), f"Condition content not correct in: {result}"
    # Check that it's not (none)
    assert "(none)" not in normalize_whitespace(result), f"Found (none) instead of condition in: {result}"


def test_list_node_with_child_having_start_condition(translate_xml):
    """Test that child nodes in a list preserve their StartCondition."""
    xml = """
    <Node NodeType="NodeList">
        <NodeId>ParentList</NodeId>
        <NodeBody>
            <NodeList>
                <Node NodeType="Empty">
                    <NodeId>First</NodeId>
                </Node>
                <Node NodeType="Command">
                    <NodeId>Second</NodeId>
                    <StartCondition>
                        <EQInternal>
                            <NodeStateVariable>
                                <NodeId>First</NodeId>
                            </NodeStateVariable>
                            <NodeStateValue>FINISHED</NodeStateValue>
                        </EQInternal>
                    </StartCondition>
                    <NodeBody>
                        <Command>
                            <Name>
                                <StringValue>doWork</StringValue>
                            </Name>
                        </Command>
                    </NodeBody>
                </Node>
            </NodeList>
        </NodeBody>
    </Node>
    """
    result = translate_xml(xml, Node)

    # The child command node should have its startc condition
    assert "command('Second" in normalize_whitespace(result), f"Second command not found in: {result}"
    assert (
        "startc: (isStatus?('First,finished))" in result
    ), f"StartCondition not translated in: {result}"


def test_command_node_with_post_condition(translate_xml):
    """Test PostCondition is also properly translated."""
    xml = """
    <Node NodeType="Command">
        <NodeId>TestPost</NodeId>
        <PostCondition>
            <BooleanVariable>success</BooleanVariable>
        </PostCondition>
        <NodeBody>
            <Command>
                <Name>
                    <StringValue>verify</StringValue>
                </Name>
            </Command>
        </NodeBody>
    </Node>
    """
    result = translate_xml(xml, Node)

    assert "post:(var('success))" in normalize_whitespace(result), f"PostCondition not found in: {result}"


def test_empty_node_with_invariant_condition(translate_xml):
    """Test InvariantCondition is properly translated."""
    xml = """
    <Node NodeType="Empty">
        <NodeId>TestInvariant</NodeId>
        <InvariantCondition>
            <GT>
                <IntegerVariable>counter</IntegerVariable>
                <IntegerValue>0</IntegerValue>
            </GT>
        </InvariantCondition>
    </Node>
    """
    result = translate_xml(xml, Node)

    assert (
        "inv: (_>_(var('counter),const(val(0))))" in result
    ), f"InvariantCondition not found in: {result}"


def test_assignment_node_with_end_condition(translate_xml):
    """Test EndCondition is properly translated."""
    xml = """
    <Node NodeType="Assignment">
        <NodeId>TestEnd</NodeId>
        <EndCondition>
            <BooleanValue>true</BooleanValue>
        </EndCondition>
        <NodeBody>
            <Assignment>
                <IntegerVariable>x</IntegerVariable>
                <NumericRHS>
                    <IntegerValue>42</IntegerValue>
                </NumericRHS>
            </Assignment>
        </NodeBody>
    </Node>
    """
    result = translate_xml(xml, Node)

    assert "endc:(const(val(true)))" in normalize_whitespace(result), f"EndCondition not found in: {result}"
