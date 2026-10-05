"""PLEXIL execution log parsing to JSON."""

from .models import Trace, Macro, Micro, Transition
from .diff import compare_traces, DiffResult

__version__ = "0.1.0"
__all__ = ["Trace", "Macro", "Micro", "Transition", "compare_traces", "DiffResult"]
