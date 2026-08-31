"""Tests for LibraryNodeCall (library) node translation."""

import pytest
from plexil.core.v1.ast import Node
from tests.conftest import normalize_whitespace


def test_library_call_no_arguments(translate_xml_with_libraries):
    """Test library call without arguments."""
    # Main plan XML
    main_xml = """
    <Node NodeType="LibraryNodeCall">
        <NodeId>libraryCall0</NodeId>
        <NodeBody>
            <LibraryNodeCall>
                <NodeId>theLibrary</NodeId>
            </LibraryNodeCall>
        </NodeBody>
    </Node>
    """

    # Library definition XML
    library_xml = """
    <Node NodeType="Empty">
        <NodeId>theLibrary</NodeId>
    </Node>
    """

    result = translate_xml_with_libraries(
        main_xml, Node, libraries={"theLibrary": library_xml}
    )
    # Format: library('callNodeId, localVardecls, aliasVardecls, callInfo(...), libraryNode)
    # Note: conditions field is omitted when there are no conditions
    expected = "library('libraryCall0,nilocdecl,(none),callInfo('theLibrary,ids(nilq),nilpar),empty('theLibrary,nilocdecl,(none)))"
    assert normalize_whitespace(result) == normalize_whitespace(expected), f"Expected: {expected}\nGot: {result}"


def test_library_call_with_one_input_argument(translate_xml_with_libraries):
    """Test library call with one input argument."""
    # Main plan XML
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

    # Library definition XML with Interface
    library_xml = """
    <Node NodeType="Empty">
        <NodeId>theLibrary</NodeId>
        <Interface>
            <In>
                <DeclareVariable>
                    <Name>number</Name>
                    <Type>Integer</Type>
                </DeclareVariable>
            </In>
        </Interface>
    </Node>
    """

    result = translate_xml_with_libraries(
        main_xml, Node, libraries={"theLibrary": library_xml}
    )
    # With one alias parameter
    # Note: Field order is aliasVars, localVars, [conditions], callInfo, body
    # Note: conditions field is omitted when there are no conditions
    # aliasVars=(('number : unknown)), localVars=(none) since no local vars at call site
    expected = "library('libraryCall1,(('number : unknown)),(none),callInfo('theLibrary,ids('number),const(val(1))),empty('theLibrary,nilocdecl,(none)))"
    assert normalize_whitespace(result) == normalize_whitespace(expected), f"Expected: {expected}\nGot: {result}"


def test_library_call_with_three_input_arguments(translate_xml_with_libraries):
    """Test library call with three input arguments."""
    # Main plan XML
    main_xml = """
    <Node NodeType="LibraryNodeCall">
        <NodeId>libraryCall2</NodeId>
        <NodeBody>
            <LibraryNodeCall>
                <NodeId>theLibrary</NodeId>
                <Alias>
                    <NodeParameter>number</NodeParameter>
                    <IntegerValue>1</IntegerValue>
                </Alias>
                <Alias>
                    <NodeParameter>flag</NodeParameter>
                    <BooleanValue>true</BooleanValue>
                </Alias>
                <Alias>
                    <NodeParameter>message</NodeParameter>
                    <StringValue>OK</StringValue>
                </Alias>
            </LibraryNodeCall>
        </NodeBody>
    </Node>
    """

    # Library definition XML with Interface
    library_xml = """
    <Node NodeType="Command">
        <NodeId>theLibrary</NodeId>
        <Interface>
            <In>
                <DeclareVariable>
                    <Name>number</Name>
                    <Type>Integer</Type>
                </DeclareVariable>
                <DeclareVariable>
                    <Name>flag</Name>
                    <Type>Boolean</Type>
                </DeclareVariable>
                <DeclareVariable>
                    <Name>message</Name>
                    <Type>String</Type>
                </DeclareVariable>
            </In>
        </Interface>
        <NodeBody>
            <Command>
                <Name>
                    <StringValue>print</StringValue>
                </Name>
                <Arguments>
                    <StringVariable>message</StringVariable>
                </Arguments>
            </Command>
        </NodeBody>
    </Node>
    """

    result = translate_xml_with_libraries(
        main_xml, Node, libraries={"theLibrary": library_xml}
    )
    # With three alias parameters
    # Note: Field order is aliasVars, localVars, [conditions], callInfo, body
    # Note: conditions field is omitted when there are no conditions
    # aliasVars=(three params), localVars=(none) since no local vars at call site
    expected = (
        "library('libraryCall2,"
        + "(('number : unknown) ('flag : unknown) ('message : unknown)),"
        + "(none),"
        + "callInfo('theLibrary,ids('number . 'flag . 'message),(const(val(1)) const(val(true)) const(val(\"OK\")))),command('theLibrary,nilocdecl,(none),(('print) / (var('message)) / nothing)))"
    )
    assert normalize_whitespace(result) == normalize_whitespace(expected), f"Expected: {expected}\nGot: {result}"


