"""Unit tests for conversion tool execution."""

import subprocess
from pathlib import Path
from unittest.mock import Mock, patch

import pytest

from plexilv_run.config import Config
from plexilv_run.conversion import ConversionRunner
from plexilv_run.workspace import Workspace


@pytest.fixture
def mock_config(tmp_path):
    """Create a mock Config for testing."""
    plan = tmp_path / "plan.plx"
    plan.touch()
    script = tmp_path / "script.psx"
    script.touch()
    semantics = tmp_path / "plexil-v.maude"
    semantics.touch()

    return Config(
        plan_path=plan,
        script_path=script,
        semantics_path=semantics,
        plx2maude_path="/usr/bin/plx2maude",
        psx2maude_path="/usr/bin/psx2maude",
        maude_path="/usr/bin/maude",
        maude_opts=[],
        maude_timeout=300,
        conversion_timeout=30,
        work_dir=None,
        log_file=None,
        debug=False,
        cleanup=False,
        force_cleanup=False,
        relative_paths=False,
    )


@pytest.fixture
def workspace(tmp_path):
    """Create a workspace for testing."""
    ws = Workspace(tmp_path / "workspace")
    ws.create()
    return ws


@pytest.mark.unit
class TestConversionRunner:
    """Test ConversionRunner initialization."""

    def test_init(self, workspace, mock_config):
        """Should initialize with workspace and config."""
        runner = ConversionRunner(workspace, mock_config)
        assert runner.workspace == workspace
        assert runner.config == mock_config


