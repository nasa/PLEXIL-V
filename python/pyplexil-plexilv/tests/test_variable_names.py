"""Tests for variable name handling.

These tests verify that variable names preserve underscores and are not
converted to hyphens (which is only done for node names).
"""

import pytest
from plexil.core.v1.ast import DeclareVariable, DeclareArray, Node


def test_variable_name_with_underscore(translate_xml):
    """Test that variable names preserve underscores."""
    xml = """
    <DeclareVariable>
        <Name>initial_drag</Name>
        <Type>Real</Type>
        <InitialValue>
            <RealValue>2.5</RealValue>
        </InitialValue>
    </DeclareVariable>
    """
    result = translate_xml(xml, DeclareVariable)
    # Variable name should keep underscore, not convert to hyphen
    assert result == "('initial_drag : val(2.5))"


def test_array_name_with_underscore(translate_xml):
    """Test that array names preserve underscores."""
    xml = """
    <DeclareArray>
        <Name>cache_array</Name>
        <Type>Integer</Type>
        <MaxSize>5</MaxSize>
    </DeclareArray>
    """
    result = translate_xml(xml, DeclareArray)
    # Array name should keep underscore, not convert to hyphen
    assert result == "('cache_array : createArray(5,unknownArray(5)))"


def test_variable_reference_with_underscore(translate_xml):
    """Test that variable references preserve underscores."""
    xml = """
    <IntegerVariable>initial_value</IntegerVariable>
    """
    from plexil.core.v1.ast import IntegerVariable

    result = translate_xml(xml, IntegerVariable)
    # Variable reference should keep underscore
    assert result == "var('initial_value)"


def test_variable_consistency_in_node(translate_xml):
    """Test that variable declarations and references use consistent names."""
    xml = """
    <Node NodeType="Empty">
        <NodeId>test_node</NodeId>
        <VariableDeclarations>
            <DeclareVariable>
                <Name>my_variable</Name>
                <Type>Integer</Type>
                <InitialValue>
                    <IntegerValue>42</IntegerValue>
                </InitialValue>
            </DeclareVariable>
        </VariableDeclarations>
        <EndCondition>
            <EQNumeric>
                <IntegerVariable>my_variable</IntegerVariable>
                <IntegerValue>42</IntegerValue>
            </EQNumeric>
        </EndCondition>
    </Node>
    """
    result = translate_xml(xml, Node)

    # Variable declaration should use underscore
    assert "('my_variable : val(42))" in result
    # Variable reference should also use underscore
    assert "var('my_variable)" in result
    # Node name should also use underscore
    assert "'test_node" in result


def test_multiple_underscores_in_variable_name(translate_xml):
    """Test variable names with multiple underscores."""
    xml = """
    <DeclareVariable>
        <Name>very_long_variable_name</Name>
        <Type>String</Type>
        <InitialValue>
            <StringValue>test</StringValue>
        </InitialValue>
    </DeclareVariable>
    """
    result = translate_xml(xml, DeclareVariable)
    # All underscores should be preserved
    assert result == '(\'very_long_variable_name : val("test"))'


def test_variable_name_vs_node_name_difference(translate_xml):
    """Test that both variable names and node names preserve underscores."""
    xml = """
    <Node NodeType="Empty">
        <NodeId>node_with_underscore</NodeId>
        <VariableDeclarations>
            <DeclareVariable>
                <Name>var_with_underscore</Name>
                <Type>Boolean</Type>
                <InitialValue>
                    <BooleanValue>true</BooleanValue>
                </InitialValue>
            </DeclareVariable>
        </VariableDeclarations>
    </Node>
    """
    result = translate_xml(xml, Node)

    # Node name should preserve underscore
    assert "'node_with_underscore" in result
    # Variable name should also preserve underscore
    assert "'var_with_underscore" in result
