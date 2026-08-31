"""Unit tests for configuration management."""

import os
from pathlib import Path
from unittest.mock import patch

import pytest

from plexilv_run.config import Config
from plexilv_run.exceptions import ConfigurationError


@pytest.mark.unit
class TestResolveSemantics:
    """Test semantics path resolution."""

    def test_direct_semantics_module_path(self, tmp_path):
        """Direct semantics module path takes highest priority."""
        semantics = tmp_path / "plexil-v.maude"
        semantics.touch()

        result = Config.resolve_semantics_path(
            semantics_module=str(semantics),
            plexilv_home=None,
        )

        assert result == semantics.resolve()

    def test_plexilv_home_option(self, tmp_path):
        """plexilv_home option is used if semantics_module not provided."""
        home = tmp_path / "plexilv"
        semantics_dir = home / "semantics" / "src"
        semantics_dir.mkdir(parents=True)
        semantics = semantics_dir / "plexil-v.maude"
        semantics.touch()

        result = Config.resolve_semantics_path(
            semantics_module=None,
            plexilv_home=str(home),
        )

        assert result == semantics.resolve()

    def test_plexilv_home_env_var(self, tmp_path, monkeypatch):
        """PLEXILV_HOME env var is used if no options provided."""
        home = tmp_path / "plexilv"
        semantics_dir = home / "semantics" / "src"
        semantics_dir.mkdir(parents=True)
        semantics = semantics_dir / "plexil-v.maude"
        semantics.touch()

        monkeypatch.setenv("PLEXILV_HOME", str(home))

        result = Config.resolve_semantics_path(
            semantics_module=None,
            plexilv_home=None,
        )

        assert result == semantics.resolve()

    def test_priority_direct_over_home(self, tmp_path):
        """Direct path takes priority over plexilv_home."""
        semantics = tmp_path / "custom" / "plexil-v.maude"
        semantics.parent.mkdir(parents=True)
        semantics.touch()

        home = tmp_path / "plexilv"
        semantics_dir = home / "semantics" / "src"
        semantics_dir.mkdir(parents=True)
        (semantics_dir / "plexil-v.maude").touch()

        result = Config.resolve_semantics_path(
            semantics_module=str(semantics),
            plexilv_home=str(home),
        )

        assert result == semantics.resolve()

    def test_priority_option_over_env(self, tmp_path, monkeypatch):
        """plexilv_home option takes priority over env var."""
        home_option = tmp_path / "plexilv-option"
        semantics_dir_option = home_option / "semantics" / "src"
        semantics_dir_option.mkdir(parents=True)
        semantics_option = semantics_dir_option / "plexil-v.maude"
        semantics_option.touch()

        home_env = tmp_path / "plexilv-env"
        semantics_dir_env = home_env / "semantics" / "src"
        semantics_dir_env.mkdir(parents=True)
        semantics_env = semantics_dir_env / "plexil-v.maude"
        semantics_env.touch()

        monkeypatch.setenv("PLEXILV_HOME", str(home_env))

        result = Config.resolve_semantics_path(
            semantics_module=None,
            plexilv_home=str(home_option),
        )

        assert result == semantics_option.resolve()

    def test_no_configuration_raises(self, monkeypatch):
        """Raise error if no configuration provided."""
        monkeypatch.delenv("PLEXILV_HOME", raising=False)

        with pytest.raises(ConfigurationError, match="PLEXILV_HOME not set"):
            Config.resolve_semantics_path(
                semantics_module=None,
                plexilv_home=None,
            )

    def test_direct_path_not_exists(self, tmp_path):
        """Raise error if direct semantics path doesn't exist."""
        semantics = tmp_path / "nonexistent.maude"

        with pytest.raises(ConfigurationError, match="Semantics file not found"):
            Config.resolve_semantics_path(
                semantics_module=str(semantics),
                plexilv_home=None,
            )

    def test_home_path_not_exists(self, tmp_path):
        """Raise error if semantics file doesn't exist in home."""
        home = tmp_path / "plexilv"
        home.mkdir()

        with pytest.raises(ConfigurationError, match="Semantics file not found"):
            Config.resolve_semantics_path(
                semantics_module=None,
                plexilv_home=str(home),
            )

    def test_direct_path_not_readable(self, tmp_path):
        """Raise error if direct semantics file is not readable."""
        semantics = tmp_path / "plexil-v.maude"
        semantics.touch()

        with patch('plexilv_run.config.os.access', return_value=False):
            with pytest.raises(ConfigurationError, match="Cannot read semantics file"):
                Config.resolve_semantics_path(
                    semantics_module=str(semantics),
                    plexilv_home=None,
                )

    def test_home_path_not_readable(self, tmp_path):
        """Raise error if semantics file in home is not readable."""
        home = tmp_path / "plexilv"
        semantics_dir = home / "semantics" / "src"
        semantics_dir.mkdir(parents=True)
        semantics = semantics_dir / "plexil-v.maude"
        semantics.touch()

        with patch('plexilv_run.config.os.access', return_value=False):
            with pytest.raises(ConfigurationError, match="Cannot read semantics file"):
                Config.resolve_semantics_path(
                    semantics_module=None,
                    plexilv_home=str(home),
                )


