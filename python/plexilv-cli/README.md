# plexilv-cli

Unified command-line interface for PLEXIL-V verification tools.

## Overview

`plexilv-cli` is a coordinator package that provides a single entry point for multiple PLEXIL verification tools:

- **run** (or **test**): Execute PLEXIL plans using the PLEXIL-V formal semantics
- **diff**: Compare PLEXIL plan executions across different interpreters
- **plexilog**: Parse PLEXIL Executive debug logs to JSON
- **plexilog-maude**: Parse PLEXIL-V/Maude execution logs to JSON
- **plexilog-diff**: Compare execution logs from different interpreters
- **help**: Display help information

## Installation

### For Users

```bash
pip install plexilv-cli
```

This will automatically install all required dependencies:
- `plexilv-run` - PLEXIL plan execution tool
- `plexilv-diff` - PLEXIL execution comparison tool
- `plexilv-log` - Log parsing and comparison tools

### For Development

```bash
# Clone the repository
cd plexilv-cli

# Install in development mode
pip install -e .

# Install development dependencies
pip install -e ".[dev]"
```

## Quick Start

### Running a PLEXIL Plan

Execute a PLEXIL plan using the PLEXIL-V formal semantics:

```bash
plexilv run -p plan.plx -s script.psx
```

The `test` command is an alias for `run`:

```bash
plexilv test -p plan.plx -s script.psx
```

For additional options, use `--help`:

```bash
plexilv run --help
```

### Comparing Plan Executions

Compare the execution of a PLEXIL plan across different interpreters: PLEXIL-V formal semantics and the official PLEXIL test interpreter (plexiltest).

```bash
plexilv diff -p plan.plx -s script.psx
```

Compare across multiple script files:

```bash
plexilv diff -p plan.plx -s script1.psx -s script2.psx
```

For additional options, use `--help`:

```bash
plexilv diff --help
```

### Getting Help

Display the main help message:

```bash
plexilv --help
```

Or use the help subcommand:

```bash
plexilv help
```

Display help for a specific command:

```bash
plexilv help run
plexilv help test
plexilv help diff
```

Display version information:

```bash
plexilv --version
```

## Architecture

### Package Structure

```
plexilv-cli/
├── plexilv_cli/
│   ├── __init__.py          # Package metadata
│   └── cli.py               # CLI coordinator
├── tests/
│   ├── unit/
│   │   └── test_cli.py      # Unit tests
│   └── __init__.py
├── pyproject.toml           # Project configuration
└── README.md                # This file
```

### How It Works

`plexilv-cli` acts as a light wrapper that:

1. Imports Click command groups from `plexilv-run` and `plexilv-diff`
2. Registers them as subcommands under the main `plexilv` command
3. Creates the `run`/`test` alias for convenience
4. Provides a `help` subcommand for easy access to help information
5. Delegates all functionality to the underlying packages

Each subcommand package maintains its own:
- Implementation and logic
- Comprehensive test suite
- Independent CLI entry point

This design allows both standalone usage and coordinated CLI access.

## Commands

### `plexilv run` / `plexilv test`

Execute PLEXIL plans using the PLEXIL-V formal semantics.

**Provided by:** `plexilv-run`

**Common options:**
- `-p, --plan TEXT`: Path to PLEXIL plan file (required)
- `-s, --script TEXT`: Path to PLEXIL script file (required)

**Additional options:**

Both `run` and `test` support additional options beyond `-p` and `-s`. Use `--help` to see the complete list of available options:

```bash
plexilv run --help
```

**Examples:**
```bash
# Basic execution
plexilv run -p my_plan.plx -s my_script.psx

# Using test alias
plexilv test -p my_plan.plx -s my_script.psx

# View all available options
plexilv run --help
```

### `plexilv diff`

Compare PLEXIL plan executions across different interpreters.

**Provided by:** `plexilv-diff`

**Purpose:**

The `diff` command executes a PLEXIL plan using two different interpreters and compares their outputs:
1. **PLEXIL-V formal semantics interpreter** - For formal verification
2. **Official PLEXIL test interpreter** (plexiltest) - For comparison

This is useful for validating that the formal semantics implementation matches the behavior of the official PLEXIL interpreter.

**Common options:**
- `-p, --plan TEXT`: Path to PLEXIL plan file (required)
- `-s, --script TEXT`: Path to PLEXIL script file (can be used multiple times)

**Multiple script files:**

You can compare executions across multiple script files by specifying `-s` multiple times:

```bash
plexilv diff -p plan.plx -s script1.psx -s script2.psx
```

**Additional options:**

The `diff` command supports additional options. Use `--help` to see the complete list of available options:

```bash
plexilv diff --help
```

**Examples:**
```bash
# Compare execution with single script
plexilv diff -p my_plan.plx -s my_script.psx

# Compare execution with multiple scripts
plexilv diff -p my_plan.plx -s script1.psx -s script2.psx

# View all available options
plexilv diff --help
```

