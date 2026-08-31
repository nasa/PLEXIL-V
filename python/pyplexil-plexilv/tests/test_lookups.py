import pytest
from plexil.core.v1.ast import LookupNow, LookupOnChange

# ====================
# LookupNow Tests
# ====================


def test_lookup_now_no_args(translate_xml):
    xml = """<LookupNow>
      <Name>
        <StringValue>r1</StringValue>
      </Name>
    </LookupNow>"""
    assert translate_xml(xml, LookupNow) == "lookup('r1,(nilpar))"


def test_lookup_now_different_name(translate_xml):
    xml = """<LookupNow>
      <Name>
        <StringValue>someValue</StringValue>
      </Name>
    </LookupNow>"""
    assert translate_xml(xml, LookupNow) == "lookup('someValue,(nilpar))"


def test_lookup_now_with_one_arg(translate_xml):
    xml = """<LookupNow>
      <Name>
        <StringValue>temperature</StringValue>
      </Name>
      <Arguments>
        <IntegerValue>1</IntegerValue>
      </Arguments>
    </LookupNow>"""
    assert translate_xml(xml, LookupNow) == "lookup('temperature,(const(val(1))))"


def test_lookup_now_with_multiple_args(translate_xml):
    xml = """<LookupNow>
      <Name>
        <StringValue>position</StringValue>
      </Name>
      <Arguments>
        <IntegerValue>0</IntegerValue>
        <IntegerValue>1</IntegerValue>
      </Arguments>
    </LookupNow>"""
    assert (
        translate_xml(xml, LookupNow)
        == "lookup('position,(const(val(0)) const(val(1))))"
    )


def test_lookup_now_with_string_args(translate_xml):
    xml = """<LookupNow>
      <Name>
        <StringValue>config</StringValue>
      </Name>
      <Arguments>
        <StringValue>mode</StringValue>
        <StringValue>active</StringValue>
      </Arguments>
    </LookupNow>"""
    assert (
        translate_xml(xml, LookupNow)
        == 'lookup(\'config,(const(val("mode")) const(val("active"))))'
    )


def test_lookup_now_with_variable_arg(translate_xml):
    xml = """<LookupNow>
      <Name>
        <StringValue>sensor</StringValue>
      </Name>
      <Arguments>
        <IntegerVariable>index</IntegerVariable>
      </Arguments>
    </LookupNow>"""
    assert translate_xml(xml, LookupNow) == "lookup('sensor,(var('index)))"


def test_lookup_now_with_mixed_args(translate_xml):
    xml = """<LookupNow>
      <Name>
        <StringValue>data</StringValue>
      </Name>
      <Arguments>
        <IntegerValue>42</IntegerValue>
        <StringVariable>name</StringVariable>
      </Arguments>
    </LookupNow>"""
    assert translate_xml(xml, LookupNow) == "lookup('data,(const(val(42)) var('name)))"


def test_lookup_now_with_variable_name(translate_xml):
    xml = """<LookupNow>
      <Name>
        <StringVariable>lookupName</StringVariable>
      </Name>
    </LookupNow>"""
    assert translate_xml(xml, LookupNow) == "lookup(var('lookupName),(nilpar))"


def test_lookup_now_with_variable_name_and_args(translate_xml):
    xml = """<LookupNow>
      <Name>
        <StringVariable>stateName</StringVariable>
      </Name>
      <Arguments>
        <IntegerValue>0</IntegerValue>
      </Arguments>
    </LookupNow>"""
    assert translate_xml(xml, LookupNow) == "lookup(var('stateName),(const(val(0))))"


# ====================
# LookupOnChange Tests
# ====================


def test_lookup_on_change_no_args(translate_xml):
    xml = """<LookupOnChange>
      <Name>
        <StringValue>inConflict</StringValue>
      </Name>
    </LookupOnChange>"""
    assert (
        translate_xml(xml, LookupOnChange)
        == "lookupOnChange('inConflict,(nilpar),val(0.0))"
    )


