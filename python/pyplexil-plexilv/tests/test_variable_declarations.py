import pytest
from plexil.core.v1.ast import (
    DeclareVariable,
    DeclareArray,
    VariableDeclarations,
)

# ====================
# DeclareVariable Tests
# ====================


def test_declare_variable_integer_with_initial_value(translate_xml):
    xml = """<DeclareVariable>
      <Name>i</Name>
      <Type>Integer</Type>
      <InitialValue>
        <IntegerValue>0</IntegerValue>
      </InitialValue>
    </DeclareVariable>"""
    assert translate_xml(xml, DeclareVariable) == "('i : val(0))"


def test_declare_variable_real_with_initial_value(translate_xml):
    xml = """<DeclareVariable>
      <Name>temperature</Name>
      <Type>Real</Type>
      <InitialValue>
        <RealValue>25.5</RealValue>
      </InitialValue>
    </DeclareVariable>"""
    assert translate_xml(xml, DeclareVariable) == "('temperature : val(25.5))"


def test_declare_variable_boolean_with_initial_value(translate_xml):
    xml = """<DeclareVariable>
      <Name>flag</Name>
      <Type>Boolean</Type>
      <InitialValue>
        <BooleanValue>true</BooleanValue>
      </InitialValue>
    </DeclareVariable>"""
    assert translate_xml(xml, DeclareVariable) == "('flag : val(true))"


def test_declare_variable_string_with_initial_value(translate_xml):
    xml = """<DeclareVariable>
      <Name>CommandName</Name>
      <Type>String</Type>
      <InitialValue>
        <StringValue>foo</StringValue>
      </InitialValue>
    </DeclareVariable>"""
    assert translate_xml(xml, DeclareVariable) == '(\'CommandName : val("foo"))'


def test_declare_variable_string_with_empty_initial_value(translate_xml):
    xml = """<DeclareVariable>
      <Name>foo</Name>
      <Type>String</Type>
      <InitialValue>
        <StringValue />
      </InitialValue>
    </DeclareVariable>"""
    assert translate_xml(xml, DeclareVariable) == '(\'foo : val(""))'


def test_declare_variable_no_initial_value(translate_xml):
    xml = """<DeclareVariable>
      <Name>x</Name>
      <Type>Real</Type>
    </DeclareVariable>"""
    assert translate_xml(xml, DeclareVariable) == "('x : unknown)"


def test_declare_variable_integer_no_initial_value(translate_xml):
    xml = """<DeclareVariable>
      <Name>counter</Name>
      <Type>Integer</Type>
    </DeclareVariable>"""
    assert translate_xml(xml, DeclareVariable) == "('counter : unknown)"


def test_declare_variable_boolean_no_initial_value(translate_xml):
    xml = """<DeclareVariable>
      <Name>enabled</Name>
      <Type>Boolean</Type>
    </DeclareVariable>"""
    assert translate_xml(xml, DeclareVariable) == "('enabled : unknown)"


def test_declare_variable_with_variable_initial_value(translate_xml):
    xml = """<DeclareVariable>
      <Name>copy</Name>
      <Type>Integer</Type>
      <InitialValue>
        <IntegerVariable>original</IntegerVariable>
      </InitialValue>
    </DeclareVariable>"""
    assert translate_xml(xml, DeclareVariable) == "('copy : var('original))"


# ====================
# DeclareArray Tests
# ====================


def test_declare_array_no_initial_value(translate_xml):
    xml = """<DeclareArray>
      <Name>acPosition</Name>
      <Type>Real</Type>
      <MaxSize>3</MaxSize>
    </DeclareArray>"""
    assert (
        translate_xml(xml, DeclareArray)
        == "('acPosition : createArray(3,unknownArray(3)))"
    )


def test_declare_array_with_initial_values(translate_xml):
    xml = """<DeclareArray>
      <Name>bar</Name>
      <Type>Real</Type>
      <MaxSize>3</MaxSize>
      <InitialValue>
        <ArrayValue Type="Real">
          <RealValue>0</RealValue>
          <RealValue>7</RealValue>
          <RealValue>13</RealValue>
        </ArrayValue>
      </InitialValue>
    </DeclareArray>"""
    assert (
        translate_xml(xml, DeclareArray)
        == "('bar : createArray(3,val(0.0) # val(7.0) # val(13.0)))"
    )