### `plexilv plexilog`

Parse PLEXIL Executive debug logs to JSON format.

**Provided by:** `plexilv-log`

**Purpose:**

Parses verbose debug logs from the PLEXIL Executive (`plexiltest`) and outputs structured JSON representing the execution trace (macros → micros → transitions).

**Usage:**
```bash
# Parse log file
plexilv plexilog executive.log

# Parse from stdin
cat executive.log | plexilv plexilog

# Output to file
plexilv plexilog executive.log > trace.json

# Compact JSON output
plexilv plexilog executive.log --compact
```

**Options:**
- `LOG_FILE`: Path to log file (optional, reads from stdin if not provided)
- `--pretty/--compact`: Pretty-print or compact JSON (default: pretty)

### `plexilv plexilog-maude`

Parse PLEXIL-V/Maude execution logs to JSON format.

**Provided by:** `plexilv-log`

**Purpose:**

Parses execution logs from the PLEXIL-V formal semantics interpreter (Maude) and outputs structured JSON.

**Usage:**
```bash
# Parse log file
plexilv plexilog-maude maude.log

# Parse from stdin
cat maude.log | plexilv plexilog-maude

# Output to file
plexilv plexilog-maude maude.log > trace.json

# Compact JSON output
plexilv plexilog-maude maude.log --compact
```

**Options:**
- `LOG_FILE`: Path to log file (optional, reads from stdin if not provided)
- `--pretty/--compact`: Pretty-print or compact JSON (default: pretty)

### `plexilv plexilog-diff`

Compare execution logs from PLEXIL Executive and PLEXIL-V.

**Provided by:** `plexilv-log`

**Purpose:**

Compares two execution log files and reports differences. Uses exit codes to indicate equality: 0 (equal), 1 (different), 2 (error).

**Usage:**
```bash
# Compare logs (shows "EQ" if equal, report if different)
plexilv plexilog-diff executive.log maude.log

# Verbose output with detailed differences
plexilv plexilog-diff executive.log maude.log --verbose

# JSON output format
plexilv plexilog-diff executive.log maude.log --json
```

**Options:**
- Two log file paths (required)
- `--verbose, -v`: Show detailed differences
- `--json, -j`: Output in JSON format

**Exit codes:**
- `0`: Traces are equal
- `1`: Traces differ
- `2`: Error occurred

**Output formats:**
- Default: "EQ" if equal, summary report if different
- Verbose: Detailed comparison report with all differences
- JSON: Machine-readable JSON format

### `plexilv help`

Display help information for the main command or specific subcommands.

**Usage:**
```bash
# Show main help
plexilv help

# Show help for specific command
plexilv help run
plexilv help test
plexilv help diff
```

**Examples:**
```bash
plexilv help              # Show main help
plexilv help run          # Show run command help
plexilv help diff         # Show diff command help
plexilv help invalid-cmd  # Error: unknown command
```

## Testing

### Run All Tests

```bash
pytest tests/
```

### Run with Coverage

```bash
pytest tests/ --cov=plexilv_cli --cov-report=html
```

### Run Specific Test Class

```bash
pytest tests/unit/test_cli.py::TestCommandRegistration -v
```

### Test Coverage

Unit tests verify:
- ✅ CLI help text and version display
- ✅ All subcommands are properly registered
- ✅ `run` and `test` are correct aliases
- ✅ `diff` command is registered separately
- ✅ `help` command works for all subcommands
- ✅ Command invocation works correctly
- ✅ Invalid commands are handled properly
- ✅ PLEXIL-V formal semantics are mentioned in help text

## Development

### Required Python Version

Python 3.9 or later

### Dependencies

**Core:**
- `click>=8.0` - CLI framework
- `plexilv-run` - Run/test subcommand
- `plexilv-diff` - Diff subcommand

**Development (optional):**
- `pytest>=7.0` - Testing framework
- `pytest-cov>=4.0` - Coverage reporting
- `pytest-mock>=3.0` - Mocking support

### Code Style

Optional tools for development:
- `black` - Code formatting
- `ruff` - Linting
- `mypy` - Type checking

### Project Configuration

All pytest configuration is in `pyproject.toml`:

```toml
[tool.setuptools]
packages = ["plexilv_cli"]

[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]
markers = [
    "unit: Unit tests (fast, mocked dependencies)",
]
```

## Contributing

When adding new features or subcommands:

1. Ensure the new subcommand package exports a Click command group
2. Update `plexilv_cli/cli.py` to import and register the command
3. Add integration tests to verify the command is properly registered
4. Update this README with command documentation and examples
5. Update the `help` command docstring if adding new subcommands

## Support

For issues with specific subcommands, refer to their respective repositories:
- `plexilv-cli` coordinator issues: Check this repository
- `plexilv-run` issues: Check the plexilv-run repository
- `plexilv-diff` issues: Check the plexilv-diff repository
- ...