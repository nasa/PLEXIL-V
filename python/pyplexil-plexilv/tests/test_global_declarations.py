"""Tests for Global Declarations.

Global declarations (CommandDeclaration, StateDeclaration, LibraryNodeDeclaration)
are not supported in the PLEXIL-V Maude format, as interface specifications are not
needed for verification. These tests verify the expected behavior: empty string output
with a warning issued when global declarations are encountered.

See: plexilv/plexil/translator/handlers/declarations.py for implementation details.
"""

import pytest
from plexil.core.v1.ast import (
    GlobalDeclarations,
    CommandDeclaration,
    StateDeclaration,
    LibraryNodeDeclaration,
)


def test_command_declaration_no_params_no_return(translate_xml):
    """Test CommandDeclaration with no parameters and no return value."""
    xml = """
    <CommandDeclaration>
        <Name>print</Name>
    </CommandDeclaration>
    """
    result = translate_xml(xml, CommandDeclaration)
    expected = ""
    assert result == expected, f"Expected: {expected}\nGot: {result}"


def test_command_declaration_with_params_no_return(translate_xml):
    """Test CommandDeclaration with parameters but no return value."""
    xml = """
    <CommandDeclaration>
        <Name>move</Name>
        <Parameter>
            <Type>Real</Type>
        </Parameter>
        <Parameter>
            <Type>Real</Type>
        </Parameter>
    </CommandDeclaration>
    """
    result = translate_xml(xml, CommandDeclaration)
    expected = ""
    assert result == expected, f"Expected: {expected}\nGot: {result}"


def test_command_declaration_with_named_params(translate_xml):
    """Test CommandDeclaration with named parameters."""
    xml = """
    <CommandDeclaration>
        <Name>setSpeed</Name>
        <Parameter>
            <Name>velocity</Name>
            <Type>Real</Type>
        </Parameter>
    </CommandDeclaration>
    """
    result = translate_xml(xml, CommandDeclaration)
    expected = ""
    assert result == expected, f"Expected: {expected}\nGot: {result}"


def test_command_declaration_with_return(translate_xml):
    """Test CommandDeclaration with return value."""
    xml = """
    <CommandDeclaration>
        <Name>getTemperature</Name>
        <Return>
            <Type>Real</Type>
        </Return>
    </CommandDeclaration>
    """
    result = translate_xml(xml, CommandDeclaration)
    expected = ""
    assert result == expected, f"Expected: {expected}\nGot: {result}"


def test_command_declaration_with_params_and_return(translate_xml):
    """Test CommandDeclaration with parameters and return value."""
    xml = """
    <CommandDeclaration>
        <Name>calculate</Name>
        <Parameter>
            <Type>Integer</Type>
        </Parameter>
        <Parameter>
            <Type>Integer</Type>
        </Parameter>
        <Return>
            <Type>Integer</Type>
        </Return>
    </CommandDeclaration>
    """
    result = translate_xml(xml, CommandDeclaration)
    expected = ""
    assert result == expected, f"Expected: {expected}\nGot: {result}"


def test_state_declaration_no_params(translate_xml):
    """Test StateDeclaration with no parameters."""
    xml = """
    <StateDeclaration>
        <Name>time</Name>
        <Return>
            <Type>Real</Type>
        </Return>
    </StateDeclaration>
    """
    result = translate_xml(xml, StateDeclaration)
    expected = ""
    assert result == expected, f"Expected: {expected}\nGot: {result}"


def test_state_declaration_with_params(translate_xml):
    """Test StateDeclaration with parameters."""
    xml = """
    <StateDeclaration>
        <Name>position</Name>
        <Parameter>
            <Type>Integer</Type>
        </Parameter>
        <Return>
            <Type>Real</Type>
        </Return>
    </StateDeclaration>
    """
    result = translate_xml(xml, StateDeclaration)
    expected = ""
    assert result == expected, f"Expected: {expected}\nGot: {result}"


