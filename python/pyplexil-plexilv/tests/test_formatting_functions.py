"""Tests for naming convention formatting functions."""

import pytest
from plexilv.plexil.translator.handlers._helpers import format_node_name, format_var_name
from tests.conftest import normalize_whitespace


def test_format_node_name_replaces_underscores():
    """Test that node names preserve underscores."""
    assert format_node_name("my_node") == "my_node"
    assert format_node_name("test_node_123") == "test_node_123"
    assert format_node_name("simple") == "simple"
    assert format_node_name("multiple_under_scores") == "multiple_under_scores"


def test_format_node_name_preserves_hyphens():
    """Test that node names with hyphens are unchanged."""
    assert format_node_name("already-hyphenated") == "already-hyphenated"
    assert format_node_name("my-node-name") == "my-node-name"


def test_format_node_name_empty_string():
    """Test that empty strings are handled."""
    assert format_node_name("") == ""


def test_format_var_name_preserves_underscores():
    """Test that variable names keep their underscores."""
    assert format_var_name("my_var") == "my_var"
    assert format_var_name("test_variable_123") == "test_variable_123"
    assert format_var_name("simple") == "simple"
    assert format_var_name("multiple_under_scores") == "multiple_under_scores"


def test_format_var_name_preserves_hyphens():
    """Test that variable names with hyphens are unchanged (though unusual)."""
    assert format_var_name("my-var") == "my-var"


def test_format_var_name_empty_string():
    """Test that empty strings are handled."""
    assert format_var_name("") == ""


def test_node_vs_var_naming_difference():
    """Test that both node and variable names preserve underscores."""
    # Node names: underscores preserved
    assert format_node_name("my_node") == "my_node"

    # Variable names: underscores preserved
    assert format_var_name("my_var") == "my_var"

    # This documents the PLEXIL-V convention:
    # - Both nodes and variables preserve underscores: 'my_node, 'my_var


def test_formatting_functions_are_idempotent():
    """Test that applying formatting twice gives same result."""
    # Node names (trivially idempotent since it's identity function)
    node_name = "my_node"
    formatted_once = format_node_name(node_name)
    formatted_twice = format_node_name(formatted_once)
    assert formatted_once == formatted_twice == "my_node"

    # Variable names (trivially idempotent since it's identity function)
    var_name = "my_var"
    formatted_once = format_var_name(var_name)
    formatted_twice = format_var_name(formatted_once)
    assert formatted_once == formatted_twice == "my_var"


def test_formatting_in_actual_translation(translate_xml):
    """Test that formatting functions are used correctly in actual translation."""
    # Test with a node that has underscores in the name
    xml = """
    <Node NodeType="Empty">
        <NodeId>test_node_with_underscores</NodeId>
    </Node>
    """

    result = translate_xml(xml, Node)

    # Node name should preserve underscores
    assert "empty('test_node_with_underscores" in normalize_whitespace(result)
    # Should NOT convert underscores to hyphens
    assert "test-node-with-underscores" not in result


def test_variable_names_keep_underscores(translate_xml):
    """Test that variable names in output preserve underscores."""
    xml = """
    <Node NodeType="Assignment">
        <NodeId>TestNode</NodeId>
        <NodeBody>
            <Assignment>
                <IntegerVariable>my_test_var</IntegerVariable>
                <NumericRHS><IntegerValue>42</IntegerValue></NumericRHS>
            </Assignment>
        </NodeBody>
    </Node>
    """

    result = translate_xml(xml, Node)

    # Variable name should keep underscores
    assert "var('my_test_var)" in normalize_whitespace(result)
    # Should NOT have hyphens in variable name
    assert "my-test-var" not in result


# Import Node at the end to avoid issues with fixtures
from plexil.core.v1 import Node
