"""Tests for Empty Node translation."""

import pytest
from plexil.core.v1.ast import Node
from tests.conftest import normalize_whitespace


def test_empty_node_minimal(translate_xml):
    """Test minimal Empty node with just an ID."""
    xml = """
    <Node NodeType="Empty">
        <NodeId>TestEmpty</NodeId>
    </Node>
    """
    result = translate_xml(xml, Node)
    expected = "empty('TestEmpty,nilocdecl,(none))"
    assert normalize_whitespace(result) == normalize_whitespace(expected), f"Expected: {expected}\nGot: {result}"


def test_empty_node_with_underscore_id(translate_xml):
    """Test Empty node with underscore in ID (preserves underscore)."""
    xml = """
    <Node NodeType="Empty">
        <NodeId>ep2cp_IfTest</NodeId>
    </Node>
    """
    result = translate_xml(xml, Node)
    expected = "empty('ep2cp_IfTest,nilocdecl,(none))"
    assert normalize_whitespace(result) == normalize_whitespace(expected), f"Expected: {expected}\nGot: {result}"


def test_empty_node_with_post_condition(translate_xml):
    """Test Empty node with PostCondition."""
    xml = """
    <Node NodeType="Empty">
        <NodeId>ep2cp_IfTest</NodeId>
        <PostCondition>
            <GE>
                <RealVariable>speedPref</RealVariable>
                <IntegerValue>0</IntegerValue>
            </GE>
        </PostCondition>
    </Node>
    """
    result = translate_xml(xml, Node)
    expected = (
        "empty('ep2cp_IfTest,nilocdecl,((post: (_>=_(var('speedPref),const(val(0)))))))"
    )
    assert normalize_whitespace(result) == normalize_whitespace(expected), f"Expected: {expected}\nGot: {result}"


def test_empty_node_with_start_condition(translate_xml):
    """Test Empty node with StartCondition."""
    xml = """
    <Node NodeType="Empty">
        <NodeId>StartTest</NodeId>
        <StartCondition>
            <BooleanValue>true</BooleanValue>
        </StartCondition>
    </Node>
    """
    result = translate_xml(xml, Node)
    expected = "empty('StartTest,nilocdecl,((startc: (const(val(true))))))"
    assert normalize_whitespace(result) == normalize_whitespace(expected), f"Expected: {expected}\nGot: {result}"


def test_empty_node_with_multiple_conditions(translate_xml):
    """Test Empty node with multiple conditions."""
    xml = """
    <Node NodeType="Empty">
        <NodeId>MultiCond</NodeId>
        <StartCondition>
            <BooleanValue>true</BooleanValue>
        </StartCondition>
        <EndCondition>
            <BooleanValue>false</BooleanValue>
        </EndCondition>
    </Node>
    """
    result = translate_xml(xml, Node)
    expected = "empty('MultiCond,nilocdecl,((startc: (const(val(true)))),(endc: (const(val(false))))))"
    assert normalize_whitespace(result) == normalize_whitespace(expected), f"Expected: {expected}\nGot: {result}"


def test_empty_node_with_invariant(translate_xml):
    """Test Empty node with InvariantCondition."""
    xml = """
    <Node NodeType="Empty">
        <NodeId>InvTest</NodeId>
        <InvariantCondition>
            <BooleanVariable>keepAlive</BooleanVariable>
        </InvariantCondition>
    </Node>
    """
    result = translate_xml(xml, Node)
    expected = "empty('InvTest,nilocdecl,((inv: (var('keepAlive)))))"
    assert normalize_whitespace(result) == normalize_whitespace(expected), f"Expected: {expected}\nGot: {result}"


def test_empty_node_with_pre_and_post(translate_xml):
    """Test Empty node with PreCondition and PostCondition."""
    xml = """
    <Node NodeType="Empty">
        <NodeId>PrePost</NodeId>
        <PreCondition>
            <BooleanValue>true</BooleanValue>
        </PreCondition>
        <PostCondition>
            <BooleanValue>true</BooleanValue>
        </PostCondition>
    </Node>
    """
    result = translate_xml(xml, Node)
    expected = "empty('PrePost,nilocdecl,((pre: (const(val(true)))),(post: (const(val(true))))))"
    assert normalize_whitespace(result) == normalize_whitespace(expected), f"Expected: {expected}\nGot: {result}"
