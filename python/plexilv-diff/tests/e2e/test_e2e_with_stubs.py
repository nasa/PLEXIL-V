"""End-to-end tests for plexilv-diff with stub executables."""

import pytest
from pathlib import Path
from click.testing import CliRunner

from plexilv_diff.cli import main
from plexilv_diff.config import Config
from plexilv_diff.pipeline import Pipeline


@pytest.mark.e2e
def test_full_workflow_no_differences(sample_plan, sample_scripts, stub_tools, tmp_path):
    """Test complete workflow with no differences between interpreters."""
    config = Config(
        plan=sample_plan,
        scripts=[sample_scripts[0]],
        plexilc=stub_tools['plexilc'],
        plexiltest=stub_tools['plexiltest'],
        plexilv_run=stub_tools['plexilv-run'],
        plexilog_diff=stub_tools['plexilog_diff'],
        work_dir=tmp_path / "workspace"
    )

    pipeline = Pipeline(config)
    result = pipeline.run()

    # Should succeed with no differences
    assert result.compilation_success is True
    assert len(result.test_results) == 1
    assert result.test_results[0].success is True
    assert result.test_results[0].diff_result is not None
    assert result.test_results[0].diff_result.identical is True
    assert result.exit_code == 0

    # Verify workspace structure
    workspace = result.workspace_path
    assert workspace.exists()
    assert (workspace / "debug.cfg").exists()
    assert (workspace / "test_plan.plx").exists()
    assert (workspace / "001").exists()
    assert (workspace / "001" / "test1.psx").exists()
    assert (workspace / "001" / "test_plan.plexil.log").exists()
    assert (workspace / "001" / "test_plan.plexilv.log").exists()
    assert (workspace / "001" / "test_plan.log.diff").exists()
    assert (workspace / "summary.txt").exists()


@pytest.mark.e2e
def test_full_workflow_with_differences(sample_plan, sample_scripts, stub_tools, tmp_path):
    """Test complete workflow with differences between interpreters."""
    config = Config(
        plan=sample_plan,
        scripts=[sample_scripts[0]],
        plexilc=stub_tools['plexilc'],
        plexiltest=stub_tools['plexiltest'],
        plexilv_run=stub_tools['plexilv_run_different'],  # Use different version
        plexilog_diff=stub_tools['plexilog_diff'],
        work_dir=tmp_path / "workspace"
    )

    pipeline = Pipeline(config)
    result = pipeline.run()

    # Should succeed but with differences
    assert result.compilation_success is True
    assert len(result.test_results) == 1
    assert result.test_results[0].success is True
    assert result.test_results[0].diff_result is not None
    assert result.test_results[0].diff_result.differ is True
    assert result.exit_code == 1  # Exit code 1 means differences found

    # Check diff file contains differences
    diff_file = result.workspace_path / "001" / "test_plan.log.diff"
    assert diff_file.exists()
    diff_content = diff_file.read_text()
    assert "Differences found" in diff_content or "TestNode" in diff_content or "DifferentNode" in diff_content


@pytest.mark.e2e
def test_plan_and_script_with_same_basename(stub_tools, tmp_path):
    """Plan and script sharing a basename (foo.ple / foo.pst) must work."""
    inputs = tmp_path / "inputs"
    inputs.mkdir()
    plan = inputs / "foo.ple"
    plan.write_text("// plan")
    script = inputs / "foo.pst"
    script.write_text("// script")

    config = Config(
        plan=plan,
        scripts=[script],
        plexilc=stub_tools['plexilc'],
        plexiltest=stub_tools['plexiltest'],
        plexilv_run=stub_tools['plexilv-run'],
        plexilog_diff=stub_tools['plexilog_diff'],
        work_dir=tmp_path / "workspace"
    )

    result = Pipeline(config).run()

    assert result.compilation_success is True
    assert result.exit_code == 0
    assert result.test_results[0].success is True

    workspace = result.workspace_path
    assert (workspace / "foo.plx").exists()
    assert (workspace / "001" / "foo.psx").exists()
    assert (workspace / "001" / "foo.plexil.log").exists()
    assert (workspace / "001" / "foo.plexilv.log").exists()


@pytest.mark.e2e
def test_multiple_tests(sample_plan, sample_scripts, stub_tools, tmp_path):
    """Test workflow with multiple test scripts."""
    config = Config(
        plan=sample_plan,
        scripts=sample_scripts,  # All 3 scripts
        plexilc=stub_tools['plexilc'],
        plexiltest=stub_tools['plexiltest'],
        plexilv_run=stub_tools['plexilv-run'],
        plexilog_diff=stub_tools['plexilog_diff'],
        work_dir=tmp_path / "workspace"
    )

    pipeline = Pipeline(config)
    result = pipeline.run()

    # All tests should succeed
    assert result.compilation_success is True
    assert len(result.test_results) == 3
    assert all(r.success for r in result.test_results)
    assert result.exit_code == 0

    # Verify all test directories exist
    workspace = result.workspace_path
    assert (workspace / "001").exists()
    assert (workspace / "002").exists()
    assert (workspace / "003").exists()


