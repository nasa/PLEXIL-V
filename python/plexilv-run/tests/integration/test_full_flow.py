"""Integration tests for complete plexilv flows."""

import subprocess
from pathlib import Path
from unittest.mock import Mock, patch

import pytest

from plexilv_run.config import Config
from plexilv_run.exceptions import MaudeError
from plexilv_run.pipeline import Pipeline


@pytest.fixture
def test_environment(tmp_path):
    """Create a complete test environment with files and mock tools."""
    # Create input files
    plan = tmp_path / "TestPlan.plx"
    plan.write_text('<?xml version="1.0"?><PlexilPlan></PlexilPlan>')

    script = tmp_path / "test_script.psx"
    script.write_text('<?xml version="1.0"?><PLEXILScript></PLEXILScript>')

    # Create PLEXILV_HOME structure
    plexilv_home = tmp_path / "plexilv"
    semantics_dir = plexilv_home / "semantics" / "src"
    semantics_dir.mkdir(parents=True)
    semantics = semantics_dir / "plexil-v.maude"
    semantics.write_text("*** PLEXIL-V semantics ***")

    # Workspace directory
    workspace = tmp_path / "workspace"

    return {
        "plan": plan,
        "script": script,
        "semantics": semantics,
        "plexilv_home": plexilv_home,
        "workspace": workspace,
        "tmp_path": tmp_path,
    }


@pytest.mark.integration
class TestSameBasename:
    """Plan and script sharing a basename (regression)."""

    @patch('plexilv_run.pipeline.check_all_tools')
    @patch('subprocess.run')
    def test_plan_and_script_with_same_basename(self, mock_run, mock_check_tools, tmp_path):
        """Regression: foo.plx and foo.psx both converted to foo.maude, so the
        script output overwrote the plan and the plan module was never loaded."""
        mock_check_tools.return_value = ("plx2maude", "psx2maude", "maude")

        plan = tmp_path / "foo.plx"
        plan.write_text("<PlexilPlan/>")
        script = tmp_path / "foo.psx"
        script.write_text("<PLEXILScript/>")
        semantics = tmp_path / "plexil-v.maude"
        semantics.write_text("*** semantics ***")

        def mock_subprocess(cmd, **kwargs):
            result = Mock(returncode=0, stdout="", stderr="")
            if "plx2maude" in cmd[0]:
                result.stdout = "mod foo-PLAN is endm"
            elif "psx2maude" in cmd[0]:
                result.stdout = "mod INPUT is endm"
            return result

        mock_run.side_effect = mock_subprocess

        config = Config(
            plan_path=plan,
            script_path=script,
            semantics_path=semantics,
            plx2maude_path="plx2maude",
            psx2maude_path="psx2maude",
            maude_path="maude",
            maude_opts=[],
            maude_timeout=300,
            conversion_timeout=30,
            work_dir=tmp_path / "workspace",
            log_file=None,
            debug=False,
            cleanup=False,
            force_cleanup=False,
            relative_paths=False,
        )

        pipeline = Pipeline(config)
        assert pipeline.run() == 0

        ws = pipeline.workspace.path
        assert (ws / "foo.plan.maude").read_text() == "mod foo-PLAN is endm"
        assert (ws / "foo.script.maude").read_text() == "mod INPUT is endm"

        loads = [l for l in (ws / "run.maude").read_text().splitlines() if l.startswith("load ")]
        assert len(set(loads)) == len(loads) == 3


