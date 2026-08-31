"""Tests for TestWait acceptance test fixes.

These tests verify the tolerance value handling in LookupOnChange.
"""

import pytest
from plexil.core.v1.ast import LookupOnChange, Node


def test_lookup_on_change_tolerance_no_const_wrapper(translate_xml):
    """Test that tolerance values in LookupOnChange use val(...) not const(val(...))."""
    xml = """
    <LookupOnChange>
        <Name>
            <StringValue>time</StringValue>
        </Name>
        <Tolerance>
            <IntegerValue>1</IntegerValue>
        </Tolerance>
    </LookupOnChange>
    """
    result = translate_xml(xml, LookupOnChange)
    # Tolerance should use val(...) not const(val(...))
    assert result == "lookupOnChange('time,(nilpar),val(1))"
    # Should NOT have const wrapper
    assert "const(val(1))" not in result


def test_lookup_on_change_real_tolerance_no_const_wrapper(translate_xml):
    """Test that real tolerance values use val(...) not const(val(...))."""
    xml = """
    <LookupOnChange>
        <Name>
            <StringValue>time</StringValue>
        </Name>
        <Tolerance>
            <RealValue>0.1</RealValue>
        </Tolerance>
    </LookupOnChange>
    """
    result = translate_xml(xml, LookupOnChange)
    # Tolerance should use val(...) not const(val(...))
    assert result == "lookupOnChange('time,(nilpar),val(0.1))"
    assert "const(val(0.1))" not in result


def test_lookup_on_change_tolerance_with_variable(translate_xml):
    """Test that variable tolerances still get proper handling."""
    xml = """
    <LookupOnChange>
        <Name>
            <StringValue>sensor</StringValue>
        </Name>
        <Tolerance>
            <RealVariable>epsilon</RealVariable>
        </Tolerance>
    </LookupOnChange>
    """
    result = translate_xml(xml, LookupOnChange)
    # Variable references should use var(...)
    assert result == "lookupOnChange('sensor,(nilpar),var('epsilon))"


def test_testwait_pattern(translate_xml):
    """Test the TestWait acceptance test pattern with timepoint and tolerance."""
    xml = """
    <Node NodeType="Empty">
        <NodeId>Wait__0</NodeId>
        <EndCondition>
            <GE>
                <LookupOnChange>
                    <Name>
                        <StringValue>time</StringValue>
                    </Name>
                    <Tolerance>
                        <IntegerValue>1</IntegerValue>
                    </Tolerance>
                </LookupOnChange>
                <ADD>
                    <IntegerValue>1</IntegerValue>
                    <NodeTimepointValue>
                        <NodeRef dir="self"/>
                        <NodeStateValue>EXECUTING</NodeStateValue>
                        <Timepoint>START</Timepoint>
                    </NodeTimepointValue>
                </ADD>
            </GE>
        </EndCondition>
    </Node>
    """
    result = translate_xml(xml, Node)

    # Tolerance should use val(1) not const(val(1))
    assert "lookupOnChange('time,(nilpar),val(1))" in result
    # Timepoint should be correct
    assert "timepoint(self,executing,start)" in result
    # Should have proper >= operator
    assert "_>=_" in result


def test_lookup_on_change_with_args_and_tolerance(translate_xml):
    """Test LookupOnChange with both arguments and tolerance."""
    xml = """
    <LookupOnChange>
        <Name>
            <StringValue>sensor</StringValue>
        </Name>
        <Arguments>
            <IntegerValue>5</IntegerValue>
        </Arguments>
        <Tolerance>
            <RealValue>2.5</RealValue>
        </Tolerance>
    </LookupOnChange>
    """
    result = translate_xml(xml, LookupOnChange)
    # Arguments should have const wrapper, tolerance should not
    assert result == "lookupOnChange('sensor,(const(val(5))),val(2.5))"