@pytest.mark.unit
class TestRunPlx2maude:
    """Test run_plx2maude method."""

    @patch('subprocess.run')
    def test_successful_conversion(self, mock_run, workspace, mock_config):
        """Successful conversion should write output and return True."""
        mock_run.return_value = Mock(
            returncode=0,
            stdout="maude content",
            stderr="",
        )

        runner = ConversionRunner(workspace, mock_config)
        result = runner.run_plx2maude()

        assert result is True

        # Check output file was created
        output_path = workspace.get_plan_maude_path("plan")
        assert output_path.exists()
        assert output_path.read_text() == "maude content"

        # Check command was correct
        call_args = mock_run.call_args
        assert call_args[0][0][0] == "/usr/bin/plx2maude"
        assert Path(call_args[0][0][1]) == mock_config.plan_path.resolve()

    @patch('subprocess.run')
    def test_conversion_failure(self, mock_run, workspace, mock_config, capsys):
        """Failed conversion should return False and print error."""
        mock_run.return_value = Mock(
            returncode=1,
            stdout="",
            stderr="Parse error",
        )

        runner = ConversionRunner(workspace, mock_config)
        result = runner.run_plx2maude()

        assert result is False

        # Check error was printed to stderr
        captured = capsys.readouterr()
        assert "plx2maude failed with exit code 1" in captured.err
        assert "Parse error" in captured.err

    @patch('subprocess.run')
    def test_conversion_timeout(self, mock_run, workspace, mock_config, capsys):
        """Timeout should return False and print error."""
        timeout_error = subprocess.TimeoutExpired(
            cmd=["plx2maude", "plan.plx"],
            timeout=30,
        )
        # Set stdout and stderr as attributes
        timeout_error.stdout = b"partial output"
        timeout_error.stderr = b""

        mock_run.side_effect = timeout_error

        runner = ConversionRunner(workspace, mock_config)
        result = runner.run_plx2maude()

        assert result is False

        # Check error was printed to stderr
        captured = capsys.readouterr()
        assert "timed out after 30 seconds" in captured.err

    @patch('subprocess.run')
    def test_debug_mode_creates_logs(self, mock_run, workspace, mock_config):
        """Debug mode should create log files."""
        mock_run.return_value = Mock(
            returncode=0,
            stdout="maude content",
            stderr="debug info",
        )

        mock_config.debug = True
        runner = ConversionRunner(workspace, mock_config)
        runner.run_plx2maude()

        # Check log files were created
        stdout_log, stderr_log = workspace.get_tool_log_paths("plx2maude")
        assert stdout_log.exists()
        assert stderr_log.exists()
        assert stdout_log.read_text() == "maude content"
        assert stderr_log.read_text() == "debug info"

    @patch('subprocess.run')
    def test_debug_mode_timeout_creates_logs(self, mock_run, workspace, mock_config):
        """Debug mode should create log files even on timeout."""
        timeout_error = subprocess.TimeoutExpired(
            cmd=["plx2maude", "plan.plx"],
            timeout=30,
        )
        timeout_error.stdout = b"partial output"
        timeout_error.stderr = b"timeout info"

        mock_run.side_effect = timeout_error

        mock_config.debug = True
        runner = ConversionRunner(workspace, mock_config)
        runner.run_plx2maude()

        # Check log files were created
        stdout_log, stderr_log = workspace.get_tool_log_paths("plx2maude")
        assert stdout_log.exists()
        assert stderr_log.exists()
        assert stdout_log.read_text() == "partial output"
        assert stderr_log.read_text() == "timeout info"

    @patch('subprocess.run')
    def test_debug_mode_error_message(self, mock_run, workspace, mock_config, capsys):
        """Debug mode should show detailed error message."""
        mock_run.return_value = Mock(
            returncode=1,
            stdout="some output",
            stderr="error details",
        )

        mock_config.debug = True
        runner = ConversionRunner(workspace, mock_config)
        runner.run_plx2maude()

        captured = capsys.readouterr()
        # Should include command, working directory, etc.
        assert "Command:" in captured.err
        assert "Working directory:" in captured.err
        assert "Exit code: 1" in captured.err
        assert "Full logs saved to:" in captured.err

    @patch('subprocess.run')
    def test_uses_absolute_paths(self, mock_run, workspace, mock_config):
        """Should use absolute paths for input file."""
        mock_run.return_value = Mock(returncode=0, stdout="", stderr="")

        runner = ConversionRunner(workspace, mock_config)
        runner.run_plx2maude()

        call_args = mock_run.call_args
        input_path = call_args[0][0][1]
        assert Path(input_path).is_absolute()

    @patch('subprocess.run')
    def test_runs_in_workspace(self, mock_run, workspace, mock_config):
        """Should run command in workspace directory."""
        mock_run.return_value = Mock(returncode=0, stdout="", stderr="")

        runner = ConversionRunner(workspace, mock_config)
        runner.run_plx2maude()

        call_args = mock_run.call_args
        assert call_args[1]['cwd'] == workspace.path


@pytest.mark.unit
class TestRunPsx2maude:
    """Test run_psx2maude method."""

    @patch('subprocess.run')
    def test_successful_conversion(self, mock_run, workspace, mock_config):
        """Successful conversion should write output and return True."""
        mock_run.return_value = Mock(
            returncode=0,
            stdout="script maude content",
            stderr="",
        )

        runner = ConversionRunner(workspace, mock_config)
        result = runner.run_psx2maude()

        assert result is True

        # Check output file was created
        output_path = workspace.get_script_maude_path("script")
        assert output_path.exists()
        assert output_path.read_text() == "script maude content"

        # Check command was correct
        call_args = mock_run.call_args
        assert call_args[0][0][0] == "/usr/bin/psx2maude"
        assert Path(call_args[0][0][1]) == mock_config.script_path.resolve()

    @patch('subprocess.run')
    def test_conversion_failure(self, mock_run, workspace, mock_config, capsys):
        """Failed conversion should return False and print error."""
        mock_run.return_value = Mock(
            returncode=1,
            stdout="",
            stderr="Parse error",
        )

        runner = ConversionRunner(workspace, mock_config)
        result = runner.run_psx2maude()

        assert result is False

        captured = capsys.readouterr()
        assert "psx2maude failed with exit code 1" in captured.err


