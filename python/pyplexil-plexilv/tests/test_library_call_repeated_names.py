"""Tests for libraryCallWithRepeatedNames acceptance test pattern.

These tests verify that library calls correctly handle repeated variable names
across different scopes (parent list node, library parameters).
"""

import pytest
from plexil.core.v1.ast import Node
from tests.conftest import normalize_whitespace


def test_repeated_variable_name_in_parent_and_library(translate_xml_with_libraries):
    """Test that the same variable name can appear in parent node and library parameter.

    This is the pattern from libraryCallWithRepeatedNames acceptance test:
    - Parent list node declares variable 'foo'
    - Library call aliases parameter 'foo' to parent's 'foo' variable
    """
    main_xml = """
    <Node NodeType="NodeList">
        <NodeId>testList</NodeId>
        <VariableDeclarations>
            <DeclareVariable>
                <Name>foo</Name>
                <Type>Boolean</Type>
            </DeclareVariable>
        </VariableDeclarations>
        <NodeBody>
            <NodeList>
                <Node NodeType="LibraryNodeCall">
                    <NodeId>LibraryCall__0</NodeId>
                    <NodeBody>
                        <LibraryNodeCall>
                            <NodeId>TestLib</NodeId>
                            <Alias>
                                <NodeParameter>foo</NodeParameter>
                                <BooleanVariable>foo</BooleanVariable>
                            </Alias>
                        </LibraryNodeCall>
                    </NodeBody>
                </Node>
            </NodeList>
        </NodeBody>
    </Node>
    """

    library_xml = """
    <Node NodeType="Empty">
        <NodeId>TestLib</NodeId>
        <Interface>
            <InOut>
                <DeclareVariable>
                    <Name>foo</Name>
                    <Type>Boolean</Type>
                </DeclareVariable>
            </InOut>
        </Interface>
    </Node>
    """

    result = translate_xml_with_libraries(
        main_xml, Node, libraries={"TestLib": library_xml}
    )

    # Parent list should have 'foo' declaration
    assert "list('testList,(('foo:unknown))" in normalize_whitespace(result)

    # Library call should have alias var 'foo' and use varForwarding
    assert "library('LibraryCall__0,(('foo:unknown)),(none)," in normalize_whitespace(result)
    assert "const(varForwarding('foo))" in normalize_whitespace(result)


def test_multiple_library_calls_same_variable_name(translate_xml_with_libraries):
    """Test multiple library calls that all use the same variable name from parent.

    This tests the exact pattern from libraryCallWithRepeatedNames:
    - Two library calls in sequence
    - Both reference the same parent variable 'foo'
    """
    main_xml = """
    <Node NodeType="NodeList">
        <NodeId>testList</NodeId>
        <VariableDeclarations>
            <DeclareVariable>
                <Name>sharedVar</Name>
                <Type>Integer</Type>
                <InitialValue>
                    <IntegerValue>0</IntegerValue>
                </InitialValue>
            </DeclareVariable>
        </VariableDeclarations>
        <NodeBody>
            <NodeList>
                <Node NodeType="LibraryNodeCall">
                    <NodeId>Call1</NodeId>
                    <NodeBody>
                        <LibraryNodeCall>
                            <NodeId>Lib1</NodeId>
                            <Alias>
                                <NodeParameter>param</NodeParameter>
                                <IntegerVariable>sharedVar</IntegerVariable>
                            </Alias>
                        </LibraryNodeCall>
                    </NodeBody>
                </Node>
                <Node NodeType="LibraryNodeCall">
                    <NodeId>Call2</NodeId>
                    <NodeBody>
                        <LibraryNodeCall>
                            <NodeId>Lib2</NodeId>
                            <Alias>
                                <NodeParameter>param</NodeParameter>
                                <IntegerVariable>sharedVar</IntegerVariable>
                            </Alias>
                        </LibraryNodeCall>
                    </NodeBody>
                </Node>
            </NodeList>
        </NodeBody>
    </Node>
    """

    library1_xml = """
    <Node NodeType="Empty">
        <NodeId>Lib1</NodeId>
        <Interface>
            <InOut>
                <DeclareVariable>
                    <Name>param</Name>
                    <Type>Integer</Type>
                </DeclareVariable>
            </InOut>
        </Interface>
    </Node>
    """

    library2_xml = """
    <Node NodeType="Empty">
        <NodeId>Lib2</NodeId>
        <Interface>
            <InOut>
                <DeclareVariable>
                    <Name>param</Name>
                    <Type>Integer</Type>
                </DeclareVariable>
            </InOut>
        </Interface>
    </Node>
    """

    result = translate_xml_with_libraries(
        main_xml, Node, libraries={"Lib1": library1_xml, "Lib2": library2_xml}
    )

    # Parent list should declare sharedVar once
    assert "list('testList,(('sharedVar:val(0)))" in normalize_whitespace(result)

    # First library call
    assert "library('Call1,(('param:unknown)),(none)," in normalize_whitespace(result)
    assert (
        normalize_whitespace(result).count("callInfo('Lib1,ids('param),const(varForwarding('sharedVar)))")
        == 1
    )

    # Second library call
    assert "library('Call2,(('param:unknown)),(none)," in normalize_whitespace(result)
    assert (
        normalize_whitespace(result).count("callInfo('Lib2,ids('param),const(varForwarding('sharedVar)))")
        == 1
    )


