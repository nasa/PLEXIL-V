"""Tests for Node reconstruction from AnyElement children.

This test suite validates that when nodes are parsed as children of a NodeList,
all their child elements (Conditions, Interface, etc.) are properly reconstructed
into the Node with correct PascalCase → snake_case attribute conversion.

This prevents regression of the bug where elements like StartCondition were
converted to 'startCondition' (camelCase) instead of 'start_condition' (snake_case),
causing them to be silently ignored.
"""

import pytest
from plexil.core.v1.ast import Node
from tests.conftest import normalize_whitespace


def test_all_condition_types_are_reconstructed(translate_xml):
    """Test that ALL condition types are properly converted and preserved.

    This test would FAIL with the old buggy conversion:
    - Old: elem_type[0].lower() + elem_type[1:] → 'startCondition'
    - New: re.sub(r'(?<!^)(?=[A-Z])', '_', elem_type).lower() → 'start_condition'
    """
    xml = """
    <Node NodeType="NodeList">
        <NodeId>ConditionTests</NodeId>
        <NodeBody>
            <NodeList>
                <!-- Child 1: StartCondition -->
                <Node NodeType="Command">
                    <NodeId>WithStart</NodeId>
                    <StartCondition>
                        <BooleanValue>true</BooleanValue>
                    </StartCondition>
                    <NodeBody>
                        <Command>
                            <Name><StringValue>cmd1</StringValue></Name>
                        </Command>
                    </NodeBody>
                </Node>

                <!-- Child 2: EndCondition -->
                <Node NodeType="Command">
                    <NodeId>WithEnd</NodeId>
                    <EndCondition>
                        <BooleanValue>false</BooleanValue>
                    </EndCondition>
                    <NodeBody>
                        <Command>
                            <Name><StringValue>cmd2</StringValue></Name>
                        </Command>
                    </NodeBody>
                </Node>

                <!-- Child 3: PreCondition -->
                <Node NodeType="Assignment">
                    <NodeId>WithPre</NodeId>
                    <PreCondition>
                        <GT>
                            <IntegerVariable>x</IntegerVariable>
                            <IntegerValue>0</IntegerValue>
                        </GT>
                    </PreCondition>
                    <NodeBody>
                        <Assignment>
                            <IntegerVariable>y</IntegerVariable>
                            <NumericRHS><IntegerValue>1</IntegerValue></NumericRHS>
                        </Assignment>
                    </NodeBody>
                </Node>

                <!-- Child 4: PostCondition -->
                <Node NodeType="Empty">
                    <NodeId>WithPost</NodeId>
                    <PostCondition>
                        <BooleanVariable>success</BooleanVariable>
                    </PostCondition>
                </Node>

                <!-- Child 5: InvariantCondition -->
                <Node NodeType="Empty">
                    <NodeId>WithInvariant</NodeId>
                    <InvariantCondition>
                        <IsKnown>
                            <IntegerVariable>counter</IntegerVariable>
                        </IsKnown>
                    </InvariantCondition>
                </Node>

                <!-- Child 6: RepeatCondition -->
                <Node NodeType="Empty">
                    <NodeId>WithRepeat</NodeId>
                    <RepeatCondition>
                        <LT>
                            <IntegerVariable>i</IntegerVariable>
                            <IntegerValue>10</IntegerValue>
                        </LT>
                    </RepeatCondition>
                </Node>

                <!-- Child 7: SkipCondition -->
                <Node NodeType="Empty">
                    <NodeId>WithSkip</NodeId>
                    <SkipCondition>
                        <BooleanVariable>skipFlag</BooleanVariable>
                    </SkipCondition>
                </Node>

                <!-- Child 8: ExitCondition -->
                <Node NodeType="Empty">
                    <NodeId>WithExit</NodeId>
                    <ExitCondition>
                        <BooleanVariable>exitFlag</BooleanVariable>
                    </ExitCondition>
                </Node>
            </NodeList>
        </NodeBody>
    </Node>
    """
    result = translate_xml(xml, Node)

    # Verify each condition type is translated (not silently dropped as (none))
    assert (
        "startc: (const(val(true)))" in result
    ), "StartCondition not found - case conversion bug?"
    assert (
        "endc: (const(val(false)))" in result
    ), "EndCondition not found - case conversion bug?"
    assert (
        "pre: (_>_(var('x),const(val(0))))" in result
    ), "PreCondition not found - case conversion bug?"
    assert (
        "post: (var('success))" in result
    ), "PostCondition not found - case conversion bug?"
    assert (
        "inv: (isKnown(var('counter)))" in result
    ), "InvariantCondition not found - case conversion bug?"
    assert (
        "repeatc: (_<_(var('i),const(val(10))))" in result
    ), "RepeatCondition not found - case conversion bug?"
    assert (
        "skip: (var('skipFlag))" in result
    ), "SkipCondition not found - case conversion bug?"
    assert (
        "exitc: (var('exitFlag))" in result
    ), "ExitCondition not found - case conversion bug?"

    # Ensure none of them output (none) instead of the actual condition
    # Simply count occurrences of each condition type in the result
    condition_markers = [
        "((startc:",
        "((endc:",
        "((pre:",
        "((post:",
        "((inv:",
        "((repeatc:",
        "((skip:",
        "((exitc:",
    ]
    conditions_present = sum(1 for marker in condition_markers if marker in result)

    assert (
        conditions_present == 8
    ), f"Expected 8 conditions but found {conditions_present} - some may have been lost to (none)"


