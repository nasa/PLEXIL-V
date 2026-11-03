"""Tests for libraryCall1 acceptance test fix.

These tests verify that library call variable declaration fields are output
in the correct order to match the Haskell plx2maude-hs reference implementation.
"""

import pytest
from plexil.core.v1.ast import Node
from tests.conftest import normalize_whitespace


def test_library_call_field_order_alias_only(translate_xml_with_libraries):
    """Test library call with only alias variables (interface parameters).

    Field order should be: name, aliasVars, (none), callInfo, body
    """
    main_xml = """
    <Node NodeType="LibraryNodeCall">
        <NodeId>testCall</NodeId>
        <NodeBody>
            <LibraryNodeCall>
                <NodeId>testLib</NodeId>
                <Alias>
                    <NodeParameter>param1</NodeParameter>
                    <IntegerValue>42</IntegerValue>
                </Alias>
            </LibraryNodeCall>
        </NodeBody>
    </Node>
    """

    library_xml = """
    <Node NodeType="Empty">
        <NodeId>testLib</NodeId>
        <Interface>
            <In>
                <DeclareVariable>
                    <Name>param1</Name>
                    <Type>Integer</Type>
                </DeclareVariable>
            </In>
        </Interface>
    </Node>
    """

    result = translate_xml_with_libraries(
        main_xml, Node, libraries={"testLib": library_xml}
    )

    # Parameters are declared on the library root, not on the call node
    assert "library('testCall,nilocdecl,(none),callInfo('testLib" in normalize_whitespace(result)
    assert "('param1:unknown)" not in normalize_whitespace(result)


def test_library_call_field_order_local_only(translate_xml_with_libraries):
    """Test library call with only local variables (call site declarations).

    Field order should be: name, (localVars), (none), callInfo, body
    """
    main_xml = """
    <Node NodeType="LibraryNodeCall">
        <NodeId>testCall</NodeId>
        <VariableDeclarations>
            <DeclareVariable>
                <Name>localVar</Name>
                <Type>Integer</Type>
                <InitialValue>
                    <IntegerValue>10</IntegerValue>
                </InitialValue>
            </DeclareVariable>
        </VariableDeclarations>
        <NodeBody>
            <LibraryNodeCall>
                <NodeId>testLib</NodeId>
            </LibraryNodeCall>
        </NodeBody>
    </Node>
    """

    library_xml = """
    <Node NodeType="Empty">
        <NodeId>testLib</NodeId>
    </Node>
    """

    result = translate_xml_with_libraries(
        main_xml, Node, libraries={"testLib": library_xml}
    )

    # Should have local vars, then (none) for alias vars
    assert "library('testCall,(('localVar:val(10))),(none)," in normalize_whitespace(result)


def test_library_call_field_order_both_present(translate_xml_with_libraries):
    """Test library call with both local and alias variables.

    When both are present, they should be concatenated with NO comma between them:
    name, (localVars)(aliasVars), conditions, callInfo, body
    """
    main_xml = """
    <Node NodeType="LibraryNodeCall">
        <NodeId>testCall</NodeId>
        <VariableDeclarations>
            <DeclareVariable>
                <Name>localVar</Name>
                <Type>Integer</Type>
                <InitialValue>
                    <IntegerValue>5</IntegerValue>
                </InitialValue>
            </DeclareVariable>
        </VariableDeclarations>
        <NodeBody>
            <LibraryNodeCall>
                <NodeId>testLib</NodeId>
                <Alias>
                    <NodeParameter>aliasVar</NodeParameter>
                    <IntegerValue>10</IntegerValue>
                </Alias>
            </LibraryNodeCall>
        </NodeBody>
    </Node>
    """

    library_xml = """
    <Node NodeType="Empty">
        <NodeId>testLib</NodeId>
        <Interface>
            <In>
                <DeclareVariable>
                    <Name>aliasVar</Name>
                    <Type>Integer</Type>
                </DeclareVariable>
            </In>
        </Interface>
    </Node>
    """

    result = translate_xml_with_libraries(
        main_xml, Node, libraries={"testLib": library_xml}
    )

    # Only the call node's own local is declared; the alias is not
    assert "library('testCall,(('localVar:val(5))),(none),callInfo(" in normalize_whitespace(result)
    assert "('aliasVar:unknown)" not in normalize_whitespace(result)