@pytest.mark.unit
class TestBothConversions:
    """Test running both conversions."""

    @patch('subprocess.run')
    def test_both_succeed(self, mock_run, workspace, mock_config):
        """Both conversions should succeed independently."""
        mock_run.return_value = Mock(returncode=0, stdout="content", stderr="")

        runner = ConversionRunner(workspace, mock_config)

        result1 = runner.run_plx2maude()
        result2 = runner.run_psx2maude()

        assert result1 is True
        assert result2 is True

    @patch('subprocess.run')
    def test_first_fails_second_succeeds(self, mock_run, workspace, mock_config):
        """Should try second conversion even if first fails."""
        # First call fails, second succeeds
        mock_run.side_effect = [
            Mock(returncode=1, stdout="", stderr="error"),
            Mock(returncode=0, stdout="content", stderr=""),
        ]

        runner = ConversionRunner(workspace, mock_config)

        result1 = runner.run_plx2maude()
        result2 = runner.run_psx2maude()

        assert result1 is False
        assert result2 is True


@pytest.mark.unit
class TestErrorFormatting:
    """Test error message formatting."""

    @patch('subprocess.run')
    def test_simple_error_format(self, mock_run, workspace, mock_config, capsys):
        """Non-debug mode should show simple error."""
        mock_run.return_value = Mock(
            returncode=1,
            stdout="some output",
            stderr="error message",
        )

        runner = ConversionRunner(workspace, mock_config)
        runner.run_plx2maude()

        captured = capsys.readouterr()
        # Should NOT include detailed info
        assert "Command:" not in captured.err
        assert "Working directory:" not in captured.err
        # Should include basic info
        assert "plx2maude failed" in captured.err
        assert "error message" in captured.err

    @patch('subprocess.run')
    def test_debug_error_format(self, mock_run, workspace, mock_config, capsys):
        """Debug mode should show detailed error."""
        # Create output with more than 10 lines
        many_lines = "\n".join([f"line {i:03d}" for i in range(20)])

        mock_run.return_value = Mock(
            returncode=1,
            stdout=many_lines,
            stderr=many_lines,
        )

        mock_config.debug = True
        runner = ConversionRunner(workspace, mock_config)
        runner.run_plx2maude()

        captured = capsys.readouterr()
        # Should include detailed info
        assert "Command:" in captured.err
        assert "Working directory:" in captured.err
        assert "last 10 lines" in captured.err
        # Should only show last 10 lines (010-019)
        assert "line 010" in captured.err
        assert "line 019" in captured.err
        # Should NOT show early lines (000-009)
        assert "line 000" not in captured.err
        assert "line 001" not in captured.err
        assert "line 009" not in captured.err

@pytest.mark.unit
class TestSameBasename:
    """Plan and script sharing a basename must not overwrite each other."""

    @patch('subprocess.run')
    def test_outputs_do_not_collide(self, mock_run, workspace, tmp_path):
        plan = tmp_path / "foo.plx"
        plan.touch()
        script = tmp_path / "foo.psx"
        script.touch()
        semantics = tmp_path / "plexil-v.maude"
        semantics.touch()
        config = Config(
            plan_path=plan,
            script_path=script,
            semantics_path=semantics,
            plx2maude_path="/usr/bin/plx2maude",
            psx2maude_path="/usr/bin/psx2maude",
            maude_path="/usr/bin/maude",
            maude_opts=[],
            maude_timeout=300,
            conversion_timeout=30,
            work_dir=None,
            log_file=None,
            debug=False,
            cleanup=False,
            force_cleanup=False,
            relative_paths=False,
        )
        mock_run.side_effect = [
            Mock(returncode=0, stdout="PLAN CONTENT", stderr=""),
            Mock(returncode=0, stdout="SCRIPT CONTENT", stderr=""),
        ]

        runner = ConversionRunner(workspace, config)
        assert runner.run_plx2maude() is True
        assert runner.run_psx2maude() is True

        assert workspace.get_plan_maude_path("foo").read_text() == "PLAN CONTENT"
        assert workspace.get_script_maude_path("foo").read_text() == "SCRIPT CONTENT"