@pytest.mark.integration
class TestHappyPath:
    """Test successful execution flow."""

    @patch('plexilv_run.pipeline.check_all_tools')
    @patch('subprocess.run')
    def test_complete_successful_flow(self, mock_run, mock_check_tools, test_environment):
        """Test complete flow: validation → conversion → run.maude → Maude execution."""
        env = test_environment

        # Mock tool checking (return the tool paths)
        mock_check_tools.return_value = ("plx2maude", "psx2maude", "maude")

        # Mock successful tool executions
        def mock_subprocess(cmd, **kwargs):
            result = Mock()
            result.returncode = 0
            result.stdout = ""
            result.stderr = ""

            # Identify which tool is being called
            if "plx2maude" in cmd[0]:
                result.stdout = "mod TestPlan-PLAN is endm"
            elif "psx2maude" in cmd[0]:
                result.stdout = "mod INPUT is endm"
            elif "maude" in cmd[0]:
                result.stdout = "Maude output"
                result.stderr = "Result: success"

            return result

        mock_run.side_effect = mock_subprocess

        # Create config
        config = Config(
            plan_path=env["plan"],
            script_path=env["script"],
            semantics_path=env["semantics"],
            plx2maude_path="plx2maude",
            psx2maude_path="psx2maude",
            maude_path="maude",
            maude_opts=[],
            maude_timeout=300,
            conversion_timeout=30,
            work_dir=env["workspace"],
            log_file=None,
            debug=False,
            cleanup=False,
            force_cleanup=False,
            relative_paths=False,
        )

        # Run pipeline
        pipeline = Pipeline(config)
        exit_code = pipeline.run()

        # Verify success
        assert exit_code == 0

        # Verify workspace was created (use actual workspace from pipeline)
        assert pipeline.workspace is not None
        workspace_path = pipeline.workspace.path
        assert workspace_path.exists()

        # Verify files were generated
        assert (workspace_path / "TestPlan.plan.maude").exists()
        assert (workspace_path / "test_script.script.maude").exists()
        assert (workspace_path / "run.maude").exists()

        # Verify run.maude content
        run_maude = (workspace_path / "run.maude").read_text()
        assert "load" in run_maude
        assert "TestPlan-PLAN" in run_maude
        assert "protecting INPUT" in run_maude
        assert "rew run(compile(rootNode,input))" in run_maude

        # Verify all tools were called
        assert mock_run.call_count == 3  # plx2maude, psx2maude, maude

    @patch('plexilv_run.pipeline.check_all_tools')
    @patch('subprocess.run')
    def test_with_cleanup_on_success(self, mock_run, mock_check_tools, test_environment):
        """Test that workspace is cleaned up on success when --cleanup is set."""
        env = test_environment

        mock_check_tools.return_value = ("plx2maude", "psx2maude", "maude")

        # Mock all subprocess calls to succeed
        def mock_subprocess(cmd, **kwargs):
            result = Mock()
            result.returncode = 0
            result.stdout = "mock output"
            result.stderr = ""
            return result

        mock_run.side_effect = mock_subprocess

        config = Config(
            plan_path=env["plan"],
            script_path=env["script"],
            semantics_path=env["semantics"],
            plx2maude_path="plx2maude",
            psx2maude_path="psx2maude",
            maude_path="maude",
            maude_opts=[],
            maude_timeout=300,
            conversion_timeout=30,
            work_dir=env["workspace"],
            log_file=None,
            debug=False,
            cleanup=True,  # Enable cleanup
            force_cleanup=False,
            relative_paths=False,
        )

        pipeline = Pipeline(config)
        exit_code = pipeline.run()

        assert exit_code == 0

        # Workspace should be cleaned up
        workspace_path = pipeline.workspace.path
        assert not workspace_path.exists()

    @patch('plexilv_run.pipeline.check_all_tools')
    @patch('subprocess.run')
    def test_with_relative_paths(self, mock_run, mock_check_tools, test_environment):
        """Test that relative paths are generated in run.maude when configured."""
        env = test_environment

        mock_check_tools.return_value = ("plx2maude", "psx2maude", "maude")

        def mock_subprocess(cmd, **kwargs):
            result = Mock()
            result.returncode = 0
            result.stdout = "mock output"
            result.stderr = ""
            return result

        mock_run.side_effect = mock_subprocess

        config = Config(
            plan_path=env["plan"],
            script_path=env["script"],
            semantics_path=env["semantics"],
            plx2maude_path="plx2maude",
            psx2maude_path="psx2maude",
            maude_path="maude",
            maude_opts=[],
            maude_timeout=300,
            conversion_timeout=30,
            work_dir=env["workspace"],
            log_file=None,
            debug=False,
            cleanup=False,
            force_cleanup=False,
            relative_paths=True,  # Enable relative paths
        )

        pipeline = Pipeline(config)
        exit_code = pipeline.run()

        assert exit_code == 0

        # Check run.maude uses relative paths
        workspace_path = pipeline.workspace.path
        run_maude = (workspace_path / "run.maude").read_text()
        # Should have relative paths, not absolute
        assert "TestPlan.plan.maude" in run_maude
        assert "test_script.script.maude" in run_maude
        # Should NOT have absolute path markers
        lines = run_maude.split('\n')
        load_lines = [line for line in lines if line.startswith('load')]
        for line in load_lines:
            if "TestPlan.plan.maude" in line or "test_script.script.maude" in line:
                # These should be just filenames (relative to workspace)
                assert not line.startswith('load /')


