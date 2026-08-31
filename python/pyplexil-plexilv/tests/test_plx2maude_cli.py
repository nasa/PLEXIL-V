"""Tests for plx2maude CLI tool.

This module tests the command-line interface tool that transpiles
PLEXIL XML files to PLEXIL-V format wrapped in Maude modules.
"""

import pytest
import tempfile
import sys
from pathlib import Path
from io import StringIO
from click.testing import CliRunner

from plexilv.plexil.translator.cli import (
    parse_plexil_plan,
    find_library_dependencies,
    load_libraries,
    main,
)
from plexil.core.v1.ast import PlexilPlan, Node, LibraryNodeCall
from xsdata.formats.dataclass.parsers import XmlParser
from xsdata.formats.dataclass.parsers.config import ParserConfig

# ====================
# Test Fixtures
# ====================


@pytest.fixture
def parser():
    """Create XML parser for tests."""
    config = ParserConfig(
        process_xinclude=False,
        fail_on_unknown_properties=False,
    )
    return XmlParser(config=config)


@pytest.fixture
def simple_plan_xml():
    """Simple PLEXIL plan without libraries."""
    return """<?xml version="1.0" encoding="UTF-8"?>
<PlexilPlan xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
  <Node NodeType="Empty">
    <NodeId>SimpleTest</NodeId>
  </Node>
</PlexilPlan>
"""


@pytest.fixture
def plan_with_variable_xml():
    """PLEXIL plan with variable declaration."""
    return """<?xml version="1.0" encoding="UTF-8"?>
<PlexilPlan xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
  <Node NodeType="Empty">
    <NodeId>WithVar</NodeId>
    <VariableDeclarations>
      <DeclareVariable>
        <Name>x</Name>
        <Type>Integer</Type>
        <InitialValue>
          <IntegerValue>42</IntegerValue>
        </InitialValue>
      </DeclareVariable>
    </VariableDeclarations>
  </Node>
</PlexilPlan>
"""


@pytest.fixture
def library_xml():
    """Library PLEXIL plan."""
    return """<?xml version="1.0" encoding="UTF-8"?>
<PlexilPlan xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
  <Node NodeType="Empty">
    <NodeId>MyLibrary</NodeId>
  </Node>
</PlexilPlan>
"""


@pytest.fixture
def plan_with_library_call_xml():
    """PLEXIL plan that calls a library."""
    return """<?xml version="1.0" encoding="UTF-8"?>
<PlexilPlan xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
  <Node NodeType="LibraryNodeCall">
    <NodeId>CallsLib</NodeId>
    <NodeBody>
      <LibraryNodeCall>
        <NodeId>MyLibrary</NodeId>
      </LibraryNodeCall>
    </NodeBody>
  </Node>
</PlexilPlan>
"""


# ====================
# parse_plexil_plan Tests
# ====================


def test_parse_simple_plan(parser, simple_plan_xml):
    """Test parsing a simple PLEXIL plan."""
    plan, node_id = parse_plexil_plan(simple_plan_xml, parser)

    assert isinstance(plan, PlexilPlan)
    assert node_id == "SimpleTest"
    assert plan.node is not None
    assert isinstance(plan.node, Node)


def test_parse_plan_with_variable(parser, plan_with_variable_xml):
    """Test parsing a plan with variable declarations."""
    plan, node_id = parse_plexil_plan(plan_with_variable_xml, parser)

    assert isinstance(plan, PlexilPlan)
    assert node_id == "WithVar"
    assert plan.node.variable_declarations is not None


def test_parse_empty_xml(parser):
    """Test parsing empty XML returns empty plan."""
    xml = """<?xml version="1.0" encoding="UTF-8"?>
<PlexilPlan xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
</PlexilPlan>
"""
    plan, node_id = parse_plexil_plan(xml, parser)

    assert isinstance(plan, PlexilPlan)
    assert node_id == "UNKNOWN"


