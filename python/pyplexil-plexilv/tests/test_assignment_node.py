"""Tests for Assignment Node translation."""

import pytest
from plexil.core.v1.ast import Node
from tests.conftest import normalize_whitespace


def test_assignment_node_simple(translate_xml):
    """Test simple Assignment node with lookup."""
    xml = """
    <Node NodeType="Assignment">
        <NodeId>ASSIGNMENT__0</NodeId>
        <NodeBody>
            <Assignment>
                <RealVariable>r1</RealVariable>
                <NumericRHS>
                    <LookupNow>
                        <Name>
                            <StringValue>r1</StringValue>
                        </Name>
                    </LookupNow>
                </NumericRHS>
            </Assignment>
        </NodeBody>
    </Node>
    """
    result = translate_xml(xml, Node)
    expected = (
        "assignment('ASSIGNMENT__0,nilocdecl,(none),(var('r1) := lookup('r1,(nilpar))))"
    )
    assert normalize_whitespace(result) == normalize_whitespace(expected), f"Expected: {expected}\nGot: {result}"


def test_assignment_node_with_lookup_args(translate_xml):
    """Test Assignment node with lookup having arguments."""
    xml = """
    <Node NodeType="Assignment">
        <NodeId>ASSIGNMENT__0</NodeId>
        <NodeBody>
            <Assignment>
                <BooleanVariable>initial_drag</BooleanVariable>
                <BooleanRHS>
                    <LookupNow>
                        <Name>
                            <StringValue>InitialDrag</StringValue>
                        </Name>
                        <Arguments>
                            <IntegerVariable>SatId</IntegerVariable>
                        </Arguments>
                    </LookupNow>
                </BooleanRHS>
            </Assignment>
        </NodeBody>
    </Node>
    """
    result = translate_xml(xml, Node)
    expected = "assignment('ASSIGNMENT__0,nilocdecl,(none),(var('initial_drag) := lookup('InitialDrag,(var('SatId)))))"
    assert normalize_whitespace(result) == normalize_whitespace(expected), f"Expected: {expected}\nGot: {result}"


def test_assignment_node_array_element(translate_xml):
    """Test Assignment node with array element."""
    xml = """
    <Node NodeType="Assignment">
        <NodeId>SimpleArrayAssignment1</NodeId>
        <NodeBody>
            <Assignment>
                <ArrayElement>
                    <ArrayVariable>foo</ArrayVariable>
                    <Index>
                        <IntegerVariable>i</IntegerVariable>
                    </Index>
                </ArrayElement>
                <NumericRHS>
                    <RealValue>1.0</RealValue>
                </NumericRHS>
            </Assignment>
        </NodeBody>
    </Node>
    """
    result = translate_xml(xml, Node)
    expected = "assignment('SimpleArrayAssignment1,nilocdecl,(none),(arrayVar('foo,var('i)) := const(val(1.0))))"
    assert normalize_whitespace(result) == normalize_whitespace(expected), f"Expected: {expected}\nGot: {result}"


def test_assignment_node_with_literal(translate_xml):
    """Test Assignment node with literal value."""
    xml = """
    <Node NodeType="Assignment">
        <NodeId>LiteralAssign</NodeId>
        <NodeBody>
            <Assignment>
                <IntegerVariable>count</IntegerVariable>
                <NumericRHS>
                    <IntegerValue>42</IntegerValue>
                </NumericRHS>
            </Assignment>
        </NodeBody>
    </Node>
    """
    result = translate_xml(xml, Node)
    expected = (
        "assignment('LiteralAssign,nilocdecl,(none),(var('count) := const(val(42))))"
    )
    assert normalize_whitespace(result) == normalize_whitespace(expected), f"Expected: {expected}\nGot: {result}"


def test_assignment_node_with_start_condition(translate_xml):
    """Test Assignment node with StartCondition."""
    xml = """
    <Node NodeType="Assignment">
        <NodeId>ConditionalAssign</NodeId>
        <StartCondition>
            <BooleanValue>true</BooleanValue>
        </StartCondition>
        <NodeBody>
            <Assignment>
                <IntegerVariable>x</IntegerVariable>
                <NumericRHS>
                    <IntegerValue>10</IntegerValue>
                </NumericRHS>
            </Assignment>
        </NodeBody>
    </Node>
    """
    result = translate_xml(xml, Node)
    expected = "assignment('ConditionalAssign,nilocdecl,((startc: (const(val(true))))),(var('x) := const(val(10))))"
    assert normalize_whitespace(result) == normalize_whitespace(expected), f"Expected: {expected}\nGot: {result}"


def test_assignment_node_with_post_condition(translate_xml):
    """Test Assignment node with PostCondition."""
    xml = """
    <Node NodeType="Assignment">
        <NodeId>PostAssign</NodeId>
        <PostCondition>
            <BooleanVariable>success</BooleanVariable>
        </PostCondition>
        <NodeBody>
            <Assignment>
                <RealVariable>result</RealVariable>
                <NumericRHS>
                    <RealValue>3.14</RealValue>
                </NumericRHS>
            </Assignment>
        </NodeBody>
    </Node>
    """
    result = translate_xml(xml, Node)
    expected = "assignment('PostAssign,nilocdecl,((post: (var('success)))),(var('result) := const(val(3.14))))"
    assert normalize_whitespace(result) == normalize_whitespace(expected), f"Expected: {expected}\nGot: {result}"


def test_assignment_node_with_multiple_conditions(translate_xml):
    """Test Assignment node with multiple conditions."""
    xml = """
    <Node NodeType="Assignment">
        <NodeId>MultiCondAssign</NodeId>
        <StartCondition>
            <BooleanValue>true</BooleanValue>
        </StartCondition>
        <EndCondition>
            <BooleanValue>false</BooleanValue>
        </EndCondition>
        <NodeBody>
            <Assignment>
                <BooleanVariable>flag</BooleanVariable>
                <BooleanRHS>
                    <BooleanValue>true</BooleanValue>
                </BooleanRHS>
            </Assignment>
        </NodeBody>
    </Node>
    """
    result = translate_xml(xml, Node)
    expected = "assignment('MultiCondAssign,nilocdecl,((startc: (const(val(true)))),(endc: (const(val(false))))),(var('flag) := const(val(true))))"
    assert normalize_whitespace(result) == normalize_whitespace(expected), f"Expected: {expected}\nGot: {result}"


def test_assignment_node_string_assignment(translate_xml):
    """Test Assignment node with string assignment."""
    xml = """
    <Node NodeType="Assignment">
        <NodeId>StringAssign</NodeId>
        <NodeBody>
            <Assignment>
                <StringVariable>message</StringVariable>
                <StringRHS>
                    <StringValue>hello</StringValue>
                </StringRHS>
            </Assignment>
        </NodeBody>
    </Node>
    """
    result = translate_xml(xml, Node)
    expected = "assignment('StringAssign,nilocdecl,(none),(var('message) := const(val(\"hello\"))))"
    assert normalize_whitespace(result) == normalize_whitespace(expected), f"Expected: {expected}\nGot: {result}"
