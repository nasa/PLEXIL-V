"""End-to-end tests with mock tool executables."""

import stat
import sys
from pathlib import Path

import pytest

from plexilv_run.config import Config
from plexilv_run.pipeline import Pipeline


@pytest.fixture
def mock_tools_dir(tmp_path):
    """Create mock executable tools for testing."""
    tools_dir = tmp_path / "mock_tools"
    tools_dir.mkdir()

    # Create mock plx2maude
    plx2maude = tools_dir / "plx2maude"
    plx2maude.write_text("""#!/usr/bin/env python3
import sys
# Read input file (not used, but validates it exists)
input_file = sys.argv[1]
# Output mock Maude module
print("mod TestPlan-PLAN is")
print("  --- Plan module content")
print("endm")
sys.exit(0)
""")
    plx2maude.chmod(plx2maude.stat().st_mode | stat.S_IEXEC)

    # Create mock psx2maude
    psx2maude = tools_dir / "psx2maude"
    psx2maude.write_text("""#!/usr/bin/env python3
import sys
# Read input file (not used, but validates it exists)
input_file = sys.argv[1]
# Output mock Maude module
print("mod INPUT is")
print("  --- Input module content")
print("endm")
sys.exit(0)
""")
    psx2maude.chmod(psx2maude.stat().st_mode | stat.S_IEXEC)

    # Create mock maude
    maude = tools_dir / "maude"
    maude.write_text("""#!/usr/bin/env python3
import sys
# Simple mock that just succeeds
print("Maude output", file=sys.stdout)
print("Result: success", file=sys.stderr)
sys.exit(0)
""")
    maude.chmod(maude.stat().st_mode | stat.S_IEXEC)

    return {
        "dir": tools_dir,
        "plx2maude": plx2maude,
        "psx2maude": psx2maude,
        "maude": maude,
    }


@pytest.fixture
def test_files(tmp_path):
    """Create test input files."""
    # Create plan file
    plan = tmp_path / "TestPlan.plx"
    plan.write_text("""<?xml version="1.0" encoding="UTF-8"?>
<PlexilPlan xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
  <Node NodeType="Empty" epx="Sequence">
    <NodeId>TestPlan</NodeId>
  </Node>
</PlexilPlan>
""")

    # Create script file
    script = tmp_path / "test_script.psx"
    script.write_text("""<?xml version="1.0" encoding="UTF-8"?>
<PLEXILScript>
  <InitialState>
  </InitialState>
</PLEXILScript>
""")

    # Create PLEXILV_HOME structure
    plexilv_home = tmp_path / "plexilv"
    semantics_dir = plexilv_home / "semantics" / "src"
    semantics_dir.mkdir(parents=True)
    semantics = semantics_dir / "plexil-v.maude"
    semantics.write_text("""*** PLEXIL-V Maude Semantics ***
mod PLEXIL-SEMANTICS is
  --- Semantics definitions
endm
""")

    return {
        "plan": plan,
        "script": script,
        "semantics": semantics,
        "plexilv_home": plexilv_home,
    }


