"""Test library name sanitization to prevent path traversal attacks."""

import pytest
from pathlib import Path
from plexilv.plexil.translator.cli import load_libraries, parse_plexil_plan
from plexilv.common import create_parser


def test_reject_library_with_path_traversal(tmp_path, capsys):
    """Test that library names with path traversal are rejected."""
    # Create a plan directory
    plan_dir = tmp_path / "plans"
    plan_dir.mkdir()

    # Create a file outside the plan directory
    secret_dir = tmp_path / "secrets"
    secret_dir.mkdir()
    secret_file = secret_dir / "secret.plx"
    secret_file.write_text("""<?xml version="1.0" encoding="UTF-8"?>
<PlexilPlan xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
  <Node NodeType="Empty">
    <NodeId>Secret</NodeId>
  </Node>
</PlexilPlan>""")

    # Create a main plan that tries to reference the secret file using path traversal
    main_plan_file = plan_dir / "main.plx"
    main_plan_file.write_text("""<?xml version="1.0" encoding="UTF-8"?>
<PlexilPlan xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
  <Node NodeType="LibraryNodeCall">
    <NodeId>CallMalicious</NodeId>
    <NodeBody>
      <LibraryNodeCall>
        <NodeId>../secrets/secret</NodeId>
      </LibraryNodeCall>
    </NodeBody>
  </Node>
</PlexilPlan>""")

    parser = create_parser()
    with open(main_plan_file, "r") as f:
        main_plan, _ = parse_plexil_plan(f.read(), parser)

    # Try to load libraries - should reject the path traversal
    libraries = load_libraries(plan_dir, main_plan, parser)

    # The malicious library should NOT be loaded
    assert "../secrets/secret" not in libraries
    assert len(libraries) == 0

    # Check that a warning was printed
    captured = capsys.readouterr()
    assert "Invalid library name" in captured.err or "escapes plan directory" in captured.err


def test_reject_library_with_special_characters(tmp_path, capsys):
    """Test that library names with special characters are rejected."""
    plan_dir = tmp_path / "plans"
    plan_dir.mkdir()

    parser = create_parser()

    # Test various invalid library names
    # (Note: avoiding < > & which break XML parsing itself)
    invalid_names = [
        "library;rm",  # Semicolon
        "library|cat",  # Pipe
        "library$(whoami)",  # Dollar sign / parens
        "library*test",  # Asterisk
        "library?test",  # Question mark
    ]

    for invalid_name in invalid_names:
        # Create a main plan that references invalid library
        main_plan_file = plan_dir / "main.plx"
        main_plan_file.write_text(f"""<?xml version="1.0" encoding="UTF-8"?>
<PlexilPlan xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
  <Node NodeType="LibraryNodeCall">
    <NodeId>CallLib</NodeId>
    <NodeBody>
      <LibraryNodeCall>
        <NodeId>{invalid_name}</NodeId>
      </LibraryNodeCall>
    </NodeBody>
  </Node>
</PlexilPlan>""")

        with open(main_plan_file, "r") as f:
            plan, _ = parse_plexil_plan(f.read(), parser)

        # Clear previous stderr
        capsys.readouterr()

        # Try to load libraries - should reject invalid names
        libraries = load_libraries(plan_dir, plan, parser)

        # The malicious library should NOT be loaded
        assert invalid_name not in libraries

        # Check that a warning was printed
        captured = capsys.readouterr()
        assert "Invalid library name" in captured.err


def test_accept_valid_library_names(tmp_path):
    """Test that valid library names with hyphens and underscores are accepted."""
    plan_dir = tmp_path / "plans"
    plan_dir.mkdir()

    # Create valid library files
    valid_names = [
        "MyLibrary",
        "my-library",
        "my_library",
        "lib-123",
        "lib_456",
    ]

    for name in valid_names:
        lib_file = plan_dir / f"{name}.plx"
        lib_file.write_text("""<?xml version="1.0" encoding="UTF-8"?>
<PlexilPlan xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
  <Node NodeType="Empty">
    <NodeId>TestNode</NodeId>
  </Node>
</PlexilPlan>""")

    parser = create_parser()

    # Test each valid name
    for name in valid_names:
        # Create a main plan that references this library
        main_plan_file = plan_dir / "main.plx"
        main_plan_file.write_text(f"""<?xml version="1.0" encoding="UTF-8"?>
<PlexilPlan xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
  <Node NodeType="LibraryNodeCall">
    <NodeId>CallLib</NodeId>
    <NodeBody>
      <LibraryNodeCall>
        <NodeId>{name}</NodeId>
      </LibraryNodeCall>
    </NodeBody>
  </Node>
</PlexilPlan>""")

        with open(main_plan_file, "r") as f:
            plan, _ = parse_plexil_plan(f.read(), parser)

        # Load libraries - should accept valid names
        libraries = load_libraries(plan_dir, plan, parser)

        # The valid library should be loaded
        assert name in libraries
