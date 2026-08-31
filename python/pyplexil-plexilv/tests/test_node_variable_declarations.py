"""Tests for variable declarations integrated into node handlers.

These tests verify that variable declarations are properly translated
when embedded within different node types (Assignment, Command, Update, Empty, List).

This prevents regression of the fix that replaced 'vardecls,' placeholders
with actual walk() calls to translate VariableDeclarations.
"""

import pytest
from plexil.core.v1.ast import Node
from tests.conftest import normalize_whitespace

# ====================
# Assignment Node with Variable Declarations
# ====================


def test_assignment_node_with_single_variable_declaration(translate_xml):
    """Test Assignment node with a single variable declaration."""
    xml = """
    <Node NodeType="Assignment">
        <NodeId>SimpleAssignment</NodeId>
        <VariableDeclarations>
            <DeclareVariable>
                <Name>foo</Name>
                <Type>Integer</Type>
                <InitialValue>
                    <IntegerValue>0</IntegerValue>
                </InitialValue>
            </DeclareVariable>
        </VariableDeclarations>
        <NodeBody>
            <Assignment>
                <IntegerVariable>foo</IntegerVariable>
                <NumericRHS>
                    <IntegerValue>3</IntegerValue>
                </NumericRHS>
            </Assignment>
        </NodeBody>
    </Node>
    """
    result = translate_xml(xml, Node)
    # Should have (('foo : val(0))) not 'vardecls,'
    assert "(('foo:val(0)))" in normalize_whitespace(result), f"Variable declaration not found in: {result}"
    assert "vardecls" not in normalize_whitespace(result), f"Found placeholder 'vardecls' in: {result}"
    assert normalize_whitespace(result).startswith("assignment('SimpleAssignment,")


def test_assignment_node_with_multiple_variable_declarations(translate_xml):
    """Test Assignment node with multiple variable declarations."""
    xml = """
    <Node NodeType="Assignment">
        <NodeId>MultiVar</NodeId>
        <VariableDeclarations>
            <DeclareVariable>
                <Name>x</Name>
                <Type>Integer</Type>
                <InitialValue>
                    <IntegerValue>0</IntegerValue>
                </InitialValue>
            </DeclareVariable>
            <DeclareVariable>
                <Name>y</Name>
                <Type>Real</Type>
                <InitialValue>
                    <RealValue>1.5</RealValue>
                </InitialValue>
            </DeclareVariable>
        </VariableDeclarations>
        <NodeBody>
            <Assignment>
                <IntegerVariable>x</IntegerVariable>
                <NumericRHS>
                    <IntegerValue>5</IntegerValue>
                </NumericRHS>
            </Assignment>
        </NodeBody>
    </Node>
    """
    result = translate_xml(xml, Node)
    assert "(('x:val(0))('y:val(1.5)))" in normalize_whitespace(result)
    assert "vardecls" not in normalize_whitespace(result)


def test_assignment_node_with_uninitialized_variable(translate_xml):
    """Test Assignment node with uninitialized variable declaration."""
    xml = """
    <Node NodeType="Assignment">
        <NodeId>UninitVar</NodeId>
        <VariableDeclarations>
            <DeclareVariable>
                <Name>counter</Name>
                <Type>Integer</Type>
            </DeclareVariable>
        </VariableDeclarations>
        <NodeBody>
            <Assignment>
                <IntegerVariable>counter</IntegerVariable>
                <NumericRHS>
                    <IntegerValue>1</IntegerValue>
                </NumericRHS>
            </Assignment>
        </NodeBody>
    </Node>
    """
    result = translate_xml(xml, Node)
    assert "(('counter:unknown))" in normalize_whitespace(result)
    assert "vardecls" not in normalize_whitespace(result)


def test_assignment_node_with_array_declaration(translate_xml):
    """Test Assignment node with array declaration."""
    xml = """
    <Node NodeType="Assignment">
        <NodeId>ArrayNode</NodeId>
        <VariableDeclarations>
            <DeclareArray>
                <Name>data</Name>
                <Type>Real</Type>
                <MaxSize>3</MaxSize>
            </DeclareArray>
        </VariableDeclarations>
        <NodeBody>
            <Assignment>
                <ArrayElement>
                    <Name>data</Name>
                    <Index>
                        <IntegerValue>0</IntegerValue>
                    </Index>
                </ArrayElement>
                <NumericRHS>
                    <RealValue>3.14</RealValue>
                </NumericRHS>
            </Assignment>
        </NodeBody>
    </Node>
    """
    result = translate_xml(xml, Node)
    assert "(('data:createArray(3,unknownArray(3))))" in normalize_whitespace(result)
    assert "vardecls" not in normalize_whitespace(result)


# ====================
# Command Node with Variable Declarations
# ====================


