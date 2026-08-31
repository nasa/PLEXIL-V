import pytest
from pathlib import Path

from plexil.core.v1.io import parse_plexil_file, serialize_plexil
from plexil.core.v1.ast import PlexilPlan
from xsdata.formats.dataclass.parsers import XmlParser

DATA_DIR = Path(__file__).resolve().parent / "data" / "plexil"


def get_plx_files():
    if not DATA_DIR.exists():
        print(f"Directory not found: {DATA_DIR}")
        return []
    files = list(DATA_DIR.glob("*.plx"))
    print(f"Found {len(files)} .plx files in {DATA_DIR}")
    return files


@pytest.mark.parametrize("plx_file", get_plx_files(), ids=lambda p: p.name)
def test_parse_plx(plx_file):
    plan = parse_plexil_file(plx_file)
    assert plan is not None
    assert isinstance(plan, PlexilPlan)


@pytest.mark.parametrize("plx_file", get_plx_files(), ids=lambda p: p.name)
def test_plexil_roundtrip(plx_file):
    # 1. Parse original
    original_plan = parse_plexil_file(plx_file)
    assert original_plan is not None

    # 2. Serialize to XML
    xml_output = serialize_plexil(original_plan)
    assert xml_output is not None

    # 3. Parse serialized XML back to AST
    parser = XmlParser()
    new_plan = parser.from_string(xml_output, PlexilPlan)

    # 4. Assert equality
    assert isinstance(new_plan, PlexilPlan)
    assert original_plan == new_plan
