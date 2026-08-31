"""Tests for NodeList (list) node translation."""

import pytest
from plexil.core.v1.ast import Node
from tests.conftest import normalize_whitespace


def test_simple_list_node_with_two_empty_children(translate_xml):
    """Test list node with two empty child nodes."""
    xml = """
    <Node NodeType="NodeList">
      <NodeId>ParentList</NodeId>
      <NodeBody>
        <NodeList>
          <Node NodeType="Empty">
            <NodeId>Child1</NodeId>
          </Node>
          <Node NodeType="Empty">
            <NodeId>Child2</NodeId>
          </Node>
        </NodeList>
      </NodeBody>
    </Node>
    """
    result = translate_xml(xml, Node)
    expected = "list('ParentList,nilocdecl,(none),(empty('Child1,nilocdecl,(none)) empty('Child2,nilocdecl,(none))))"
    assert normalize_whitespace(result) == normalize_whitespace(expected), f"Expected: {expected}\nGot: {result}"


def test_list_node_with_start_condition(translate_xml):
    """Test list node with start condition."""
    xml = """
    <Node NodeType="NodeList">
      <NodeId>SequentialTasks</NodeId>
      <StartCondition>
        <BooleanValue>true</BooleanValue>
      </StartCondition>
      <NodeBody>
        <NodeList>
          <Node NodeType="Empty">
            <NodeId>Task1</NodeId>
          </Node>
          <Node NodeType="Empty">
            <NodeId>Task2</NodeId>
          </Node>
        </NodeList>
      </NodeBody>
    </Node>
    """
    result = translate_xml(xml, Node)
    expected = (
        "list('SequentialTasks,nilocdecl,((startc: (const(val(true))))),"
        + "(empty('Task1,nilocdecl,(none)) empty('Task2,nilocdecl,(none))))"
    )
    assert normalize_whitespace(result) == normalize_whitespace(expected), f"Expected: {expected}\nGot: {result}"


def test_list_node_with_assignment_children(translate_xml):
    """Test list node with assignment child nodes."""
    xml = """
    <Node NodeType="NodeList">
      <NodeId>AssignmentList</NodeId>
      <NodeBody>
        <NodeList>
          <Node NodeType="Assignment">
            <NodeId>Assign1</NodeId>
            <NodeBody>
              <Assignment>
                <IntegerVariable>x</IntegerVariable>
                <NumericRHS>
                  <IntegerValue>10</IntegerValue>
                </NumericRHS>
              </Assignment>
            </NodeBody>
          </Node>
          <Node NodeType="Assignment">
            <NodeId>Assign2</NodeId>
            <NodeBody>
              <Assignment>
                <IntegerVariable>y</IntegerVariable>
                <NumericRHS>
                  <IntegerValue>20</IntegerValue>
                </NumericRHS>
              </Assignment>
            </NodeBody>
          </Node>
        </NodeList>
      </NodeBody>
    </Node>
    """
    result = translate_xml(xml, Node)
    expected = (
        "list('AssignmentList,nilocdecl,(none),"
        + "(assignment('Assign1,nilocdecl,(none),(var('x) := const(val(10)))) "
        + "assignment('Assign2,nilocdecl,(none),(var('y) := const(val(20))))))"
    )
    assert normalize_whitespace(result) == normalize_whitespace(expected), f"Expected: {expected}\nGot: {result}"


def test_list_node_with_command_children(translate_xml):
    """Test list node with command child nodes."""
    xml = """
    <Node NodeType="NodeList">
      <NodeId>CommandList</NodeId>
      <NodeBody>
        <NodeList>
          <Node NodeType="Command">
            <NodeId>Cmd1</NodeId>
            <NodeBody>
              <Command>
                <Name>
                  <StringValue>print</StringValue>
                </Name>
              </Command>
            </NodeBody>
          </Node>
          <Node NodeType="Command">
            <NodeId>Cmd2</NodeId>
            <NodeBody>
              <Command>
                <Name>
                  <StringValue>flush</StringValue>
                </Name>
              </Command>
            </NodeBody>
          </Node>
        </NodeList>
      </NodeBody>
    </Node>
    """
    result = translate_xml(xml, Node)
    expected = (
        "list('CommandList,nilocdecl,(none),"
        + "(command('Cmd1,nilocdecl,(none),(('print) / (nilpar) / nothing)) "
        + "command('Cmd2,nilocdecl,(none),(('flush) / (nilpar) / nothing))))"
    )
    assert normalize_whitespace(result) == normalize_whitespace(expected), f"Expected: {expected}\nGot: {result}"


