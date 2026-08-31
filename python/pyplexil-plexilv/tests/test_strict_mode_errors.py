"""Tests for strict mode - verifying exceptions are raised for invalid PLEXIL."""

import pytest
from unittest.mock import Mock
from plexilv.plexil.translator.constants import TranspilationError
from tests.conftest import normalize_whitespace


def test_unsupported_node_type_raises_error():
    """Test that unsupported node types raise TranspilationError.

    We test this at the Python level by constructing a Node object
    with a mock node_type that isn't handled by the transpiler.
    """
    from unittest.mock import Mock
    from plexilv.common import IndentedWriter
    from plexilv.plexil.translator.state import TranspilerContext
    from plexilv.plexil.translator.handlers.nodes import translate

    # Create a mock node with an unsupported type
    node = Mock(spec=Node)
    node.node_id = Mock()
    node.node_id.value = "UnsupportedNode"
    node.node_type = Mock()
    node.node_type.value = "FutureNodeType"  # Not in the switch statement

    writer = IndentedWriter()
    context = TranspilerContext()

    with pytest.raises(TranspilationError) as exc_info:
        translate(node, writer, context)

    assert "Unsupported node type" in str(exc_info.value)
    assert "UnsupportedNode" in str(exc_info.value)
    assert "FutureNodeType" in str(exc_info.value)


def test_assignment_node_missing_body_raises_error(translate_xml):
    """Test that assignment node without body raises TranspilationError."""
    xml = """
    <Node NodeType="Assignment">
        <NodeId>MissingBody</NodeId>
    </Node>
    """

    with pytest.raises(TranspilationError) as exc_info:
        translate_xml(xml, Node)

    assert "missing node body" in str(exc_info.value).lower()
    assert "MissingBody" in str(exc_info.value)


def test_assignment_node_wrong_body_type_raises_error(translate_xml):
    """Test that assignment node with command body raises TranspilationError."""
    xml = """
    <Node NodeType="Assignment">
        <NodeId>WrongBody</NodeId>
        <NodeBody>
            <Command>
                <Name><StringValue>print</StringValue></Name>
            </Command>
        </NodeBody>
    </Node>
    """

    with pytest.raises(TranspilationError) as exc_info:
        translate_xml(xml, Node)

    assert "wrong body type" in str(exc_info.value).lower()
    assert "WrongBody" in str(exc_info.value)
    assert "Command" in str(exc_info.value)


def test_command_node_missing_body_raises_error(translate_xml):
    """Test that command node without body raises TranspilationError."""
    xml = """
    <Node NodeType="Command">
        <NodeId>NoBody</NodeId>
    </Node>
    """

    with pytest.raises(TranspilationError) as exc_info:
        translate_xml(xml, Node)

    assert "missing node body" in str(exc_info.value).lower()
    assert "NoBody" in str(exc_info.value)


def test_command_node_wrong_body_type_raises_error(translate_xml):
    """Test that command node with assignment body raises TranspilationError."""
    xml = """
    <Node NodeType="Command">
        <NodeId>BadCommand</NodeId>
        <NodeBody>
            <Assignment>
                <IntegerVariable>x</IntegerVariable>
                <NumericRHS><IntegerValue>5</IntegerValue></NumericRHS>
            </Assignment>
        </NodeBody>
    </Node>
    """

    with pytest.raises(TranspilationError) as exc_info:
        translate_xml(xml, Node)

    assert "wrong body type" in str(exc_info.value).lower()
    assert "BadCommand" in str(exc_info.value)
    assert "Assignment" in str(exc_info.value)


def test_update_node_missing_body_raises_error(translate_xml):
    """Test that update node without body raises TranspilationError."""
    xml = """
    <Node NodeType="Update">
        <NodeId>NoUpdateBody</NodeId>
    </Node>
    """

    with pytest.raises(TranspilationError) as exc_info:
        translate_xml(xml, Node)

    assert "missing node body" in str(exc_info.value).lower()
    assert "NoUpdateBody" in str(exc_info.value)


def test_update_node_wrong_body_type_raises_error(translate_xml):
    """Test that update node with command body raises TranspilationError."""
    xml = """
    <Node NodeType="Update">
        <NodeId>BadUpdate</NodeId>
        <NodeBody>
            <Command>
                <Name><StringValue>print</StringValue></Name>
            </Command>
        </NodeBody>
    </Node>
    """

    with pytest.raises(TranspilationError) as exc_info:
        translate_xml(xml, Node)

    assert "wrong body type" in str(exc_info.value).lower()
    assert "BadUpdate" in str(exc_info.value)
    assert "Command" in str(exc_info.value)


def test_library_node_missing_library_raises_error(translate_xml):
    """Test that library node call without library definition raises error."""
    xml = """
    <Node NodeType="LibraryNodeCall">
        <NodeId>CallUndefined</NodeId>
        <NodeBody>
            <LibraryNodeCall>
                <NodeId>NonExistentLibrary</NodeId>
            </LibraryNodeCall>
        </NodeBody>
    </Node>
    """

    with pytest.raises(TranspilationError) as exc_info:
        translate_xml(xml, Node)

    assert "undefined library" in str(exc_info.value).lower()
    assert "NonExistentLibrary" in str(exc_info.value)
    assert "CallUndefined" in str(exc_info.value)


