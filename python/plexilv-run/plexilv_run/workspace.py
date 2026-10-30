"""Workspace management for plexilv."""

import shutil
from datetime import datetime
from pathlib import Path

from plexilv_run.exceptions import WorkspaceError


class Workspace:
    """Manages workspace directory for plexilv execution.

    The workspace is named run-YYYY-MM-DD-HH-MM-SS by default.

    The workspace contains:
    - Converted .maude files (plan and script)
    - Generated run.maude file
    - Log files (if debug mode enabled)

    Attributes:
        path: Path to the workspace directory
        debug: Whether debug mode is enabled
        created: Whether the workspace has been created
    """

    def __init__(self, base_dir: Path | None, debug: bool = False):
        """
        Initialize workspace manager.

        Args:
            base_dir: Custom workspace directory, or None to auto-generate
            debug: Enable debug mode (affects logging behavior)
        """
        self.debug = debug
        self.created = False

        if base_dir:
            self.path = base_dir
        else:
            # Auto-generate timestamped directory name
            timestamp = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
            self.path = Path.cwd() / f"run-{timestamp}"

    def create(self) -> None:
        """
        Create the workspace directory.

        Raises:
            WorkspaceError: If directory already exists or cannot be created
        """
        try:
            # Check if path exists
            if self.path.exists():
                raise WorkspaceError(f"Workspace already exists: {self.path}")

            # Try to create the directory
            self.path.mkdir(parents=True, exist_ok=False)
            self.created = True
        except PermissionError as e:
            raise WorkspaceError(f"Cannot create workspace {self.path}: {e}") from e
        except OSError as e:
            raise WorkspaceError(f"Cannot create workspace {self.path}: {e}") from e

    def get_plan_maude_path(self, plan_stem: str) -> Path:
        """
        Get path for the plan .maude file.

        Args:
            plan_stem: Plan filename without extension (e.g., 'MyPlan')

        Returns:
            Path to <plan_stem>.plan.maude in workspace

        Note:
            The role suffix keeps plan and script outputs distinct when both
            files share a basename, and avoids clobbering run.maude.
        """
        return self.path / f"{plan_stem}.plan.maude"

    def get_script_maude_path(self, script_stem: str) -> Path:
        """
        Get path for the script .maude file.

        Args:
            script_stem: Script filename without extension (e.g., 'test_script')

        Returns:
            Path to <script_stem>.script.maude in workspace
        """
        return self.path / f"{script_stem}.script.maude"

    def get_run_maude_path(self) -> Path:
        """
        Get path for the run.maude file.

        Returns:
            Path to run.maude in workspace
        """
        return self.path / "run.maude"

    def get_tool_log_paths(self, tool_name: str) -> tuple[Path, Path]:
        """
        Get paths for tool stdout and stderr log files.

        Args:
            tool_name: Name of the tool (e.g., 'plx2maude', 'maude')

        Returns:
            Tuple of (stdout_path, stderr_path)
        """
        stdout_path = self.path / f"{tool_name}.stdout.log"
        stderr_path = self.path / f"{tool_name}.stderr.log"
        return stdout_path, stderr_path

    def cleanup(self) -> None:
        """
        Clean up workspace directory.

        Raises:
            WorkspaceError: If cleanup fails
        """
        if not self.created:
            # Workspace was never created, nothing to clean
            return

        if not self.path.exists():
            # Already cleaned up or never existed
            return

        try:
            shutil.rmtree(self.path)
        except OSError as e:
            raise WorkspaceError(f"Failed to cleanup workspace {self.path}: {e}") from e

    def __enter__(self) -> "Workspace":
        """Context manager entry."""
        self.create()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """Context manager exit - cleanup handled explicitly by caller."""
        # Don't auto-cleanup - let caller control cleanup behavior
        # based on success/failure and cleanup flags
        pass