def test_declare_array_integer_with_initial_values(translate_xml):
    xml = """<DeclareArray>
      <Name>numbers</Name>
      <Type>Integer</Type>
      <MaxSize>4</MaxSize>
      <InitialValue>
        <ArrayValue Type="Integer">
          <IntegerValue>1</IntegerValue>
          <IntegerValue>2</IntegerValue>
          <IntegerValue>3</IntegerValue>
          <IntegerValue>4</IntegerValue>
        </ArrayValue>
      </InitialValue>
    </DeclareArray>"""
    assert (
        translate_xml(xml, DeclareArray)
        == "('numbers : createArray(4,val(1) # val(2) # val(3) # val(4)))"
    )


def test_declare_array_boolean_no_initial_value(translate_xml):
    xml = """<DeclareArray>
      <Name>flags</Name>
      <Type>Boolean</Type>
      <MaxSize>5</MaxSize>
    </DeclareArray>"""
    assert (
        translate_xml(xml, DeclareArray) == "('flags : createArray(5,unknownArray(5)))"
    )


def test_declare_array_string_with_initial_values(translate_xml):
    xml = """<DeclareArray>
      <Name>names</Name>
      <Type>String</Type>
      <MaxSize>2</MaxSize>
      <InitialValue>
        <ArrayValue Type="String">
          <StringValue>Alice</StringValue>
          <StringValue>Bob</StringValue>
        </ArrayValue>
      </InitialValue>
    </DeclareArray>"""
    assert (
        translate_xml(xml, DeclareArray)
        == '(\'names : createArray(2,val("Alice") # val("Bob")))'
    )


def test_declare_array_size_one(translate_xml):
    xml = """<DeclareArray>
      <Name>single</Name>
      <Type>Integer</Type>
      <MaxSize>1</MaxSize>
    </DeclareArray>"""
    assert (
        translate_xml(xml, DeclareArray) == "('single : createArray(1,unknownArray(1)))"
    )


def test_declare_array_large_size(translate_xml):
    xml = """<DeclareArray>
      <Name>buffer</Name>
      <Type>Real</Type>
      <MaxSize>100</MaxSize>
    </DeclareArray>"""
    assert (
        translate_xml(xml, DeclareArray)
        == "('buffer : createArray(100,unknownArray(100)))"
    )


# ====================
# VariableDeclarations Tests
# ====================


def test_variable_declarations_single_variable(translate_xml):
    xml = """<VariableDeclarations>
      <DeclareVariable>
        <Name>x</Name>
        <Type>Integer</Type>
        <InitialValue>
          <IntegerValue>5</IntegerValue>
        </InitialValue>
      </DeclareVariable>
    </VariableDeclarations>"""
    assert translate_xml(xml, VariableDeclarations) == "(('x : val(5)))"


def test_variable_declarations_multiple_variables(translate_xml):
    xml = """<VariableDeclarations>
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
    </VariableDeclarations>"""
    assert translate_xml(xml, VariableDeclarations) == "(('x : val(0))('y : val(1.5)))"


def test_variable_declarations_with_array(translate_xml):
    xml = """<VariableDeclarations>
      <DeclareVariable>
        <Name>counter</Name>
        <Type>Integer</Type>
        <InitialValue>
          <IntegerValue>0</IntegerValue>
        </InitialValue>
      </DeclareVariable>
      <DeclareArray>
        <Name>data</Name>
        <Type>Real</Type>
        <MaxSize>3</MaxSize>
      </DeclareArray>
    </VariableDeclarations>"""
    assert (
        translate_xml(xml, VariableDeclarations)
        == "(('counter : val(0))('data : createArray(3,unknownArray(3))))"
    )


def test_variable_declarations_mixed_initialized_and_uninitialized(translate_xml):
    xml = """<VariableDeclarations>
      <DeclareVariable>
        <Name>a</Name>
        <Type>Integer</Type>
        <InitialValue>
          <IntegerValue>10</IntegerValue>
        </InitialValue>
      </DeclareVariable>
      <DeclareVariable>
        <Name>b</Name>
        <Type>Real</Type>
      </DeclareVariable>
    </VariableDeclarations>"""
    assert translate_xml(xml, VariableDeclarations) == "(('a : val(10))('b : unknown))"


def test_variable_declarations_empty(translate_xml):
    xml = """<VariableDeclarations>
    </VariableDeclarations>"""
    assert translate_xml(xml, VariableDeclarations) == "()"
