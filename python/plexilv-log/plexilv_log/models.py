"""Data models for PLEXIL execution traces."""

from dataclasses import dataclass, field
from typing import List
import json


@dataclass(frozen=True, order=True)
class Transition:
    """A single node state transition.

    Attributes:
        node_id: Node identifier (local name, e.g., "node1", "squareRoot")
        from_state: Origin state (e.g., "inactive", "waiting")
        to_state: Destination state (e.g., "waiting", "executing")
    """
    node_id: str
    from_state: str
    to_state: str

    def to_dict(self):
        """Convert to dictionary for JSON serialization."""
        return {
            "nodeId": self.node_id,
            "fromState": self.from_state,
            "toState": self.to_state
        }


@dataclass(frozen=True)
class Micro:
    """A micro-step containing concurrent transitions.

    Transitions within a micro-step occur simultaneously in the
    synchronous execution model.

    Attributes:
        transitions: List of concurrent node state transitions
    """
    transitions: List[Transition] = field(default_factory=list)

    def to_dict(self):
        """Convert to dictionary for JSON serialization."""
        return {
            "transitions": [t.to_dict() for t in self.transitions]
        }


@dataclass(frozen=True)
class Macro:
    """A macro-step containing multiple micro-steps.

    A macro-step represents one quiescence cycle in PLEXIL execution,
    consisting of multiple micro-steps followed by environment input.

    Attributes:
        micros: Ordered list of micro-steps in this macro-step
    """
    micros: List[Micro] = field(default_factory=list)

    def to_dict(self):
        """Convert to dictionary for JSON serialization."""
        return {
            "micros": [m.to_dict() for m in self.micros]
        }


@dataclass(frozen=True)
class Trace:
    """Complete execution trace containing macro-steps.

    Represents the full execution history of a PLEXIL plan,
    organized as a sequence of macro-steps.

    Attributes:
        macros: Ordered list of macro-steps in execution order
    """
    macros: List[Macro] = field(default_factory=list)

    def to_dict(self):
        """Convert to dictionary for JSON serialization."""
        return {
            "macros": [m.to_dict() for m in self.macros]
        }

    def to_json(self, indent=2):
        """Convert to JSON string.

        Args:
            indent: Indentation level for pretty printing (None for compact)

        Returns:
            JSON string representation of the trace
        """
        return json.dumps(self.to_dict(), indent=indent)
