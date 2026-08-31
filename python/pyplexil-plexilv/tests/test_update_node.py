"""Tests for Update node translation."""

import pytest
from plexil.core.v1.ast import Node
from tests.conftest import normalize_whitespace


def test_update_node_simple(translate_xml):
    """Test simple Update node with single pair."""
    xml = """
    <Node NodeType="Update">
      <NodeId>SimpleUpdate</NodeId>
      <NodeBody>
        <Update>
          <Pair>
            <Name>status</Name>
            <StringValue>active</StringValue>
          </Pair>
        </Update>
      </NodeBody>
    </Node>
    """
    result = translate_xml(xml, Node)
    expected = (
        "update('SimpleUpdate,nilocdecl,(none),(< 'status ; const(val(\"active\")) >))"
    )
    assert normalize_whitespace(result) == normalize_whitespace(expected), f"Expected: {expected}\nGot: {result}"


def test_update_node_with_multiple_pairs(translate_xml):
    """Test Update node with multiple pairs."""
    xml = """
    <Node NodeType="Update">
      <NodeId>UpdateLookupTest</NodeId>
      <NodeBody>
        <Update>
          <Pair>
            <Name>xValue</Name>
            <IntegerVariable>x</IntegerVariable>
          </Pair>
          <Pair>
            <Name>yValue</Name>
            <BooleanVariable>y</BooleanVariable>
          </Pair>
          <Pair>
            <Name>realconstant</Name>
            <RealValue>3.141</RealValue>
          </Pair>
        </Update>
      </NodeBody>
    </Node>
    """
    result = translate_xml(xml, Node)
    expected = "update('UpdateLookupTest,nilocdecl,(none),(< 'xValue ; var('x) > < 'yValue ; var('y) > < 'realconstant ; const(val(3.141)) >))"
    assert normalize_whitespace(result) == normalize_whitespace(expected), f"Expected: {expected}\nGot: {result}"


def test_update_node_with_start_condition(translate_xml):
    """Test Update node with start condition."""
    xml = """
    <Node NodeType="Update">
      <NodeId>ConditionalUpdate</NodeId>
      <StartCondition>
        <BooleanValue>true</BooleanValue>
      </StartCondition>
      <NodeBody>
        <Update>
          <Pair>
            <Name>flag</Name>
            <BooleanValue>true</BooleanValue>
          </Pair>
        </Update>
      </NodeBody>
    </Node>
    """
    result = translate_xml(xml, Node)
    expected = "update('ConditionalUpdate,nilocdecl,((startc: (const(val(true))))),(< 'flag ; const(val(true)) >))"
    assert normalize_whitespace(result) == normalize_whitespace(expected), f"Expected: {expected}\nGot: {result}"


def test_update_node_with_post_condition(translate_xml):
    """Test Update node with post condition."""
    xml = """
    <Node NodeType="Update">
      <NodeId>UpdateWithPost</NodeId>
      <PostCondition>
        <BooleanVariable>done</BooleanVariable>
      </PostCondition>
      <NodeBody>
        <Update>
          <Pair>
            <Name>count</Name>
            <IntegerValue>1</IntegerValue>
          </Pair>
        </Update>
      </NodeBody>
    </Node>
    """
    result = translate_xml(xml, Node)
    expected = "update('UpdateWithPost,nilocdecl,((post: (var('done)))),(< 'count ; const(val(1)) >))"
    assert normalize_whitespace(result) == normalize_whitespace(expected), f"Expected: {expected}\nGot: {result}"


def test_update_node_with_multiple_conditions(translate_xml):
    """Test Update node with multiple conditions."""
    xml = """
    <Node NodeType="Update">
      <NodeId>UpdateMultiCond</NodeId>
      <StartCondition>
        <BooleanValue>true</BooleanValue>
      </StartCondition>
      <EndCondition>
        <BooleanVariable>finished</BooleanVariable>
      </EndCondition>
      <InvariantCondition>
        <BooleanVariable>safe</BooleanVariable>
      </InvariantCondition>
      <NodeBody>
        <Update>
          <Pair>
            <Name>progress</Name>
            <IntegerValue>50</IntegerValue>
          </Pair>
        </Update>
      </NodeBody>
    </Node>
    """
    result = translate_xml(xml, Node)
    expected = (
        "update('UpdateMultiCond,nilocdecl,"
        + "((startc: (const(val(true)))),(endc: (var('finished))),(inv: (var('safe)))),"
        + "(< 'progress ; const(val(50)) >))"
    )
    assert normalize_whitespace(result) == normalize_whitespace(expected), f"Expected: {expected}\nGot: {result}"


def test_update_node_with_lookup(translate_xml):
    """Test Update node with lookup expression."""
    xml = """
    <Node NodeType="Update">
      <NodeId>UpdateWithLookup</NodeId>
      <NodeBody>
        <Update>
          <Pair>
            <Name>sensorValue</Name>
            <LookupNow>
              <Name>
                <StringValue>temperature</StringValue>
              </Name>
            </LookupNow>
          </Pair>
        </Update>
      </NodeBody>
    </Node>
    """
    result = translate_xml(xml, Node)
    expected = "update('UpdateWithLookup,nilocdecl,(none),(< 'sensorValue ; lookup('temperature,(nilpar)) >))"
    assert normalize_whitespace(result) == normalize_whitespace(expected), f"Expected: {expected}\nGot: {result}"


def test_update_node_with_array_variable(translate_xml):
    """Test Update node with array variable."""
    xml = """
    <Node NodeType="Update">
      <NodeId>UpdateWithArray</NodeId>
      <NodeBody>
        <Update>
          <Pair>
            <Name>arrayData</Name>
            <ArrayVariable>sourceArray</ArrayVariable>
          </Pair>
        </Update>
      </NodeBody>
    </Node>
    """
    result = translate_xml(xml, Node)
    expected = "update('UpdateWithArray,nilocdecl,(none),(< 'arrayData ; arrayVar('sourceArray) >))"
    assert normalize_whitespace(result) == normalize_whitespace(expected), f"Expected: {expected}\nGot: {result}"


def test_update_node_mixed_types(translate_xml):
    """Test Update node with mixed value types."""
    xml = """
    <Node NodeType="Update">
      <NodeId>MixedUpdate</NodeId>
      <NodeBody>
        <Update>
          <Pair>
            <Name>intVal</Name>
            <IntegerValue>42</IntegerValue>
          </Pair>
          <Pair>
            <Name>realVal</Name>
            <RealValue>3.14</RealValue>
          </Pair>
          <Pair>
            <Name>boolVal</Name>
            <BooleanValue>false</BooleanValue>
          </Pair>
          <Pair>
            <Name>strVal</Name>
            <StringValue>test</StringValue>
          </Pair>
        </Update>
      </NodeBody>
    </Node>
    """
    result = translate_xml(xml, Node)
    expected = (
        "update('MixedUpdate,nilocdecl,(none),"
        + "(< 'intVal ; const(val(42)) > < 'realVal ; const(val(3.14)) > "
        + "< 'boolVal ; const(val(false)) > < 'strVal ; const(val(\"test\")) >))"
    )
    assert normalize_whitespace(result) == normalize_whitespace(expected), f"Expected: {expected}\nGot: {result}"
