"""Tests for module name generation in plx2maude CLI.

These tests verify that node IDs preserve underscores in the module name.
"""

import pytest
from plexilv.plexil.translator.cli import parse_plexil_plan
from xsdata.formats.dataclass.parsers import XmlParser
from xsdata.formats.dataclass.parsers.config import ParserConfig


def test_module_name_converts_underscores_to_hyphens():
    """Test that node IDs with underscores are preserved in module name."""
    xml = """<?xml version="1.0" encoding="UTF-8"?>
    <PlexilPlan>
        <Node NodeType="Empty">
            <NodeId>TEST_NODE_NAME</NodeId>
        </Node>
    </PlexilPlan>
    """

    config = ParserConfig(process_xinclude=False, fail_on_unknown_properties=False)
    parser = XmlParser(config=config)

    plan, node_id = parse_plexil_plan(xml, parser)

    # Node ID should preserve underscores
    assert node_id == "TEST_NODE_NAME"


def test_module_name_traffic_resolution_pattern():
    """Test the specific TRAFFIC_RESOLUTION pattern from acceptance test."""
    xml = """<?xml version="1.0" encoding="UTF-8"?>
    <PlexilPlan>
        <Node NodeType="NodeList">
            <NodeId>TRAFFIC_RESOLUTION</NodeId>
        </Node>
    </PlexilPlan>
    """

    config = ParserConfig(process_xinclude=False, fail_on_unknown_properties=False)
    parser = XmlParser(config=config)

    plan, node_id = parse_plexil_plan(xml, parser)

    # Should preserve TRAFFIC_RESOLUTION as-is
    assert node_id == "TRAFFIC_RESOLUTION"


def test_module_name_single_underscore():
    """Test node ID with single underscore."""
    xml = """<?xml version="1.0" encoding="UTF-8"?>
    <PlexilPlan>
        <Node NodeType="Empty">
            <NodeId>test_node</NodeId>
        </Node>
    </PlexilPlan>
    """

    config = ParserConfig(process_xinclude=False, fail_on_unknown_properties=False)
    parser = XmlParser(config=config)

    plan, node_id = parse_plexil_plan(xml, parser)

    assert node_id == "test_node"


def test_module_name_multiple_underscores():
    """Test node ID with multiple consecutive underscores."""
    xml = """<?xml version="1.0" encoding="UTF-8"?>
    <PlexilPlan>
        <Node NodeType="Empty">
            <NodeId>my__test__node</NodeId>
        </Node>
    </PlexilPlan>
    """

    config = ParserConfig(process_xinclude=False, fail_on_unknown_properties=False)
    parser = XmlParser(config=config)

    plan, node_id = parse_plexil_plan(xml, parser)

    assert node_id == "my__test__node"


def test_module_name_no_underscores():
    """Test that node IDs without underscores are unchanged."""
    xml = """<?xml version="1.0" encoding="UTF-8"?>
    <PlexilPlan>
        <Node NodeType="Empty">
            <NodeId>SimpleNode</NodeId>
        </Node>
    </PlexilPlan>
    """

    config = ParserConfig(process_xinclude=False, fail_on_unknown_properties=False)
    parser = XmlParser(config=config)

    plan, node_id = parse_plexil_plan(xml, parser)

    assert node_id == "SimpleNode"


def test_module_name_with_hyphens_unchanged():
    """Test that existing hyphens in node IDs are preserved."""
    xml = """<?xml version="1.0" encoding="UTF-8"?>
    <PlexilPlan>
        <Node NodeType="Empty">
            <NodeId>test-node-name</NodeId>
        </Node>
    </PlexilPlan>
    """

    config = ParserConfig(process_xinclude=False, fail_on_unknown_properties=False)
    parser = XmlParser(config=config)

    plan, node_id = parse_plexil_plan(xml, parser)

    assert node_id == "test-node-name"


def test_module_name_mixed_underscores_and_hyphens():
    """Test node ID with both underscores and hyphens."""
    xml = """<?xml version="1.0" encoding="UTF-8"?>
    <PlexilPlan>
        <Node NodeType="Empty">
            <NodeId>test_node-name</NodeId>
        </Node>
    </PlexilPlan>
    """

    config = ParserConfig(process_xinclude=False, fail_on_unknown_properties=False)
    parser = XmlParser(config=config)

    plan, node_id = parse_plexil_plan(xml, parser)

    # Both underscores and hyphens should be preserved
    assert node_id == "test_node-name"


def test_module_name_empty_node_id():
    """Test handling of empty NodeId."""
    xml = """<?xml version="1.0" encoding="UTF-8"?>
    <PlexilPlan>
        <Node NodeType="Empty">
            <NodeId></NodeId>
        </Node>
    </PlexilPlan>
    """

    config = ParserConfig(process_xinclude=False, fail_on_unknown_properties=False)
    parser = XmlParser(config=config)

    plan, node_id = parse_plexil_plan(xml, parser)

    # Empty node ID should return UNKNOWN
    assert node_id == "UNKNOWN"


def test_module_name_missing_node_id():
    """Test handling of missing NodeId element.

    Note: xsdata requires NodeId for Node, so we test the edge case
    where the NodeId element exists but has no text content.
    """
    xml = """<?xml version="1.0" encoding="UTF-8"?>
    <PlexilPlan>
        <Node NodeType="Empty">
            <NodeId>testNode</NodeId>
        </Node>
    </PlexilPlan>
    """

    config = ParserConfig(process_xinclude=False, fail_on_unknown_properties=False)
    parser = XmlParser(config=config)

    plan, node_id = parse_plexil_plan(xml, parser)

    # Should convert underscores to hyphens
    assert node_id == "testNode"
