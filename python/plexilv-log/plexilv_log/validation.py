"""Log validation framework for plexilv-log tools."""

from dataclasses import dataclass
from enum import Enum
from typing import List


class ValidationLevel(Enum):
    """Validation strictness levels."""
    LENIENT = "lenient"  # Parse what you can, ignore validation errors
    STRICT = "strict"     # Fail on any structural issues or error entries


class LogValidationError(Exception):
    """Raised when log validation fails in strict mode."""
    pass


@dataclass
class ValidationResult:
    """Result of log validation."""
    is_valid: bool
    errors: List[str]
    warnings: List[str]


def validate_log_content(content: str, log_type: str) -> ValidationResult:
    """
    Validate log content before parsing.

    Args:
        content: Raw log content
        log_type: 'plexil' for PLEXIL Executive logs, 'maude' for Maude logs

    Returns:
        ValidationResult with any errors/warnings found
    """
    errors = []
    warnings = []

    # Check for empty content
    if not content or not content.strip():
        errors.append("Log file is empty")
        return ValidationResult(False, errors, warnings)

    # Check for ERROR/WARNING entries (plexiltest logs)
    if log_type == 'plexil':
        lines = content.split('\n')

        # ERROR entries cause validation failure
        error_lines = [i for i, line in enumerate(lines, 1)
                      if line.strip().startswith('ERROR:')]
        if error_lines:
            # Show first 5 line numbers
            line_nums = ', '.join(str(n) for n in error_lines[:5])
            if len(error_lines) > 5:
                line_nums += f', ... ({len(error_lines)} total)'
            errors.append(f"Log contains ERROR entries at lines: {line_nums}")

        # WARNING entries also cause validation failure (user confirmed)
        warning_lines = [i for i, line in enumerate(lines, 1)
                        if line.strip().startswith('WARNING:')]
        if warning_lines:
            line_nums = ', '.join(str(n) for n in warning_lines[:5])
            if len(warning_lines) > 5:
                line_nums += f', ... ({len(warning_lines)} total)'
            errors.append(f"Log contains WARNING entries at lines: {line_nums}")

    # Check for structural markers (minimum requirement)
    # User confirmed: Just need structure markers, can be empty of transitions
    if log_type == 'plexil':
        # PLEXIL Executive logs must have cycle markers
        if '==>Start cycle' not in content and '==>End cycle' not in content:
            errors.append(
                "Log contains no cycle markers (==>Start cycle / ==>End cycle). "
                "This may indicate the executive did not run or the log is truncated."
            )
    elif log_type == 'maude':
        # Maude logs must have MACRO markers at start of line
        import re
        if not re.search(r'^MACRO$', content, re.MULTILINE):
            errors.append(
                "Log contains no MACRO markers. "
                "This may indicate no execution occurred or the log is malformed."
            )

    is_valid = len(errors) == 0
    return ValidationResult(is_valid, errors, warnings)