@pytest.mark.unit
class TestConfigValidation:
    """Test configuration validation."""

    def create_valid_config(self, tmp_path):
        """Helper to create a valid config for testing."""
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
            plx2maude_path="plx2maude",
            psx2maude_path="psx2maude",
            maude_path="maude",
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

    def test_valid_config(self, tmp_path):
        """Valid configuration should not raise."""
        config = self.create_valid_config(tmp_path)
        config.validate()  # Should not raise

    def test_negative_maude_timeout(self, tmp_path):
        """Negative maude timeout should raise."""
        config = self.create_valid_config(tmp_path)
        config.maude_timeout = -1

        with pytest.raises(ConfigurationError, match="Maude timeout must be positive"):
            config.validate()

    def test_zero_maude_timeout(self, tmp_path):
        """Zero maude timeout should raise."""
        config = self.create_valid_config(tmp_path)
        config.maude_timeout = 0

        with pytest.raises(ConfigurationError, match="Maude timeout must be positive"):
            config.validate()

    def test_negative_conversion_timeout(self, tmp_path):
        """Negative conversion timeout should raise."""
        config = self.create_valid_config(tmp_path)
        config.conversion_timeout = -1

        with pytest.raises(ConfigurationError, match="Conversion timeout must be positive"):
            config.validate()

    def test_zero_conversion_timeout(self, tmp_path):
        """Zero conversion timeout should raise."""
        config = self.create_valid_config(tmp_path)
        config.conversion_timeout = 0

        with pytest.raises(ConfigurationError, match="Conversion timeout must be positive"):
            config.validate()

    def test_both_cleanup_flags(self, tmp_path):
        """Both cleanup flags set should raise."""
        config = self.create_valid_config(tmp_path)
        config.cleanup = True
        config.force_cleanup = True

        with pytest.raises(ConfigurationError, match="Cannot specify both"):
            config.validate()

    def test_existing_log_file(self, tmp_path):
        """Existing log file should raise."""
        config = self.create_valid_config(tmp_path)
        log_file = tmp_path / "output.log"
        log_file.touch()
        config.log_file = log_file

        with pytest.raises(ConfigurationError, match="Log file already exists"):
            config.validate()

    def test_nonexistent_log_file(self, tmp_path):
        """Non-existent log file should not raise."""
        config = self.create_valid_config(tmp_path)
        config.log_file = tmp_path / "output.log"
        config.validate()  # Should not raise

    def test_existing_work_dir(self, tmp_path):
        """Existing work directory should raise."""
        config = self.create_valid_config(tmp_path)
        work_dir = tmp_path / "workspace"
        work_dir.mkdir()
        config.work_dir = work_dir

        with pytest.raises(ConfigurationError, match="Workspace directory already exists"):
            config.validate()

    def test_nonexistent_work_dir(self, tmp_path):
        """Non-existent work directory should not raise."""
        config = self.create_valid_config(tmp_path)
        config.work_dir = tmp_path / "workspace"
        config.validate()  # Should not raise

    def test_none_work_dir(self, tmp_path):
        """None work directory (auto-generate) should not raise."""
        config = self.create_valid_config(tmp_path)
        config.work_dir = None
        config.validate()  # Should not raise

    def test_cleanup_alone_valid(self, tmp_path):
        """cleanup flag alone should be valid."""
        config = self.create_valid_config(tmp_path)
        config.cleanup = True
        config.force_cleanup = False
        config.validate()  # Should not raise

    def test_force_cleanup_alone_valid(self, tmp_path):
        """force_cleanup flag alone should be valid."""
        config = self.create_valid_config(tmp_path)
        config.cleanup = False
        config.force_cleanup = True
        config.validate()  # Should not raise