def test_state_declaration_with_named_params(translate_xml):
    """Test StateDeclaration with named parameters."""
    xml = """
    <StateDeclaration>
        <Name>sensorValue</Name>
        <Parameter>
            <Name>sensorId</Name>
            <Type>Integer</Type>
        </Parameter>
        <Return>
            <Type>Real</Type>
        </Return>
    </StateDeclaration>
    """
    result = translate_xml(xml, StateDeclaration)
    expected = ""
    assert result == expected, f"Expected: {expected}\nGot: {result}"


def test_library_node_declaration_simple(translate_xml):
    """Test LibraryNodeDeclaration with just a name."""
    xml = """
    <LibraryNodeDeclaration>
        <Name>SafeDrive</Name>
    </LibraryNodeDeclaration>
    """
    result = translate_xml(xml, LibraryNodeDeclaration)
    expected = ""
    assert result == expected, f"Expected: {expected}\nGot: {result}"


def test_library_node_declaration_with_interface(translate_xml):
    """Test LibraryNodeDeclaration with interface."""
    xml = """
    <LibraryNodeDeclaration>
        <Name>Navigate</Name>
        <Interface>
            <In>
                <DeclareVariable>
                    <Name>targetX</Name>
                    <Type>Real</Type>
                </DeclareVariable>
            </In>
        </Interface>
    </LibraryNodeDeclaration>
    """
    result = translate_xml(xml, LibraryNodeDeclaration)
    expected = ""
    assert result == expected, f"Expected: {expected}\nGot: {result}"


def test_global_declarations_empty(translate_xml):
    """Test empty GlobalDeclarations."""
    xml = """
    <GlobalDeclarations>
    </GlobalDeclarations>
    """
    result = translate_xml(xml, GlobalDeclarations)
    expected = ""
    assert result == expected, f"Expected: {expected}\nGot: {result}"


def test_global_declarations_with_command(translate_xml):
    """Test GlobalDeclarations with CommandDeclaration."""
    xml = """
    <GlobalDeclarations>
        <CommandDeclaration>
            <Name>print</Name>
        </CommandDeclaration>
    </GlobalDeclarations>
    """
    result = translate_xml(xml, GlobalDeclarations)
    expected = ""
    assert result == expected, f"Expected: {expected}\nGot: {result}"


def test_global_declarations_with_state(translate_xml):
    """Test GlobalDeclarations with StateDeclaration."""
    xml = """
    <GlobalDeclarations>
        <StateDeclaration>
            <Name>time</Name>
            <Return>
                <Type>Real</Type>
            </Return>
        </StateDeclaration>
    </GlobalDeclarations>
    """
    result = translate_xml(xml, GlobalDeclarations)
    expected = ""
    assert result == expected, f"Expected: {expected}\nGot: {result}"


def test_global_declarations_with_library_node(translate_xml):
    """Test GlobalDeclarations with LibraryNodeDeclaration."""
    xml = """
    <GlobalDeclarations>
        <LibraryNodeDeclaration>
            <Name>SafeDrive</Name>
        </LibraryNodeDeclaration>
    </GlobalDeclarations>
    """
    result = translate_xml(xml, GlobalDeclarations)
    expected = ""
    assert result == expected, f"Expected: {expected}\nGot: {result}"


def test_global_declarations_mixed(translate_xml):
    """Test GlobalDeclarations with mixed declaration types."""
    xml = """
    <GlobalDeclarations>
        <CommandDeclaration>
            <Name>print</Name>
        </CommandDeclaration>
        <StateDeclaration>
            <Name>time</Name>
            <Return>
                <Type>Real</Type>
            </Return>
        </StateDeclaration>
        <LibraryNodeDeclaration>
            <Name>SafeDrive</Name>
        </LibraryNodeDeclaration>
    </GlobalDeclarations>
    """
    result = translate_xml(xml, GlobalDeclarations)
    expected = ""
    assert result == expected, f"Expected: {expected}\nGot: {result}"