def test_parse_plan_extracts_node_id(parser):
    """Test that node ID is correctly extracted."""
    xml = """<?xml version="1.0" encoding="UTF-8"?>
<PlexilPlan xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
  <Node NodeType="Empty">
    <NodeId>MyCustomName</NodeId>
  </Node>
</PlexilPlan>
"""
    plan, node_id = parse_plexil_plan(xml, parser)
    assert node_id == "MyCustomName"


# ====================
# find_library_dependencies Tests
# ====================


def test_find_library_dependencies_no_libraries(parser, simple_plan_xml):
    """Test finding dependencies in a plan with no library calls."""
    plan, _ = parse_plexil_plan(simple_plan_xml, parser)
    deps = find_library_dependencies(plan)

    assert isinstance(deps, set)
    assert len(deps) == 0


def test_find_library_dependencies_one_library(parser, plan_with_library_call_xml):
    """Test finding a single library dependency."""
    plan, _ = parse_plexil_plan(plan_with_library_call_xml, parser)
    deps = find_library_dependencies(plan)

    assert isinstance(deps, set)
    assert "MyLibrary" in deps


def test_find_library_dependencies_multiple_libraries(parser):
    """Test finding multiple library dependencies."""
    xml = """<?xml version="1.0" encoding="UTF-8"?>
<PlexilPlan xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
  <Node NodeType="NodeList">
    <NodeId>Root</NodeId>
    <NodeBody>
      <NodeList>
        <Node NodeType="LibraryNodeCall">
          <NodeId>Call1</NodeId>
          <NodeBody>
            <LibraryNodeCall>
              <NodeId>Lib1</NodeId>
            </LibraryNodeCall>
          </NodeBody>
        </Node>
        <Node NodeType="LibraryNodeCall">
          <NodeId>Call2</NodeId>
          <NodeBody>
            <LibraryNodeCall>
              <NodeId>Lib2</NodeId>
            </LibraryNodeCall>
          </NodeBody>
        </Node>
      </NodeList>
    </NodeBody>
  </Node>
</PlexilPlan>
"""
    plan, _ = parse_plexil_plan(xml, parser)
    deps = find_library_dependencies(plan)

    assert len(deps) == 2
    assert "Lib1" in deps
    assert "Lib2" in deps


def test_find_library_dependencies_handles_none():
    """Test that finding dependencies handles None input gracefully."""
    deps = find_library_dependencies(None)
    assert isinstance(deps, set)
    assert len(deps) == 0


# ====================
# load_libraries Tests
# ====================


def test_load_libraries_no_dependencies(parser, simple_plan_xml, tmp_path):
    """Test loading libraries when there are no dependencies."""
    plan, _ = parse_plexil_plan(simple_plan_xml, parser)
    libraries = load_libraries(tmp_path, plan, parser)

    assert isinstance(libraries, dict)
    assert len(libraries) == 0


def test_load_libraries_single_library(
    parser, plan_with_library_call_xml, library_xml, tmp_path
):
    """Test loading a single library dependency."""
    # Create library file
    lib_file = tmp_path / "MyLibrary.plx"
    lib_file.write_text(library_xml)

    # Parse main plan
    plan, _ = parse_plexil_plan(plan_with_library_call_xml, parser)

    # Load libraries
    libraries = load_libraries(tmp_path, plan, parser)

    assert "MyLibrary" in libraries
    assert isinstance(libraries["MyLibrary"], PlexilPlan)


def test_load_libraries_missing_file(
    parser, plan_with_library_call_xml, tmp_path, capsys
):
    """Test loading libraries when library file is missing."""
    plan, _ = parse_plexil_plan(plan_with_library_call_xml, parser)

    # Load libraries (file doesn't exist)
    libraries = load_libraries(tmp_path, plan, parser)

    # Should return empty dict and print warning
    assert len(libraries) == 0
    captured = capsys.readouterr()
    assert "Warning" in captured.err
    assert "MyLibrary" in captured.err


