"""Tests for PLEXIL compiler."""

import pytest
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock, call
from plumbum.commands.processes import ProcessTimedOut

from plexilv_diff.compiler import Compiler
from plexilv_diff.exceptions import CompilationError, TimeoutError as DiffPlexilvTimeoutError


@pytest.fixture(autouse=True)
def mock_plumbum_local():
    """Mock plumbum local to avoid requiring external tools in tests."""
    with patch('plexilv_diff.compiler.local') as mock_local:
        mock_local.__getitem__.return_value = MagicMock()
        yield mock_local


@pytest.fixture
def sample_ple_file(tmp_path):
    """Create a sample .ple file."""
    ple = tmp_path / "plan.ple"
    ple.write_text("// Sample PLEXIL plan")
    return ple


@pytest.fixture
def sample_pst_file(tmp_path):
    """Create a sample .pst file."""
    pst = tmp_path / "test.pst"
    pst.write_text("// Sample PLEXIL script")
    return pst


@pytest.fixture
def sample_plx_file(tmp_path):
    """Create a sample .plx file."""
    plx = tmp_path / "plan.plx"
    plx.write_text("<?xml version='1.0'?><PlexilPlan/>")
    return plx


@pytest.fixture
def sample_psx_file(tmp_path):
    """Create a sample .psx file."""
    psx = tmp_path / "test.psx"
    psx.write_text("<?xml version='1.0'?><PLEXILScript/>")
    return psx


def test_compiler_init_defaults():
    """Test compiler initialization with defaults."""
    compiler = Compiler()

    assert compiler.plexilc_path == "plexilc"
    assert compiler.timeout == 30
    assert compiler.additional_flags == []
    assert compiler.output_log is None


def test_compiler_init_custom():
    """Test compiler initialization with custom values."""
    log_path = Path("/tmp/compile.log")
    compiler = Compiler(
        plexilc_path="/usr/local/bin/plexilc",
        timeout=60,
        additional_flags="--quiet --debug",
        output_log=log_path
    )

    assert compiler.plexilc_path == "/usr/local/bin/plexilc"
    assert compiler.timeout == 60
    assert compiler.additional_flags == ["--quiet", "--debug"]
    assert compiler.output_log == log_path


def test_compiler_parse_flags_empty():
    """Test parsing empty flags."""
    compiler = Compiler()

    assert compiler._parse_flags("") == []
    assert compiler._parse_flags("   ") == []


def test_compiler_parse_flags_single():
    """Test parsing single flag."""
    compiler = Compiler()

    assert compiler._parse_flags("--quiet") == ["--quiet"]


def test_compiler_parse_flags_multiple():
    """Test parsing multiple flags."""
    compiler = Compiler()

    flags = compiler._parse_flags("--flag1 --flag2 value --flag3")
    assert flags == ["--flag1", "--flag2", "value", "--flag3"]


@patch('plexilv_diff.compiler.local')
def test_compile_file_success(mock_local, sample_ple_file, tmp_path):
    """Test successful compilation."""
    # Create expected output file
    output_file = sample_ple_file.with_suffix('.plx')
    output_file.write_text("<?xml version='1.0'?><PlexilPlan/>")

    # Mock the command chain: local['plexilc'][args].run()
    mock_run_result = MagicMock()
    mock_run_result.run.return_value = (0, "Compilation successful", "")

    mock_plexilc = MagicMock()
    mock_plexilc.__getitem__.return_value = mock_run_result

    mock_local.__getitem__.return_value = mock_plexilc

    # Mock cwd context manager
    mock_cwd = MagicMock()
    mock_local.cwd.return_value = mock_cwd

    compiler = Compiler()
    result = compiler.compile_file(sample_ple_file)

    assert result == output_file
    mock_run_result.run.assert_called_once()


