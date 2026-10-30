"""Unit tests for Maude execution and run.maude generation."""

import subprocess
from pathlib import Path
from unittest.mock import Mock, patch

import pytest

from plexilv_run.config import Config
from plexilv_run.exceptions import MaudeError, MaudeTimeoutError
from plexilv_run.maude import MaudeRunner
from plexilv_run.workspace import Workspace


@pytest.fixture
def mock_config(tmp_path):
    """Create a mock Config for testing."""
    plan = tmp_path / "test_plan.plx"
    plan.touch()
    script = tmp_path / "test_script.psx"
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
class TestMaudeRunner:
    """Test MaudeRunner initialization."""

    def test_init(self, workspace, mock_config):
        """Should initialize with workspace and config."""
        runner = MaudeRunner(workspace, mock_config)
        assert runner.workspace == workspace
        assert runner.config == mock_config


@pytest.mark.unit
class TestComputePlanModuleName:
    """Test plan module name computation."""

    def test_simple_name(self, workspace, mock_config):
        """Simple name should just add -PLAN suffix."""
        runner = MaudeRunner(workspace, mock_config)
        assert runner.compute_plan_module_name("MyPlan") == "MyPlan-PLAN"

    def test_with_underscores(self, workspace, mock_config):
        """Underscores should be replaced with dashes."""
        runner = MaudeRunner(workspace, mock_config)
        assert runner.compute_plan_module_name("test_plan_01") == "test-plan-01-PLAN"

    def test_no_underscores(self, workspace, mock_config):
        """Name without underscores should work."""
        runner = MaudeRunner(workspace, mock_config)
        assert runner.compute_plan_module_name("Plan123") == "Plan123-PLAN"

    def test_multiple_underscores(self, workspace, mock_config):
        """Multiple underscores should all be replaced."""
        runner = MaudeRunner(workspace, mock_config)
        assert runner.compute_plan_module_name("my_test_plan_v2") == "my-test-plan-v2-PLAN"


@pytest.mark.unit
class TestGetLoadPath:
    """Test load path generation."""

    def test_absolute_path_default(self, workspace, mock_config):
        """Default should return absolute path."""
        runner = MaudeRunner(workspace, mock_config)
        test_path = Path("/some/absolute/path/file.maude")

        result = runner.get_load_path(test_path)

        assert result == str(test_path.resolve())

    def test_relative_path_mode(self, workspace, mock_config, tmp_path):
        """Relative paths mode should return path relative to workspace."""
        mock_config.relative_paths = True
        runner = MaudeRunner(workspace, mock_config)

        # Create a file in the workspace
        test_file = workspace.path / "test.maude"
        test_file.touch()

        result = runner.get_load_path(test_file)

        assert result == "test.maude"

    def test_relative_path_parent_dir(self, workspace, mock_config, tmp_path):
        """Relative path to parent directory should work."""
        mock_config.relative_paths = True
        runner = MaudeRunner(workspace, mock_config)

        # Create a file outside workspace
        test_file = tmp_path / "outside.maude"
        test_file.touch()

        result = runner.get_load_path(test_file)

        # Should be relative to workspace
        assert not Path(result).is_absolute()
        assert ".." in result


@pytest.mark.unit
class TestGenerateRunFile:
    """Test run.maude file generation."""

    def test_generate_basic_structure(self, workspace, mock_config):
        """Should generate run.maude with correct structure."""
        runner = MaudeRunner(workspace, mock_config)

        # Create mock .maude files
        workspace.get_plan_maude_path("test_plan").touch()
        workspace.get_script_maude_path("test_script").touch()

        runner.generate_run_file("test_plan", "test_script")

        run_maude = workspace.get_run_maude_path()
        assert run_maude.exists()

        content = run_maude.read_text()
        assert "load" in content
        assert "test_plan.plan.maude" in content
        assert "test_script.script.maude" in content
        assert "mod PLAN-SIMULATION is" in content
        assert "protecting test-plan-PLAN" in content
        assert "protecting INPUT" in content
        assert "rew run(compile(rootNode,input))" in content
        assert "q" in content

    def test_generate_with_same_plan_and_script_stem(self, workspace, mock_config):
        """Should load two distinct files when plan and script share a basename."""
        runner = MaudeRunner(workspace, mock_config)

        runner.generate_run_file("same", "same")

        loads = [
            line.split(maxsplit=1)[1]
            for line in workspace.get_run_maude_path().read_text().splitlines()
            if line.startswith("load ")
        ]
        assert len(loads) == 3
        assert len(set(loads)) == 3
        assert any(l.endswith("same.plan.maude") for l in loads)
        assert any(l.endswith("same.script.maude") for l in loads)

    def test_generate_with_absolute_paths(self, workspace, mock_config):
        """Should use absolute paths by default."""
        runner = MaudeRunner(workspace, mock_config)

        workspace.get_plan_maude_path("MyPlan").touch()
        workspace.get_script_maude_path("script").touch()

        runner.generate_run_file("MyPlan", "script")

        content = workspace.get_run_maude_path().read_text()
        # Should contain absolute path to semantics
        assert str(mock_config.semantics_path.resolve()) in content

    def test_generate_with_relative_paths(self, workspace, mock_config):
        """Should use relative paths when configured."""
        mock_config.relative_paths = True
        runner = MaudeRunner(workspace, mock_config)

        workspace.get_plan_maude_path("MyPlan").touch()
        workspace.get_script_maude_path("script").touch()

        runner.generate_run_file("MyPlan", "script")

        content = workspace.get_run_maude_path().read_text()
        # Paths should be relative
        assert "MyPlan.plan.maude" in content
        assert "script.script.maude" in content

    def test_module_name_with_underscores(self, workspace, mock_config):
        """Module name should have underscores replaced with dashes."""
        runner = MaudeRunner(workspace, mock_config)

        workspace.get_plan_maude_path("test_plan_01").touch()
        workspace.get_script_maude_path("script").touch()

        runner.generate_run_file("test_plan_01", "script")

        content = workspace.get_run_maude_path().read_text()
        assert "protecting test-plan-01-PLAN" in content


