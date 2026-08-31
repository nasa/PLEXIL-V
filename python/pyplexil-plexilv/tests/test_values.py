import pytest
from plexil.core.v1.ast import (
    IntegerValue,
    RealValue,
    BooleanValue,
    StringValue,
    ArrayValue,
)


# IntegerValue tests
def test_integer_value_positive(translate_xml):
    assert (
        translate_xml("<IntegerValue>42</IntegerValue>", IntegerValue)
        == "const(val(42))"
    )


def test_integer_value_zero(translate_xml):
    assert (
        translate_xml("<IntegerValue>0</IntegerValue>", IntegerValue) == "const(val(0))"
    )


def test_integer_value_negative(translate_xml):
    assert (
        translate_xml("<IntegerValue>-100</IntegerValue>", IntegerValue)
        == "const(val(-100))"
    )


def test_integer_value_large(translate_xml):
    assert (
        translate_xml("<IntegerValue>1000000</IntegerValue>", IntegerValue)
        == "const(val(1000000))"
    )


# RealValue tests
def test_real_value_integer_notation(translate_xml):
    assert (
        translate_xml("<RealValue>1000</RealValue>", RealValue) == "const(val(1000.0))"
    )


def test_real_value_decimal_notation(translate_xml):
    assert (
        translate_xml("<RealValue>1000.0</RealValue>", RealValue)
        == "const(val(1000.0))"
    )


def test_real_value_zero(translate_xml):
    assert translate_xml("<RealValue>0</RealValue>", RealValue) == "const(val(0.0))"


def test_real_value_negative(translate_xml):
    assert (
        translate_xml("<RealValue>-100</RealValue>", RealValue) == "const(val(-100.0))"
    )


def test_real_value_scientific_notation(translate_xml):
    assert (
        translate_xml("<RealValue>-1e2</RealValue>", RealValue) == "const(val(-100.0))"
    )


def test_real_value_decimal(translate_xml):
    assert translate_xml("<RealValue>1.0</RealValue>", RealValue) == "const(val(1.0))"


def test_real_value_fractional(translate_xml):
    assert translate_xml("<RealValue>7.5</RealValue>", RealValue) == "const(val(7.5))"


# BooleanValue tests
def test_boolean_value_true(translate_xml):
    assert (
        translate_xml("<BooleanValue>true</BooleanValue>", BooleanValue)
        == "const(val(true))"
    )


def test_boolean_value_false(translate_xml):
    assert (
        translate_xml("<BooleanValue>false</BooleanValue>", BooleanValue)
        == "const(val(false))"
    )


# StringValue tests
def test_string_value_simple(translate_xml):
    assert (
        translate_xml("<StringValue>foo</StringValue>", StringValue)
        == 'const(val("foo"))'
    )


def test_string_value_empty(translate_xml):
    assert translate_xml("<StringValue />", StringValue) == 'const(val(""))'


def test_string_value_with_content(translate_xml):
    assert (
        translate_xml("<StringValue>one</StringValue>", StringValue)
        == 'const(val("one"))'
    )


def test_string_value_multi_word(translate_xml):
    assert (
        translate_xml("<StringValue>hello world</StringValue>", StringValue)
        == 'const(val("hello world"))'
    )


# ArrayValue tests
def test_array_value_integer_empty(translate_xml):
    xml = '<ArrayValue Type="Integer"></ArrayValue>'
    assert translate_xml(xml, ArrayValue) == "const(array(emptyList))"


def test_array_value_integer_single(translate_xml):
    xml = '<ArrayValue Type="Integer"><IntegerValue>1</IntegerValue></ArrayValue>'
    assert translate_xml(xml, ArrayValue) == "const(array(val(1)))"


def test_array_value_integer_multiple(translate_xml):
    xml = '<ArrayValue Type="Integer"><IntegerValue>1</IntegerValue><IntegerValue>2</IntegerValue><IntegerValue>3</IntegerValue></ArrayValue>'
    assert translate_xml(xml, ArrayValue) == "const(array(val(1) # val(2) # val(3)))"


def test_array_value_real_multiple(translate_xml):
    xml = '<ArrayValue Type="Real"><RealValue>0</RealValue><RealValue>7</RealValue><RealValue>13</RealValue></ArrayValue>'
    assert (
        translate_xml(xml, ArrayValue)
        == "const(array(val(0.0) # val(7.0) # val(13.0)))"
    )


def test_array_value_boolean_multiple(translate_xml):
    xml = '<ArrayValue Type="Boolean"><BooleanValue>true</BooleanValue><BooleanValue>false</BooleanValue></ArrayValue>'
    assert translate_xml(xml, ArrayValue) == "const(array(val(true) # val(false)))"


def test_array_value_string_multiple(translate_xml):
    xml = '<ArrayValue Type="String"><StringValue>one</StringValue><StringValue>two</StringValue></ArrayValue>'
    assert translate_xml(xml, ArrayValue) == 'const(array(val("one") # val("two")))'