def test_load_libraries_transitive_dependencies(parser, tmp_path):
    """Test loading transitive library dependencies."""
    # Create library that depends on another library
    lib2_xml = """<?xml version="1.0" encoding="UTF-8"?>
<PlexilPlan xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
  <Node NodeType="Empty">
    <NodeId>Lib2</NodeId>
  </Node>
</PlexilPlan>
"""

    lib1_xml = """<?xml version="1.0" encoding="UTF-8"?>
<PlexilPlan xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
  <Node NodeType="LibraryNodeCall">
    <NodeId>Lib1</NodeId>
    <NodeBody>
      <LibraryNodeCall>
        <NodeId>Lib2</NodeId>
      </LibraryNodeCall>
    </NodeBody>
  </Node>
</PlexilPlan>
"""

    main_xml = """<?xml version="1.0" encoding="UTF-8"?>
<PlexilPlan xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
  <Node NodeType="LibraryNodeCall">
    <NodeId>Main</NodeId>
    <NodeBody>
      <LibraryNodeCall>
        <NodeId>Lib1</NodeId>
      </LibraryNodeCall>
    </NodeBody>
  </Node>
</PlexilPlan>
"""

    # Create library files
    (tmp_path / "Lib1.plx").write_text(lib1_xml)
    (tmp_path / "Lib2.plx").write_text(lib2_xml)

    # Parse main plan
    plan, _ = parse_plexil_plan(main_xml, parser)

    # Load libraries
    libraries = load_libraries(tmp_path, plan, parser)

    # Should load both Lib1 and Lib2 (transitive)
    assert "Lib1" in libraries
    assert "Lib2" in libraries
    assert len(libraries) == 2


def test_load_libraries_avoids_cycles(parser, tmp_path):
    """Test that load_libraries handles circular dependencies."""
    # Create two libraries that reference each other
    lib1_xml = """<?xml version="1.0" encoding="UTF-8"?>
<PlexilPlan xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
  <Node NodeType="LibraryNodeCall">
    <NodeId>Lib1</NodeId>
    <NodeBody>
      <LibraryNodeCall>
        <NodeId>Lib2</NodeId>
      </LibraryNodeCall>
    </NodeBody>
  </Node>
</PlexilPlan>
"""

    lib2_xml = """<?xml version="1.0" encoding="UTF-8"?>
<PlexilPlan xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
  <Node NodeType="LibraryNodeCall">
    <NodeId>Lib2</NodeId>
    <NodeBody>
      <LibraryNodeCall>
        <NodeId>Lib1</NodeId>
      </LibraryNodeCall>
    </NodeBody>
  </Node>
</PlexilPlan>
"""

    (tmp_path / "Lib1.plx").write_text(lib1_xml)
    (tmp_path / "Lib2.plx").write_text(lib2_xml)

    # Parse plan that calls Lib1
    main_xml = """<?xml version="1.0" encoding="UTF-8"?>
<PlexilPlan xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
  <Node NodeType="LibraryNodeCall">
    <NodeId>Main</NodeId>
    <NodeBody>
      <LibraryNodeCall>
        <NodeId>Lib1</NodeId>
      </LibraryNodeCall>
    </NodeBody>
  </Node>
</PlexilPlan>
"""

    plan, _ = parse_plexil_plan(main_xml, parser)
    libraries = load_libraries(tmp_path, plan, parser)

    # Should load both libraries without infinite loop
    assert "Lib1" in libraries
    assert "Lib2" in libraries


# ====================
# main() CLI Tests
# ====================


def test_main_missing_input_file():
    """Test main() with missing input file."""
    runner = CliRunner()
    result = runner.invoke(main, ["nonexistent.plx"])

    assert result.exit_code != 0
    assert "does not exist" in result.output


def test_main_simple_plan(simple_plan_xml, tmp_path):
    """Test main() with a simple plan."""
    # Create test file
    test_file = tmp_path / "test.plx"
    test_file.write_text(simple_plan_xml)

    runner = CliRunner()
    result = runner.invoke(main, [str(test_file)])

    assert result.exit_code == 0
    output = result.output

    # Check Maude module structure
    assert "mod SimpleTest-PLAN is" in output
    assert "protecting PLEXIL-V ." in output
    assert "op rootNode : -> Plexil ." in output
    assert "eq rootNode =" in output
    # Check for multi-line formatted empty node
    assert "empty(" in output
    assert "'SimpleTest," in output
    assert "nilocdecl," in output
    assert "endm" in output


