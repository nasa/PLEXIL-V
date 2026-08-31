import pytest
from plexil.core.v1.ast import ArrayElement, ArraySize, ArrayMaxSize

# ====================
# ArrayElement Tests
# ====================


def test_array_element_integer_variable_index(translate_xml):
    xml = """<ArrayElement>
      <ArrayVariable>foo</ArrayVariable>
      <Index>
        <IntegerVariable>i</IntegerVariable>
      </Index>
    </ArrayElement>"""
    assert translate_xml(xml, ArrayElement) == "arrayVar('foo,var('i))"


def test_array_element_integer_value_index(translate_xml):
    xml = """<ArrayElement>
      <ArrayVariable>velCmd</ArrayVariable>
      <Index>
        <IntegerValue>0</IntegerValue>
      </Index>
    </ArrayElement>"""
    assert translate_xml(xml, ArrayElement) == "arrayVar('velCmd,const(val(0)))"


def test_array_element_complex_index(translate_xml):
    xml = """<ArrayElement>
      <ArrayVariable>data</ArrayVariable>
      <Index>
        <ADD>
          <IntegerVariable>i</IntegerVariable>
          <IntegerValue>1</IntegerValue>
        </ADD>
      </Index>
    </ArrayElement>"""
    assert (
        translate_xml(xml, ArrayElement) == "arrayVar('data,_+_(var('i),const(val(1))))"
    )


def test_array_element_nested(translate_xml):
    xml = """<ArrayElement>
      <ArrayVariable>matrix</ArrayVariable>
      <Index>
        <ArrayElement>
          <ArrayVariable>indices</ArrayVariable>
          <Index>
            <IntegerValue>0</IntegerValue>
          </Index>
        </ArrayElement>
      </Index>
    </ArrayElement>"""
    assert (
        translate_xml(xml, ArrayElement)
        == "arrayVar('matrix,arrayVar('indices,const(val(0))))"
    )


def test_array_element_multiple_arrays(translate_xml):
    xml = """<ArrayElement>
      <ArrayVariable>acVelocity</ArrayVariable>
      <Index>
        <IntegerValue>0</IntegerValue>
      </Index>
    </ArrayElement>"""
    assert translate_xml(xml, ArrayElement) == "arrayVar('acVelocity,const(val(0)))"


def test_array_element_with_subtraction_index(translate_xml):
    xml = """<ArrayElement>
      <ArrayVariable>buffer</ArrayVariable>
      <Index>
        <SUB>
          <IntegerVariable>count</IntegerVariable>
          <IntegerValue>1</IntegerValue>
        </SUB>
      </Index>
    </ArrayElement>"""
    assert (
        translate_xml(xml, ArrayElement)
        == "arrayVar('buffer,_-_(var('count),const(val(1))))"
    )


def test_array_element_with_name_element(translate_xml):
    """Test array element with <Name> instead of <ArrayVariable>."""
    xml = """<ArrayElement>
      <Name>myStringArray</Name>
      <Index>
        <IntegerValue>0</IntegerValue>
      </Index>
    </ArrayElement>"""
    assert translate_xml(xml, ArrayElement) == "arrayVar('myStringArray,const(val(0)))"


# ====================
# ArraySize Tests
# ====================


def test_array_size_simple(translate_xml):
    xml = """<ArraySize>
      <ArrayVariable>myArray</ArrayVariable>
    </ArraySize>"""
    assert translate_xml(xml, ArraySize) == "arraySize(var('myArray))"


def test_array_size_different_name(translate_xml):
    xml = """<ArraySize>
      <ArrayVariable>data</ArrayVariable>
    </ArraySize>"""
    assert translate_xml(xml, ArraySize) == "arraySize(var('data))"


def test_array_size_camel_case(translate_xml):
    xml = """<ArraySize>
      <ArrayVariable>velocityCmd</ArrayVariable>
    </ArraySize>"""
    assert translate_xml(xml, ArraySize) == "arraySize(var('velocityCmd))"


# ====================
# ArrayMaxSize Tests
# ====================


def test_array_max_size_simple(translate_xml):
    xml = """<ArrayMaxSize>
      <ArrayVariable>myArray</ArrayVariable>
    </ArrayMaxSize>"""
    assert translate_xml(xml, ArrayMaxSize) == "arrayMaxSize(var('myArray))"


def test_array_max_size_different_name(translate_xml):
    xml = """<ArrayMaxSize>
      <ArrayVariable>buffer</ArrayVariable>
    </ArrayMaxSize>"""
    assert translate_xml(xml, ArrayMaxSize) == "arrayMaxSize(var('buffer))"


def test_array_max_size_camel_case(translate_xml):
    xml = """<ArrayMaxSize>
      <ArrayVariable>resultArray</ArrayVariable>
    </ArrayMaxSize>"""
    assert translate_xml(xml, ArrayMaxSize) == "arrayMaxSize(var('resultArray))"
