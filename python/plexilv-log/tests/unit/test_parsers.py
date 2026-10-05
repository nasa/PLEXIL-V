"""Unit tests for parsers."""

import pytest

from plexilv_log.parsers.plexil_executive import PlexilExecutiveParser
from plexilv_log.parsers.maude import MaudeParser
from plexilv_log.validation import ValidationLevel, LogValidationError
from plexilv_log.models import Trace


def test_plexil_executive_parser_basic(squareroot_plexil_log):
    """Test basic PLEXIL Executive parsing."""
    parser = PlexilExecutiveParser()
    trace = parser.parse(squareroot_plexil_log)

    assert len(trace.macros) >= 1
    assert len(trace.macros[0].micros) >= 1
    assert len(trace.macros[0].micros[0].transitions) >= 1

    # Check first transition
    first_trans = trace.macros[0].micros[0].transitions[0]
    assert first_trans.node_id == "squareRoot"
    assert first_trans.from_state == "inactive"
    assert first_trans.to_state == "waiting"


def test_plexil_executive_parser_state_normalization(squareroot_plexil_log):
    """Test that state names are normalized correctly."""
    parser = PlexilExecutiveParser()
    trace = parser.parse(squareroot_plexil_log)

    # Find transition to ITERATION_ENDED
    found = False
    for macro in trace.macros:
        for micro in macro.micros:
            for trans in micro.transitions:
                if trans.to_state == "iterationEnded":
                    found = True
                    break

    assert found, "Should normalize ITERATION_ENDED to iterationEnded"


def test_plexil_executive_parser_multiple_macros(squareroot_plexil_log):
    """Test parsing multiple macro-steps."""
    parser = PlexilExecutiveParser()
    trace = parser.parse(squareroot_plexil_log)

    # squareRoot test should have at least 3 cycles
    assert len(trace.macros) >= 3


def test_maude_parser_basic(squareroot_maude_log):
    """Test basic Maude parsing."""
    parser = MaudeParser()
    trace = parser.parse(squareroot_maude_log)

    assert len(trace.macros) >= 1
    assert len(trace.macros[0].micros) >= 1

    # Check first transition
    first_trans = trace.macros[0].micros[0].transitions[0]
    assert first_trans.node_id == "squareRoot"
    assert first_trans.from_state == "inactive"
    assert first_trans.to_state == "waiting"


def test_maude_parser_qualified_ids(lookup8_maude_log):
    """Test that qualified IDs are simplified to local names."""
    parser = MaudeParser()
    trace = parser.parse(lookup8_maude_log)

    # Collect all node IDs
    all_node_ids = set()
    for macro in trace.macros:
        for micro in macro.micros:
            for trans in micro.transitions:
                all_node_ids.add(trans.node_id)

    # Should have local names
    assert "node1" in all_node_ids
    assert "node2" in all_node_ids
    assert "node3" in all_node_ids
    assert "lookup8" in all_node_ids

    # Should NOT have qualified paths (no dots in node IDs)
    assert not any('.' in nid for nid in all_node_ids), \
        f"Found qualified paths in node IDs: {[nid for nid in all_node_ids if '.' in nid]}"


def test_maude_parser_multiple_macros(squareroot_maude_log):
    """Test parsing multiple macro-steps."""
    parser = MaudeParser()
    trace = parser.parse(squareroot_maude_log)

    # squareRoot test should have at least 3 macros
    assert len(trace.macros) >= 3


def test_maude_parser_state_normalization(lookup8_maude_log):
    """Test that state names are normalized correctly."""
    parser = MaudeParser()
    trace = parser.parse(lookup8_maude_log)

    # Find transition to iterationEnded
    found = False
    for macro in trace.macros:
        for micro in macro.micros:
            for trans in micro.transitions:
                if trans.to_state == "iterationEnded":
                    found = True
                    break

    assert found, "Should normalize iterationended to iterationEnded"


def test_empty_log():
    """Test parsing empty log in lenient mode."""
    parser = PlexilExecutiveParser()
    trace = parser.parse("", validation_level=ValidationLevel.LENIENT)
    assert len(trace.macros) == 0

    parser = MaudeParser()
    trace = parser.parse("", validation_level=ValidationLevel.LENIENT)
    assert len(trace.macros) == 0


def test_malformed_log():
    """Test parsing malformed log doesn't crash in lenient mode."""
    parser = PlexilExecutiveParser()
    trace = parser.parse("This is not a valid log\nMore garbage\n",
                        validation_level=ValidationLevel.LENIENT)
    # Should return empty or partial trace, not crash
    assert isinstance(trace.macros, list)

    parser = MaudeParser()
    trace = parser.parse("This is not a valid log\nMore garbage\n",
                        validation_level=ValidationLevel.LENIENT)
    assert isinstance(trace.macros, list)


class TestParserValidation:
    """Test parser validation behavior."""

    def test_plexil_parser_raises_on_error_log(self):
        """Parser should raise LogValidationError for logs with ERROR entries."""
        content = """
Running executive from /path/to/plexil
ERROR: Node test: variable not found
WARNING: Error parsing plan
"""
        parser = PlexilExecutiveParser()
        with pytest.raises(LogValidationError) as exc_info:
            parser.parse(content)
        assert "ERROR entries" in str(exc_info.value)

    def test_plexil_parser_lenient_mode_allows_errors(self):
        """Parser in lenient mode should accept logs with errors."""
        content = "ERROR: some error\n"
        parser = PlexilExecutiveParser()
        trace = parser.parse(content, validation_level=ValidationLevel.LENIENT)
        # Should return trace, not raise
        assert isinstance(trace, Trace)

    def test_plexil_parser_empty_log_raises(self):
        """Parser should raise on empty logs in strict mode."""
        parser = PlexilExecutiveParser()
        with pytest.raises(LogValidationError) as exc_info:
            parser.parse("")
        assert "empty" in str(exc_info.value).lower()

    def test_plexil_parser_no_cycles_raises(self):
        """Parser should raise on logs without cycle markers."""
        content = "Running executive\nSome content\n"
        parser = PlexilExecutiveParser()
        with pytest.raises(LogValidationError) as exc_info:
            parser.parse(content)
        assert "cycle markers" in str(exc_info.value)

    def test_maude_parser_empty_log_raises(self):
        """Maude parser should raise on empty logs in strict mode."""
        parser = MaudeParser()
        with pytest.raises(LogValidationError) as exc_info:
            parser.parse("")
        assert "empty" in str(exc_info.value).lower()

    def test_maude_parser_no_macro_raises(self):
        """Maude parser should raise on logs without MACRO markers."""
        content = "some content\nno MACRO here\n"
        parser = MaudeParser()
        with pytest.raises(LogValidationError) as exc_info:
            parser.parse(content)
        assert "MACRO markers" in str(exc_info.value)

    def test_maude_parser_lenient_mode(self):
        """Maude parser in lenient mode should accept empty logs."""
        parser = MaudeParser()
        trace = parser.parse("", validation_level=ValidationLevel.LENIENT)
        assert isinstance(trace, Trace)
        assert len(trace.macros) == 0

    def test_validation_level_default_is_strict(self):
        """Default validation level should be STRICT."""
        content = "ERROR: test\n"
        parser = PlexilExecutiveParser()
        # Should raise without explicit validation_level parameter
        with pytest.raises(LogValidationError):
            parser.parse(content)
