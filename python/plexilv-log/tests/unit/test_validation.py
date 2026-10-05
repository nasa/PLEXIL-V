"""Unit tests for log validation."""

import pytest
from plexilv_log.validation import (
    validate_log_content,
    ValidationLevel,
    LogValidationError,
    ValidationResult,
)


class TestValidationResult:
    """Test ValidationResult dataclass."""

    def test_valid_result(self):
        """Valid result has no errors."""
        result = ValidationResult(True, [], [])
        assert result.is_valid
        assert len(result.errors) == 0
        assert len(result.warnings) == 0

    def test_invalid_result(self):
        """Invalid result has errors."""
        result = ValidationResult(False, ["Error 1", "Error 2"], [])
        assert not result.is_valid
        assert len(result.errors) == 2


class TestPlexilLogValidation:
    """Test validation of PLEXIL Executive logs."""

    def test_empty_log_fails(self):
        """Empty logs should fail validation."""
        result = validate_log_content("", "plexil")
        assert not result.is_valid
        assert "empty" in result.errors[0].lower()

    def test_whitespace_only_log_fails(self):
        """Whitespace-only logs should fail validation."""
        result = validate_log_content("   \n  \n  ", "plexil")
        assert not result.is_valid
        assert "empty" in result.errors[0].lower()

    def test_error_entries_fail(self):
        """Logs with ERROR entries should fail."""
        content = """
Running executive from /path/to/plexil
ERROR: Node test: In interface variable "x" not found
WARNING: Some warning
==>Start cycle 1
==>End cycle 1
"""
        result = validate_log_content(content, "plexil")
        assert not result.is_valid
        assert any("ERROR entries" in err for err in result.errors)
        assert "8" in result.errors[0] or "3" in result.errors[0]  # Line number

    def test_warning_entries_fail(self):
        """Logs with WARNING entries should fail (user confirmed)."""
        content = """
Running executive from /path/to/plexil
WARNING: Some warning message
==>Start cycle 1
==>End cycle 1
"""
        result = validate_log_content(content, "plexil")
        assert not result.is_valid
        assert any("WARNING entries" in err for err in result.errors)

    def test_both_error_and_warning_fail(self):
        """Logs with both ERROR and WARNING should report both."""
        content = """
Running executive from /path/to/plexil
ERROR: Node test: variable not found
WARNING: Error parsing plan
==>Start cycle 1
==>End cycle 1
"""
        result = validate_log_content(content, "plexil")
        assert not result.is_valid
        assert len(result.errors) >= 2
        assert any("ERROR entries" in err for err in result.errors)
        assert any("WARNING entries" in err for err in result.errors)

    def test_no_cycle_markers_fails(self):
        """Logs with no cycle markers should fail."""
        content = """
Running executive from /path/to/plexil
Some random content
Node transitions would be here
"""
        result = validate_log_content(content, "plexil")
        assert not result.is_valid
        assert any("no cycle markers" in err for err in result.errors)

    def test_only_start_cycle_passes(self):
        """Logs with just Start cycle marker should pass (minimum structure)."""
        content = """
Running executive from /path/to/plexil
==>Start cycle 1
"""
        result = validate_log_content(content, "plexil")
        assert result.is_valid

    def test_only_end_cycle_passes(self):
        """Logs with just End cycle marker should pass (minimum structure)."""
        content = """
Running executive from /path/to/plexil
==>End cycle 1
"""
        result = validate_log_content(content, "plexil")
        assert result.is_valid

    def test_empty_cycles_valid(self):
        """Logs with cycle markers but no transitions are valid."""
        content = """
Running executive from /path/to/plexil
==>Start cycle 1
==>End cycle 1
==>Start cycle 2
==>End cycle 2
"""
        result = validate_log_content(content, "plexil")
        assert result.is_valid
        assert len(result.errors) == 0

    def test_valid_plexil_log_passes(self):
        """Valid PLEXIL logs should pass."""
        content = """
Running executive from /path/to/plexil
  Plan:           test.plx
==>Start cycle 1
[PlexilExec:step][1:0:0] Transitioning NodeList node test from INACTIVE to WAITING
==>End cycle 1
==>Start cycle 2
[PlexilExec:step][2:0:0] Transitioning NodeList node test from WAITING to EXECUTING
==>End cycle 2
"""
        result = validate_log_content(content, "plexil")
        assert result.is_valid
        assert len(result.errors) == 0

    def test_multiple_error_lines_shown(self):
        """Multiple ERROR lines should be reported."""
        content = """
Running executive from /path/to/plexil
ERROR: First error
ERROR: Second error
ERROR: Third error
==>Start cycle 1
==>End cycle 1
"""
        result = validate_log_content(content, "plexil")
        assert not result.is_valid
        assert "ERROR entries" in result.errors[0]
        # Should show line numbers
        assert "3" in result.errors[0] or "4" in result.errors[0]

    def test_many_errors_truncated(self):
        """More than 5 errors should be truncated in output."""
        errors = "\n".join([f"ERROR: Error {i}" for i in range(10)])
        content = f"""
Running executive from /path/to/plexil
{errors}
==>Start cycle 1
==>End cycle 1
"""
        result = validate_log_content(content, "plexil")
        assert not result.is_valid
        assert "10 total" in result.errors[0]  # Should indicate truncation

    def test_error_case_sensitive(self):
        """ERROR must be uppercase to be detected."""
        content = """
Running executive from /path/to/plexil
error: This should not trigger
Error: This should not trigger
==>Start cycle 1
==>End cycle 1
"""
        result = validate_log_content(content, "plexil")
        assert result.is_valid  # Lowercase/mixed case not detected