def test_interface_is_reconstructed_in_library_node(translate_xml_with_libraries):
    """Test that Interface elements are properly preserved.

    Interface uses the same reconstruction logic, so this would also fail
    with the buggy case conversion.
    """
    # Define the library that will be called
    library_xml = """
    <Node NodeType="Empty">
        <NodeId>SomeLibrary</NodeId>
    </Node>
    """

    xml = """
    <Node NodeType="NodeList">
        <NodeId>LibraryTest</NodeId>
        <NodeBody>
            <NodeList>
                <Node NodeType="LibraryNodeCall">
                    <NodeId>CallWithInterface</NodeId>
                    <Interface>
                        <In>
                            <DeclareVariable>
                                <Name>inputParam</Name>
                                <Type>Integer</Type>
                            </DeclareVariable>
                        </In>
                        <InOut>
                            <DeclareVariable>
                                <Name>inoutParam</Name>
                                <Type>Real</Type>
                            </DeclareVariable>
                        </InOut>
                    </Interface>
                    <NodeBody>
                        <LibraryNodeCall>
                            <NodeId>SomeLibrary</NodeId>
                        </LibraryNodeCall>
                    </NodeBody>
                </Node>
            </NodeList>
        </NodeBody>
    </Node>
    """
    result = translate_xml_with_libraries(xml, Node, {"SomeLibrary": library_xml})
    normalized = normalize_whitespace(result)

    # If Interface is not preserved, the library call would be missing interface info
    # The library translation includes interface parameters
    assert "library('CallWithInterface" in normalized, "Library node not found"
    # When interface is present, it should show the parameter declarations
    assert (
        "'inputParam:unknown" in normalized or "ids(" in normalized
    ), "Interface parameters not preserved"


def test_variable_declarations_still_work(translate_xml):
    """Test that VariableDeclarations (which was hardcoded) still works.

    This ensures we didn't break existing hardcoded elements when making
    the conversion generic.
    """
    xml = """
    <Node NodeType="NodeList">
        <NodeId>VarDeclTest</NodeId>
        <NodeBody>
            <NodeList>
                <Node NodeType="Empty">
                    <NodeId>WithVars</NodeId>
                    <VariableDeclarations>
                        <DeclareVariable>
                            <Name>localVar</Name>
                            <Type>Integer</Type>
                            <InitialValue>
                                <IntegerValue>42</IntegerValue>
                            </InitialValue>
                        </DeclareVariable>
                    </VariableDeclarations>
                </Node>
            </NodeList>
        </NodeBody>
    </Node>
    """
    result = translate_xml(xml, Node)

    assert "(('localVar : val(42)))" in result, "VariableDeclarations not preserved"
    assert (
        "nilocdecl" not in result or "(('localVar" in result
    ), "Variables should not be nilocdecl"


def test_multiple_elements_together(translate_xml):
    """Test that a node with multiple special elements works correctly.

    This catches issues where the conversion loop might exit early or
    overwrite previously set attributes.
    """
    xml = """
    <Node NodeType="NodeList">
        <NodeId>ComplexTest</NodeId>
        <NodeBody>
            <NodeList>
                <Node NodeType="Command">
                    <NodeId>ComplexNode</NodeId>
                    <VariableDeclarations>
                        <DeclareVariable>
                            <Name>temp</Name>
                            <Type>Real</Type>
                        </DeclareVariable>
                    </VariableDeclarations>
                    <StartCondition>
                        <BooleanValue>true</BooleanValue>
                    </StartCondition>
                    <EndCondition>
                        <BooleanValue>false</BooleanValue>
                    </EndCondition>
                    <InvariantCondition>
                        <GT>
                            <RealVariable>temp</RealVariable>
                            <RealValue>0.0</RealValue>
                        </GT>
                    </InvariantCondition>
                    <NodeBody>
                        <Command>
                            <Name><StringValue>measure</StringValue></Name>
                        </Command>
                    </NodeBody>
                </Node>
            </NodeList>
        </NodeBody>
    </Node>
    """
    result = translate_xml(xml, Node)
    normalized = normalize_whitespace(result)

    # All elements should be present
    assert "(('temp:unknown))" in normalized, "VariableDeclarations lost"
    assert "startc:(const(val(true)))" in normalized, "StartCondition lost"
    assert "endc:(const(val(false)))" in normalized, "EndCondition lost"
    assert "inv:(_>_(var('temp),const(val(0.0))))" in normalized, "InvariantCondition lost"

    # The node should have all three conditions, not (none)
    assert "command('ComplexNode" in normalized
    # Should have the pattern: command('ComplexNode,(vardecls),((startc:...) (endc:...) (inv:...))
    # Count the conditions - should be 3
    node_match = normalized[normalized.find("command('ComplexNode") :]
    node_match = node_match[
        : node_match.find("(('measure)")
    ]  # Just the node declaration part
    condition_count = (
        node_match.count("startc:")
        + node_match.count("endc:")
        + node_match.count("inv:")
    )
    assert condition_count == 3, f"Expected 3 conditions but found {condition_count}"


