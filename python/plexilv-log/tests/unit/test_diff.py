"""Unit tests for diff functionality."""

import pytest

from plexilv_log.models import Transition, Micro, Macro, Trace
from plexilv_log.diff import compare_traces, DiffResult, format_diff_report


def test_compare_equal_traces():
    """Test comparing two identical traces."""
    t1 = Transition(node_id="node1", from_state="inactive", to_state="waiting")
    trace1 = Trace(macros=[Macro(micros=[Micro(transitions=[t1])])])
    trace2 = Trace(macros=[Macro(micros=[Micro(transitions=[t1])])])

    result, details = compare_traces(trace1, trace2)

    assert result == DiffResult.EQUAL
    assert details["result"] == "equal"
    assert len(details["differences"]) == 0


def test_compare_different_macro_count():
    """Test comparing traces with different number of macros."""
    t1 = Transition(node_id="node1", from_state="inactive", to_state="waiting")
    trace1 = Trace(macros=[Macro(micros=[Micro(transitions=[t1])])])
    trace2 = Trace(macros=[
        Macro(micros=[Micro(transitions=[t1])]),
        Macro(micros=[Micro(transitions=[t1])])
    ])

    result, details = compare_traces(trace1, trace2)

    assert result == DiffResult.DIFFERENT
    assert len(details["differences"]) > 0
    assert any(d["type"] == "macro_count" for d in details["differences"])


def test_compare_different_transitions():
    """Test comparing traces with different transitions."""
    t1 = Transition(node_id="node1", from_state="inactive", to_state="waiting")
    t2 = Transition(node_id="node2", from_state="inactive", to_state="waiting")

    trace1 = Trace(macros=[Macro(micros=[Micro(transitions=[t1])])])
    trace2 = Trace(macros=[Macro(micros=[Micro(transitions=[t2])])])

    result, details = compare_traces(trace1, trace2)

    assert result == DiffResult.DIFFERENT
    assert len(details["differences"]) > 0
    # Should have 2 differences: node1 only in first, node2 only in second
    assert len(details["differences"]) == 2


def test_compare_different_micro_count():
    """Test comparing macros with different number of micros."""
    t1 = Transition(node_id="node1", from_state="inactive", to_state="waiting")
    trace1 = Trace(macros=[Macro(micros=[
        Micro(transitions=[t1])
    ])])
    trace2 = Trace(macros=[Macro(micros=[
        Micro(transitions=[t1]),
        Micro(transitions=[t1])
    ])])

    result, details = compare_traces(trace1, trace2)

    assert result == DiffResult.DIFFERENT
    assert any(d["type"] == "micro_count" for d in details["differences"])


def test_compare_concurrent_transitions_order():
    """Test that order doesn't matter for concurrent transitions in same micro."""
    t1 = Transition(node_id="node1", from_state="inactive", to_state="waiting")
    t2 = Transition(node_id="node2", from_state="inactive", to_state="waiting")

    trace1 = Trace(macros=[Macro(micros=[Micro(transitions=[t1, t2])])])
    trace2 = Trace(macros=[Macro(micros=[Micro(transitions=[t2, t1])])])  # Different order

    result, details = compare_traces(trace1, trace2)

    assert result == DiffResult.EQUAL
    assert len(details["differences"]) == 0


def test_format_diff_report_equal():
    """Test formatting report for equal traces."""
    t1 = Transition(node_id="node1", from_state="inactive", to_state="waiting")
    trace1 = Trace(macros=[Macro(micros=[Micro(transitions=[t1])])])
    trace2 = Trace(macros=[Macro(micros=[Micro(transitions=[t1])])])

    result, details = compare_traces(trace1, trace2)
    report = format_diff_report(details)

    assert "EQUAL" in report
    assert "✓" in report


def test_format_diff_report_different():
    """Test formatting report for different traces."""
    t1 = Transition(node_id="node1", from_state="inactive", to_state="waiting")
    t2 = Transition(node_id="node2", from_state="inactive", to_state="waiting")

    trace1 = Trace(macros=[Macro(micros=[Micro(transitions=[t1])])])
    trace2 = Trace(macros=[Macro(micros=[Micro(transitions=[t2])])])

    result, details = compare_traces(trace1, trace2)
    report = format_diff_report(details, verbose=True)

    assert "DIFFER" in report
    assert "✗" in report
    assert "node1" in report
    assert "node2" in report


def test_compare_empty_traces():
    """Test comparing empty traces."""
    trace1 = Trace(macros=[])
    trace2 = Trace(macros=[])

    result, details = compare_traces(trace1, trace2)

    assert result == DiffResult.EQUAL
    assert len(details["differences"]) == 0


def test_compare_empty_vs_nonempty():
    """Test comparing empty trace with non-empty trace."""
    t1 = Transition(node_id="node1", from_state="inactive", to_state="waiting")
    trace1 = Trace(macros=[])
    trace2 = Trace(macros=[Macro(micros=[Micro(transitions=[t1])])])

    result, details = compare_traces(trace1, trace2)

    assert result == DiffResult.DIFFERENT
    assert details["stats"]["first_macros"] == 0
    assert details["stats"]["second_macros"] == 1


def test_diff_statistics():
    """Test that diff statistics are correctly calculated."""
    t1 = Transition(node_id="node1", from_state="inactive", to_state="waiting")
    trace1 = Trace(macros=[
        Macro(micros=[Micro(transitions=[t1])]),
        Macro(micros=[Micro(transitions=[t1])])
    ])
    trace2 = Trace(macros=[
        Macro(micros=[Micro(transitions=[t1])])
    ])

    result, details = compare_traces(trace1, trace2)

    assert details["stats"]["first_macros"] == 2
    assert details["stats"]["second_macros"] == 1
    assert details["stats"]["total_differences"] == len(details["differences"])
