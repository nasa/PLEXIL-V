"""Tests for remainder operator fix.

These tests verify the MOD operator translates to _rem_ not _%_.
"""

import pytest
from plexil.core.v1.ast import Mod, Node, Eqnumeric, Add


def test_remainder_operator_naming(translate_xml):
    """Test that MOD operator uses _rem_ not _%_."""
    xml = """
    <MOD>
        <IntegerValue>10</IntegerValue>
        <IntegerValue>3</IntegerValue>
    </MOD>
    """
    result = translate_xml(xml, Mod)
    # Should use _rem_ operator
    assert result == "_rem_(const(val(10)),const(val(3)))"
    # Should NOT use _%_ operator
    assert "_%_" not in result


def test_remainder_with_real_values(translate_xml):
    """Test remainder with real (floating point) operands."""
    xml = """
    <MOD>
        <RealValue>7.5</RealValue>
        <RealValue>2.0</RealValue>
    </MOD>
    """
    result = translate_xml(xml, Mod)
    assert result == "_rem_(const(val(7.5)),const(val(2.0)))"
    assert "_rem_" in result


def test_remainder_with_variables(translate_xml):
    """Test remainder with variable operands."""
    xml = """
    <MOD>
        <IntegerValue>9</IntegerValue>
        <IntegerVariable>divisor</IntegerVariable>
    </MOD>
    """
    result = translate_xml(xml, Mod)
    assert result == "_rem_(const(val(9)),var('divisor))"


def test_remainder_both_variables(translate_xml):
    """Test remainder with both operands as variables."""
    xml = """
    <MOD>
        <IntegerVariable>dividend</IntegerVariable>
        <IntegerVariable>divisor</IntegerVariable>
    </MOD>
    """
    result = translate_xml(xml, Mod)
    assert result == "_rem_(var('dividend),var('divisor))"


def test_remainder_in_equality(translate_xml):
    """Test remainder operator inside an equality comparison."""
    xml = """
    <EQNumeric>
        <MOD>
            <RealValue>7.5</RealValue>
            <RealVariable>r</RealVariable>
        </MOD>
        <RealValue>1.5</RealValue>
    </EQNumeric>
    """
    result = translate_xml(xml, Eqnumeric)
    # Should have _equ_ wrapping _rem_
    assert "_equ_(_rem_(const(val(7.5)),var('r)),const(val(1.5)))" == result


def test_remainder_acceptance_pattern(translate_xml):
    """Test the pattern from remainder acceptance test."""
    xml = """
    <Node NodeType="Empty">
        <NodeId>remainder</NodeId>
        <VariableDeclarations>
            <DeclareVariable>
                <Name>r</Name>
                <Type>Real</Type>
                <InitialValue>
                    <RealValue>2.0</RealValue>
                </InitialValue>
            </DeclareVariable>
            <DeclareVariable>
                <Name>i</Name>
                <Type>Integer</Type>
                <InitialValue>
                    <IntegerValue>8</IntegerValue>
                </InitialValue>
            </DeclareVariable>
        </VariableDeclarations>
        <InvariantCondition>
            <AND>
                <EQNumeric>
                    <MOD>
                        <RealValue>7.5</RealValue>
                        <RealVariable>r</RealVariable>
                    </MOD>
                    <RealValue>1.5</RealValue>
                </EQNumeric>
                <EQNumeric>
                    <MOD>
                        <IntegerValue>9</IntegerValue>
                        <IntegerVariable>i</IntegerVariable>
                    </MOD>
                    <RealValue>1.0</RealValue>
                </EQNumeric>
            </AND>
        </InvariantCondition>
    </Node>
    """
    result = translate_xml(xml, Node)

    # Should have _rem_ in both remainder operations
    assert result.count("_rem_") == 2
    # First remainder: 7.5 % r == 1.5
    assert "_equ_(_rem_(const(val(7.5)),var('r)),const(val(1.5)))" in result
    # Second remainder: 9 % i == 1.0
    assert "_equ_(_rem_(const(val(9)),var('i)),const(val(1.0)))" in result
    # Should NOT have old _%_ operator
    assert "_%_" not in result


def test_remainder_nested_in_arithmetic(translate_xml):
    """Test remainder nested in other arithmetic operations."""
    xml = """
    <ADD>
        <MOD>
            <IntegerValue>10</IntegerValue>
            <IntegerValue>3</IntegerValue>
        </MOD>
        <IntegerValue>5</IntegerValue>
    </ADD>
    """
    result = translate_xml(xml, Add)
    # Should be: (10 % 3) + 5
    assert "_+_(_rem_(const(val(10)),const(val(3))),const(val(5)))" == result