@pytest.mark.e2e
class TestCompleteE2E:
    """End-to-end tests with real mock tool execution."""

    def test_successful_execution_with_mock_tools(self, mock_tools_dir, test_files, tmp_path):
        """Test complete execution with mock tools."""
        # Create config
        workspace = tmp_path / "workspace"

        config = Config(
            plan_path=test_files["plan"],
            script_path=test_files["script"],
            semantics_path=test_files["semantics"],
            plx2maude_path=str(mock_tools_dir["plx2maude"]),
            psx2maude_path=str(mock_tools_dir["psx2maude"]),
            maude_path=str(mock_tools_dir["maude"]),
            maude_opts=[],
            maude_timeout=300,
            conversion_timeout=30,
            work_dir=workspace,
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

        # Verify workspace exists
        assert pipeline.workspace.path.exists()

        # Verify converted files were created
        assert (pipeline.workspace.path / "TestPlan.plan.maude").exists()
        assert (pipeline.workspace.path / "test_script.script.maude").exists()

        # Verify run.maude was created
        run_maude_path = pipeline.workspace.path / "run.maude"
        assert run_maude_path.exists()

        # Verify run.maude content
        run_maude_content = run_maude_path.read_text()
        assert "load" in run_maude_content
        assert "TestPlan-PLAN" in run_maude_content
        assert "protecting INPUT" in run_maude_content
        assert "rew run(compile(rootNode,input))" in run_maude_content
        assert "q" in run_maude_content

        # Verify converted file content
        plan_maude = (pipeline.workspace.path / "TestPlan.plan.maude").read_text()
        assert "mod TestPlan-PLAN is" in plan_maude

        script_maude = (pipeline.workspace.path / "test_script.script.maude").read_text()
        assert "mod INPUT is" in script_maude

    def test_with_cleanup_flag(self, mock_tools_dir, test_files, tmp_path):
        """Test that cleanup flag removes workspace on success."""
        workspace = tmp_path / "workspace"

        config = Config(
            plan_path=test_files["plan"],
            script_path=test_files["script"],
            semantics_path=test_files["semantics"],
            plx2maude_path=str(mock_tools_dir["plx2maude"]),
            psx2maude_path=str(mock_tools_dir["psx2maude"]),
            maude_path=str(mock_tools_dir["maude"]),
            maude_opts=[],
            maude_timeout=300,
            conversion_timeout=30,
            work_dir=workspace,
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
        assert not pipeline.workspace.path.exists()

    def test_with_debug_mode(self, mock_tools_dir, test_files, tmp_path):
        """Test that debug mode creates log files."""
        workspace = tmp_path / "workspace"

        config = Config(
            plan_path=test_files["plan"],
            script_path=test_files["script"],
            semantics_path=test_files["semantics"],
            plx2maude_path=str(mock_tools_dir["plx2maude"]),
            psx2maude_path=str(mock_tools_dir["psx2maude"]),
            maude_path=str(mock_tools_dir["maude"]),
            maude_opts=[],
            maude_timeout=300,
            conversion_timeout=30,
            work_dir=workspace,
            log_file=None,
            debug=True,  # Enable debug
            cleanup=False,
            force_cleanup=False,
            relative_paths=False,
        )

        pipeline = Pipeline(config)
        exit_code = pipeline.run()

        assert exit_code == 0

        # Verify log files were created
        ws_path = pipeline.workspace.path
        assert (ws_path / "plx2maude.stdout.log").exists()
        assert (ws_path / "plx2maude.stderr.log").exists()
        assert (ws_path / "psx2maude.stdout.log").exists()
        assert (ws_path / "psx2maude.stderr.log").exists()
        assert (ws_path / "maude.stdout.log").exists()
        assert (ws_path / "maude.stderr.log").exists()

    def test_with_relative_paths(self, mock_tools_dir, test_files, tmp_path):
        """Test with relative paths in run.maude."""
        workspace = tmp_path / "workspace"

        config = Config(
            plan_path=test_files["plan"],
            script_path=test_files["script"],
            semantics_path=test_files["semantics"],
            plx2maude_path=str(mock_tools_dir["plx2maude"]),
            psx2maude_path=str(mock_tools_dir["psx2maude"]),
            maude_path=str(mock_tools_dir["maude"]),
            maude_opts=[],
            maude_timeout=300,
            conversion_timeout=30,
            work_dir=workspace,
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
        run_maude = (pipeline.workspace.path / "run.maude").read_text()
        assert "TestPlan.plan.maude" in run_maude
        assert "test_script.script.maude" in run_maude

    def test_with_log_file(self, mock_tools_dir, test_files, tmp_path):
        """Test output redirection to log file."""
        workspace = tmp_path / "workspace"
        log_file = tmp_path / "output.log"

        config = Config(
            plan_path=test_files["plan"],
            script_path=test_files["script"],
            semantics_path=test_files["semantics"],
            plx2maude_path=str(mock_tools_dir["plx2maude"]),
            psx2maude_path=str(mock_tools_dir["psx2maude"]),
            maude_path=str(mock_tools_dir["maude"]),
            maude_opts=[],
            maude_timeout=300,
            conversion_timeout=30,
            work_dir=workspace,
            log_file=log_file,
            debug=False,
            cleanup=False,
            force_cleanup=False,
            relative_paths=False,
        )

        pipeline = Pipeline(config)
        exit_code = pipeline.run()

        assert exit_code == 0

        # Verify log file was created and contains stderr
        assert log_file.exists()
        log_content = log_file.read_text()
        assert "Result: success" in log_content


@pytest.mark.e2e
class TestE2EFailureScenarios:
    """Test failure scenarios with mock tools."""

    def test_plx2maude_failure(self, tmp_path, test_files, capsys):
        """Test plx2maude failure is handled correctly."""
        tools_dir = tmp_path / "mock_tools"
        tools_dir.mkdir()

        # Create failing plx2maude
        plx2maude = tools_dir / "plx2maude"
        plx2maude.write_text("""#!/usr/bin/env python3
import sys
print("Parse error: Invalid XML", file=sys.stderr)
sys.exit(1)
""")
        plx2maude.chmod(plx2maude.stat().st_mode | stat.S_IEXEC)

        # Create successful psx2maude
        psx2maude = tools_dir / "psx2maude"
        psx2maude.write_text("""#!/usr/bin/env python3
import sys
print("mod INPUT is endm")
sys.exit(0)
""")
        psx2maude.chmod(psx2maude.stat().st_mode | stat.S_IEXEC)

        # Create mock maude (shouldn't be called)
        maude = tools_dir / "maude"
        maude.write_text("""#!/usr/bin/env python3
import sys
print("Should not reach here")
sys.exit(0)
""")
        maude.chmod(maude.stat().st_mode | stat.S_IEXEC)

        workspace = tmp_path / "workspace"

        config = Config(
            plan_path=test_files["plan"],
            script_path=test_files["script"],
            semantics_path=test_files["semantics"],
            plx2maude_path=str(plx2maude),
            psx2maude_path=str(psx2maude),
            maude_path=str(maude),
            maude_opts=[],
            maude_timeout=300,
            conversion_timeout=30,
            work_dir=workspace,
            log_file=None,
            debug=False,
            cleanup=False,
            force_cleanup=False,
            relative_paths=False,
        )

        pipeline = Pipeline(config)
        exit_code = pipeline.run()

        assert exit_code == 1

        # Check error was reported
        captured = capsys.readouterr()
        assert "plx2maude failed" in captured.err
        assert "Parse error: Invalid XML" in captured.err

    def test_maude_failure(self, tmp_path, test_files, capsys):
        """Test Maude execution failure is handled correctly."""
        tools_dir = tmp_path / "mock_tools"
        tools_dir.mkdir()

        # Create successful plx2maude
        plx2maude = tools_dir / "plx2maude"
        plx2maude.write_text("""#!/usr/bin/env python3
import sys
print("mod TestPlan-PLAN is endm")
sys.exit(0)
""")
        plx2maude.chmod(plx2maude.stat().st_mode | stat.S_IEXEC)

        # Create successful psx2maude
        psx2maude = tools_dir / "psx2maude"
        psx2maude.write_text("""#!/usr/bin/env python3
import sys
print("mod INPUT is endm")
sys.exit(0)
""")
        psx2maude.chmod(psx2maude.stat().st_mode | stat.S_IEXEC)

        # Create failing maude
        maude = tools_dir / "maude"
        maude.write_text("""#!/usr/bin/env python3
import sys
print("Execution error", file=sys.stderr)
sys.exit(1)
""")
        maude.chmod(maude.stat().st_mode | stat.S_IEXEC)

        workspace = tmp_path / "workspace"

        config = Config(
            plan_path=test_files["plan"],
            script_path=test_files["script"],
            semantics_path=test_files["semantics"],
            plx2maude_path=str(plx2maude),
            psx2maude_path=str(psx2maude),
            maude_path=str(maude),
            maude_opts=[],
            maude_timeout=300,
            conversion_timeout=30,
            work_dir=workspace,
            log_file=None,
            debug=False,
            cleanup=False,
            force_cleanup=False,
            relative_paths=False,
        )

        pipeline = Pipeline(config)
        exit_code = pipeline.run()

        assert exit_code == 1

        # Check error was reported
        captured = capsys.readouterr()
        assert "Error:" in captured.err

    def test_conversion_timeout(self, tmp_path, test_files, capsys):
        """Test that conversion timeout works."""
        tools_dir = tmp_path / "mock_tools"
        tools_dir.mkdir()

        # Create slow plx2maude (sleeps longer than timeout)
        plx2maude = tools_dir / "plx2maude"
        plx2maude.write_text("""#!/usr/bin/env python3
import sys
import time
time.sleep(60)  # Sleep longer than timeout
print("mod TestPlan-PLAN is endm")
sys.exit(0)
""")
        plx2maude.chmod(plx2maude.stat().st_mode | stat.S_IEXEC)

        # Create successful psx2maude
        psx2maude = tools_dir / "psx2maude"
        psx2maude.write_text("""#!/usr/bin/env python3
import sys
print("mod INPUT is endm")
sys.exit(0)
""")
        psx2maude.chmod(psx2maude.stat().st_mode | stat.S_IEXEC)

        # Create mock maude
        maude = tools_dir / "maude"
        maude.write_text("""#!/usr/bin/env python3
import sys
print("success")
sys.exit(0)
""")
        maude.chmod(maude.stat().st_mode | stat.S_IEXEC)

        workspace = tmp_path / "workspace"

        config = Config(
            plan_path=test_files["plan"],
            script_path=test_files["script"],
            semantics_path=test_files["semantics"],
            plx2maude_path=str(plx2maude),
            psx2maude_path=str(psx2maude),
            maude_path=str(maude),
            maude_opts=[],
            maude_timeout=300,
            conversion_timeout=2,  # Short timeout
            work_dir=workspace,
            log_file=None,
            debug=False,
            cleanup=False,
            force_cleanup=False,
            relative_paths=False,
        )

        pipeline = Pipeline(config)
        exit_code = pipeline.run()

        assert exit_code == 1

        # Check timeout error was reported
        captured = capsys.readouterr()
        assert "timed out" in captured.err


@pytest.mark.e2e
class TestE2EWithMaudeOpts:
    """Test passing custom options to Maude."""

    def test_custom_maude_options(self, mock_tools_dir, test_files, tmp_path):
        """Test that custom Maude options are passed correctly."""
        # Create a maude mock that echoes its arguments
        maude = mock_tools_dir["dir"] / "maude_verbose"
        maude.write_text("""#!/usr/bin/env python3
import sys
# Echo all arguments to stderr for verification
print(f"Args: {sys.argv[1:]}", file=sys.stderr)
sys.exit(0)
""")
        maude.chmod(maude.stat().st_mode | stat.S_IEXEC)

        workspace = tmp_path / "workspace"

        config = Config(
            plan_path=test_files["plan"],
            script_path=test_files["script"],
            semantics_path=test_files["semantics"],
            plx2maude_path=str(mock_tools_dir["plx2maude"]),
            psx2maude_path=str(mock_tools_dir["psx2maude"]),
            maude_path=str(maude),
            maude_opts=["-verbose", "-custom-flag"],
            maude_timeout=300,
            conversion_timeout=30,
            work_dir=workspace,
            log_file=None,
            debug=False,
            cleanup=False,
            force_cleanup=False,
            relative_paths=False,
        )

        pipeline = Pipeline(config)
        exit_code = pipeline.run()

        assert exit_code == 0


@pytest.mark.e2e
class TestE2EModuleNames:
    """Test module name generation with various filenames."""

    def test_plan_with_underscores(self, mock_tools_dir, tmp_path):
        """Test that plan filenames with underscores are converted correctly."""
        # Create plan with underscores
        plan = tmp_path / "test_plan_v2.plx"
        plan.write_text('<?xml version="1.0"?><PlexilPlan></PlexilPlan>')

        script = tmp_path / "script.psx"
        script.write_text('<?xml version="1.0"?><PLEXILScript></PLEXILScript>')

        # Create semantics
        plexilv_home = tmp_path / "plexilv"
        semantics_dir = plexilv_home / "semantics" / "src"
        semantics_dir.mkdir(parents=True)
        semantics = semantics_dir / "plexil-v.maude"
        semantics.write_text("*** semantics ***")

        workspace = tmp_path / "workspace"

        config = Config(
            plan_path=plan,
            script_path=script,
            semantics_path=semantics,
            plx2maude_path=str(mock_tools_dir["plx2maude"]),
            psx2maude_path=str(mock_tools_dir["psx2maude"]),
            maude_path=str(mock_tools_dir["maude"]),
            maude_opts=[],
            maude_timeout=300,
            conversion_timeout=30,
            work_dir=workspace,
            log_file=None,
            debug=False,
            cleanup=False,
            force_cleanup=False,
            relative_paths=False,
        )

        pipeline = Pipeline(config)
        exit_code = pipeline.run()

        assert exit_code == 0

        # Verify module name in run.maude has dashes not underscores
        run_maude = (pipeline.workspace.path / "run.maude").read_text()
        assert "protecting test-plan-v2-PLAN" in run_maude
        assert "test_plan_v2-PLAN" not in run_maude


@pytest.mark.e2e
@pytest.mark.slow
class TestE2ETimeouts:
    """Test timeout scenarios (marked as slow)."""

    def test_maude_timeout(self, tmp_path, test_files, capsys):
        """Test that Maude timeout works correctly."""
        tools_dir = tmp_path / "mock_tools"
        tools_dir.mkdir()

        # Create successful converters
        plx2maude = tools_dir / "plx2maude"
        plx2maude.write_text("""#!/usr/bin/env python3
import sys
print("mod TestPlan-PLAN is endm")
sys.exit(0)
""")
        plx2maude.chmod(plx2maude.stat().st_mode | stat.S_IEXEC)

        psx2maude = tools_dir / "psx2maude"
        psx2maude.write_text("""#!/usr/bin/env python3
import sys
print("mod INPUT is endm")
sys.exit(0)
""")
        psx2maude.chmod(psx2maude.stat().st_mode | stat.S_IEXEC)

        # Create slow maude
        maude = tools_dir / "maude"
        maude.write_text("""#!/usr/bin/env python3
import sys
import time
time.sleep(60)  # Sleep longer than timeout
print("success")
sys.exit(0)
""")
        maude.chmod(maude.stat().st_mode | stat.S_IEXEC)

        workspace = tmp_path / "workspace"

        config = Config(
            plan_path=test_files["plan"],
            script_path=test_files["script"],
            semantics_path=test_files["semantics"],
            plx2maude_path=str(plx2maude),
            psx2maude_path=str(psx2maude),
            maude_path=str(maude),
            maude_opts=[],
            maude_timeout=2,  # Short timeout
            conversion_timeout=30,
            work_dir=workspace,
            log_file=None,
            debug=False,
            cleanup=False,
            force_cleanup=False,
            relative_paths=False,
        )

        pipeline = Pipeline(config)
        exit_code = pipeline.run()

        assert exit_code == 1

        # Check timeout error was reported
        captured = capsys.readouterr()
        assert "timed out" in captured.err


@pytest.mark.e2e
class TestE2EWorkspaceManagement:
    """Test workspace management scenarios."""

    def test_auto_generated_workspace_name(self, mock_tools_dir, test_files, tmp_path, monkeypatch):
        """Test auto-generated workspace with timestamp."""
        # Change to tmp_path so workspace is created there
        monkeypatch.chdir(tmp_path)

        config = Config(
            plan_path=test_files["plan"],
            script_path=test_files["script"],
            semantics_path=test_files["semantics"],
            plx2maude_path=str(mock_tools_dir["plx2maude"]),
            psx2maude_path=str(mock_tools_dir["psx2maude"]),
            maude_path=str(mock_tools_dir["maude"]),
            maude_opts=[],
            maude_timeout=300,
            conversion_timeout=30,
            work_dir=None,  # Auto-generate
            log_file=None,
            debug=False,
            cleanup=False,
            force_cleanup=False,
            relative_paths=False,
        )

        pipeline = Pipeline(config)
        exit_code = pipeline.run()

        assert exit_code == 0

        # Verify workspace was created with timestamp format
        workspace_name = pipeline.workspace.path.name
        assert workspace_name.startswith("run-")

        # Verify it's in current directory (tmp_path)
        assert pipeline.workspace.path.parent == tmp_path

    def test_workspace_collision_error(self, mock_tools_dir, test_files, tmp_path):
        """Test that existing workspace causes error."""
        workspace = tmp_path / "workspace"
        workspace.mkdir()  # Pre-create workspace

        config = Config(
            plan_path=test_files["plan"],
            script_path=test_files["script"],
            semantics_path=test_files["semantics"],
            plx2maude_path=str(mock_tools_dir["plx2maude"]),
            psx2maude_path=str(mock_tools_dir["psx2maude"]),
            maude_path=str(mock_tools_dir["maude"]),
            maude_opts=[],
            maude_timeout=300,
            conversion_timeout=30,
            work_dir=workspace,
            log_file=None,
            debug=False,
            cleanup=False,
            force_cleanup=False,
            relative_paths=False,
        )

        pipeline = Pipeline(config)
        exit_code = pipeline.run()

        assert exit_code == 1