def test_library_call_with_one_inout_argument(translate_xml_with_libraries):
    """Test library call with one InOut argument (variable forwarding)."""
    # Main plan XML
    main_xml = """
    <Node NodeType="LibraryNodeCall">
        <NodeId>libraryCall3</NodeId>
        <VariableDeclarations>
            <DeclareVariable>
                <Name>myNumber</Name>
                <Type>Integer</Type>
                <InitialValue>
                    <IntegerValue>1</IntegerValue>
                </InitialValue>
            </DeclareVariable>
        </VariableDeclarations>
        <EndCondition>
            <EQNumeric>
                <IntegerVariable>myNumber</IntegerVariable>
                <IntegerValue>2</IntegerValue>
            </EQNumeric>
        </EndCondition>
        <NodeBody>
            <LibraryNodeCall>
                <NodeId>theLibrary</NodeId>
                <Alias>
                    <NodeParameter>number</NodeParameter>
                    <IntegerVariable>myNumber</IntegerVariable>
                </Alias>
            </LibraryNodeCall>
        </NodeBody>
    </Node>
    """

    # Library definition XML with InOut Interface
    library_xml = """
    <Node NodeType="Assignment">
        <NodeId>theLibrary</NodeId>
        <Interface>
            <InOut>
                <DeclareVariable>
                    <Name>number</Name>
                    <Type>Integer</Type>
                </DeclareVariable>
            </InOut>
        </Interface>
        <NodeBody>
            <Assignment>
                <IntegerVariable>number</IntegerVariable>
                <NumericRHS>
                    <IntegerValue>2</IntegerValue>
                </NumericRHS>
            </Assignment>
        </NodeBody>
    </Node>
    """

    result = translate_xml_with_libraries(
        main_xml, Node, libraries={"theLibrary": library_xml}
    )
    # Variable as alias value should use varForwarding
    # NOTE: When both local and alias vars are present, they're concatenated with NO comma
    expected = (
        "library('libraryCall3,"
        + "(('myNumber : val(1)))(('number : unknown)),"
        + "((endc: (_equ_(var('myNumber),const(val(2)))))),"
        + "callInfo('theLibrary,ids('number),const(varForwarding('myNumber))),assignment('theLibrary,nilocdecl,(none),(var('number) := const(val(2)))))"
    )
    assert normalize_whitespace(result) == normalize_whitespace(expected), f"Expected: {expected}\nGot: {result}"


def test_library_call_with_start_condition(translate_xml_with_libraries):
    """Test library call with start condition."""
    # Main plan XML
    main_xml = """
    <Node NodeType="LibraryNodeCall">
        <NodeId>ConditionalLibCall</NodeId>
        <StartCondition>
            <BooleanValue>true</BooleanValue>
        </StartCondition>
        <NodeBody>
            <LibraryNodeCall>
                <NodeId>theLibrary</NodeId>
            </LibraryNodeCall>
        </NodeBody>
    </Node>
    """

    # Library definition XML
    library_xml = """
    <Node NodeType="Empty">
        <NodeId>theLibrary</NodeId>
    </Node>
    """

    result = translate_xml_with_libraries(
        main_xml, Node, libraries={"theLibrary": library_xml}
    )
    expected = "library('ConditionalLibCall,nilocdecl,(none),((startc: (const(val(true))))),callInfo('theLibrary,ids(nilq),nilpar),empty('theLibrary,nilocdecl,(none)))"
    assert normalize_whitespace(result) == normalize_whitespace(expected), f"Expected: {expected}\nGot: {result}"