@patch('plexilv_diff.compiler.local')
def test_compile_file_with_additional_flags(mock_local, sample_ple_file, tmp_path):
    """Test compilation with additional flags."""
    # Create expected output file
    output_file = sample_ple_file.with_suffix('.plx')
    output_file.write_text("<?xml version='1.0'?><PlexilPlan/>")

    # Mock the command chain
    mock_run_result = MagicMock()
    mock_run_result.run.return_value = (0, "", "")

    mock_plexilc = MagicMock()
    mock_plexilc.__getitem__.return_value = mock_run_result

    mock_local.__getitem__.return_value = mock_plexilc
    mock_local.cwd.return_value = MagicMock()

    compiler = Compiler(additional_flags="--quiet --debug")
    result = compiler.compile_file(sample_ple_file)

    # Verify flags were passed
    call_args = mock_plexilc.__getitem__.call_args[0][0]
    assert "--quiet" in call_args
    assert "--debug" in call_args
    assert str(sample_ple_file) in call_args


@patch('plexilv_diff.compiler.local')
def test_compile_file_nonzero_exit(mock_local, sample_ple_file):
    """Test compilation failure with non-zero exit code."""
    # Mock the command chain
    mock_run_result = MagicMock()
    mock_run_result.run.return_value = (1, "", "Syntax error on line 42")

    mock_plexilc = MagicMock()
    mock_plexilc.__getitem__.return_value = mock_run_result

    mock_local.__getitem__.return_value = mock_plexilc
    mock_local.cwd.return_value = MagicMock()

    compiler = Compiler()

    with pytest.raises(CompilationError, match="Compilation failed with exit code 1"):
        compiler.compile_file(sample_ple_file)


@patch('plexilv_diff.compiler.local')
def test_compile_file_timeout(mock_local, sample_ple_file):
    """Test compilation timeout."""
    # Mock the command chain
    mock_run_result = MagicMock()
    # ProcessTimedOut takes (argv, retcode) as positional args
    mock_run_result.run.side_effect = ProcessTimedOut(["plexilc", "plan.ple"], 124)

    mock_plexilc = MagicMock()
    mock_plexilc.__getitem__.return_value = mock_run_result

    mock_local.__getitem__.return_value = mock_plexilc
    mock_local.cwd.return_value = MagicMock()

    compiler = Compiler(timeout=5)

    with pytest.raises(DiffPlexilvTimeoutError, match="timed out after 5s"):
        compiler.compile_file(sample_ple_file)


@patch('plexilv_diff.compiler.local')
def test_compile_file_output_not_created(mock_local, sample_ple_file):
    """Test error when output file is not created."""
    # Mock the command chain - success but no output file created
    mock_run_result = MagicMock()
    mock_run_result.run.return_value = (0, "", "")

    mock_plexilc = MagicMock()
    mock_plexilc.__getitem__.return_value = mock_run_result

    mock_local.__getitem__.return_value = mock_plexilc
    mock_local.cwd.return_value = MagicMock()

    compiler = Compiler()

    with pytest.raises(CompilationError, match="output file not created"):
        compiler.compile_file(sample_ple_file)


def test_compile_file_input_not_exists():
    """Test error when input file doesn't exist."""
    compiler = Compiler()

    with pytest.raises(CompilationError, match="does not exist"):
        compiler.compile_file(Path("/nonexistent/file.ple"))


def test_compile_file_invalid_extension(tmp_path):
    """Test error with invalid input file extension."""
    compiler = Compiler()

    invalid_file = tmp_path / "file.txt"
    invalid_file.write_text("content")

    with pytest.raises(CompilationError, match="Invalid input file extension"):
        compiler.compile_file(invalid_file)


@patch('plexilv_diff.compiler.local')
def test_compile_file_logs_output(mock_local, sample_ple_file, tmp_path):
    """Test that stdout/stderr are logged to output file."""
    log_file = tmp_path / "compile.log"

    # Create expected output file
    output_file = sample_ple_file.with_suffix('.plx')
    output_file.write_text("<?xml version='1.0'?><PlexilPlan/>")

    # Mock the command chain
    mock_run_result = MagicMock()
    mock_run_result.run.return_value = (0, "stdout content", "stderr content")

    mock_plexilc = MagicMock()
    mock_plexilc.__getitem__.return_value = mock_run_result

    mock_local.__getitem__.return_value = mock_plexilc
    mock_local.cwd.return_value = MagicMock()

    compiler = Compiler(output_log=log_file)
    compiler.compile_file(sample_ple_file)

    # Check log file contains output
    assert log_file.exists()
    log_content = log_file.read_text()
    assert "stdout content" in log_content
    assert "stderr content" in log_content
    assert "STDOUT" in log_content
    assert "STDERR" in log_content