def test_main_plan_with_variable(plan_with_variable_xml, tmp_path):
    """Test main() with a plan containing variables."""
    test_file = tmp_path / "test.plx"
    test_file.write_text(plan_with_variable_xml)

    runner = CliRunner()
    result = runner.invoke(main, [str(test_file)])

    assert result.exit_code == 0
    output = result.output

    # Should have variable declaration
    assert "(('x : val(42)))" in output
    # Should NOT have vardecls placeholder
    assert "vardecls" not in output


def test_main_plan_with_library(
    plan_with_library_call_xml, library_xml, tmp_path
):
    """Test main() with a plan that calls a library."""
    # Create files
    main_file = tmp_path / "main.plx"
    main_file.write_text(plan_with_library_call_xml)

    lib_file = tmp_path / "MyLibrary.plx"
    lib_file.write_text(library_xml)

    runner = CliRunner()
    result = runner.invoke(main, [str(main_file)])

    assert result.exit_code == 0
    output = result.output

    # Library should be inlined (multi-line format)
    assert "library(" in output
    assert "'CallsLib," in output
    assert "'MyLibrary" in output


def test_main_non_plx_extension_warns(simple_plan_xml, tmp_path):
    """Test that main() warns about non-.plx extension."""
    test_file = tmp_path / "test.xml"
    test_file.write_text(simple_plan_xml)

    runner = CliRunner()
    result = runner.invoke(main, [str(test_file)])

    assert result.exit_code == 0
    # Should emit warning but still work
    assert "Warning" in result.output or "Warning" in str(result.stderr_bytes)
    assert "mod SimpleTest-PLAN is" in result.output


def test_main_parse_error(tmp_path):
    """Test main() with invalid XML."""
    test_file = tmp_path / "bad.plx"
    test_file.write_text("<invalid>xml")

    runner = CliRunner()
    result = runner.invoke(main, [str(test_file)])

    assert result.exit_code != 0
    assert "Error" in result.output


# ====================
# Integration Tests
# ====================


def test_end_to_end_math_operations(tmp_path, parser):
    """Test end-to-end transpilation of math operations."""
    xml = """<?xml version="1.0" encoding="UTF-8"?>
<PlexilPlan xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
  <Node NodeType="Empty">
    <NodeId>MathTest</NodeId>
    <VariableDeclarations>
      <DeclareVariable>
        <Name>x</Name>
        <Type>Integer</Type>
        <InitialValue>
          <IntegerValue>-5</IntegerValue>
        </InitialValue>
      </DeclareVariable>
    </VariableDeclarations>
    <InvariantCondition>
      <EQNumeric>
        <ABS>
          <IntegerVariable>x</IntegerVariable>
        </ABS>
        <IntegerValue>5</IntegerValue>
      </EQNumeric>
    </InvariantCondition>
  </Node>
</PlexilPlan>
"""
    test_file = tmp_path / "math.plx"
    test_file.write_text(xml)

    runner = CliRunner()
    result = runner.invoke(main, [str(test_file)])

    assert result.exit_code == 0
    output = result.output

    # Check for absolute value function
    assert "func(absp,var('x))" in output
    # Check for variable declaration
    assert "(('x : val(-5)))" in output
    # Check for equality
    assert "_equ_" in output


def test_end_to_end_no_variable_declarations(tmp_path):
    """Test that nodes without variables output nilocdecl."""
    xml = """<?xml version="1.0" encoding="UTF-8"?>
<PlexilPlan xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
  <Node NodeType="Empty">
    <NodeId>NoVars</NodeId>
  </Node>
</PlexilPlan>
"""
    test_file = tmp_path / "novars.plx"
    test_file.write_text(xml)

    runner = CliRunner()
    result = runner.invoke(main, [str(test_file)])

    assert result.exit_code == 0
    output = result.output

    assert "nilocdecl," in output
    assert "vardecls" not in output