def test_list_node_with_multiple_conditions(translate_xml):
    """Test list node with multiple conditions."""
    xml = """
    <Node NodeType="NodeList">
      <NodeId>ConditionalList</NodeId>
      <StartCondition>
        <BooleanValue>true</BooleanValue>
      </StartCondition>
      <EndCondition>
        <BooleanVariable>done</BooleanVariable>
      </EndCondition>
      <InvariantCondition>
        <BooleanVariable>safe</BooleanVariable>
      </InvariantCondition>
      <NodeBody>
        <NodeList>
          <Node NodeType="Empty">
            <NodeId>Step1</NodeId>
          </Node>
        </NodeList>
      </NodeBody>
    </Node>
    """
    result = translate_xml(xml, Node)
    expected = (
        "list('ConditionalList,nilocdecl,"
        + "((startc: (const(val(true)))),(endc: (var('done))),(inv: (var('safe)))),"
        + "(empty('Step1,nilocdecl,(none))))"
    )
    assert normalize_whitespace(result) == normalize_whitespace(expected), f"Expected: {expected}\nGot: {result}"


def test_nested_list_nodes(translate_xml):
    """Test nested list nodes."""
    xml = """
    <Node NodeType="NodeList">
      <NodeId>OuterList</NodeId>
      <NodeBody>
        <NodeList>
          <Node NodeType="NodeList">
            <NodeId>InnerList</NodeId>
            <NodeBody>
              <NodeList>
                <Node NodeType="Empty">
                  <NodeId>Leaf</NodeId>
                </Node>
              </NodeList>
            </NodeBody>
          </Node>
        </NodeList>
      </NodeBody>
    </Node>
    """
    result = translate_xml(xml, Node)
    expected = "list('OuterList,nilocdecl,(none),(list('InnerList,nilocdecl,(none),(empty('Leaf,nilocdecl,(none))))))"
    assert normalize_whitespace(result) == normalize_whitespace(expected), f"Expected: {expected}\nGot: {result}"


def test_list_node_with_single_child(translate_xml):
    """Test list node with a single child."""
    xml = """
    <Node NodeType="NodeList">
      <NodeId>SingleChild</NodeId>
      <NodeBody>
        <NodeList>
          <Node NodeType="Empty">
            <NodeId>OnlyChild</NodeId>
          </Node>
        </NodeList>
      </NodeBody>
    </Node>
    """
    result = translate_xml(xml, Node)
    expected = (
        "list('SingleChild,nilocdecl,(none),(empty('OnlyChild,nilocdecl,(none))))"
    )
    assert normalize_whitespace(result) == normalize_whitespace(expected), f"Expected: {expected}\nGot: {result}"


def test_list_node_with_mixed_child_types(translate_xml):
    """Test list node with different types of children."""
    xml = """
    <Node NodeType="NodeList">
      <NodeId>MixedList</NodeId>
      <NodeBody>
        <NodeList>
          <Node NodeType="Empty">
            <NodeId>EmptyNode</NodeId>
          </Node>
          <Node NodeType="Assignment">
            <NodeId>AssignNode</NodeId>
            <NodeBody>
              <Assignment>
                <IntegerVariable>counter</IntegerVariable>
                <NumericRHS>
                  <IntegerValue>1</IntegerValue>
                </NumericRHS>
              </Assignment>
            </NodeBody>
          </Node>
          <Node NodeType="Command">
            <NodeId>CmdNode</NodeId>
            <NodeBody>
              <Command>
                <Name>
                  <StringValue>execute</StringValue>
                </Name>
              </Command>
            </NodeBody>
          </Node>
        </NodeList>
      </NodeBody>
    </Node>
    """
    result = translate_xml(xml, Node)
    expected = (
        "list('MixedList,nilocdecl,(none),"
        + "(empty('EmptyNode,nilocdecl,(none)) "
        + "assignment('AssignNode,nilocdecl,(none),(var('counter) := const(val(1)))) "
        + "command('CmdNode,nilocdecl,(none),(('execute) / (nilpar) / nothing))))"
    )
    assert normalize_whitespace(result) == normalize_whitespace(expected), f"Expected: {expected}\nGot: {result}"
