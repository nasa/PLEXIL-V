import pytest
from plexil.core.v1.ast import (
    IntegerVariable,
    RealVariable,
    BooleanVariable,
    StringVariable,
    ArrayVariable,
)


# IntegerVariable tests
def test_integer_variable_simple(translate_xml):
    assert (
        translate_xml("<IntegerVariable>i</IntegerVariable>", IntegerVariable)
        == "var('i)"
    )


def test_integer_variable_descriptive_name(translate_xml):
    assert (
        translate_xml("<IntegerVariable>count</IntegerVariable>", IntegerVariable)
        == "var('count)"
    )


def test_integer_variable_camel_case(translate_xml):
    assert (
        translate_xml("<IntegerVariable>maxCount</IntegerVariable>", IntegerVariable)
        == "var('maxCount)"
    )


# RealVariable tests
def test_real_variable_simple(translate_xml):
    assert translate_xml("<RealVariable>r</RealVariable>", RealVariable) == "var('r)"


def test_real_variable_descriptive_name(translate_xml):
    assert (
        translate_xml("<RealVariable>speedPref</RealVariable>", RealVariable)
        == "var('speedPref)"
    )


def test_real_variable_multi_word(translate_xml):
    assert translate_xml("<RealVariable>r1</RealVariable>", RealVariable) == "var('r1)"


def test_real_variable_ret(translate_xml):
    assert (
        translate_xml("<RealVariable>ret</RealVariable>", RealVariable) == "var('ret)"
    )


# BooleanVariable tests
def test_boolean_variable_simple(translate_xml):
    assert (
        translate_xml("<BooleanVariable>flag</BooleanVariable>", BooleanVariable)
        == "var('flag)"
    )


def test_boolean_variable_descriptive(translate_xml):
    assert (
        translate_xml("<BooleanVariable>isActive</BooleanVariable>", BooleanVariable)
        == "var('isActive)"
    )


def test_boolean_variable_camel_case(translate_xml):
    assert (
        translate_xml(
            "<BooleanVariable>hasCompleted</BooleanVariable>", BooleanVariable
        )
        == "var('hasCompleted)"
    )


# StringVariable tests
def test_string_variable_simple(translate_xml):
    assert (
        translate_xml("<StringVariable>name</StringVariable>", StringVariable)
        == "var('name)"
    )


def test_string_variable_command_name(translate_xml):
    assert (
        translate_xml("<StringVariable>CommandName</StringVariable>", StringVariable)
        == "var('CommandName)"
    )


def test_string_variable_camel_case(translate_xml):
    assert (
        translate_xml("<StringVariable>nodeName</StringVariable>", StringVariable)
        == "var('nodeName)"
    )


# ArrayVariable tests
def test_array_variable_simple(translate_xml):
    assert (
        translate_xml("<ArrayVariable>foo</ArrayVariable>", ArrayVariable)
        == "var('foo)"
    )


def test_array_variable_descriptive(translate_xml):
    assert (
        translate_xml("<ArrayVariable>velCmd</ArrayVariable>", ArrayVariable)
        == "var('velCmd)"
    )


def test_array_variable_camel_case(translate_xml):
    assert (
        translate_xml("<ArrayVariable>acVelocity</ArrayVariable>", ArrayVariable)
        == "var('acVelocity)"
    )
