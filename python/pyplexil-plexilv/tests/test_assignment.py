"""Tests for Assignment translation."""

import pytest
from plexil.core.v1.ast import Assignment


def test_simple_variable_assignment(translate_xml):
    """Test simple variable assignment: r1 := lookup."""
    xml = """
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
    """
    result = translate_xml(xml, Assignment)
    expected = "(var('r1) := lookup('r1,(nilpar)))"
    assert result == expected, f"Expected: {expected}\nGot: {result}"


def test_simple_array_element_assignment(translate_xml):
    """Test array element assignment: foo[i] := 1.0."""
    xml = """
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
    """
    result = translate_xml(xml, Assignment)
    expected = "(arrayVar('foo,var('i)) := const(val(1.0)))"
    assert result == expected, f"Expected: {expected}\nGot: {result}"


def test_complex_array_assignment(translate_xml):
    """Test array element to array element assignment: velCmd[0] := acVelocity[0]."""
    xml = """
    <Assignment>
      <ArrayElement>
        <ArrayVariable>velCmd</ArrayVariable>
        <Index>
          <IntegerValue>0</IntegerValue>
        </Index>
      </ArrayElement>
      <NumericRHS>
        <ArrayElement>
          <ArrayVariable>acVelocity</ArrayVariable>
          <Index>
            <IntegerValue>0</IntegerValue>
          </Index>
        </ArrayElement>
      </NumericRHS>
    </Assignment>
    """
    result = translate_xml(xml, Assignment)
    expected = (
        "(arrayVar('velCmd,const(val(0))) := arrayVar('acVelocity,const(val(0))))"
    )
    assert result == expected, f"Expected: {expected}\nGot: {result}"


def test_integer_variable_assignment(translate_xml):
    """Test integer variable assignment."""
    xml = """
    <Assignment>
      <IntegerVariable>count</IntegerVariable>
      <NumericRHS>
        <IntegerValue>42</IntegerValue>
      </NumericRHS>
    </Assignment>
    """
    result = translate_xml(xml, Assignment)
    expected = "(var('count) := const(val(42)))"
    assert result == expected, f"Expected: {expected}\nGot: {result}"


def test_boolean_variable_assignment(translate_xml):
    """Test boolean variable assignment."""
    xml = """
    <Assignment>
      <BooleanVariable>flag</BooleanVariable>
      <BooleanRHS>
        <BooleanValue>true</BooleanValue>
      </BooleanRHS>
    </Assignment>
    """
    result = translate_xml(xml, Assignment)
    expected = "(var('flag) := const(val(true)))"
    assert result == expected, f"Expected: {expected}\nGot: {result}"


def test_string_variable_assignment(translate_xml):
    """Test string variable assignment."""
    xml = """
    <Assignment>
      <StringVariable>message</StringVariable>
      <StringRHS>
        <StringValue>hello</StringValue>
      </StringRHS>
    </Assignment>
    """
    result = translate_xml(xml, Assignment)
    expected = '(var(\'message) := const(val("hello")))'
    assert result == expected, f"Expected: {expected}\nGot: {result}"
