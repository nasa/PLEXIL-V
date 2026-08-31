"""Tests for string value escaping.

These tests verify that special characters in string values are properly
escaped in the PLEXIL-V output format.
"""

import pytest
from plexil.core.v1.ast import StringValue, Command, Node, DeclareVariable, DeclareArray
from tests.conftest import normalize_whitespace


def test_string_with_newlines(translate_xml):
    """Test that newlines in strings are escaped as \\n."""
    xml = """
    <StringValue>Line 1
Line 2
Line 3</StringValue>
    """
    result = translate_xml(xml, StringValue)
    assert result == 'const(val("Line 1\\nLine 2\\nLine 3"))'
    # Should NOT contain literal newlines
    assert "\n" not in result.split("(")[2].split(")")[0]


def test_string_with_tabs(translate_xml):
    """Test that tabs in strings are escaped as \\t."""
    xml = """
    <StringValue>Column1	Column2	Column3</StringValue>
    """
    result = translate_xml(xml, StringValue)
    assert result == 'const(val("Column1\\tColumn2\\tColumn3"))'
    # Should NOT contain literal tabs
    assert "\t" not in result


def test_string_with_double_quotes(translate_xml):
    """Test that double quotes in strings are escaped as \\"."""
    xml = """
    <StringValue>He said "Hello"</StringValue>
    """
    result = translate_xml(xml, StringValue)
    assert result == 'const(val("He said \\"Hello\\""))'


def test_string_with_backslashes(translate_xml):
    """Test that backslashes in strings are escaped as \\\\."""
    xml = """
    <StringValue>C:\\Users\\Documents\\file.txt</StringValue>
    """
    result = translate_xml(xml, StringValue)
    assert result == 'const(val("C:\\\\Users\\\\Documents\\\\file.txt"))'


def test_string_with_carriage_return(translate_xml):
    """Test that carriage returns in strings are escaped as \\r."""
    xml = """
    <StringValue>Line 1&#13;Line 2</StringValue>
    """
    result = translate_xml(xml, StringValue)
    assert result == 'const(val("Line 1\\rLine 2"))'


def test_string_with_mixed_special_characters(translate_xml):
    """Test string with multiple types of special characters."""
    xml = """
    <StringValue>Path: "C:\\temp"
	Value: 42
End</StringValue>
    """
    result = translate_xml(xml, StringValue)
    # Should escape quotes, backslashes, newlines, and tabs
    assert '\\"' in normalize_whitespace(result)  # Escaped quotes
    assert "\\\\" in normalize_whitespace(result)  # Escaped backslashes
    assert "\\n" in normalize_whitespace(result)  # Escaped newlines
    assert "\\t" in normalize_whitespace(result)  # Escaped tabs
    # Should NOT contain literal special characters
    assert "\n" not in result.split('val("')[1].split('")')[0]


def test_empty_string(translate_xml):
    """Test that empty strings are handled correctly."""
    xml = """
    <StringValue></StringValue>
    """
    result = translate_xml(xml, StringValue)
    assert result == 'const(val(""))'


def test_string_in_command_argument(translate_xml):
    """Test that strings in command arguments are properly escaped."""
    xml = """
    <Command>
        <Name>
            <StringValue>print</StringValue>
        </Name>
        <Arguments>
            <StringValue>Line 1
Line 2</StringValue>
        </Arguments>
    </Command>
    """
    result = translate_xml(xml, Command)
    # Command arguments should have const wrapper and escaped newlines
    assert 'const(val("Line 1\\nLine 2"))' in normalize_whitespace(result)
    # Verify no literal newlines in the string value
    assert '("Line 1\\nLine 2")' in normalize_whitespace(result)


def test_string_in_variable_declaration(translate_xml):
    """Test that strings in variable declarations are properly escaped."""
    xml = """
    <DeclareVariable>
        <Name>message</Name>
        <Type>String</Type>
        <InitialValue>
            <StringValue>Hello
World</StringValue>
        </InitialValue>
    </DeclareVariable>
    """
    result = translate_xml(xml, DeclareVariable)
    assert '(\'message : val("Hello\\nWorld"))' in result
    # Should NOT contain literal newlines
    assert result.count("\n") == 0


def test_string_in_array_declaration(translate_xml):
    """Test that strings in array initial values are properly escaped."""
    xml = """
    <DeclareArray>
        <Name>messages</Name>
        <Type>String</Type>
        <MaxSize>3</MaxSize>
        <InitialValue>
            <ArrayValue Type="String">
                <StringValue>Line 1</StringValue>
                <StringValue>Line	2</StringValue>
                <StringValue>"Quote"</StringValue>
            </ArrayValue>
        </InitialValue>
    </DeclareArray>
    """
    result = translate_xml(xml, DeclareArray)
    # Should have escaped tab in second element
    assert 'val("Line\\t2")' in normalize_whitespace(result)
    # Should have escaped quotes in third element
    assert 'val("\\"Quote\\"")' in normalize_whitespace(result)


def test_print_acceptance_pattern(translate_xml):
    """Test the pattern from the print acceptance test."""
    xml = """
    <Node NodeType="Command">
        <NodeId>COMMAND__0</NodeId>
        <NodeBody>
            <Command>
                <Name>
                    <StringValue>print</StringValue>
                </Name>
                <Arguments>
                    <StringValue>

THIS IS THE MESSAGE

</StringValue>
                </Arguments>
            </Command>
        </NodeBody>
    </Node>
    """
    result = translate_xml(xml, Node)
    # Should match Haskell format with escaped newlines
    assert 'const(val("\\n\\nTHIS IS THE MESSAGE\\n\\n"))' in normalize_whitespace(result)
    # The command should be properly formatted
    assert (
        "command('COMMAND__0,nilocdecl,(none),(('print)/(const(val(\"\\n\\nTHIS IS THE MESSAGE\\n\\n\")))/nothing))"
        in normalize_whitespace(result)
    )


def test_string_with_only_newline(translate_xml):
    """Test string that contains only a newline."""
    xml = """
    <StringValue>
</StringValue>
    """
    result = translate_xml(xml, StringValue)
    assert result == 'const(val("\\n"))'


def test_string_with_multiple_consecutive_newlines(translate_xml):
    """Test string with multiple consecutive newlines."""
    xml = """
    <StringValue>


</StringValue>
    """
    result = translate_xml(xml, StringValue)
    assert result == 'const(val("\\n\\n\\n"))'


def test_string_without_special_characters(translate_xml):
    """Test that normal strings without special characters are unchanged."""
    xml = """
    <StringValue>Hello World</StringValue>
    """
    result = translate_xml(xml, StringValue)
    assert result == 'const(val("Hello World"))'


def test_string_with_all_escapable_characters(translate_xml):
    """Test string containing all types of escapable characters."""
    xml = r"""
    <StringValue>Backslash: \ Quote: " Newline:
Tab:	End</StringValue>
    """
    result = translate_xml(xml, StringValue)
    # Should escape all special characters
    assert "\\\\" in normalize_whitespace(result)  # Backslash
    assert '\\"' in normalize_whitespace(result)  # Quote
    assert "\\n" in normalize_whitespace(result)  # Newline
    assert "\\t" in normalize_whitespace(result)  # Tab