# ====================
# Indentation Tests
# ====================


def test_indent_default_2_spaces(tmp_path):
    """Test default 2-space indentation produces correctly formatted output."""
    xml = """<?xml version="1.0" encoding="UTF-8"?>
<PlexilPlan xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
  <Node NodeType="Empty">
    <NodeId>Test</NodeId>
  </Node>
</PlexilPlan>
"""
    test_file = tmp_path / "test.plx"
    test_file.write_text(xml)

    runner = CliRunner()
    result = runner.invoke(main, [str(test_file)])

    assert result.exit_code == 0

    # Extract just the transpiled node (between eq rootNode = and .)
    lines = result.output.split('\n')
    start_idx = next(i for i, line in enumerate(lines) if 'eq rootNode =' in line)
    end_idx = next(i for i, line in enumerate(lines[start_idx:], start_idx) if line.strip() == '.')

    # Get non-empty lines between eq rootNode = and .
    transpiled_lines = [line.rstrip() for line in lines[start_idx + 1:end_idx] if line.strip()]

    # Verify indentation structure (each line should start with correct spaces)
    expected_indents = [
        (0, "empty("),           # Level 0
        (2, "'Test,"),           # Level 1
        (2, "nilocdecl,"),       # Level 1
        (2, "(none)"),           # Level 1
        (0, ")")                 # Level 0
    ]

    for i, ((expected_spaces, expected_content), actual_line) in enumerate(zip(expected_indents, transpiled_lines)):
        # Count leading spaces
        leading_spaces = len(actual_line) - len(actual_line.lstrip())
        assert leading_spaces == expected_spaces, \
            f"Line {i}: Expected {expected_spaces} spaces but got {leading_spaces} for: {actual_line}"
        assert actual_line.lstrip().startswith(expected_content), \
            f"Line {i}: Expected content '{expected_content}' but got: {actual_line}"


def test_indent_4_spaces(tmp_path):
    """Test 4-space indentation produces correctly formatted output."""
    xml = """<?xml version="1.0" encoding="UTF-8"?>
<PlexilPlan xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
  <Node NodeType="Empty">
    <NodeId>Test</NodeId>
    <VariableDeclarations>
      <DeclareVariable>
        <Name>x</Name>
        <Type>Integer</Type>
        <InitialValue>
          <IntegerValue>42</IntegerValue>
        </InitialValue>
      </DeclareVariable>
    </VariableDeclarations>
  </Node>
</PlexilPlan>
"""
    test_file = tmp_path / "test.plx"
    test_file.write_text(xml)

    runner = CliRunner()
    result = runner.invoke(main, ["--indent", "4", str(test_file)])

    assert result.exit_code == 0

    # Extract transpiled node
    lines = result.output.split('\n')
    start_idx = next(i for i, line in enumerate(lines) if 'eq rootNode =' in line)
    end_idx = next(i for i, line in enumerate(lines[start_idx:], start_idx) if line.strip() == '.')

    # Get non-empty lines
    transpiled_lines = [line.rstrip() for line in lines[start_idx + 1:end_idx] if line.strip()]

    # Verify 4-space indentation structure
    expected_indents = [
        (0, "empty("),                   # Level 0
        (4, "'Test,"),                   # Level 1 (0 + 4)
        (4, "(('x : val(42))),"),        # Level 1
        (4, "(none)"),                   # Level 1
        (0, ")")                         # Level 0
    ]

    for i, ((expected_spaces, expected_content), actual_line) in enumerate(zip(expected_indents, transpiled_lines)):
        leading_spaces = len(actual_line) - len(actual_line.lstrip())
        assert leading_spaces == expected_spaces, \
            f"Line {i}: Expected {expected_spaces} spaces but got {leading_spaces} for: {actual_line}"
        assert actual_line.lstrip().startswith(expected_content), \
            f"Line {i}: Expected content '{expected_content}' but got: {actual_line}"


