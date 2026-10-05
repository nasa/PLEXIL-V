"""Unit tests for data models."""

import json
import pytest

from plexilv_log.models import Transition, Micro, Macro, Trace


def test_transition_creation():
    """Test creating a Transition."""
    t = Transition(node_id="node1", from_state="inactive", to_state="waiting")
    assert t.node_id == "node1"
    assert t.from_state == "inactive"
    assert t.to_state == "waiting"


def test_transition_to_dict():
    """Test Transition JSON serialization."""
    t = Transition(node_id="node1", from_state="inactive", to_state="waiting")
    d = t.to_dict()
    assert d == {
        "nodeId": "node1",
        "fromState": "inactive",
        "toState": "waiting"
    }


def test_transition_immutable():
    """Test that Transition is immutable."""
    t = Transition(node_id="node1", from_state="inactive", to_state="waiting")
    with pytest.raises(AttributeError):
        t.node_id = "node2"


def test_micro_creation():
    """Test creating a Micro."""
    t1 = Transition(node_id="node1", from_state="inactive", to_state="waiting")
    t2 = Transition(node_id="node2", from_state="inactive", to_state="waiting")
    micro = Micro(transitions=[t1, t2])
    assert len(micro.transitions) == 2


def test_micro_to_dict():
    """Test Micro JSON serialization."""
    t = Transition(node_id="node1", from_state="inactive", to_state="waiting")
    micro = Micro(transitions=[t])
    d = micro.to_dict()
    assert "transitions" in d
    assert len(d["transitions"]) == 1
    assert d["transitions"][0]["nodeId"] == "node1"


def test_macro_creation():
    """Test creating a Macro."""
    t = Transition(node_id="test", from_state="inactive", to_state="waiting")
    micro = Micro(transitions=[t])
    macro = Macro(micros=[micro])
    assert len(macro.micros) == 1


def test_trace_creation():
    """Test creating a Trace."""
    t = Transition(node_id="test", from_state="inactive", to_state="waiting")
    micro = Micro(transitions=[t])
    macro = Macro(micros=[micro])
    trace = Trace(macros=[macro])
    assert len(trace.macros) == 1


def test_trace_to_json():
    """Test Trace JSON serialization."""
    t = Transition(node_id="test", from_state="inactive", to_state="waiting")
    micro = Micro(transitions=[t])
    macro = Macro(micros=[micro])
    trace = Trace(macros=[macro])

    json_str = trace.to_json()
    assert isinstance(json_str, str)
    assert '"nodeId": "test"' in json_str


def test_trace_json_roundtrip():
    """Test that JSON output can be parsed back."""
    t = Transition(node_id="test", from_state="inactive", to_state="waiting")
    micro = Micro(transitions=[t])
    macro = Macro(micros=[micro])
    trace = Trace(macros=[macro])

    json_str = trace.to_json()
    parsed = json.loads(json_str)

    assert "macros" in parsed
    assert len(parsed["macros"]) == 1
    assert "micros" in parsed["macros"][0]
    assert len(parsed["macros"][0]["micros"]) == 1
    assert "transitions" in parsed["macros"][0]["micros"][0]
    assert len(parsed["macros"][0]["micros"][0]["transitions"]) == 1
    assert parsed["macros"][0]["micros"][0]["transitions"][0]["nodeId"] == "test"


def test_trace_compact_json():
    """Test compact JSON output."""
    t = Transition(node_id="test", from_state="inactive", to_state="waiting")
    trace = Trace(macros=[Macro(micros=[Micro(transitions=[t])])])

    compact = trace.to_json(indent=None)
    assert "\n" not in compact  # No newlines in compact format


def test_trace_pretty_json():
    """Test pretty JSON output."""
    t = Transition(node_id="test", from_state="inactive", to_state="waiting")
    trace = Trace(macros=[Macro(micros=[Micro(transitions=[t])])])

    pretty = trace.to_json(indent=2)
    assert "\n" in pretty  # Has newlines in pretty format