def test_library_node_with_empty_library_raises_error():
    """Test that library with no root node raises error.

    We test this at the Python level by constructing a PlexilPlan object
    with node=None, simulating a library that somehow has no root node.
    """
    from plexil.core.v1 import PlexilPlan, LibraryNodeCall, NodeId
    from plexilv.common import IndentedWriter
    from plexilv.plexil.translator.state import TranspilerContext
    from plexilv.plexil.translator.handlers.nodes import translate_library_node

    # Create an empty library (PlexilPlan with node=None)
    empty_library = PlexilPlan(node=None)

    # Create a proper LibraryNodeCall object (not mock)
    lib_call = LibraryNodeCall(node_id=NodeId(value="EmptyLib"))

    # Create the node with proper structure
    node = Mock()
    node.node_id = Mock()
    node.node_id.value = "CallEmpty"
    node.node_body = Mock()
    node.node_body.choice = lib_call  # This is a real LibraryNodeCall
    node.variable_declarations = None

    writer = IndentedWriter()
    context = TranspilerContext(libraries={"EmptyLib": empty_library})

    with pytest.raises(TranspilationError) as exc_info:
        translate_library_node(node, "CallEmpty", writer, context)

    error_msg = str(exc_info.value).lower()
    assert "no root node" in error_msg or "empty library" in error_msg
    assert "EmptyLib" in str(exc_info.value)


def test_library_node_missing_body_raises_error(translate_xml):
    """Test that library node without LibraryNodeCall body raises error."""
    xml = """
    <Node NodeType="LibraryNodeCall">
        <NodeId>MissingLibBody</NodeId>
    </Node>
    """

    with pytest.raises(TranspilationError) as exc_info:
        translate_xml(xml, Node)

    assert "missing" in str(exc_info.value).lower()
    assert "MissingLibBody" in str(exc_info.value)


def test_valid_nodes_do_not_raise_errors(translate_xml):
    """Test that valid nodes transpile without raising exceptions."""
    # Test each valid node type to ensure we don't have false positives

    # Empty node
    xml_empty = """
    <Node NodeType="Empty">
        <NodeId>ValidEmpty</NodeId>
    </Node>
    """
    result = translate_xml(xml_empty, Node)
    assert "empty('ValidEmpty" in normalize_whitespace(result)

    # Assignment node
    xml_assignment = """
    <Node NodeType="Assignment">
        <NodeId>ValidAssignment</NodeId>
        <NodeBody>
            <Assignment>
                <IntegerVariable>x</IntegerVariable>
                <NumericRHS><IntegerValue>42</IntegerValue></NumericRHS>
            </Assignment>
        </NodeBody>
    </Node>
    """
    result = translate_xml(xml_assignment, Node)
    assert "assignment('ValidAssignment" in normalize_whitespace(result)

    # Command node
    xml_command = """
    <Node NodeType="Command">
        <NodeId>ValidCommand</NodeId>
        <NodeBody>
            <Command>
                <Name><StringValue>print</StringValue></Name>
            </Command>
        </NodeBody>
    </Node>
    """
    result = translate_xml(xml_command, Node)
    assert "command('ValidCommand" in normalize_whitespace(result)

    # Update node
    xml_update = """
    <Node NodeType="Update">
        <NodeId>ValidUpdate</NodeId>
        <NodeBody>
            <Update>
                <Pair>
                    <Name>status</Name>
                    <StringValue>done</StringValue>
                </Pair>
            </Update>
        </NodeBody>
    </Node>
    """
    result = translate_xml(xml_update, Node)
    assert "update('ValidUpdate" in normalize_whitespace(result)


def test_valid_library_call_does_not_raise_error(translate_xml_with_libraries):
    """Test that valid library call transpiles without errors."""
    library_xml = """
    <Node NodeType="Empty">
        <NodeId>MyLib</NodeId>
    </Node>
    """

    xml = """
    <Node NodeType="LibraryNodeCall">
        <NodeId>CallMyLib</NodeId>
        <NodeBody>
            <LibraryNodeCall>
                <NodeId>MyLib</NodeId>
            </LibraryNodeCall>
        </NodeBody>
    </Node>
    """

    result = translate_xml_with_libraries(xml, Node, {"MyLib": library_xml})
    assert "library('CallMyLib" in normalize_whitespace(result)
    assert "empty('MyLib" in normalize_whitespace(result)


def test_exception_includes_node_context(translate_xml):
    """Test that exceptions include useful context about which node failed."""
    xml = """
    <Node NodeType="NodeList">
        <NodeId>ParentList</NodeId>
        <NodeBody>
            <NodeList>
                <Node NodeType="Empty">
                    <NodeId>Child1</NodeId>
                </Node>
                <Node NodeType="Assignment">
                    <NodeId>BrokenChild</NodeId>
                    <!-- Missing body - should fail here -->
                </Node>
                <Node NodeType="Empty">
                    <NodeId>Child3</NodeId>
                </Node>
            </NodeList>
        </NodeBody>
    </Node>
    """

    with pytest.raises(TranspilationError) as exc_info:
        translate_xml(xml, Node)

    # The exception should mention the specific broken node
    assert "BrokenChild" in str(exc_info.value)
    assert "missing" in str(exc_info.value).lower()


# Import Node at the end to avoid issues with fixtures
from plexil.core.v1 import Node