@patch('plexilv_diff.compiler.local')
def test_compile_plan_ple(mock_local, sample_ple_file, tmp_path):
    """Test compile_plan with .ple file."""
    # Create expected output file
    output_file = sample_ple_file.with_suffix('.plx')
    output_file.write_text("<?xml version='1.0'?><PlexilPlan/>")

    # Mock the command chain
    mock_run_result = MagicMock()
    mock_run_result.run.return_value = (0, "", "")

    mock_plexilc = MagicMock()
    mock_plexilc.__getitem__.return_value = mock_run_result

    mock_local.__getitem__.return_value = mock_plexilc
    mock_local.cwd.return_value = MagicMock()

    compiler = Compiler()
    result = compiler.compile_plan(sample_ple_file, tmp_path)

    assert result == output_file


def test_compile_plan_plx(sample_plx_file, tmp_path):
    """Test compile_plan with already compiled .plx file."""
    compiler = Compiler()

    # Should return the file as-is without compilation
    result = compiler.compile_plan(sample_plx_file, tmp_path)

    assert result == sample_plx_file


def test_compile_plan_invalid_extension(tmp_path):
    """Test compile_plan with invalid extension."""
    compiler = Compiler()

    invalid_file = tmp_path / "plan.txt"
    invalid_file.write_text("content")

    with pytest.raises(CompilationError, match="Invalid plan file extension"):
        compiler.compile_plan(invalid_file, tmp_path)


@patch('plexilv_diff.compiler.local')
def test_compile_script_pst(mock_local, sample_pst_file, tmp_path):
    """Test compile_script with .pst file."""
    # Create expected output file
    output_file = sample_pst_file.with_suffix('.psx')
    output_file.write_text("<?xml version='1.0'?><PLEXILScript/>")

    # Mock the command chain
    mock_run_result = MagicMock()
    mock_run_result.run.return_value = (0, "", "")

    mock_plexilc = MagicMock()
    mock_plexilc.__getitem__.return_value = mock_run_result

    mock_local.__getitem__.return_value = mock_plexilc
    mock_local.cwd.return_value = MagicMock()

    compiler = Compiler()
    result = compiler.compile_script(sample_pst_file, tmp_path)

    assert result == output_file


def test_compile_script_psx(sample_psx_file, tmp_path):
    """Test compile_script with already compiled .psx file."""
    compiler = Compiler()

    # Should return the file as-is without compilation
    result = compiler.compile_script(sample_psx_file, tmp_path)

    assert result == sample_psx_file


def test_compile_script_invalid_extension(tmp_path):
    """Test compile_script with invalid extension."""
    compiler = Compiler()

    invalid_file = tmp_path / "script.txt"
    invalid_file.write_text("content")

    with pytest.raises(CompilationError, match="Invalid script file extension"):
        compiler.compile_script(invalid_file, tmp_path)


@patch('plexilv_diff.compiler.local')
def test_compile_file_working_directory(mock_local, sample_ple_file, tmp_path):
    """Test that compilation runs from correct working directory."""
    # Create expected output file
    output_file = sample_ple_file.with_suffix('.plx')
    output_file.write_text("<?xml version='1.0'?><PlexilPlan/>")

    # Mock the command chain
    mock_run_result = MagicMock()
    mock_run_result.run.return_value = (0, "", "")

    mock_plexilc = MagicMock()
    mock_plexilc.__getitem__.return_value = mock_run_result

    mock_local.__getitem__.return_value = mock_plexilc

    mock_cwd = MagicMock()
    mock_local.cwd.return_value = mock_cwd

    custom_dir = tmp_path / "custom"
    custom_dir.mkdir()

    compiler = Compiler()
    compiler.compile_file(sample_ple_file, working_dir=custom_dir)

    # Verify cwd was called with the custom directory
    mock_local.cwd.assert_called_once_with(custom_dir)