import pytest
from plexil.core.v1.ast import Concat, Strlen

# ====================
# Concat Tests
# ====================


def test_concat_two_strings(translate_xml):
    """Test concatenation of two string values."""
    xml = """<Concat>
      <StringValue>Hello</StringValue>
      <StringValue>World</StringValue>
    </Concat>"""
    assert translate_xml(xml, Concat) == '_+_(const(val("Hello")),const(val("World")))'


def test_concat_string_and_variable(translate_xml):
    """Test concatenation of string value and variable."""
    xml = """<Concat>
      <StringValue>Name: </StringValue>
      <StringVariable>name</StringVariable>
    </Concat>"""
    assert translate_xml(xml, Concat) == '_+_(const(val("Name: ")),var(\'name))'


def test_concat_multiple_strings(translate_xml):
    """Test concatenation of multiple strings - nested binary operations."""
    xml = """<Concat>
      <StringValue>First</StringValue>
      <StringValue>Second</StringValue>
      <StringValue>Third</StringValue>
    </Concat>"""
    assert (
        translate_xml(xml, Concat)
        == '_+_(_+_(const(val("First")),const(val("Second"))),const(val("Third")))'
    )


def test_concat_with_lookup(translate_xml):
    """Test concatenation with lookup expression."""
    xml = """<Concat>
      <StringValue>Prefix_</StringValue>
      <LookupNow>
        <Name>
          <StringValue>suffix</StringValue>
        </Name>
      </LookupNow>
    </Concat>"""
    assert (
        translate_xml(xml, Concat)
        == '_+_(const(val("Prefix_")),lookup(\'suffix,(nilpar)))'
    )


# ====================
# Integration Test - command5 Acceptance Test Pattern
# ====================


def test_concat_in_command_arguments(translate_xml):
    """Test the exact pattern from command5.plx acceptance test.

    This ensures that Concat expressions work correctly as command arguments,
    translating string concatenation to the + operator.
    """
    xml = """<Command>
      <Name><StringValue>foo</StringValue></Name>
      <Arguments>
        <Concat>
          <StringValue>Test</StringValue>
          <StringValue>Arg</StringValue>
        </Concat>
      </Arguments>
    </Command>"""
    from plexil.core.v1.ast import Command

    result = translate_xml(xml, Command)
    # Should have the command name and concatenated arguments
    assert "('foo" in result
    assert '_+_(const(val("Test")),const(val("Arg")))' in result
    assert result == '(\'foo / (_+_(const(val("Test")),const(val("Arg")))) / nothing)'


# ====================
# Strlen Tests (Unsupported)
# ====================


def test_strlen_with_string_value_raises_error(translate_xml):
    xml = """<Strlen>
      <StringValue>test</StringValue>
    </Strlen>"""
    with pytest.raises(
        NotImplementedError, match="String length.*not.*supported.*PLEXIL-V"
    ):
        translate_xml(xml, Strlen)


def test_strlen_with_string_variable_raises_error(translate_xml):
    xml = """<Strlen>
      <StringVariable>myString</StringVariable>
    </Strlen>"""
    with pytest.raises(
        NotImplementedError, match="String length.*not.*supported.*PLEXIL-V"
    ):
        translate_xml(xml, Strlen)


def test_strlen_with_concat_raises_error(translate_xml):
    xml = """<Strlen>
      <Concat>
        <StringValue>Hello</StringValue>
        <StringValue>World</StringValue>
      </Concat>
    </Strlen>"""
    with pytest.raises(
        NotImplementedError, match="String length.*not.*supported.*PLEXIL-V"
    ):
        translate_xml(xml, Strlen)


def test_strlen_with_lookup_raises_error(translate_xml):
    xml = """<Strlen>
      <LookupNow>
        <Name>
          <StringValue>stringState</StringValue>
        </Name>
      </LookupNow>
    </Strlen>"""
    with pytest.raises(
        NotImplementedError, match="String length.*not.*supported.*PLEXIL-V"
    ):
        translate_xml(xml, Strlen)