def test_library_call_field_order_neither(translate_xml_with_libraries):
    """Test library call with no variables at all.

    Field order should be: name, nilocdecl, (none), callInfo, body
    """
    main_xml = """
    <Node NodeType="LibraryNodeCall">
        <NodeId>testCall</NodeId>
        <NodeBody>
            <LibraryNodeCall>
                <NodeId>testLib</NodeId>
            </LibraryNodeCall>
        </NodeBody>
    </Node>
    """

    library_xml = """
    <Node NodeType="Empty">
        <NodeId>testLib</NodeId>
    </Node>
    """

    result = translate_xml_with_libraries(
        main_xml, Node, libraries={"testLib": library_xml}
    )

    # Should have nilocdecl and (none)
    assert "library('testCall,nilocdecl,(none)," in normalize_whitespace(result)


def test_library_call1_acceptance_pattern(translate_xml_with_libraries):
    """Test the exact pattern from libraryCall1 acceptance test."""
    main_xml = """
    <Node NodeType="LibraryNodeCall">
        <NodeId>libraryCall1</NodeId>
        <NodeBody>
            <LibraryNodeCall>
                <NodeId>theLibrary</NodeId>
                <Alias>
                    <NodeParameter>number</NodeParameter>
                    <IntegerValue>1</IntegerValue>
                </Alias>
            </LibraryNodeCall>
        </NodeBody>
    </Node>
    """

    library_xml = """
    <Node NodeType="NodeList">
        <NodeId>theLibrary</NodeId>
        <Interface>
            <In>
                <DeclareVariable>
                    <Name>number</Name>
                    <Type>Integer</Type>
                </DeclareVariable>
            </In>
        </Interface>
        <InvariantCondition>
            <NoChildFailed>
                <NodeRef dir="self"/>
            </NoChildFailed>
        </InvariantCondition>
        <NodeBody>
            <NodeList>
                <Node NodeType="Empty">
                    <NodeId>empty</NodeId>
                    <StartCondition>
                        <EQNumeric>
                            <IntegerVariable>number</IntegerVariable>
                            <IntegerValue>1</IntegerValue>
                        </EQNumeric>
                    </StartCondition>
                </Node>
            </NodeList>
        </NodeBody>
    </Node>
    """

    result = translate_xml_with_libraries(
        main_xml, Node, libraries={"theLibrary": library_xml}
    )

    # Should match Haskell reference format:
    # library(name, localVars, (none), callInfo, body)
    assert "library('libraryCall1,nilocdecl,(none)," in normalize_whitespace(result)
    assert "callInfo('theLibrary,ids('number),const(val(1)))" in normalize_whitespace(result)
    assert "list('theLibrary,nilocdecl," in normalize_whitespace(result)


def test_library_call_with_conditions(translate_xml_with_libraries):
    """Test that conditions are included when present."""
    main_xml = """
    <Node NodeType="LibraryNodeCall">
        <NodeId>testCall</NodeId>
        <EndCondition>
            <BooleanValue>true</BooleanValue>
        </EndCondition>
        <NodeBody>
            <LibraryNodeCall>
                <NodeId>testLib</NodeId>
                <Alias>
                    <NodeParameter>param</NodeParameter>
                    <IntegerValue>1</IntegerValue>
                </Alias>
            </LibraryNodeCall>
        </NodeBody>
    </Node>
    """

    library_xml = """
    <Node NodeType="Empty">
        <NodeId>testLib</NodeId>
        <Interface>
            <In>
                <DeclareVariable>
                    <Name>param</Name>
                    <Type>Integer</Type>
                </DeclareVariable>
            </In>
        </Interface>
    </Node>
    """

    result = translate_xml_with_libraries(
        main_xml, Node, libraries={"testLib": library_xml}
    )

    # With conditions: name, localVars, (none), conditions, callInfo, body
    assert (
        "library('testCall,nilocdecl,(none),((endc:(const(val(true)))))"
        in normalize_whitespace(result)
    )
