"""Acceptance tests for PLEXILScript parsing.

Tests that all .psx files from the TestExec regression test suite
can be successfully parsed and round-tripped.
"""

import pytest
from pathlib import Path

from plexil.plexilscript.v1.io import parse_plexilscript_file, serialize_plexilscript
from plexil.plexilscript.v1.ast import PLEXILScript
from xsdata.formats.dataclass.parsers import XmlParser

DATA_DIR = Path(__file__).resolve().parent / "data" / "plexilscript"


def get_psx_files():
    """Get all .psx files from the test data directory."""
    if not DATA_DIR.exists():
        print(f"Directory not found: {DATA_DIR}")
        return []
    files = list(DATA_DIR.glob("*.psx"))
    print(f"Found {len(files)} .psx files in {DATA_DIR}")
    return files


@pytest.mark.parametrize("psx_file", get_psx_files(), ids=lambda p: p.name)
def test_parse_psx(psx_file):
    """Test that each .psx file can be parsed successfully."""
    script = parse_plexilscript_file(psx_file)

    assert script is not None
    assert isinstance(script, PLEXILScript)
    assert script.script is not None


@pytest.mark.parametrize("psx_file", get_psx_files(), ids=lambda p: p.name)
def test_plexilscript_roundtrip(psx_file):
    """Test that each .psx file can be parsed, serialized, and parsed again.

    This tests the round-trip capability:
    1. Parse original XML to AST
    2. Serialize AST back to XML
    3. Parse serialized XML to AST
    4. Assert both ASTs are equal
    """
    # 1. Parse original
    original_script = parse_plexilscript_file(psx_file)
    assert original_script is not None

    # 2. Serialize to XML
    xml_output = serialize_plexilscript(original_script)
    assert xml_output is not None

    # 3. Parse serialized XML back to AST
    parser = XmlParser()
    new_script = parser.from_string(xml_output, PLEXILScript)

    # 4. Assert equality
    assert isinstance(new_script, PLEXILScript)
    assert original_script == new_script