@pytest.mark.integration
class TestConversionFailure:
    """Test conversion failure scenarios."""

    @patch('plexilv_run.pipeline.check_all_tools')
    @patch('subprocess.run')
    def test_plx2maude_failure(self, mock_run, mock_check_tools, test_environment, capsys):
        """Test that plx2maude failure is reported correctly."""
        env = test_environment

        mock_check_tools.return_value = ("plx2maude", "psx2maude", "maude")

        call_count = [0]

        def mock_subprocess(cmd, **kwargs):
            result = Mock()
            call_count[0] += 1

            if "plx2maude" in cmd[0]:
                # plx2maude fails
                result.returncode = 1
                result.stdout = "partial output"
                result.stderr = "Parse error: invalid XML"
            elif "psx2maude" in cmd[0]:
                # psx2maude succeeds
                result.returncode = 0
                result.stdout = "mod INPUT is endm"
                result.stderr = ""
            else:
                # Should not reach maude
                result.returncode = 0
                result.stdout = ""
                result.stderr = ""

            return result

        mock_run.side_effect = mock_subprocess

        config = Config(
            plan_path=env["plan"],
            script_path=env["script"],
            semantics_path=env["semantics"],
            plx2maude_path="plx2maude",
            psx2maude_path="psx2maude",
            maude_path="maude",
            maude_opts=[],
            maude_timeout=300,
            conversion_timeout=30,
            work_dir=env["workspace"],
            log_file=None,
            debug=False,
            cleanup=False,
            force_cleanup=False,
            relative_paths=False,
        )

        pipeline = Pipeline(config)
        exit_code = pipeline.run()

        # Should fail
        assert exit_code == 1

        # Should have tried both conversions
        assert call_count[0] == 2  # plx2maude and psx2maude

        # Check error was printed
        captured = capsys.readouterr()
        assert "plx2maude failed" in captured.err
        assert "Parse error: invalid XML" in captured.err
        assert "Conversion failed" in captured.err

        # Workspace should still exist (not cleaned up on failure)
        workspace_path = pipeline.workspace.path
        assert workspace_path.exists()

    @patch('plexilv_run.pipeline.check_all_tools')
    @patch('subprocess.run')
    def test_both_conversions_fail(self, mock_run, mock_check_tools, test_environment, capsys):
        """Test that both conversion failures are reported."""
        env = test_environment

        mock_check_tools.return_value = ("plx2maude", "psx2maude", "maude")

        def mock_subprocess(cmd, **kwargs):
            result = Mock()
            # Both conversions fail
            result.returncode = 1

            if "plx2maude" in cmd[0]:
                result.stdout = ""
                result.stderr = "plx2maude error"
            elif "psx2maude" in cmd[0]:
                result.stdout = ""
                result.stderr = "psx2maude error"

            return result

        mock_run.side_effect = mock_subprocess

        config = Config(
            plan_path=env["plan"],
            script_path=env["script"],
            semantics_path=env["semantics"],
            plx2maude_path="plx2maude",
            psx2maude_path="psx2maude",
            maude_path="maude",
            maude_opts=[],
            maude_timeout=300,
            conversion_timeout=30,
            work_dir=env["workspace"],
            log_file=None,
            debug=False,
            cleanup=False,
            force_cleanup=False,
            relative_paths=False,
        )

        pipeline = Pipeline(config)
        exit_code = pipeline.run()

        assert exit_code == 1

        # Both errors should be printed
        captured = capsys.readouterr()
        assert "plx2maude error" in captured.err
        assert "psx2maude error" in captured.err

    @patch('plexilv_run.pipeline.check_all_tools')
    @patch('subprocess.run')
    def test_workspace_preserved_on_conversion_failure(self, mock_run, mock_check_tools, test_environment):
        """Test that workspace is preserved when conversion fails, even with --cleanup."""
        env = test_environment

        mock_check_tools.return_value = ("plx2maude", "psx2maude", "maude")

        def mock_subprocess(cmd, **kwargs):
            result = Mock()
            if "plx2maude" in cmd[0]:
                result.returncode = 1
                result.stdout = ""
                result.stderr = "conversion error"
            else:
                result.returncode = 0
                result.stdout = "success"
                result.stderr = ""
            return result

        mock_run.side_effect = mock_subprocess

        config = Config(
            plan_path=env["plan"],
            script_path=env["script"],
            semantics_path=env["semantics"],
            plx2maude_path="plx2maude",
            psx2maude_path="psx2maude",
            maude_path="maude",
            maude_opts=[],
            maude_timeout=300,
            conversion_timeout=30,
            work_dir=env["workspace"],
            log_file=None,
            debug=False,
            cleanup=True,  # Cleanup enabled
            force_cleanup=False,
            relative_paths=False,
        )

        pipeline = Pipeline(config)
        exit_code = pipeline.run()

        assert exit_code == 1

        # Workspace should NOT be cleaned up (failure)
        workspace_path = pipeline.workspace.path
        assert workspace_path.exists()


