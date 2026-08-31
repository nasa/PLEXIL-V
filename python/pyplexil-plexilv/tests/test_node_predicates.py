import pytest
from plexil.core.v1.ast import (
    # Node State Predicates
    Waiting,
    Executing,
    Finished,
    IterationEnded,
    Inactive,
    # Node Outcome Predicates
    Succeeded,
    Failed,
    Skipped,
    PostconditionFailed,
    # Composite Predicates
    NoChildFailed,
    # Knowledge Tests
    AllKnown,
    AnyKnown,
)

# ====================
# Node State Predicates
# ====================


def test_waiting_with_sibling(translate_xml):
    xml = """<Waiting>
      <NodeRef dir="sibling">Node1</NodeRef>
    </Waiting>"""
    assert translate_xml(xml, Waiting) == "isWaiting?(sibling('Node1))"


def test_waiting_with_self(translate_xml):
    xml = """<Waiting>
      <NodeRef dir="self" />
    </Waiting>"""
    assert translate_xml(xml, Waiting) == "isWaiting?(self)"


def test_executing_with_child(translate_xml):
    xml = """<Executing>
      <NodeRef dir="child">ChildNode</NodeRef>
    </Executing>"""
    assert translate_xml(xml, Executing) == "isExecuting?(child('ChildNode))"


def test_executing_with_node_id(translate_xml):
    xml = """<Executing>
      <NodeId>MyNode</NodeId>
    </Executing>"""
    assert translate_xml(xml, Executing) == "isExecuting?('MyNode)"


def test_finished_with_sibling(translate_xml):
    xml = """<Finished>
      <NodeRef dir="sibling">ASSIGNMENT__0</NodeRef>
    </Finished>"""
    assert translate_xml(xml, Finished) == "isFinished?(sibling('ASSIGNMENT__0))"


def test_finished_with_node_id(translate_xml):
    xml = """<Finished>
      <NodeId>ConjunctTest1</NodeId>
    </Finished>"""
    assert translate_xml(xml, Finished) == "isFinished?('ConjunctTest1)"


def test_iteration_ended_with_self(translate_xml):
    xml = """<IterationEnded>
      <NodeRef dir="self" />
    </IterationEnded>"""
    assert translate_xml(xml, IterationEnded) == "hasIterationEnded?(self)"


def test_iteration_ended_with_child(translate_xml):
    xml = """<IterationEnded>
      <NodeRef dir="child">LoopNode</NodeRef>
    </IterationEnded>"""
    assert translate_xml(xml, IterationEnded) == "hasIterationEnded?(child('LoopNode))"


def test_inactive_with_sibling(translate_xml):
    xml = """<Inactive>
      <NodeRef dir="sibling">IdleNode</NodeRef>
    </Inactive>"""
    assert translate_xml(xml, Inactive) == "isInactive?(sibling('IdleNode))"


def test_inactive_with_parent(translate_xml):
    xml = """<Inactive>
      <NodeRef dir="parent" />
    </Inactive>"""
    assert translate_xml(xml, Inactive) == "isInactive?(parent)"


# ====================
# Node Outcome Predicates
# ====================


def test_succeeded_with_sibling(translate_xml):
    xml = """<Succeeded>
      <NodeRef dir="sibling">ep2cp_IfTest</NodeRef>
    </Succeeded>"""
    assert translate_xml(xml, Succeeded) == "hasSucceeded?(sibling('ep2cp_IfTest))"


def test_succeeded_with_child(translate_xml):
    xml = """<Succeeded>
      <NodeRef dir="child">Task1</NodeRef>
    </Succeeded>"""
    assert translate_xml(xml, Succeeded) == "hasSucceeded?(child('Task1))"


def test_failed_with_sibling(translate_xml):
    xml = """<Failed>
      <NodeRef dir="sibling">TestNode</NodeRef>
    </Failed>"""
    assert translate_xml(xml, Failed) == "hasFailed?(sibling('TestNode))"


def test_failed_with_node_id(translate_xml):
    xml = """<Failed>
      <NodeId>CriticalTask</NodeId>
    </Failed>"""
    assert translate_xml(xml, Failed) == "hasFailed?('CriticalTask)"


def test_skipped_with_sibling(translate_xml):
    xml = """<Skipped>
      <NodeRef dir="sibling">ep2cp_ElseIf-1</NodeRef>
    </Skipped>"""
    assert translate_xml(xml, Skipped) == "hasSkipped?(sibling('ep2cp_ElseIf-1))"


def test_skipped_with_self(translate_xml):
    xml = """<Skipped>
      <NodeRef dir="self" />
    </Skipped>"""
    assert translate_xml(xml, Skipped) == "hasSkipped?(self)"


def test_postcondition_failed_with_sibling(translate_xml):
    xml = """<PostconditionFailed>
      <NodeRef dir="sibling">ep2cp_IfTest</NodeRef>
    </PostconditionFailed>"""
    assert (
        translate_xml(xml, PostconditionFailed)
        == "hasPostconditionFailed?(sibling('ep2cp_IfTest))"
    )


def test_postcondition_failed_with_child(translate_xml):
    xml = """<PostconditionFailed>
      <NodeRef dir="child">ValidationNode</NodeRef>
    </PostconditionFailed>"""
    assert (
        translate_xml(xml, PostconditionFailed)
        == "hasPostconditionFailed?(child('ValidationNode))"
    )


# ====================
# Composite Predicates
# ====================


def test_no_child_failed_with_self(translate_xml):
    xml = """<NoChildFailed>
      <NodeRef dir="self"/>
    </NoChildFailed>"""
    assert translate_xml(xml, NoChildFailed) == "noChildFailed"


def test_no_child_failed_with_parent(translate_xml):
    xml = """<NoChildFailed>
      <NodeRef dir="parent"/>
    </NoChildFailed>"""
    assert translate_xml(xml, NoChildFailed) == "noChildFailed"


def test_no_child_failed_with_node_id(translate_xml):
    xml = """<NoChildFailed>
      <NodeId>ParentNode</NodeId>
    </NoChildFailed>"""
    assert translate_xml(xml, NoChildFailed) == "noChildFailed"


# ====================
# Knowledge Tests
# ====================


def test_all_known_with_array_variable(translate_xml):
    xml = """<ALL_KNOWN>
      <ArrayVariable>myArray</ArrayVariable>
    </ALL_KNOWN>"""
    assert translate_xml(xml, AllKnown) == "allKnown(var('myArray))"


def test_all_known_with_lookup(translate_xml):
    xml = """<ALL_KNOWN>
      <LookupNow>
        <Name>
          <StringValue>arrayState</StringValue>
        </Name>
      </LookupNow>
    </ALL_KNOWN>"""
    assert translate_xml(xml, AllKnown) == "allKnown(lookup('arrayState,(nilpar)))"


def test_any_known_with_array_variable(translate_xml):
    xml = """<ANY_KNOWN>
      <ArrayVariable>dataArray</ArrayVariable>
    </ANY_KNOWN>"""
    assert translate_xml(xml, AnyKnown) == "anyKnown(var('dataArray))"


def test_any_known_with_array_value(translate_xml):
    xml = """<ANY_KNOWN>
      <ArrayValue Type="Integer">
        <IntegerValue>1</IntegerValue>
        <IntegerValue>2</IntegerValue>
      </ArrayValue>
    </ANY_KNOWN>"""
    assert translate_xml(xml, AnyKnown) == "anyKnown(const(array(val(1) # val(2))))"