def test_command_node_with_variable_declaration(translate_xml):
    """Test Command node with variable declaration."""
    xml = """
    <Node NodeType="Command">
        <NodeId>CmdWithVar</NodeId>
        <VariableDeclarations>
            <DeclareVariable>
                <Name>result</Name>
                <Type>Integer</Type>
            </DeclareVariable>
        </VariableDeclarations>
        <NodeBody>
            <Command>
                <IntegerVariable>result</IntegerVariable>
                <Name>
                    <StringValue>GetValue</StringValue>
                </Name>
            </Command>
        </NodeBody>
    </Node>
    """
    result = translate_xml(xml, Node)
    assert "(('result:unknown))" in normalize_whitespace(result)
    assert "vardecls" not in normalize_whitespace(result)
    assert normalize_whitespace(result).startswith("command('CmdWithVar,")


def test_command_node_with_multiple_variables(translate_xml):
    """Test Command node with multiple variable declarations."""
    xml = """
    <Node NodeType="Command">
        <NodeId>CmdMultiVar</NodeId>
        <VariableDeclarations>
            <DeclareVariable>
                <Name>status</Name>
                <Type>Boolean</Type>
                <InitialValue>
                    <BooleanValue>false</BooleanValue>
                </InitialValue>
            </DeclareVariable>
            <DeclareVariable>
                <Name>msg</Name>
                <Type>String</Type>
                <InitialValue>
                    <StringValue>ready</StringValue>
                </InitialValue>
            </DeclareVariable>
        </VariableDeclarations>
        <NodeBody>
            <Command>
                <Name>
                    <StringValue>Initialize</StringValue>
                </Name>
            </Command>
        </NodeBody>
    </Node>
    """
    result = translate_xml(xml, Node)
    assert "(('status:val(false))('msg:val(\"ready\")))" in normalize_whitespace(result)
    assert "vardecls" not in normalize_whitespace(result)


# ====================
# Update Node with Variable Declarations
# ====================


def test_update_node_with_variable_declaration(translate_xml):
    """Test Update node with variable declaration."""
    xml = """
    <Node NodeType="Update">
        <NodeId>UpdateWithVar</NodeId>
        <VariableDeclarations>
            <DeclareVariable>
                <Name>timestamp</Name>
                <Type>Real</Type>
                <InitialValue>
                    <RealValue>0.0</RealValue>
                </InitialValue>
            </DeclareVariable>
        </VariableDeclarations>
        <NodeBody>
            <Update>
                <Pair>
                    <Name>Time</Name>
                    <RealVariable>timestamp</RealVariable>
                </Pair>
            </Update>
        </NodeBody>
    </Node>
    """
    result = translate_xml(xml, Node)
    assert "(('timestamp:val(0.0)))" in normalize_whitespace(result)
    assert "vardecls" not in normalize_whitespace(result)
    assert normalize_whitespace(result).startswith("update('UpdateWithVar,")


# ====================
# Empty Node with Variable Declarations
# ====================


def test_empty_node_with_variable_declaration(translate_xml):
    """Test Empty node with variable declaration."""
    xml = """
    <Node NodeType="Empty">
        <NodeId>EmptyWithVar</NodeId>
        <VariableDeclarations>
            <DeclareVariable>
                <Name>flag</Name>
                <Type>Boolean</Type>
                <InitialValue>
                    <BooleanValue>true</BooleanValue>
                </InitialValue>
            </DeclareVariable>
        </VariableDeclarations>
    </Node>
    """
    result = translate_xml(xml, Node)
    assert "(('flag:val(true)))" in normalize_whitespace(result)
    assert "vardecls" not in normalize_whitespace(result)
    assert normalize_whitespace(result).startswith("empty('EmptyWithVar,")


def test_empty_node_with_array_declaration(translate_xml):
    """Test Empty node with array declaration."""
    xml = """
    <Node NodeType="Empty">
        <NodeId>EmptyWithArray</NodeId>
        <VariableDeclarations>
            <DeclareArray>
                <Name>buffer</Name>
                <Type>Integer</Type>
                <MaxSize>10</MaxSize>
                <InitialValue>
                    <ArrayValue Type="Integer">
                        <IntegerValue>1</IntegerValue>
                        <IntegerValue>2</IntegerValue>
                    </ArrayValue>
                </InitialValue>
            </DeclareArray>
        </VariableDeclarations>
    </Node>
    """
    result = translate_xml(xml, Node)
    assert "(('buffer:createArray(10,val(1)#val(2))))" in normalize_whitespace(result)
    assert "vardecls" not in normalize_whitespace(result)


# ====================
# List Node with Variable Declarations
# ====================