def test_lookup_on_change_one_arg(translate_xml):
    xml = """<LookupOnChange>
      <Name>
        <StringValue>A</StringValue>
      </Name>
      <Arguments>
        <IntegerValue>1</IntegerValue>
      </Arguments>
    </LookupOnChange>"""
    assert (
        translate_xml(xml, LookupOnChange)
        == "lookupOnChange('A,(const(val(1))),val(0.0))"
    )


def test_lookup_on_change_two_string_args(translate_xml):
    xml = """<LookupOnChange>
      <Name>
        <StringValue>A</StringValue>
      </Name>
      <Arguments>
        <StringValue>is</StringValue>
        <StringValue>isnot</StringValue>
      </Arguments>
    </LookupOnChange>"""
    assert (
        translate_xml(xml, LookupOnChange)
        == 'lookupOnChange(\'A,(const(val("is")) const(val("isnot"))),val(0.0))'
    )


def test_lookup_on_change_with_tolerance(translate_xml):
    xml = """<LookupOnChange>
      <Name>
        <StringValue>B</StringValue>
      </Name>
      <Arguments>
        <StringValue>param</StringValue>
      </Arguments>
      <Tolerance>
        <RealValue>0.5</RealValue>
      </Tolerance>
    </LookupOnChange>"""
    # Note: Tolerance values use val(...) without const() wrapper
    assert (
        translate_xml(xml, LookupOnChange)
        == 'lookupOnChange(\'B,(const(val("param"))),val(0.5))'
    )


def test_lookup_on_change_different_name(translate_xml):
    xml = """<LookupOnChange>
      <Name>
        <StringValue>statusFlag</StringValue>
      </Name>
    </LookupOnChange>"""
    assert (
        translate_xml(xml, LookupOnChange)
        == "lookupOnChange('statusFlag,(nilpar),val(0.0))"
    )


def test_lookup_on_change_with_variable_arg(translate_xml):
    xml = """<LookupOnChange>
      <Name>
        <StringValue>sensor</StringValue>
      </Name>
      <Arguments>
        <IntegerVariable>id</IntegerVariable>
      </Arguments>
    </LookupOnChange>"""
    assert (
        translate_xml(xml, LookupOnChange)
        == "lookupOnChange('sensor,(var('id)),val(0.0))"
    )


def test_lookup_on_change_with_real_tolerance(translate_xml):
    xml = """<LookupOnChange>
      <Name>
        <StringValue>temperature</StringValue>
      </Name>
      <Tolerance>
        <RealValue>1.5</RealValue>
      </Tolerance>
    </LookupOnChange>"""
    # Note: Tolerance values use val(...) without const() wrapper
    assert (
        translate_xml(xml, LookupOnChange)
        == "lookupOnChange('temperature,(nilpar),val(1.5))"
    )


def test_lookup_on_change_with_variable_tolerance(translate_xml):
    xml = """<LookupOnChange>
      <Name>
        <StringValue>velocity</StringValue>
      </Name>
      <Tolerance>
        <RealVariable>epsilon</RealVariable>
      </Tolerance>
    </LookupOnChange>"""
    assert (
        translate_xml(xml, LookupOnChange)
        == "lookupOnChange('velocity,(nilpar),var('epsilon))"
    )


def test_lookup_on_change_with_variable_name(translate_xml):
    xml = """<LookupOnChange>
      <Name>
        <StringVariable>lookupName</StringVariable>
      </Name>
    </LookupOnChange>"""
    assert (
        translate_xml(xml, LookupOnChange)
        == "lookupOnChange(var('lookupName),(nilpar),val(0.0))"
    )


def test_lookup_on_change_with_variable_name_and_tolerance(translate_xml):
    xml = """<LookupOnChange>
      <Name>
        <StringVariable>stateName</StringVariable>
      </Name>
      <Arguments>
        <IntegerValue>1</IntegerValue>
      </Arguments>
      <Tolerance>
        <RealValue>0.1</RealValue>
      </Tolerance>
    </LookupOnChange>"""
    # Note: Tolerance values use val(...) without const() wrapper
    assert (
        translate_xml(xml, LookupOnChange)
        == "lookupOnChange(var('stateName),(const(val(1))),val(0.1))"
    )
