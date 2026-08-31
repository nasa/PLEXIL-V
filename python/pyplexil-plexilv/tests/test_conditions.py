"""Tests for Condition translation."""

import pytest
from plexil.core.v1.ast import (
    StartCondition,
    EndCondition,
    PreCondition,
    PostCondition,
    InvariantCondition,
    RepeatCondition,
    ExitCondition,
    SkipCondition,
)


def test_start_condition_with_boolean_value(translate_xml):
    """Test StartCondition with boolean value."""
    xml = """
    <StartCondition>
        <BooleanValue>true</BooleanValue>
    </StartCondition>
    """
    result = translate_xml(xml, StartCondition)
    expected = "(startc: (const(val(true))))"
    assert result == expected, f"Expected: {expected}\nGot: {result}"


def test_start_condition_with_variable(translate_xml):
    """Test StartCondition with variable."""
    xml = """
    <StartCondition>
        <BooleanVariable>readyFlag</BooleanVariable>
    </StartCondition>
    """
    result = translate_xml(xml, StartCondition)
    expected = "(startc: (var('readyFlag)))"
    assert result == expected, f"Expected: {expected}\nGot: {result}"


def test_start_condition_with_expression(translate_xml):
    """Test StartCondition with complex expression."""
    xml = """
    <StartCondition>
        <EQInternal>
            <NodeStateVariable>
                <NodeRef dir="sibling">TestVars1</NodeRef>
            </NodeStateVariable>
            <NodeStateValue>FINISHED</NodeStateValue>
        </EQInternal>
    </StartCondition>
    """
    result = translate_xml(xml, StartCondition)
    expected = "(startc: (isStatus?('TestVars1,finished)))"
    assert result == expected, f"Expected: {expected}\nGot: {result}"


def test_end_condition_with_boolean_value(translate_xml):
    """Test EndCondition with boolean value."""
    xml = """
    <EndCondition>
        <BooleanValue>true</BooleanValue>
    </EndCondition>
    """
    result = translate_xml(xml, EndCondition)
    expected = "(endc: (const(val(true))))"
    assert result == expected, f"Expected: {expected}\nGot: {result}"


def test_end_condition_with_variable(translate_xml):
    """Test EndCondition with variable."""
    xml = """
    <EndCondition>
        <BooleanVariable>doneFlag</BooleanVariable>
    </EndCondition>
    """
    result = translate_xml(xml, EndCondition)
    expected = "(endc: (var('doneFlag)))"
    assert result == expected, f"Expected: {expected}\nGot: {result}"


def test_pre_condition_with_boolean_value(translate_xml):
    """Test PreCondition with boolean value."""
    xml = """
    <PreCondition>
        <BooleanValue>true</BooleanValue>
    </PreCondition>
    """
    result = translate_xml(xml, PreCondition)
    expected = "(pre: (const(val(true))))"
    assert result == expected, f"Expected: {expected}\nGot: {result}"


def test_pre_condition_with_false(translate_xml):
    """Test PreCondition with false value."""
    xml = """
    <PreCondition>
        <BooleanValue>false</BooleanValue>
    </PreCondition>
    """
    result = translate_xml(xml, PreCondition)
    expected = "(pre: (const(val(false))))"
    assert result == expected, f"Expected: {expected}\nGot: {result}"


def test_post_condition_with_boolean_value(translate_xml):
    """Test PostCondition with boolean value."""
    xml = """
    <PostCondition>
        <BooleanValue>false</BooleanValue>
    </PostCondition>
    """
    result = translate_xml(xml, PostCondition)
    expected = "(post: (const(val(false))))"
    assert result == expected, f"Expected: {expected}\nGot: {result}"


def test_post_condition_with_variable(translate_xml):
    """Test PostCondition with variable."""
    xml = """
    <PostCondition>
        <BooleanVariable>successFlag</BooleanVariable>
    </PostCondition>
    """
    result = translate_xml(xml, PostCondition)
    expected = "(post: (var('successFlag)))"
    assert result == expected, f"Expected: {expected}\nGot: {result}"


def test_invariant_condition_with_boolean_value(translate_xml):
    """Test InvariantCondition with boolean value."""
    xml = """
    <InvariantCondition>
        <BooleanValue>true</BooleanValue>
    </InvariantCondition>
    """
    result = translate_xml(xml, InvariantCondition)
    expected = "(inv: (const(val(true))))"
    assert result == expected, f"Expected: {expected}\nGot: {result}"