class TestMaudeLogValidation:
    """Test validation of Maude logs."""

    def test_empty_log_fails(self):
        """Empty Maude logs should fail."""
        result = validate_log_content("", "maude")
        assert not result.is_valid
        assert "empty" in result.errors[0].lower()

    def test_no_macro_markers_fails(self):
        """Maude logs with no MACRO markers should fail."""
        content = "some random content\nwithout MACRO markers\n"
        result = validate_log_content(content, "maude")
        assert not result.is_valid
        assert any("no MACRO markers" in err for err in result.errors)

    def test_valid_maude_log_passes(self):
        """Valid Maude logs should pass."""
        content = """
MACRO
    'test from inactive to waiting
 micro
    'test from waiting to executing
 micro
"""
        result = validate_log_content(content, "maude")
        assert result.is_valid
        assert len(result.errors) == 0

    def test_macro_with_quiescence_passes(self):
        """Maude logs with MACRO and QuIeScEnCe should pass."""
        content = """
MACRO
    'test from inactive to waiting
 micro
QuIeScEnCe
"""
        result = validate_log_content(content, "maude")
        assert result.is_valid

    def test_just_macro_marker_passes(self):
        """Logs with just MACRO marker should pass (minimum structure)."""
        content = "MACRO\n"
        result = validate_log_content(content, "maude")
        assert result.is_valid

    def test_empty_macro_steps_valid(self):
        """Logs with MACRO markers but no transitions are valid."""
        content = """
MACRO
MACRO
MACRO
"""
        result = validate_log_content(content, "maude")
        assert result.is_valid

    def test_macro_case_sensitive(self):
        """MACRO must be uppercase to be detected."""
        content = "macro\nMacro\n"
        result = validate_log_content(content, "maude")
        assert not result.is_valid
        assert "no MACRO markers" in result.errors[0]


class TestValidationLevelEnum:
    """Test ValidationLevel enum."""

    def test_enum_values(self):
        """Enum should have correct values."""
        assert ValidationLevel.STRICT.value == "strict"
        assert ValidationLevel.LENIENT.value == "lenient"

    def test_enum_members(self):
        """Enum should have exactly two members."""
        assert len(ValidationLevel) == 2
        assert ValidationLevel.STRICT in ValidationLevel
        assert ValidationLevel.LENIENT in ValidationLevel


class TestLogValidationError:
    """Test LogValidationError exception."""

    def test_exception_creation(self):
        """Should be able to create exception with message."""
        error = LogValidationError("Test error message")
        assert str(error) == "Test error message"

    def test_exception_inheritance(self):
        """Should inherit from Exception."""
        error = LogValidationError("Test")
        assert isinstance(error, Exception)