@pytest.mark.e2e
def test_cli_full_run(sample_plan, sample_scripts, stub_tools, tmp_path):
    """Test full CLI execution."""
    runner = CliRunner()

    result = runner.invoke(main, [
        '-p', str(sample_plan),
        '-s', str(sample_scripts[0]),
        '-s', str(sample_scripts[1]),
        '--plexilc', stub_tools['plexilc'],
        '--plexiltest', stub_tools['plexiltest'],
        '--plexilv-run', stub_tools['plexilv-run'],
        '--plexilog-diff', stub_tools['plexilog_diff'],
        '--work-dir', str(tmp_path / "cli-workspace"),
        '--quiet'
    ])

    assert result.exit_code == 0
    assert "Workspace:" in result.output

    # Verify workspace was created
    workspace = tmp_path / "cli-workspace"
    assert workspace.exists()
    assert (workspace / "summary.txt").exists()


@pytest.mark.e2e
def test_cleanup_on_success(sample_plan, sample_scripts, stub_tools, tmp_path):
    """Test that --cleanup removes workspace on success."""
    import os
    from pathlib import Path

    runner = CliRunner()

    work_dir = tmp_path / "cleanup-workspace"

    # Save current directory to restore after cleanup
    original_cwd = os.getcwd()

    result = runner.invoke(main, [
        '-p', str(sample_plan),
        '-s', str(sample_scripts[0]),
        '--plexilc', stub_tools['plexilc'],
        '--plexiltest', stub_tools['plexiltest'],
        '--plexilv-run', stub_tools['plexilv-run'],
        '--plexilog-diff', stub_tools['plexilog_diff'],
        '--work-dir', str(work_dir),
        '--cleanup',
        '--quiet'
    ])

    # Ensure we're back in a safe directory before checking cleanup
    try:
        os.chdir(original_cwd)
    except FileNotFoundError:
        # Original directory was deleted, go to project root
        os.chdir(Path(__file__).parent.parent.parent)

    assert result.exit_code == 0
    assert not work_dir.exists(), "Workspace should be cleaned up"


@pytest.mark.e2e
def test_already_compiled_files(tmp_path, stub_tools):
    """Test workflow with already compiled files (.plx and .psx)."""
    # Create pre-compiled files
    plan = tmp_path / "plan.plx"
    plan.write_text('<?xml version="1.0"?><PlexilPlan></PlexilPlan>')

    script = tmp_path / "test.psx"
    script.write_text('<?xml version="1.0"?><PLEXILScript></PLEXILScript>')

    config = Config(
        plan=plan,
        scripts=[script],
        plexilc=stub_tools['plexilc'],
        plexiltest=stub_tools['plexiltest'],
        plexilv_run=stub_tools['plexilv-run'],
        plexilog_diff=stub_tools['plexilog_diff'],
        work_dir=tmp_path / "workspace"
    )

    pipeline = Pipeline(config)
    result = pipeline.run()

    # Should succeed without compilation
    assert result.compilation_success is True
    assert result.exit_code == 0


@pytest.mark.e2e
def test_fail_fast(sample_plan, sample_scripts, stub_tools, tmp_path):
    """Test --fail-fast stops on first failure."""
    # We'd need a failing stub for this, but we can at least test the flag works
    config = Config(
        plan=sample_plan,
        scripts=sample_scripts,
        plexilc=stub_tools['plexilc'],
        plexiltest=stub_tools['plexiltest'],
        plexilv_run=stub_tools['plexilv-run'],
        plexilog_diff=stub_tools['plexilog_diff'],
        work_dir=tmp_path / "workspace",
        fail_fast=True
    )

    pipeline = Pipeline(config)
    result = pipeline.run()

    # With our passing stubs, should still succeed
    assert result.exit_code == 0


@pytest.mark.e2e
def test_custom_timeouts(sample_plan, sample_scripts, stub_tools, tmp_path):
    """Test custom timeout values."""
    config = Config(
        plan=sample_plan,
        scripts=[sample_scripts[0]],
        plexilc=stub_tools['plexilc'],
        plexiltest=stub_tools['plexiltest'],
        plexilv_run=stub_tools['plexilv-run'],
        plexilog_diff=stub_tools['plexilog_diff'],
        work_dir=tmp_path / "workspace",
        compilation_timeout=60,
        execution_timeout=600
    )

    pipeline = Pipeline(config)
    result = pipeline.run()

    assert result.exit_code == 0