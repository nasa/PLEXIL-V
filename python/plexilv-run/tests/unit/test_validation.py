"""Unit tests for validation functions."""

import os
import sys
from pathlib import Path
from unittest.mock import patch

import pytest

from plexilv_run.exceptions import ValidationError
from plexilv_run.validation import (
    validate_file_extension,
    validate_file_readable,
    validate_plan_file,
    validate_plexil_identifier,
    validate_script_file,
)


@pytest.mark.unit
class TestValidatePlexilIdentifier:
    """Test PLEXIL identifier validation."""

    def test_valid_simple_name(self):
        """Valid identifier: simple name."""
        validate_plexil_identifier("MyPlan")  # Should not raise

    def test_valid_with_numbers(self):
        """Valid identifier: with numbers."""
        validate_plexil_identifier("Plan123")  # Should not raise

    def test_valid_with_underscores(self):
        """Valid identifier: with underscores."""
        validate_plexil_identifier("test_plan_01")  # Should not raise

    def test_valid_single_letter(self):
        """Valid identifier: single letter."""
        validate_plexil_identifier("A")  # Should not raise

    def test_valid_mixed_case(self):
        """Valid identifier: mixed case."""
        validate_plexil_identifier("MyTest_Plan_123")  # Should not raise

    def test_invalid_starts_with_number(self):
        """Invalid identifier: starts with number."""
        with pytest.raises(ValidationError, match="Start with a letter"):
            validate_plexil_identifier("123Plan")

    def test_invalid_starts_with_underscore(self):
        """Invalid identifier: starts with underscore."""
        with pytest.raises(ValidationError, match="Start with a letter"):
            validate_plexil_identifier("_plan")

    def test_invalid_contains_dash(self):
        """Invalid identifier: contains dash."""
        with pytest.raises(ValidationError, match="Contain only letters, numbers, and underscores"):
            validate_plexil_identifier("my-plan")

    def test_invalid_contains_space(self):
        """Invalid identifier: contains space."""
        with pytest.raises(ValidationError, match="Contain only letters, numbers, and underscores"):
            validate_plexil_identifier("my plan")

    def test_invalid_contains_dot(self):
        """Invalid identifier: contains dot."""
        with pytest.raises(ValidationError, match="Contain only letters, numbers, and underscores"):
            validate_plexil_identifier("my.plan")

    def test_invalid_empty(self):
        """Invalid identifier: empty string."""
        with pytest.raises(ValidationError, match="cannot be empty"):
            validate_plexil_identifier("")

    def test_invalid_special_characters(self):
        """Invalid identifier: special characters."""
        with pytest.raises(ValidationError):
            validate_plexil_identifier("plan@test")

    def test_error_message_includes_examples(self):
        """Error message should include examples of valid names."""
        with pytest.raises(ValidationError, match="MyPlan.plx"):
            validate_plexil_identifier("bad-name")


@pytest.mark.unit
class TestValidateFileExtension:
    """Test file extension validation."""

    def test_valid_extension(self, tmp_path):
        """File with correct extension should not raise."""
        path = tmp_path / "test.plx"
        path.touch()
        validate_file_extension(path, ".plx", "Plan")  # Should not raise

    def test_invalid_extension(self, tmp_path):
        """File with wrong extension should raise."""
        path = tmp_path / "test.xml"
        path.touch()
        with pytest.raises(ValidationError, match="must have .plx extension"):
            validate_file_extension(path, ".plx", "Plan")

    def test_no_extension(self, tmp_path):
        """File without extension should raise."""
        path = tmp_path / "test"
        path.touch()
        with pytest.raises(ValidationError, match="must have .plx extension"):
            validate_file_extension(path, ".plx", "Plan")

    def test_case_sensitive(self, tmp_path):
        """Extension check should be case-sensitive."""
        path = tmp_path / "test.PLX"
        path.touch()
        with pytest.raises(ValidationError):
            validate_file_extension(path, ".plx", "Plan")

    def test_error_message_includes_filename(self, tmp_path):
        """Error message should include the actual filename."""
        path = tmp_path / "myfile.xml"
        path.touch()
        with pytest.raises(ValidationError, match="myfile.xml"):
            validate_file_extension(path, ".plx", "Plan")