def test_invariant_condition_with_no_child_failed(translate_xml):
    """Test InvariantCondition with NoChildFailed."""
    xml = """
    <InvariantCondition>
        <NoChildFailed>
            <NodeRef dir="self"/>
        </NoChildFailed>
    </InvariantCondition>
    """
    result = translate_xml(xml, InvariantCondition)
    expected = "(inv: (noChildFailed))"
    assert result == expected, f"Expected: {expected}\nGot: {result}"


def test_repeat_condition_with_variable(translate_xml):
    """Test RepeatCondition with variable."""
    xml = """
    <RepeatCondition>
        <BooleanVariable>Variable1</BooleanVariable>
    </RepeatCondition>
    """
    result = translate_xml(xml, RepeatCondition)
    expected = "(repeatc: (var('Variable1)))"
    assert result == expected, f"Expected: {expected}\nGot: {result}"


def test_repeat_condition_with_boolean_value(translate_xml):
    """Test RepeatCondition with boolean value."""
    xml = """
    <RepeatCondition>
        <BooleanValue>true</BooleanValue>
    </RepeatCondition>
    """
    result = translate_xml(xml, RepeatCondition)
    expected = "(repeatc: (const(val(true))))"
    assert result == expected, f"Expected: {expected}\nGot: {result}"


def test_exit_condition_with_boolean_value(translate_xml):
    """Test ExitCondition with boolean value."""
    xml = """
    <ExitCondition>
        <BooleanValue>true</BooleanValue>
    </ExitCondition>
    """
    result = translate_xml(xml, ExitCondition)
    expected = "(exitc: (const(val(true))))"
    assert result == expected, f"Expected: {expected}\nGot: {result}"


def test_exit_condition_with_variable(translate_xml):
    """Test ExitCondition with variable."""
    xml = """
    <ExitCondition>
        <BooleanVariable>exitFlag</BooleanVariable>
    </ExitCondition>
    """
    result = translate_xml(xml, ExitCondition)
    expected = "(exitc: (var('exitFlag)))"
    assert result == expected, f"Expected: {expected}\nGot: {result}"


def test_skip_condition_with_boolean_value(translate_xml):
    """Test SkipCondition with boolean value."""
    xml = """
    <SkipCondition>
        <BooleanValue>true</BooleanValue>
    </SkipCondition>
    """
    result = translate_xml(xml, SkipCondition)
    expected = "(skip: (const(val(true))))"
    assert result == expected, f"Expected: {expected}\nGot: {result}"


def test_skip_condition_with_variable(translate_xml):
    """Test SkipCondition with variable."""
    xml = """
    <SkipCondition>
        <BooleanVariable>skipFlag</BooleanVariable>
    </SkipCondition>
    """
    result = translate_xml(xml, SkipCondition)
    expected = "(skip: (var('skipFlag)))"
    assert result == expected, f"Expected: {expected}\nGot: {result}"


def test_condition_with_and_expression(translate_xml):
    """Test condition with AND expression."""
    xml = """
    <PreCondition>
        <AND>
            <BooleanVariable>flag1</BooleanVariable>
            <BooleanVariable>flag2</BooleanVariable>
        </AND>
    </PreCondition>
    """
    result = translate_xml(xml, PreCondition)
    expected = "(pre: (_and_(var('flag1),var('flag2))))"
    assert result == expected, f"Expected: {expected}\nGot: {result}"


def test_condition_with_or_expression(translate_xml):
    """Test condition with OR expression."""
    xml = """
    <PostCondition>
        <OR>
            <BooleanValue>true</BooleanValue>
            <BooleanVariable>errorFlag</BooleanVariable>
        </OR>
    </PostCondition>
    """
    result = translate_xml(xml, PostCondition)
    expected = "(post: (_or_(const(val(true)),var('errorFlag))))"
    assert result == expected, f"Expected: {expected}\nGot: {result}"


def test_condition_with_not_expression(translate_xml):
    """Test condition with NOT expression."""
    xml = """
    <InvariantCondition>
        <NOT>
            <BooleanVariable>errorFlag</BooleanVariable>
        </NOT>
    </InvariantCondition>
    """
    result = translate_xml(xml, InvariantCondition)
    expected = "(inv: (not_(var('errorFlag))))"
    assert result == expected, f"Expected: {expected}\nGot: {result}"
