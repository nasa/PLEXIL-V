"""Tests for Update translation."""

import pytest
from plexil.core.v1.ast import Update


def test_update_with_variables(translate_xml):
    """Test update with variable pairs."""
    xml = """
    <Update>
      <Pair>
        <Name>taskId</Name>
        <IntegerVariable>waypt_id</IntegerVariable>
      </Pair>
      <Pair>
        <Name>result</Name>
        <IntegerVariable>cmd_return_val</IntegerVariable>
      </Pair>
    </Update>
    """
    result = translate_xml(xml, Update)
    expected = "(< 'taskId ; var('waypt_id) > < 'result ; var('cmd_return_val) >)"
    assert result == expected, f"Expected: {expected}\nGot: {result}"


def test_update_with_lookup(translate_xml):
    """Test update with lookup expression."""
    xml = """
    <Update>
      <Pair>
        <Name>lookup</Name>
        <LookupNow>
          <Name>
            <StringValue>someValue</StringValue>
          </Name>
        </LookupNow>
      </Pair>
    </Update>
    """
    result = translate_xml(xml, Update)
    expected = "(< 'lookup ; lookup('someValue,(nilpar)) >)"
    assert result == expected, f"Expected: {expected}\nGot: {result}"


def test_update_with_literal_and_array_variable(translate_xml):
    """Test update with literal value and array variable."""
    xml = """
    <Update>
      <Pair>
        <Name>realconstant</Name>
        <RealValue>3.141</RealValue>
      </Pair>
      <Pair>
        <Name>val</Name>
        <ArrayVariable>src</ArrayVariable>
      </Pair>
    </Update>
    """
    result = translate_xml(xml, Update)
    expected = "(< 'realconstant ; const(val(3.141)) > < 'val ; arrayVar('src) >)"
    assert result == expected, f"Expected: {expected}\nGot: {result}"


def test_update_single_pair(translate_xml):
    """Test update with single pair."""
    xml = """
    <Update>
      <Pair>
        <Name>status</Name>
        <StringValue>active</StringValue>
      </Pair>
    </Update>
    """
    result = translate_xml(xml, Update)
    expected = '(< \'status ; const(val("active")) >)'
    assert result == expected, f"Expected: {expected}\nGot: {result}"


def test_update_with_boolean(translate_xml):
    """Test update with boolean value."""
    xml = """
    <Update>
      <Pair>
        <Name>flag</Name>
        <BooleanValue>true</BooleanValue>
      </Pair>
    </Update>
    """
    result = translate_xml(xml, Update)
    expected = "(< 'flag ; const(val(true)) >)"
    assert result == expected, f"Expected: {expected}\nGot: {result}"


def test_update_with_integer_value(translate_xml):
    """Test update with integer value."""
    xml = """
    <Update>
      <Pair>
        <Name>count</Name>
        <IntegerValue>42</IntegerValue>
      </Pair>
    </Update>
    """
    result = translate_xml(xml, Update)
    expected = "(< 'count ; const(val(42)) >)"
    assert result == expected, f"Expected: {expected}\nGot: {result}"
