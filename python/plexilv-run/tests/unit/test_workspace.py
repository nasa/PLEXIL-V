"""Unit tests for workspace management."""

import os
from datetime import datetime
from pathlib import Path
from unittest.mock import patch, MagicMock

import pytest

from plexilv_run.exceptions import WorkspaceError
from plexilv_run.workspace import Workspace


@pytest.mark.unit
class TestWorkspaceInit:
    """Test workspace initialization."""

    def test_custom_base_dir(self, tmp_path):
        """Custom base directory should be used."""
        custom_dir = tmp_path / "custom-workspace"
        workspace = Workspace(custom_dir)

        assert workspace.path == custom_dir
        assert workspace.debug is False
        assert workspace.created is False

    def test_auto_generate_name(self, tmp_path, monkeypatch):
        """Auto-generated name should have timestamp format."""
        # Change to tmp_path so workspace is created there
        monkeypatch.chdir(tmp_path)

        workspace = Workspace(None)

        # Check it's in current directory
        assert workspace.path.parent == Path.cwd()

        # Check name format: run-YYYY-MM-DD-HH-MM-SS
        name = workspace.path.name
        assert name.startswith("run-")

        # Parse timestamp part
        timestamp_str = name.removeprefix("run-")
        try:
            datetime.strptime(timestamp_str, "%Y-%m-%d-%H-%M-%S")
        except ValueError:
            pytest.fail(f"Invalid timestamp format: {timestamp_str}")

    def test_debug_mode(self, tmp_path):
        """Debug mode should be stored."""
        workspace = Workspace(tmp_path / "workspace", debug=True)
        assert workspace.debug is True


@pytest.mark.unit
class TestWorkspaceCreate:
    """Test workspace creation."""

    def test_create_new_directory(self, tmp_path):
        """Should create new directory."""
        workspace_dir = tmp_path / "new-workspace"
        workspace = Workspace(workspace_dir)

        assert not workspace_dir.exists()

        workspace.create()

        assert workspace_dir.exists()
        assert workspace_dir.is_dir()
        assert workspace.created is True

    def test_create_with_parents(self, tmp_path):
        """Should create parent directories if needed."""
        workspace_dir = tmp_path / "parent" / "child" / "workspace"
        workspace = Workspace(workspace_dir)

        workspace.create()

        assert workspace_dir.exists()
        assert workspace_dir.is_dir()

    def test_create_existing_directory(self, tmp_path):
        """Should raise error if directory already exists."""
        workspace_dir = tmp_path / "existing"
        workspace_dir.mkdir()

        workspace = Workspace(workspace_dir)

        with pytest.raises(WorkspaceError, match="Workspace already exists"):
            workspace.create()

    def test_create_twice(self, tmp_path):
        """Creating twice should raise error."""
        workspace = Workspace(tmp_path / "workspace")

        workspace.create()

        with pytest.raises(WorkspaceError, match="Workspace already exists"):
            workspace.create()

    def test_create_no_permission(self, tmp_path):
        """Should raise error if cannot create directory."""
        workspace = Workspace(tmp_path / "workspace")

        with patch.object(Path, 'mkdir', side_effect=PermissionError("Permission denied")):
            with pytest.raises(WorkspaceError, match="Cannot create workspace"):
                workspace.create()


@pytest.mark.unit
class TestWorkspacePathGetters:
    """Test workspace path getter methods."""

    def test_get_plan_maude_path(self, tmp_path):
        """Should return correct plan .maude path."""
        workspace = Workspace(tmp_path / "workspace")
        path = workspace.get_plan_maude_path("MyPlan")

        assert path == workspace.path / "MyPlan.maude"

    def test_get_script_maude_path(self, tmp_path):
        """Should return correct script .maude path."""
        workspace = Workspace(tmp_path / "workspace")
        path = workspace.get_script_maude_path("test_script")

        assert path == workspace.path / "test_script.maude"

    def test_get_run_maude_path(self, tmp_path):
        """Should return correct run.maude path."""
        workspace = Workspace(tmp_path / "workspace")
        path = workspace.get_run_maude_path()

        assert path == workspace.path / "run.maude"

    def test_get_tool_log_paths(self, tmp_path):
        """Should return correct tool log paths."""
        workspace = Workspace(tmp_path / "workspace")
        stdout_path, stderr_path = workspace.get_tool_log_paths("plx2maude")

        assert stdout_path == workspace.path / "plx2maude.stdout.log"
        assert stderr_path == workspace.path / "plx2maude.stderr.log"

    def test_different_tool_names(self, tmp_path):
        """Should handle different tool names."""
        workspace = Workspace(tmp_path / "workspace")

        stdout1, stderr1 = workspace.get_tool_log_paths("plx2maude")
        stdout2, stderr2 = workspace.get_tool_log_paths("psx2maude")
        stdout3, stderr3 = workspace.get_tool_log_paths("maude")

        assert stdout1.name == "plx2maude.stdout.log"
        assert stdout2.name == "psx2maude.stdout.log"
        assert stdout3.name == "maude.stdout.log"


