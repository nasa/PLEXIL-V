"""Constants and exceptions for PLEXIL to PLEXIL-V translation.

This module defines exceptions and placeholder strings used during transpilation.
"""


class TranspilationError(Exception):
    """Base exception for transpilation errors.

    Raised when the transpiler encounters invalid, unsupported, or malformed
    PLEXIL constructs that cannot be translated to PLEXIL-V format.
    """

    pass


# Placeholder for unknown or incomplete elements
# Used when the transpiler encounters elements that need further implementation
UNKNOWN = "unknown"
