"""Pytest configuration and fixtures."""

import pytest
from pathlib import Path

# Path to acceptance test logs
ACCEPTANCE_TESTS = Path(__file__).parent.parent.parent.parent / "semantics/test/acceptance/tests"


@pytest.fixture
def squareroot_plexil_log():
    """Load squareRoot PLEXIL Executive log."""
    log_file = ACCEPTANCE_TESTS / "squareRoot" / "output.plexil"
    if not log_file.exists():
        pytest.skip(f"Log file not found: {log_file}")
    return log_file.read_text()


@pytest.fixture
def squareroot_maude_log():
    """Load squareRoot Maude log."""
    log_file = ACCEPTANCE_TESTS / "squareRoot" / "output.maude"
    if not log_file.exists():
        pytest.skip(f"Log file not found: {log_file}")
    return log_file.read_text()


@pytest.fixture
def lookup8_plexil_log():
    """Load lookup8 PLEXIL Executive log."""
    log_file = ACCEPTANCE_TESTS / "lookup8" / "output.plexil"
    if not log_file.exists():
        pytest.skip(f"Log file not found: {log_file}")
    return log_file.read_text()


@pytest.fixture
def lookup8_maude_log():
    """Load lookup8 Maude log."""
    log_file = ACCEPTANCE_TESTS / "lookup8" / "output.maude"
    if not log_file.exists():
        pytest.skip(f"Log file not found: {log_file}")
    return log_file.read_text()
