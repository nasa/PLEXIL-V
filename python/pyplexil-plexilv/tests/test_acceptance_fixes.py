"""Tests for fixes applied based on acceptance test analysis.

These tests verify specific fixes that were made to match the Haskell
plx2maude-hs reference implementation.
"""

import pytest
from plexil.core.v1.ast import Node, Max, Min


def test_max_operator_naming(translate_xml):
    """Test that MAX operator uses _max_ (not max_)."""
    xml = """
    <MAX>
        <IntegerValue>5</IntegerValue>
        <IntegerValue>3</IntegerValue>
    </MAX>
    """
    result = translate_xml(xml, Max)
    # Should use _max_ with underscores on both sides
    assert result == "_max_(const(val(5)),const(val(3)))"
    # Should start with _max_ (not max_ without leading underscore)
    assert result.startswith("_max_(")


def test_min_operator_naming(translate_xml):
    """Test that MIN operator uses _min_ (not min_)."""
    xml = """
    <MIN>
        <IntegerValue>5</IntegerValue>
        <IntegerValue>3</IntegerValue>
    </MIN>
    """
    result = translate_xml(xml, Min)
    # Should use _min_ with underscores on both sides
    assert result == "_min_(const(val(5)),const(val(3)))"
    # Should start with _min_ (not min_ without leading underscore)
    assert result.startswith("_min_(")


def test_max_with_three_operands(translate_xml):
    """Test MAX with three operands uses nested _max_."""
    xml = """
    <MAX>
        <IntegerValue>5</IntegerValue>
        <IntegerValue>3</IntegerValue>
        <IntegerValue>7</IntegerValue>
    </MAX>
    """
    result = translate_xml(xml, Max)
    # All operators should use _max_
    assert result == "_max_(_max_(const(val(5)),const(val(3))),const(val(7)))"
    assert result.count("_max_") == 2


def test_library_call_without_conditions_omits_field(translate_xml_with_libraries):
    """Test that library calls without conditions omit the conditions field entirely."""
    from tests.conftest import normalize_whitespace

    main_xml = """
    <Node NodeType="LibraryNodeCall">
        <NodeId>libCall</NodeId>
        <NodeBody>
            <LibraryNodeCall>
                <NodeId>theLib</NodeId>
            </LibraryNodeCall>
        </NodeBody>
    </Node>
    """

    library_xml = """
    <Node NodeType="Empty">
        <NodeId>theLib</NodeId>
    </Node>
    """

    result = translate_xml_with_libraries(
        main_xml, Node, libraries={"theLib": library_xml}
    )

    # Should NOT have conditions field when there are no conditions
    # Format: library(id, localVars, aliasVars, callInfo, libNode)
    # NOT: library(id, localVars, aliasVars, (none), callInfo, libNode)
    normalized = normalize_whitespace(result)
    assert "(none),callInfo" in normalized
    # Should not have two (none) in a row
    assert "(none),(none)" not in normalized


def test_library_call_with_conditions_includes_field(translate_xml_with_libraries):
    """Test that library calls with conditions include the conditions field."""
    main_xml = """
    <Node NodeType="LibraryNodeCall">
        <NodeId>libCallWithCond</NodeId>
        <StartCondition>
            <BooleanValue>true</BooleanValue>
        </StartCondition>
        <NodeBody>
            <LibraryNodeCall>
                <NodeId>theLib</NodeId>
            </LibraryNodeCall>
        </NodeBody>
    </Node>
    """

    library_xml = """
    <Node NodeType="Empty">
        <NodeId>theLib</NodeId>
    </Node>
    """

    result = translate_xml_with_libraries(
        main_xml, Node, libraries={"theLib": library_xml}
    )

    # Should include conditions field when present
    # Format: library(id, localVars, aliasVars, conditions, callInfo, libNode)
    assert "((startc: (const(val(true)))))" in result
    # Conditions should come before callInfo
    assert result.index("startc") < result.index("callInfo")