@pytest.mark.integration
class TestMaudeFailure:
    """Test Maude execution failure scenarios."""

    @patch('plexilv_run.pipeline.check_all_tools')
    @patch('subprocess.run')
    def test_maude_execution_error(self, mock_run, mock_check_tools, test_environment, capsys):
        """Test that Maude execution errors are handled correctly."""
        env = test_environment

        mock_check_tools.return_value = ("plx2maude", "psx2maude", "maude")

        def mock_subprocess(cmd, **kwargs):
            result = Mock()
            result.returncode = 0
            result.stdout = "mock output"
            result.stderr = ""

            # Maude fails
            if "maude" in cmd[0]:
                result.returncode = 1
                result.stdout = "partial maude output"
                result.stderr = "Maude execution error"

            return result

        mock_run.side_effect = mock_subprocess

        config = Config(
            plan_path=env["plan"],
            script_path=env["script"],
            semantics_path=env["semantics"],
            plx2maude_path="plx2maude",
            psx2maude_path="psx2maude",
            maude_path="maude",
            maude_opts=[],
            maude_timeout=300,
            conversion_timeout=30,
            work_dir=env["workspace"],
            log_file=None,
            debug=False,
            cleanup=False,
            force_cleanup=False,
            relative_paths=False,
        )

        pipeline = Pipeline(config)
        exit_code = pipeline.run()

        assert exit_code == 1

        # Check error output
        captured = capsys.readouterr()
        assert "Error:" in captured.err

        # Workspace should be preserved
        workspace_path = pipeline.workspace.path
        assert workspace_path.exists()

    @patch('plexilv_run.pipeline.check_all_tools')
    @patch('subprocess.run')
    def test_force_cleanup_on_maude_failure(self, mock_run, mock_check_tools, test_environment):
        """Test that --force-cleanup removes workspace even on Maude failure."""
        env = test_environment

        mock_check_tools.return_value = ("plx2maude", "psx2maude", "maude")

        def mock_subprocess(cmd, **kwargs):
            result = Mock()
            result.returncode = 0
            result.stdout = "mock output"
            result.stderr = ""

            if "maude" in cmd[0]:
                result.returncode = 1
                result.stderr = "Maude error"

            return result

        mock_run.side_effect = mock_subprocess

        config = Config(
            plan_path=env["plan"],
            script_path=env["script"],
            semantics_path=env["semantics"],
            plx2maude_path="plx2maude",
            psx2maude_path="psx2maude",
            maude_path="maude",
            maude_opts=[],
            maude_timeout=300,
            conversion_timeout=30,
            work_dir=env["workspace"],
            log_file=None,
            debug=False,
            cleanup=False,
            force_cleanup=True,  # Force cleanup
            relative_paths=False,
        )

        pipeline = Pipeline(config)
        exit_code = pipeline.run()

        assert exit_code == 1

        # Workspace SHOULD be cleaned up (force)
        workspace_path = pipeline.workspace.path
        assert not workspace_path.exists()


@pytest.mark.integration
class TestDebugMode:
    """Test debug mode behavior."""

    @patch('plexilv_run.pipeline.check_all_tools')
    @patch('subprocess.run')
    def test_debug_mode_creates_logs(self, mock_run, mock_check_tools, test_environment):
        """Test that debug mode creates log files for all tool executions."""
        env = test_environment

        mock_check_tools.return_value = ("plx2maude", "psx2maude", "maude")

        def mock_subprocess(cmd, **kwargs):
            result = Mock()
            result.returncode = 0
            result.stdout = "stdout content"
            result.stderr = "stderr content"
            return result

        mock_run.side_effect = mock_subprocess

        config = Config(
            plan_path=env["plan"],
            script_path=env["script"],
            semantics_path=env["semantics"],
            plx2maude_path="plx2maude",
            psx2maude_path="psx2maude",
            maude_path="maude",
            maude_opts=[],
            maude_timeout=300,
            conversion_timeout=30,
            work_dir=env["workspace"],
            log_file=None,
            debug=True,  # Debug mode
            cleanup=False,
            force_cleanup=False,
            relative_paths=False,
        )

        pipeline = Pipeline(config)
        exit_code = pipeline.run()

        assert exit_code == 0

        # Get actual workspace path
        workspace_path = pipeline.workspace.path

        # Check log files were created
        assert (workspace_path / "plx2maude.stdout.log").exists()
        assert (workspace_path / "plx2maude.stderr.log").exists()
        assert (workspace_path / "psx2maude.stdout.log").exists()
        assert (workspace_path / "psx2maude.stderr.log").exists()
        assert (workspace_path / "maude.stdout.log").exists()
        assert (workspace_path / "maude.stderr.log").exists()

        # Verify log content
        assert (workspace_path / "plx2maude.stdout.log").read_text() == "stdout content"