def test_list_node_with_variable_declaration(translate_xml):
    """Test List node with variable declaration."""
    xml = """
    <Node NodeType="NodeList">
        <NodeId>ListWithVar</NodeId>
        <VariableDeclarations>
            <DeclareVariable>
                <Name>index</Name>
                <Type>Integer</Type>
                <InitialValue>
                    <IntegerValue>0</IntegerValue>
                </InitialValue>
            </DeclareVariable>
        </VariableDeclarations>
        <NodeBody>
            <NodeList>
                <Node NodeType="Empty">
                    <NodeId>Child1</NodeId>
                </Node>
            </NodeList>
        </NodeBody>
    </Node>
    """
    result = translate_xml(xml, Node)
    assert "(('index:val(0)))" in normalize_whitespace(result)
    assert "vardecls" not in normalize_whitespace(result)
    assert normalize_whitespace(result).startswith("list('ListWithVar,")


def test_list_node_with_mixed_declarations(translate_xml):
    """Test List node with both variable and array declarations."""
    xml = """
    <Node NodeType="NodeList">
        <NodeId>ListMixed</NodeId>
        <VariableDeclarations>
            <DeclareVariable>
                <Name>count</Name>
                <Type>Integer</Type>
            </DeclareVariable>
            <DeclareArray>
                <Name>items</Name>
                <Type>String</Type>
                <MaxSize>5</MaxSize>
            </DeclareArray>
        </VariableDeclarations>
        <NodeBody>
            <NodeList>
                <Node NodeType="Empty">
                    <NodeId>Child</NodeId>
                </Node>
            </NodeList>
        </NodeBody>
    </Node>
    """
    result = translate_xml(xml, Node)
    assert "(('count:unknown)('items:createArray(5,unknownArray(5))))" in normalize_whitespace(result)
    assert "vardecls" not in normalize_whitespace(result)


# ====================
# Nodes WITHOUT Variable Declarations (should output nilocdecl)
# ====================


def test_assignment_node_without_variable_declarations(translate_xml):
    """Test Assignment node without variable declarations outputs nilocdecl."""
    xml = """
    <Node NodeType="Assignment">
        <NodeId>NoVars</NodeId>
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
    assert "nilocdecl," in normalize_whitespace(result)
    assert "vardecls" not in normalize_whitespace(result)
    assert "((" not in result or "nilocdecl" in result  # No parens for var decls


def test_command_node_without_variable_declarations(translate_xml):
    """Test Command node without variable declarations outputs nilocdecl."""
    xml = """
    <Node NodeType="Command">
        <NodeId>NoVarsCmd</NodeId>
        <NodeBody>
            <Command>
                <Name>
                    <StringValue>Execute</StringValue>
                </Name>
            </Command>
        </NodeBody>
    </Node>
    """
    result = translate_xml(xml, Node)
    assert "nilocdecl," in normalize_whitespace(result)
    assert "vardecls" not in normalize_whitespace(result)


def test_empty_node_without_variable_declarations(translate_xml):
    """Test Empty node without variable declarations outputs nilocdecl."""
    xml = """
    <Node NodeType="Empty">
        <NodeId>NoVarsEmpty</NodeId>
    </Node>
    """
    result = translate_xml(xml, Node)
    assert "nilocdecl," in normalize_whitespace(result)
    assert "vardecls" not in normalize_whitespace(result)


# ====================
# Edge Cases
# ====================


def test_empty_variable_declarations_block(translate_xml):
    """Test node with empty VariableDeclarations block."""
    xml = """
    <Node NodeType="Assignment">
        <NodeId>EmptyVarBlock</NodeId>
        <VariableDeclarations>
        </VariableDeclarations>
        <NodeBody>
            <Assignment>
                <IntegerVariable>x</IntegerVariable>
                <NumericRHS>
                    <IntegerValue>1</IntegerValue>
                </NumericRHS>
            </Assignment>
        </NodeBody>
    </Node>
    """
    result = translate_xml(xml, Node)
    # Empty VariableDeclarations should produce ()
    assert "()" in normalize_whitespace(result) or "nilocdecl" in result
    assert "vardecls" not in normalize_whitespace(result)


def test_variable_with_expression_initial_value(translate_xml):
    """Test variable declared with expression as initial value."""
    xml = """
    <Node NodeType="Assignment">
        <NodeId>ExprInit</NodeId>
        <VariableDeclarations>
            <DeclareVariable>
                <Name>result</Name>
                <Type>Integer</Type>
                <InitialValue>
                    <IntegerVariable>input</IntegerVariable>
                </InitialValue>
            </DeclareVariable>
        </VariableDeclarations>
        <NodeBody>
            <Assignment>
                <IntegerVariable>result</IntegerVariable>
                <NumericRHS>
                    <IntegerValue>10</IntegerValue>
                </NumericRHS>
            </Assignment>
        </NodeBody>
    </Node>
    """
    result = translate_xml(xml, Node)
    # Variable initialized from another variable
    assert "(('result:var('input)))" in normalize_whitespace(result)
    assert "vardecls" not in normalize_whitespace(result)