def test_case_conversion_regression_detector(translate_xml):
    """Explicit test for the exact bug: wrong case conversion.

    This test uses element types that would DEFINITELY fail with the old
    buggy conversion and includes assertions that check for the specific
    failure mode (outputting 'none' instead of the condition).
    """
    # These element types have capital letters in the middle that require
    # proper snake_case conversion:
    # - StartCondition -> start_condition (not startCondition)
    # - EndCondition -> end_condition (not endCondition)
    # - PostCondition -> post_condition (not postCondition)
    # - InvariantCondition -> invariant_condition (not invariantCondition)

    xml = """
    <Node NodeType="NodeList">
        <NodeId>CaseConversionTest</NodeId>
        <NodeBody>
            <NodeList>
                <Node NodeType="Command">
                    <NodeId>TestNode</NodeId>
                    <StartCondition>
                        <EQInternal>
                            <NodeStateVariable>
                                <NodeId>OtherNode</NodeId>
                            </NodeStateVariable>
                            <NodeStateValue>FINISHED</NodeStateValue>
                        </EQInternal>
                    </StartCondition>
                    <NodeBody>
                        <Command>
                            <Name><StringValue>test</StringValue></Name>
                        </Command>
                    </NodeBody>
                </Node>
            </NodeList>
        </NodeBody>
    </Node>
    """
    result = translate_xml(xml, Node)

    # The bug symptom: condition becomes (none) instead of being translated
    assert (
        "(none)" not in result or "startc:" in result
    ), "Found (none) without startc: - this means StartCondition was SILENTLY DROPPED due to case conversion bug!"

    # The correct output: condition is present
    assert (
        "startc: (isStatus?('OtherNode,finished))" in result
    ), "StartCondition not found - the case conversion is broken (PascalCase → snake_case failed)"

    # Make it very explicit what went wrong if this fails
    if "(none)" in result and "startc:" not in result:
        raise AssertionError(
            "CASE CONVERSION BUG DETECTED!\n"
            "The StartCondition was dropped because the PascalCase → snake_case conversion is broken.\n"
            "Expected: 'StartCondition' -> 'start_condition'\n"
            "Got: 'StartCondition' -> 'startCondition' (wrong!)\n"
            "The attribute 'startCondition' doesn't exist on Node (it's 'start_condition'),\n"
            "so the condition was silently ignored and output as (none).\n"
            f"Actual output:\n{result}"
        )


def test_node_id_and_node_body_still_work(translate_xml):
    """Test that NodeId and NodeBody (special cases) still work.

    These were handled specially in the old code, make sure they work
    with the generic conversion too.
    """
    xml = """
    <Node NodeType="NodeList">
        <NodeId>SpecialCasesTest</NodeId>
        <NodeBody>
            <NodeList>
                <Node NodeType="Empty">
                    <NodeId>ChildNode</NodeId>
                </Node>
                <Node NodeType="Command">
                    <NodeId>AnotherChild</NodeId>
                    <NodeBody>
                        <Command>
                            <Name><StringValue>cmd</StringValue></Name>
                        </Command>
                    </NodeBody>
                </Node>
            </NodeList>
        </NodeBody>
    </Node>
    """
    result = translate_xml(xml, Node)
    normalized = normalize_whitespace(result)

    # NodeId should be converted and used
    assert "empty('ChildNode" in normalized, "NodeId not converted (node_id)"
    assert (
        "command('AnotherChild" in normalized
    ), "NodeId not converted in command node (node_id)"

    # NodeBody should be converted and used to determine node type
    assert (
        "command(" in normalized
    ), "NodeBody not processed (node_body) - command node became wrong type"
