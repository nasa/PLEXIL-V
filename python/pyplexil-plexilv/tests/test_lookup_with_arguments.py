"""Tests for lookupWithArguments acceptance test pattern.

These tests verify that variable names with underscores are preserved
correctly in lookups with arguments.
"""

import pytest
from plexil.core.v1.ast import Node


def test_lookup_with_arguments_variable_names(translate_xml):
    """Test that variable names with underscores are preserved in lookups."""
    xml = """
    <Node NodeType="NodeList">
        <NodeId>lookupWithArguments</NodeId>
        <VariableDeclarations>
            <DeclareVariable>
                <Name>SatId</Name>
                <Type>Integer</Type>
                <InitialValue>
                    <IntegerValue>1</IntegerValue>
                </InitialValue>
            </DeclareVariable>
            <DeclareVariable>
                <Name>initial_drag</Name>
                <Type>Boolean</Type>
            </DeclareVariable>
        </VariableDeclarations>
        <ExitCondition>
            <NOT>
                <BooleanVariable>initial_drag</BooleanVariable>
            </NOT>
        </ExitCondition>
        <NodeBody>
            <NodeList>
                <Node NodeType="Assignment">
                    <NodeId>theAssignment</NodeId>
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
            </NodeList>
        </NodeBody>
    </Node>
    """
    result = translate_xml(xml, Node)

    # Variable declaration should use underscore
    assert "'initial_drag : unknown" in result

    # Variable references should use underscore (not hyphen)
    assert "var('initial_drag)" in result

    # Should NOT convert to hyphen
    assert "'initial-drag" not in result


def test_lookup_with_variable_argument(translate_xml):
    """Test lookup with a variable as argument."""
    xml = """
    <Node NodeType="Assignment">
        <NodeId>lookupTest</NodeId>
        <VariableDeclarations>
            <DeclareVariable>
                <Name>sat_id</Name>
                <Type>Integer</Type>
                <InitialValue>
                    <IntegerValue>42</IntegerValue>
                </InitialValue>
            </DeclareVariable>
            <DeclareVariable>
                <Name>result_value</Name>
                <Type>Boolean</Type>
            </DeclareVariable>
        </VariableDeclarations>
        <NodeBody>
            <Assignment>
                <BooleanVariable>result_value</BooleanVariable>
                <BooleanRHS>
                    <LookupNow>
                        <Name>
                            <StringValue>SomeState</StringValue>
                        </Name>
                        <Arguments>
                            <IntegerVariable>sat_id</IntegerVariable>
                        </Arguments>
                    </LookupNow>
                </BooleanRHS>
            </Assignment>
        </NodeBody>
    </Node>
    """
    result = translate_xml(xml, Node)

    # Both variable names should preserve underscores
    assert "'sat_id : val(42)" in result
    assert "'result_value : unknown" in result
    assert "var('sat_id)" in result
    assert "var('result_value)" in result

    # Should NOT convert to hyphens
    assert "'sat-id" not in result
    assert "'result-value" not in result


def test_lookup_with_multiple_arguments(translate_xml):
    """Test lookup with multiple variable arguments."""
    xml = """
    <Node NodeType="Assignment">
        <NodeId>multiArgLookup</NodeId>
        <VariableDeclarations>
            <DeclareVariable>
                <Name>first_arg</Name>
                <Type>Integer</Type>
                <InitialValue>
                    <IntegerValue>1</IntegerValue>
                </InitialValue>
            </DeclareVariable>
            <DeclareVariable>
                <Name>second_arg</Name>
                <Type>Integer</Type>
                <InitialValue>
                    <IntegerValue>2</IntegerValue>
                </InitialValue>
            </DeclareVariable>
            <DeclareVariable>
                <Name>lookup_result</Name>
                <Type>Real</Type>
            </DeclareVariable>
        </VariableDeclarations>
        <NodeBody>
            <Assignment>
                <RealVariable>lookup_result</RealVariable>
                <NumericRHS>
                    <LookupNow>
                        <Name>
                            <StringValue>MultiArgState</StringValue>
                        </Name>
                        <Arguments>
                            <IntegerVariable>first_arg</IntegerVariable>
                            <IntegerVariable>second_arg</IntegerVariable>
                        </Arguments>
                    </LookupNow>
                </NumericRHS>
            </Assignment>
        </NodeBody>
    </Node>
    """
    result = translate_xml(xml, Node)

    # All variable declarations should preserve underscores
    assert "'first_arg : val(1)" in result
    assert "'second_arg : val(2)" in result
    assert "'lookup_result : unknown" in result

    # All variable references should preserve underscores
    assert "var('first_arg)" in result
    assert "var('second_arg)" in result
    assert "var('lookup_result)" in result

    # Lookup should have both arguments (space-separated, not comma-separated)
    assert "lookup('MultiArgState,(var('first_arg) var('second_arg)))" in result


def test_lookup_exit_condition_with_underscored_variable(translate_xml):
    """Test that exit condition correctly references variable with underscore."""
    xml = """
    <Node NodeType="Empty">
        <NodeId>exitConditionTest</NodeId>
        <VariableDeclarations>
            <DeclareVariable>
                <Name>should_exit</Name>
                <Type>Boolean</Type>
                <InitialValue>
                    <BooleanValue>false</BooleanValue>
                </InitialValue>
            </DeclareVariable>
        </VariableDeclarations>
        <ExitCondition>
            <NOT>
                <BooleanVariable>should_exit</BooleanVariable>
            </NOT>
        </ExitCondition>
    </Node>
    """
    result = translate_xml(xml, Node)

    # Variable declaration should use underscore
    assert "'should_exit : val(false)" in result

    # Exit condition should reference with underscore
    assert "not_(var('should_exit))" in result

    # Should NOT use hyphen
    assert "'should-exit" not in result