@pytest.mark.unit
class TestValidateFileReadable:
    """Test file readability validation."""

    def test_readable_file(self, tmp_path):
        """Readable file should not raise."""
        path = tmp_path / "test.plx"
        path.touch()
        validate_file_readable(path, "Plan")  # Should not raise

    def test_unreadable_file(self, tmp_path):
        """Unreadable file should raise."""
        path = tmp_path / "test.plx"
        path.touch()

        with patch('plexilv_run.validation.os.access', return_value=False):
            with pytest.raises(ValidationError, match="permission denied"):
                validate_file_readable(path, "Plan")

    def test_error_message_includes_path(self, tmp_path):
        """Error message should include the file path."""
        path = tmp_path / "test.plx"
        path.touch()

        with patch('plexilv_run.validation.os.access', return_value=False):
            with pytest.raises(ValidationError, match=str(path)):
                validate_file_readable(path, "Plan")


@pytest.mark.unit
class TestValidatePlanFile:
    """Test plan file validation."""

    def test_valid_plan_file(self, tmp_path):
        """Valid plan file should not raise."""
        path = tmp_path / "MyPlan.plx"
        path.touch()
        validate_plan_file(path)  # Should not raise

    def test_valid_plan_with_underscores(self, tmp_path):
        """Valid plan file with underscores should not raise."""
        path = tmp_path / "test_plan_01.plx"
        path.touch()
        validate_plan_file(path)  # Should not raise

    def test_invalid_extension(self, tmp_path):
        """Plan file with wrong extension should raise."""
        path = tmp_path / "MyPlan.xml"
        path.touch()
        with pytest.raises(ValidationError, match="must have .plx extension"):
            validate_plan_file(path)

    def test_invalid_identifier(self, tmp_path):
        """Plan file with invalid identifier should raise."""
        path = tmp_path / "my-plan.plx"
        path.touch()
        with pytest.raises(ValidationError, match="Invalid plan filename"):
            validate_plan_file(path)

    def test_unreadable_file(self, tmp_path):
        """Unreadable plan file should raise."""
        path = tmp_path / "MyPlan.plx"
        path.touch()

        with patch('plexilv_run.validation.os.access', return_value=False):
            with pytest.raises(ValidationError, match="permission denied"):
                validate_plan_file(path)

    def test_identifier_starting_with_number(self, tmp_path):
        """Plan filename starting with number should raise."""
        path = tmp_path / "123Plan.plx"
        path.touch()
        with pytest.raises(ValidationError, match="Start with a letter"):
            validate_plan_file(path)


@pytest.mark.unit
class TestValidateScriptFile:
    """Test script file validation."""

    def test_valid_script_file(self, tmp_path):
        """Valid script file should not raise."""
        path = tmp_path / "test_script.psx"
        path.touch()
        validate_script_file(path)  # Should not raise

    def test_valid_script_any_name(self, tmp_path):
        """Script file can have any valid filename (no identifier check)."""
        path = tmp_path / "my-script.psx"
        path.touch()
        validate_script_file(path)  # Should not raise (dashes allowed for scripts)

    def test_invalid_extension(self, tmp_path):
        """Script file with wrong extension should raise."""
        path = tmp_path / "test_script.xml"
        path.touch()
        with pytest.raises(ValidationError, match="must have .psx extension"):
            validate_script_file(path)

    def test_unreadable_file(self, tmp_path):
        """Unreadable script file should raise."""
        path = tmp_path / "test_script.psx"
        path.touch()

        with patch('plexilv_run.validation.os.access', return_value=False):
            with pytest.raises(ValidationError, match="permission denied"):
                validate_script_file(path)