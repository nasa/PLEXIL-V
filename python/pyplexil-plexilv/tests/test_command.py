"""Tests for Command translation."""

import pytest
from plexil.core.v1.ast import Command


def test_simple_command_no_args_no_return(translate_xml):
    """Test simple command: pprint with no arguments and no return."""
    xml = """
    <Command>
      <Name>
        <StringValue>pprint</StringValue>
      </Name>
    </Command>
    """
    result = translate_xml(xml, Command)
    expected = "('pprint / (nilpar) / nothing)"
    assert result == expected, f"Expected: {expected}\nGot: {result}"


def test_command_with_arguments(translate_xml):
    """Test command with arguments: pprint(\"r:\", r)."""
    xml = """
    <Command>
      <Name>
        <StringValue>pprint</StringValue>
      </Name>
      <Arguments>
        <StringValue>r:</StringValue>
        <RealVariable>r</RealVariable>
      </Arguments>
    </Command>
    """
    result = translate_xml(xml, Command)
    expected = "('pprint / (const(val(\"r:\")) var('r)) / nothing)"
    assert result == expected, f"Expected: {expected}\nGot: {result}"


def test_command_with_return_variable(translate_xml):
    """Test command with return variable: r = get_real()."""
    xml = """
    <Command>
      <RealVariable>r</RealVariable>
      <Name>
        <StringValue>get_real</StringValue>
      </Name>
    </Command>
    """
    result = translate_xml(xml, Command)
    expected = "('get_real / (nilpar) / just('r))"
    assert result == expected, f"Expected: {expected}\nGot: {result}"


def test_command_with_return_and_arguments(translate_xml):
    """Test command with return variable and arguments: r = whatever(\"r:\", r)."""
    xml = """
    <Command>
      <RealVariable>r</RealVariable>
      <Name>
        <StringValue>whatever</StringValue>
      </Name>
      <Arguments>
        <StringValue>r:</StringValue>
        <RealVariable>r</RealVariable>
      </Arguments>
    </Command>
    """
    result = translate_xml(xml, Command)
    expected = "('whatever / (const(val(\"r:\")) var('r)) / just('r))"
    assert result == expected, f"Expected: {expected}\nGot: {result}"


def test_command_with_array_argument(translate_xml):
    """Test command with array variable argument: SetVel(velCmd)."""
    xml = """
    <Command>
      <Name>
        <StringValue>SetVel</StringValue>
      </Name>
      <Arguments>
        <ArrayVariable>velCmd</ArrayVariable>
      </Arguments>
    </Command>
    """
    result = translate_xml(xml, Command)
    expected = "('SetVel / (var('velCmd)) / nothing)"
    assert result == expected, f"Expected: {expected}\nGot: {result}"


def test_command_with_variable_name(translate_xml):
    """Test command with variable name: cmdId(var('CommandName))(\"\")."""
    xml = """
    <Command>
      <Name>
        <StringVariable>CommandName</StringVariable>
      </Name>
      <Arguments>
        <StringValue></StringValue>
      </Arguments>
    </Command>
    """
    result = translate_xml(xml, Command)
    expected = '(cmdId(var(\'CommandName)) / (const(val(""))) / nothing)'
    assert result == expected, f"Expected: {expected}\nGot: {result}"


def test_command_with_multiple_arguments(translate_xml):
    """Test command with multiple arguments: pprint(\"r1:\", r1, \"r2:\", r2)."""
    xml = """
    <Command>
      <Name>
        <StringValue>pprint</StringValue>
      </Name>
      <Arguments>
        <StringValue>r1:</StringValue>
        <RealVariable>r1</RealVariable>
        <StringValue>r2:</StringValue>
        <RealVariable>r2</RealVariable>
      </Arguments>
    </Command>
    """
    result = translate_xml(xml, Command)
    expected = '(\'pprint / (const(val("r1:")) var(\'r1) const(val("r2:")) var(\'r2)) / nothing)'
    assert result == expected, f"Expected: {expected}\nGot: {result}"


def test_command_with_single_variable_argument_and_return(translate_xml):
    """Test command with single variable argument and return: ret = complexCommand(ret)."""
    xml = """
    <Command>
      <RealVariable>ret</RealVariable>
      <Name>
        <StringValue>complexCommand</StringValue>
      </Name>
      <Arguments>
        <RealVariable>ret</RealVariable>
      </Arguments>
    </Command>
    """
    result = translate_xml(xml, Command)
    expected = "('complexCommand / (var('ret)) / just('ret))"
    assert result == expected, f"Expected: {expected}\nGot: {result}"