def test_library_call_alias_field_order(translate_xml_with_libraries):
    """Test that library calls with only alias parameters have correct field order.

    When a library call has:
    - No local variables (no VariableDeclarations at call site)
    - Only alias parameters (from Interface)

    The format should be: library(name, (aliasVars), (none), callInfo, body)
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
            <InOut>
                <DeclareVariable>
                    <Name>param1</Name>
                    <Type>Integer</Type>
                </DeclareVariable>
            </InOut>
        </Interface>
    </Node>
    """

    result = translate_xml_with_libraries(
        main_xml, Node, libraries={"testLib": library_xml}
    )

    # Should have alias vars first, then (none) for empty local vars
    assert "library('testCall,(('param1:unknown)),(none)," in normalize_whitespace(result)

    # Should NOT have nilocdecl in second position (that would be wrong)
    assert "library('testCall,nilocdecl," not in normalize_whitespace(result)


def test_varforwarding_with_repeated_names(translate_xml_with_libraries):
    """Test that varForwarding correctly references parent variable.

    When an alias parameter uses a variable from the parent scope,
    the callInfo should use varForwarding to indicate the parameter
    is forwarding a variable reference (not a constant value).
    """
    main_xml = """
    <Node NodeType="NodeList">
        <NodeId>parent</NodeId>
        <VariableDeclarations>
            <DeclareVariable>
                <Name>myVar</Name>
                <Type>String</Type>
                <InitialValue>
                    <StringValue>test</StringValue>
                </InitialValue>
            </DeclareVariable>
        </VariableDeclarations>
        <NodeBody>
            <NodeList>
                <Node NodeType="LibraryNodeCall">
                    <NodeId>childCall</NodeId>
                    <NodeBody>
                        <LibraryNodeCall>
                            <NodeId>childLib</NodeId>
                            <Alias>
                                <NodeParameter>libParam</NodeParameter>
                                <StringVariable>myVar</StringVariable>
                            </Alias>
                        </LibraryNodeCall>
                    </NodeBody>
                </Node>
            </NodeList>
        </NodeBody>
    </Node>
    """

    library_xml = """
    <Node NodeType="Empty">
        <NodeId>childLib</NodeId>
        <Interface>
            <InOut>
                <DeclareVariable>
                    <Name>libParam</Name>
                    <Type>String</Type>
                </DeclareVariable>
            </InOut>
        </Interface>
    </Node>
    """

    result = translate_xml_with_libraries(
        main_xml, Node, libraries={"childLib": library_xml}
    )

    # Parent should declare myVar
    assert '((\'myVar : val("test")))' in result

    # Library call should use varForwarding for the variable reference
    assert "callInfo('childLib,ids('libParam),const(varForwarding('myVar)))" in normalize_whitespace(result)

    # Should NOT use a direct value or var() reference
    assert 'const(val("test"))' not in result or "varForwarding" in result