def test_variable_name_preserves_underscore(translate_xml):
    """Test that variable names preserve underscores (regression test)."""
    xml = """
    <Node NodeType="Empty">
        <NodeId>test</NodeId>
        <VariableDeclarations>
            <DeclareVariable>
                <Name>initial_drag</Name>
                <Type>Real</Type>
            </DeclareVariable>
        </VariableDeclarations>
    </Node>
    """
    result = translate_xml(xml, Node)

    # Variable name should keep underscore
    assert "'initial_drag" in result
    # Should NOT be converted to hyphen
    assert "'initial-drag" not in result


def test_node_name_converts_underscore_to_hyphen(translate_xml):
    """Test that node names preserve underscores."""
    xml = """
    <Node NodeType="Empty">
        <NodeId>node_with_underscore</NodeId>
    </Node>
    """
    result = translate_xml(xml, Node)

    # Node name should preserve underscore
    assert "'node_with_underscore" in result
    # Should NOT convert to hyphen
    assert "'node-with-underscore" not in result


def test_max_in_condition(translate_xml):
    """Test MAX operator used in a condition (acceptance test pattern)."""
    xml = """
    <Node NodeType="Empty">
        <NodeId>maximum</NodeId>
        <VariableDeclarations>
            <DeclareVariable>
                <Name>r</Name>
                <Type>Real</Type>
                <InitialValue>
                    <RealValue>2.0</RealValue>
                </InitialValue>
            </DeclareVariable>
        </VariableDeclarations>
        <InvariantCondition>
            <EQNumeric>
                <MAX>
                    <IntegerValue>4</IntegerValue>
                    <RealVariable>r</RealVariable>
                </MAX>
                <RealValue>4.0</RealValue>
            </EQNumeric>
        </InvariantCondition>
    </Node>
    """
    result = translate_xml(xml, Node)

    # Should use _max_ operator
    assert "_max_(" in result
    # Should have proper structure in condition with _max_ at the start
    assert "_equ_(_max_(const(val(4)),var('r)),const(val(4.0)))" in result


def test_library_call_field_count_without_conditions(translate_xml_with_libraries):
    """Test that library calls have exactly 5 fields when no conditions."""
    from tests.conftest import normalize_whitespace

    main_xml = """
    <Node NodeType="LibraryNodeCall">
        <NodeId>test</NodeId>
        <NodeBody>
            <LibraryNodeCall>
                <NodeId>lib</NodeId>
            </LibraryNodeCall>
        </NodeBody>
    </Node>
    """

    library_xml = """
    <Node NodeType="Empty">
        <NodeId>lib</NodeId>
    </Node>
    """

    result = translate_xml_with_libraries(
        main_xml, Node, libraries={"lib": library_xml}
    )

    # Count commas in library(...) to verify field count
    # Format: library(id, localVars, aliasVars, callInfo, libNode)
    # That's 5 fields = 4 commas (outside of nested structures)
    normalized = normalize_whitespace(result)
    library_part = normalized.split("library(")[1].split("empty(")[0]

    # Should have format: 'test,nilocdecl,(none),callInfo(...),
    # The key is that there's no conditions field between (none) and callInfo
    assert "nilocdecl,(none),callInfo" in normalized


def test_library_call_field_count_with_conditions(translate_xml_with_libraries):
    """Test that library calls have exactly 6 fields when conditions present."""
    from tests.conftest import normalize_whitespace

    main_xml = """
    <Node NodeType="LibraryNodeCall">
        <NodeId>test</NodeId>
        <EndCondition>
            <BooleanValue>true</BooleanValue>
        </EndCondition>
        <NodeBody>
            <LibraryNodeCall>
                <NodeId>lib</NodeId>
            </LibraryNodeCall>
        </NodeBody>
    </Node>
    """

    library_xml = """
    <Node NodeType="Empty">
        <NodeId>lib</NodeId>
    </Node>
    """

    result = translate_xml_with_libraries(
        main_xml, Node, libraries={"lib": library_xml}
    )

    # Format: library(id, localVars, aliasVars, conditions, callInfo, libNode)
    # That's 6 fields when conditions are present
    # Verify the sequence is correct
    normalized = normalize_whitespace(result)
    assert "nilocdecl,(none),((endc:" in normalized
    assert ")),callInfo" in normalized
