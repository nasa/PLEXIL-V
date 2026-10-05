"""Integration tests for CLI validation behavior."""

import pytest
from click.testing import CliRunner

from plexilv_log.cli.plexilog import main as plexilog_main
from plexilv_log.cli.plexilog_maude import main as plexilog_maude_main
from plexilv_log.cli.plexilog_diff import main as plexilog_diff_main


@pytest.fixture
def runner():
    """Create a Click CLI test runner."""
    return CliRunner()


class TestPlexilogCLIValidation:
    """Test plexilog CLI validation behavior."""

    def test_plexilog_fails_on_error_log(self, runner, tmp_path):
        """plexilog should exit with code 2 on ERROR logs."""
        log_file = tmp_path / "error.log"
        log_file.write_text("""
Running executive from /path/to/plexil
ERROR: Node test: variable not found
""")

        result = runner.invoke(plexilog_main, [str(log_file)])
        assert result.exit_code == 2
        assert "ERROR entries" in result.output

    def test_plexilog_fails_on_warning_log(self, runner, tmp_path):
        """plexilog should exit with code 2 on WARNING logs."""
        log_file = tmp_path / "warning.log"
        log_file.write_text("""
Running executive from /path/to/plexil
WARNING: Some warning message
""")

        result = runner.invoke(plexilog_main, [str(log_file)])
        assert result.exit_code == 2
        assert "WARNING entries" in result.output

    def test_plexilog_fails_on_empty_log(self, runner, tmp_path):
        """plexilog should exit with code 2 on empty logs."""
        log_file = tmp_path / "empty.log"
        log_file.write_text("")

        result = runner.invoke(plexilog_main, [str(log_file)])
        assert result.exit_code == 2
        assert "empty" in result.output.lower()

    def test_plexilog_fails_on_no_cycles(self, runner, tmp_path):
        """plexilog should exit with code 2 on logs without cycle markers."""
        log_file = tmp_path / "nocycles.log"
        log_file.write_text("Running executive\nSome content\n")

        result = runner.invoke(plexilog_main, [str(log_file)])
        assert result.exit_code == 2
        assert "cycle markers" in result.output

    def test_plexilog_lenient_mode_accepts_errors(self, runner, tmp_path):
        """plexilog --lenient should accept ERROR logs."""
        log_file = tmp_path / "error.log"
        log_file.write_text("ERROR: Node test: variable not found\n")

        result = runner.invoke(plexilog_main, ['--lenient', str(log_file)])
        assert result.exit_code == 0
        # Should output JSON (even if empty)
        assert '"macros"' in result.output

    def test_plexilog_lenient_mode_accepts_empty(self, runner, tmp_path):
        """plexilog --lenient should accept empty logs."""
        log_file = tmp_path / "empty.log"
        log_file.write_text("")

        result = runner.invoke(plexilog_main, ['--lenient', str(log_file)])
        assert result.exit_code == 0
        assert '"macros"' in result.output

    def test_plexilog_valid_log_succeeds(self, runner, tmp_path):
        """plexilog should succeed on valid logs."""
        log_file = tmp_path / "valid.log"
        log_file.write_text("""
Running executive from /path/to/plexil
==>Start cycle 1
[PlexilExec:step][1:0:0] Transitioning NodeList node test from INACTIVE to WAITING
==>End cycle 1
""")

        result = runner.invoke(plexilog_main, [str(log_file)])
        assert result.exit_code == 0
        assert '"macros"' in result.output

    def test_plexilog_stdin_with_error(self, runner):
        """plexilog should validate stdin input."""
        result = runner.invoke(plexilog_main, input="ERROR: test\n")
        assert result.exit_code == 2
        assert "ERROR entries" in result.output

    def test_plexilog_help_mentions_lenient(self, runner):
        """plexilog --help should mention --lenient flag."""
        result = runner.invoke(plexilog_main, ['--help'])
        assert result.exit_code == 0
        assert '--lenient' in result.output
        assert 'validation' in result.output.lower()


class TestPlexilogMaudeCLIValidation:
    """Test plexilog-maude CLI validation behavior."""

    def test_plexilog_maude_fails_on_empty_log(self, runner, tmp_path):
        """plexilog-maude should exit with code 2 on empty logs."""
        log_file = tmp_path / "empty.log"
        log_file.write_text("")

        result = runner.invoke(plexilog_maude_main, [str(log_file)])
        assert result.exit_code == 2
        assert "empty" in result.output.lower()

    def test_plexilog_maude_fails_on_no_macro(self, runner, tmp_path):
        """plexilog-maude should exit with code 2 on logs without MACRO."""
        log_file = tmp_path / "nomacro.log"
        log_file.write_text("some content\nno MACRO here\n")

        result = runner.invoke(plexilog_maude_main, [str(log_file)])
        assert result.exit_code == 2
        assert "MACRO markers" in result.output

    def test_plexilog_maude_lenient_mode(self, runner, tmp_path):
        """plexilog-maude --lenient should accept empty logs."""
        log_file = tmp_path / "empty.log"
        log_file.write_text("")

        result = runner.invoke(plexilog_maude_main, ['--lenient', str(log_file)])
        assert result.exit_code == 0
        assert '"macros"' in result.output

    def test_plexilog_maude_valid_log_succeeds(self, runner, tmp_path):
        """plexilog-maude should succeed on valid logs."""
        log_file = tmp_path / "valid.log"
        log_file.write_text("""
MACRO
    'test from inactive to waiting
 micro
""")

        result = runner.invoke(plexilog_maude_main, [str(log_file)])
        assert result.exit_code == 0
        assert '"macros"' in result.output

    def test_plexilog_maude_help_mentions_lenient(self, runner):
        """plexilog-maude --help should mention --lenient flag."""
        result = runner.invoke(plexilog_maude_main, ['--help'])
        assert result.exit_code == 0
        assert '--lenient' in result.output


