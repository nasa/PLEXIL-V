"""Tests for Command Node translation."""

import pytest
from plexil.core.v1.ast import Node
from tests.conftest import normalize_whitespace


def test_command_node_simple(translate_xml):
    """Test simple Command node with arguments."""
    xml = """
    <Node NodeType="Command">
        <NodeId>Example1</NodeId>
        <StartCondition>
            <BooleanValue>true</BooleanValue>
        </StartCondition>
        <NodeBody>
            <Command>
                <Name>
                    <StringValue>pprint</StringValue>
                </Name>
                <Arguments>
                    <StringValue>r:</StringValue>
                    <RealVariable>r</RealVariable>
                </Arguments>
            </Command>
        </NodeBody>
    </Node>
    """
    result = translate_xml(xml, Node)
    expected = "command('Example1,nilocdecl,((startc: (const(val(true))))),(('pprint) / (const(val(\"r:\")) var('r)) / nothing))"
    assert normalize_whitespace(result) == normalize_whitespace(expected), f"Expected: {expected}\nGot: {result}"


def test_command_node_complex(translate_xml):
    """Test complex Command node with multiple conditions."""
    xml = """
    <Node NodeType="Command">
        <NodeId>Printer0</NodeId>
        <StartCondition>
            <BooleanValue>false</BooleanValue>
        </StartCondition>
        <EndCondition>
            <AND>
                <EQInternal>
                    <NodeStateVariable>
                        <NodeRef dir="sibling">TestReal__2</NodeRef>
                    </NodeStateVariable>
                    <NodeStateValue>FINISHED</NodeStateValue>
                </EQInternal>
                <EQInternal>
                    <NodeStateVariable>
                        <NodeRef>TestVars1</NodeRef>
                    </NodeStateVariable>
                    <NodeStateValue>FINISHED</NodeStateValue>
                </EQInternal>
            </AND>
        </EndCondition>
        <NodeBody>
            <Command>
                <Name>
                    <StringValue>pprint</StringValue>
                </Name>
                <Arguments>
                    <StringValue>r1:</StringValue>
                    <RealVariable>r1</RealVariable>
                    <StringValue>r2:</StringValue>
                    <RealVariable>r2</RealVariable>
                </Arguments>
            </Command>
        </NodeBody>
    </Node>
    """
    result = translate_xml(xml, Node)
    expected = "command('Printer0,nilocdecl,((startc: (const(val(false)))),(endc: (_and_(isStatus?('TestReal__2,finished),isStatus?('TestVars1,finished))))),(('pprint) / (const(val(\"r1:\")) var('r1) const(val(\"r2:\")) var('r2)) / nothing))"
    assert normalize_whitespace(result) == normalize_whitespace(expected), f"Expected: {expected}\nGot: {result}"


def test_command_node_with_return(translate_xml):
    """Test Command node with return value."""
    xml = """
    <Node NodeType="Command">
        <NodeId>BLOCK__0</NodeId>
        <NodeBody>
            <Command>
                <RealVariable>ret</RealVariable>
                <Name>
                    <StringValue>complexCommand</StringValue>
                </Name>
                <Arguments>
                    <RealVariable>ret</RealVariable>
                </Arguments>
            </Command>
        </NodeBody>
    </Node>
    """
    result = translate_xml(xml, Node)
    expected = "command('BLOCK__0,nilocdecl,(none),(('complexCommand) / (var('ret)) / just('ret)))"
    assert normalize_whitespace(result) == normalize_whitespace(expected), f"Expected: {expected}\nGot: {result}"


def test_command_node_no_args(translate_xml):
    """Test Command node with no arguments."""
    xml = """
    <Node NodeType="Command">
        <NodeId>SimpleCmd</NodeId>
        <NodeBody>
            <Command>
                <Name>
                    <StringValue>initialize</StringValue>
                </Name>
            </Command>
        </NodeBody>
    </Node>
    """
    result = translate_xml(xml, Node)
    expected = (
        "command('SimpleCmd,nilocdecl,(none),(('initialize) / (nilpar) / nothing))"
    )
    assert normalize_whitespace(result) == normalize_whitespace(expected), f"Expected: {expected}\nGot: {result}"


def test_command_node_with_post_condition(translate_xml):
    """Test Command node with PostCondition."""
    xml = """
    <Node NodeType="Command">
        <NodeId>CheckCmd</NodeId>
        <PostCondition>
            <BooleanVariable>success</BooleanVariable>
        </PostCondition>
        <NodeBody>
            <Command>
                <Name>
                    <StringValue>checkStatus</StringValue>
                </Name>
            </Command>
        </NodeBody>
    </Node>
    """
    result = translate_xml(xml, Node)
    expected = "command('CheckCmd,nilocdecl,((post: (var('success)))),(('checkStatus) / (nilpar) / nothing))"
    assert normalize_whitespace(result) == normalize_whitespace(expected), f"Expected: {expected}\nGot: {result}"


def test_command_node_with_variable_name(translate_xml):
    """Test Command node with variable command name."""
    xml = """
    <Node NodeType="Command">
        <NodeId>DynamicCmd</NodeId>
        <NodeBody>
            <Command>
                <Name>
                    <StringVariable>cmdName</StringVariable>
                </Name>
            </Command>
        </NodeBody>
    </Node>
    """
    result = translate_xml(xml, Node)
    expected = "command('DynamicCmd,nilocdecl,(none),(cmdId(var('cmdName)) / (nilpar) / nothing))"
    assert normalize_whitespace(result) == normalize_whitespace(expected), f"Expected: {expected}\nGot: {result}"


def test_command_node_single_arg(translate_xml):
    """Test Command node with single argument."""
    xml = """
    <Node NodeType="Command">
        <NodeId>OneArg</NodeId>
        <NodeBody>
            <Command>
                <Name>
                    <StringValue>setValue</StringValue>
                </Name>
                <Arguments>
                    <IntegerValue>42</IntegerValue>
                </Arguments>
            </Command>
        </NodeBody>
    </Node>
    """
    result = translate_xml(xml, Node)
    expected = (
        "command('OneArg,nilocdecl,(none),(('setValue) / (const(val(42))) / nothing))"
    )
    assert normalize_whitespace(result) == normalize_whitespace(expected), f"Expected: {expected}\nGot: {result}"


def test_command_node_with_invariant(translate_xml):
    """Test Command node with InvariantCondition."""
    xml = """
    <Node NodeType="Command">
        <NodeId>InvariantCmd</NodeId>
        <InvariantCondition>
            <BooleanVariable>keepRunning</BooleanVariable>
        </InvariantCondition>
        <NodeBody>
            <Command>
                <Name>
                    <StringValue>monitor</StringValue>
                </Name>
            </Command>
        </NodeBody>
    </Node>
    """
    result = translate_xml(xml, Node)
    expected = "command('InvariantCmd,nilocdecl,((inv: (var('keepRunning)))),(('monitor) / (nilpar) / nothing))"
    assert normalize_whitespace(result) == normalize_whitespace(expected), f"Expected: {expected}\nGot: {result}"