@pytest.mark.unit
class TestWorkspaceCleanup:
    """Test workspace cleanup."""

    def test_cleanup_removes_workspace(self, tmp_path):
        """Should cleanup workspace."""
        workspace = Workspace(tmp_path / "workspace")
        workspace.create()

        assert workspace.path.exists()

        workspace.cleanup()

        assert not workspace.path.exists()

    def test_cleanup_with_files(self, tmp_path):
        """Should cleanup workspace with files inside."""
        workspace = Workspace(tmp_path / "workspace")
        workspace.create()

        # Create some files
        (workspace.path / "plan.maude").write_text("content")
        (workspace.path / "script.maude").write_text("content")
        (workspace.path / "run.maude").write_text("content")

        workspace.cleanup()

        assert not workspace.path.exists()

    def test_cleanup_not_created(self, tmp_path):
        """Cleanup should handle workspace that was never created."""
        workspace = Workspace(tmp_path / "workspace")
        # Don't call create()

        workspace.cleanup()  # Should not raise

    def test_cleanup_already_removed(self, tmp_path):
        """Cleanup should handle already-removed workspace."""
        workspace = Workspace(tmp_path / "workspace")
        workspace.create()

        # Manually remove it
        workspace.path.rmdir()

        workspace.cleanup()  # Should not raise

    def test_cleanup_nested_directories(self, tmp_path):
        """Should cleanup workspace with nested directories."""
        workspace = Workspace(tmp_path / "workspace")
        workspace.create()

        # Create nested structure
        subdir = workspace.path / "subdir"
        subdir.mkdir()
        (subdir / "file.txt").write_text("content")

        workspace.cleanup()

        assert not workspace.path.exists()


@pytest.mark.unit
class TestWorkspaceContextManager:
    """Test workspace context manager."""

    def test_context_manager_creates_workspace(self, tmp_path):
        """Context manager should create workspace."""
        workspace_dir = tmp_path / "workspace"

        with Workspace(workspace_dir) as workspace:
            assert workspace.path.exists()
            assert workspace.created is True

    def test_context_manager_returns_self(self, tmp_path):
        """Context manager should return workspace instance."""
        workspace_dir = tmp_path / "workspace"

        with Workspace(workspace_dir) as workspace:
            assert isinstance(workspace, Workspace)
            assert workspace.path == workspace_dir

    def test_context_manager_no_auto_cleanup(self, tmp_path):
        """Context manager should not auto-cleanup (caller controls cleanup)."""
        workspace_dir = tmp_path / "workspace"

        with Workspace(workspace_dir) as workspace:
            pass

        # Workspace should still exist after context exit
        assert workspace_dir.exists()

    def test_context_manager_with_exception(self, tmp_path):
        """Context manager should not cleanup on exception."""
        workspace_dir = tmp_path / "workspace"

        try:
            with Workspace(workspace_dir) as workspace:
                raise ValueError("Test exception")
        except ValueError:
            pass

        # Workspace should still exist after exception
        assert workspace_dir.exists()

    def test_manual_cleanup_after_context(self, tmp_path):
        """Should allow manual cleanup after context exit."""
        workspace_dir = tmp_path / "workspace"

        with Workspace(workspace_dir) as workspace:
            pass

        assert workspace_dir.exists()

        # Manual cleanup (no arguments now)
        workspace.cleanup()

        assert not workspace_dir.exists()