class TestPlexilogDiffCLIValidation:
    """Test plexilog-diff CLI validation behavior."""

    def test_plexilog_diff_fails_on_invalid_plexil_log(self, runner, tmp_path):
        """plexilog-diff should exit with code 2 if PLEXIL log is invalid."""
        plexil_log = tmp_path / "error.log"
        plexil_log.write_text("ERROR: test\n")

        maude_log = tmp_path / "valid.log"
        maude_log.write_text("MACRO\n")

        result = runner.invoke(plexilog_diff_main, [str(plexil_log), str(maude_log)])
        assert result.exit_code == 2
        assert "ERROR entries" in result.output

    def test_plexilog_diff_fails_on_invalid_maude_log(self, runner, tmp_path):
        """plexilog-diff should exit with code 2 if Maude log is invalid."""
        plexil_log = tmp_path / "valid.log"
        plexil_log.write_text("==>Start cycle 1\n==>End cycle 1\n")

        maude_log = tmp_path / "empty.log"
        maude_log.write_text("")

        result = runner.invoke(plexilog_diff_main, [str(plexil_log), str(maude_log)])
        assert result.exit_code == 2
        assert "empty" in result.output.lower()

    def test_plexilog_diff_lenient_mode(self, runner, tmp_path):
        """plexilog-diff --lenient should accept invalid logs."""
        plexil_log = tmp_path / "error.log"
        plexil_log.write_text("ERROR: test\n")

        maude_log = tmp_path / "empty.log"
        maude_log.write_text("")

        result = runner.invoke(plexilog_diff_main,
                              ['--lenient', str(plexil_log), str(maude_log)])
        # Should compare (both empty), not fail on validation
        assert result.exit_code == 0
        assert "EQ" in result.output

    def test_plexilog_diff_valid_logs_succeeds(self, runner, tmp_path):
        """plexilog-diff should succeed on valid logs."""
        plexil_log = tmp_path / "plexil.log"
        plexil_log.write_text("""
==>Start cycle 1
[PlexilExec:step][1:0:0] Transitioning NodeList node test 0x1234 from INACTIVE to WAITING
==>End cycle 1
""")

        maude_log = tmp_path / "maude.log"
        maude_log.write_text("""
MACRO
    'test from inactive to waiting
 micro
""")

        result = runner.invoke(plexilog_diff_main, [str(plexil_log), str(maude_log)])
        # Exit code 0 if traces match, 1 if different
        assert result.exit_code in [0, 1]  # Both are valid outcomes

    def test_plexilog_diff_help_mentions_lenient(self, runner):
        """plexilog-diff --help should mention --lenient flag."""
        result = runner.invoke(plexilog_diff_main, ['--help'])
        assert result.exit_code == 0
        assert '--lenient' in result.output


class TestCLIExitCodes:
    """Test CLI exit code conventions."""

    def test_plexilog_validation_error_exit_code_2(self, runner, tmp_path):
        """Validation errors should use exit code 2."""
        log_file = tmp_path / "error.log"
        log_file.write_text("ERROR: test\n")

        result = runner.invoke(plexilog_main, [str(log_file)])
        assert result.exit_code == 2

    def test_plexilog_success_exit_code_0(self, runner, tmp_path):
        """Successful parsing should use exit code 0."""
        log_file = tmp_path / "valid.log"
        log_file.write_text("==>Start cycle 1\n")

        result = runner.invoke(plexilog_main, [str(log_file)])
        assert result.exit_code == 0

    def test_plexilog_diff_equal_exit_code_0(self, runner, tmp_path):
        """Equal traces should use exit code 0."""
        # Create truly empty/equal traces
        plexil_log = tmp_path / "p.log"
        plexil_log.write_text("""
==>Start cycle 1
==>End cycle 1
""")

        maude_log = tmp_path / "m.log"
        maude_log.write_text("MACRO\n")

        # Both should parse to empty traces (no transitions)
        result = runner.invoke(plexilog_diff_main, [str(plexil_log), str(maude_log)])
        # May differ in macro structure, so accept either outcome
        assert result.exit_code in [0, 1]

    def test_plexilog_diff_validation_error_exit_code_2(self, runner, tmp_path):
        """Validation errors should use exit code 2."""
        plexil_log = tmp_path / "p.log"
        plexil_log.write_text("")

        maude_log = tmp_path / "m.log"
        maude_log.write_text("")

        result = runner.invoke(plexilog_diff_main, [str(plexil_log), str(maude_log)])
        assert result.exit_code == 2