def test_indent_nested_nodes(tmp_path):
    """Test indentation with nested list nodes - each level should add indent."""
    xml = """<?xml version="1.0" encoding="UTF-8"?>
<PlexilPlan xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
  <Node NodeType="NodeList">
    <NodeId>Parent</NodeId>
    <NodeBody>
      <NodeList>
        <Node NodeType="Empty">
          <NodeId>Child1</NodeId>
        </Node>
        <Node NodeType="Empty">
          <NodeId>Child2</NodeId>
        </Node>
      </NodeList>
    </NodeBody>
  </Node>
</PlexilPlan>
"""
    test_file = tmp_path / "test.plx"
    test_file.write_text(xml)

    runner = CliRunner()
    result = runner.invoke(main, ["--indent", "2", str(test_file)])

    assert result.exit_code == 0

    # Extract transpiled node
    lines = result.output.split('\n')
    start_idx = next(i for i, line in enumerate(lines) if 'eq rootNode =' in line)
    end_idx = next(i for i, line in enumerate(lines[start_idx:], start_idx) if line.strip() == '.')

    transpiled_lines = [line.rstrip() for line in lines[start_idx + 1:end_idx] if line.strip()]

    # Verify nested structure has proper indentation levels
    # Level 0: list(
    # Level 1: 'Parent, nilocdecl, (none), (
    # Level 2: empty( for children
    # Level 3: child arguments
    expected_structure = [
        (0, "list("),              # Level 0
        (2, "'Parent,"),           # Level 1
        (2, "nilocdecl,"),         # Level 1
        (2, "(none),"),            # Level 1
        (2, "("),                  # Level 1 - children wrapper
        (4, "empty("),             # Level 2 - child 1
        (6, "'Child1,"),           # Level 3
        (6, "nilocdecl,"),         # Level 3
        (6, "(none)"),             # Level 3
        (4, ")"),                  # Level 2 - close child 1
        (4, "empty("),             # Level 2 - child 2
        (6, "'Child2,"),           # Level 3
        (6, "nilocdecl,"),         # Level 3
        (6, "(none)"),             # Level 3
        (4, ")"),                  # Level 2 - close child 2
        (2, ")"),                  # Level 1 - close children
        (0, ")")                   # Level 0 - close list
    ]

    assert len(transpiled_lines) == len(expected_structure), \
        f"Expected {len(expected_structure)} lines but got {len(transpiled_lines)}"

    for i, ((expected_spaces, expected_content), actual_line) in enumerate(zip(expected_structure, transpiled_lines)):
        leading_spaces = len(actual_line) - len(actual_line.lstrip())
        assert leading_spaces == expected_spaces, \
            f"Line {i}: Expected {expected_spaces} spaces but got {leading_spaces} for: {actual_line}"
        assert actual_line.lstrip().startswith(expected_content), \
            f"Line {i}: Expected content '{expected_content}' but got: {actual_line}"


def test_indent_0_spaces(tmp_path):
    """Test 0-space indentation produces no indentation."""
    xml = """<?xml version="1.0" encoding="UTF-8"?>
<PlexilPlan xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
  <Node NodeType="Empty">
    <NodeId>Test</NodeId>
  </Node>
</PlexilPlan>
"""
    test_file = tmp_path / "test.plx"
    test_file.write_text(xml)

    runner = CliRunner()
    result = runner.invoke(main, ["--indent", "0", str(test_file)])

    assert result.exit_code == 0

    # Extract transpiled node
    lines = result.output.split('\n')
    start_idx = next(i for i, line in enumerate(lines) if 'eq rootNode =' in line)
    end_idx = next(i for i, line in enumerate(lines[start_idx:], start_idx) if line.strip() == '.')

    transpiled_lines = [line.rstrip() for line in lines[start_idx + 1:end_idx] if line.strip()]

    # With 0 indentation, all lines should have no leading spaces
    for line in transpiled_lines:
        assert not line.startswith(' '), \
            f"Expected no indentation but found leading space in: {line}"