@pytest.mark.unit
class TestExecute:
    """Test Maude execution."""

    @patch('subprocess.run')
    def test_successful_execution(self, mock_run, workspace, mock_config, capsys):
        """Successful execution should return 0."""
        mock_run.return_value = Mock(
            returncode=0,
            stdout="Maude output",
            stderr="Maude stderr",
        )

        runner = MaudeRunner(workspace, mock_config)
        result = runner.execute()

        assert result == 0

        # Check output was printed (only stderr by default)
        captured = capsys.readouterr()
        assert "Maude stderr" in captured.out
        # stdout should NOT be printed
        assert "Maude output" not in captured.out

    @patch('subprocess.run')
    def test_execution_failure(self, mock_run, workspace, mock_config):
        """Failed execution should raise MaudeError."""
        mock_run.return_value = Mock(
            returncode=1,
            stdout="",
            stderr="Error message",
        )

        runner = MaudeRunner(workspace, mock_config)

        with pytest.raises(MaudeError) as exc_info:
            runner.execute()

        assert exc_info.value.exit_code == 1
        assert exc_info.value.stderr == "Error message"

    @patch('subprocess.run')
    def test_execution_timeout(self, mock_run, workspace, mock_config):
        """Timeout should raise MaudeTimeoutError."""
        timeout_error = subprocess.TimeoutExpired(
            cmd=["maude", "run.maude"],
            timeout=300,
        )
        timeout_error.stdout = b"partial output"
        timeout_error.stderr = b""

        mock_run.side_effect = timeout_error

        runner = MaudeRunner(workspace, mock_config)

        with pytest.raises(MaudeTimeoutError) as exc_info:
            runner.execute()

        assert exc_info.value.timeout == 300

    @patch('subprocess.run')
    def test_with_custom_maude_opts(self, mock_run, workspace, mock_config):
        """Should include custom Maude options in command."""
        mock_run.return_value = Mock(returncode=0, stdout="", stderr="")

        mock_config.maude_opts = ["-verbose", "-print-to-stdout"]
        runner = MaudeRunner(workspace, mock_config)
        runner.execute()

        call_args = mock_run.call_args[0][0]
        assert "-verbose" in call_args
        assert "-print-to-stdout" in call_args

    @patch('subprocess.run')
    def test_with_space_separated_opts(self, mock_run, workspace, mock_config):
        """Should split space-separated options."""
        mock_run.return_value = Mock(returncode=0, stdout="", stderr="")

        mock_config.maude_opts = ["-verbose -print-to-stdout"]
        runner = MaudeRunner(workspace, mock_config)
        runner.execute()

        call_args = mock_run.call_args[0][0]
        assert "-verbose" in call_args
        assert "-print-to-stdout" in call_args

    @patch('subprocess.run')
    def test_debug_mode_creates_logs(self, mock_run, workspace, mock_config):
        """Debug mode should create log files."""
        mock_run.return_value = Mock(
            returncode=0,
            stdout="Maude output",
            stderr="Maude stderr",
        )

        mock_config.debug = True
        runner = MaudeRunner(workspace, mock_config)
        runner.execute()

        stdout_log, stderr_log = workspace.get_tool_log_paths("maude")
        assert stdout_log.exists()
        assert stderr_log.exists()
        assert stdout_log.read_text() == "Maude output"
        assert stderr_log.read_text() == "Maude stderr"

    @patch('subprocess.run')
    def test_log_file_output(self, mock_run, workspace, mock_config, tmp_path):
        """Should write stderr to log file when configured."""
        mock_run.return_value = Mock(
            returncode=0,
            stdout="Maude output",
            stderr="Maude stderr",
        )

        log_file = tmp_path / "output.log"
        mock_config.log_file = log_file

        runner = MaudeRunner(workspace, mock_config)
        runner.execute()

        assert log_file.exists()
        assert log_file.read_text() == "Maude stderr"

    @patch('subprocess.run')
    def test_runs_in_workspace(self, mock_run, workspace, mock_config):
        """Should run Maude in workspace directory."""
        mock_run.return_value = Mock(returncode=0, stdout="", stderr="")

        runner = MaudeRunner(workspace, mock_config)
        runner.execute()

        call_args = mock_run.call_args
        assert call_args[1]['cwd'] == workspace.path

    @patch('subprocess.run')
    def test_command_structure(self, mock_run, workspace, mock_config):
        """Should build correct Maude command."""
        mock_run.return_value = Mock(returncode=0, stdout="", stderr="")

        runner = MaudeRunner(workspace, mock_config)
        runner.execute()

        cmd = mock_run.call_args[0][0]
        assert cmd[0] == "/usr/bin/maude"
        assert "-no-ansi-color" in cmd
        assert "-no-wrap" in cmd
        assert "-no-banner" in cmd
        assert "-no-advise" in cmd
        assert "-print-to-stderr" in cmd
        # Should use absolute path to run.maude (not just "run.maude")
        assert cmd[-1].endswith("run.maude")
        assert Path(cmd[-1]).is_absolute()