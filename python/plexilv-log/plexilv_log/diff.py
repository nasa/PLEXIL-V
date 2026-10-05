"""Diff functionality for comparing execution traces."""

import json
from typing import Any, Dict, List, Tuple
from enum import Enum

from .models import Trace, Macro, Micro, Transition


class DiffResult(Enum):
    """Result of comparison."""
    EQUAL = "equal"
    DIFFERENT = "different"


def compare_traces(first: Trace, second: Trace) -> Tuple[DiffResult, Dict[str, Any]]:
    """Compare two traces and return detailed diff information.

    Args:
        first: First trace (typically from PLEXIL Executive)
        second: Second trace (typically from Maude)

    Returns:
        Tuple of (result, diff_details) where diff_details contains:
        - result: "equal" or "different"
        - differences: List of differences found (empty if equal)
        - stats: Statistics about the comparison
    """
    differences = []

    # Compare number of macros
    if len(first.macros) != len(second.macros):
        differences.append({
            "type": "macro_count",
            "first": len(first.macros),
            "second": len(second.macros),
            "message": f"Different number of macro-steps: {len(first.macros)} vs {len(second.macros)}"
        })

    # Compare each macro
    max_macros = max(len(first.macros), len(second.macros))
    for i in range(max_macros):
        first_macro = first.macros[i] if i < len(first.macros) else None
        second_macro = second.macros[i] if i < len(second.macros) else None

        if first_macro is None:
            differences.append({
                "type": "missing_macro",
                "macro_index": i,
                "location": "first",
                "message": f"Macro {i}: missing in first trace"
            })
            continue

        if second_macro is None:
            differences.append({
                "type": "missing_macro",
                "macro_index": i,
                "location": "second",
                "message": f"Macro {i}: missing in second trace"
            })
            continue

        # Compare micros in this macro
        macro_diffs = _compare_macros(first_macro, second_macro, i)
        differences.extend(macro_diffs)

    result = DiffResult.EQUAL if not differences else DiffResult.DIFFERENT

    diff_details = {
        "result": result.value,
        "differences": differences,
        "stats": {
            "first_macros": len(first.macros),
            "second_macros": len(second.macros),
            "total_differences": len(differences)
        }
    }

    return result, diff_details


def _compare_macros(first: Macro, second: Macro, macro_index: int) -> List[Dict[str, Any]]:
    """Compare two macros and return list of differences."""
    differences = []

    if len(first.micros) != len(second.micros):
        differences.append({
            "type": "micro_count",
            "macro_index": macro_index,
            "first": len(first.micros),
            "second": len(second.micros),
            "message": f"Macro {macro_index}: different number of micro-steps: {len(first.micros)} vs {len(second.micros)}"
        })

    # Compare each micro
    max_micros = max(len(first.micros), len(second.micros))
    for i in range(max_micros):
        first_micro = first.micros[i] if i < len(first.micros) else None
        second_micro = second.micros[i] if i < len(second.micros) else None

        if first_micro is None:
            differences.append({
                "type": "missing_micro",
                "macro_index": macro_index,
                "micro_index": i,
                "location": "first",
                "message": f"Macro {macro_index}, Micro {i}: missing in first trace"
            })
            continue

        if second_micro is None:
            differences.append({
                "type": "missing_micro",
                "macro_index": macro_index,
                "micro_index": i,
                "location": "second",
                "message": f"Macro {macro_index}, Micro {i}: missing in second trace"
            })
            continue

        # Compare transitions in this micro
        micro_diffs = _compare_micros(first_micro, second_micro, macro_index, i)
        differences.extend(micro_diffs)

    return differences


def _compare_micros(first: Micro, second: Micro, macro_index: int, micro_index: int) -> List[Dict[str, Any]]:
    """Compare two micros and return list of differences."""
    differences = []

    # Convert to sets for comparison
    first_set = {(t.node_id, t.from_state, t.to_state) for t in first.transitions}
    second_set = {(t.node_id, t.from_state, t.to_state) for t in second.transitions}

    # Find transitions only in first
    only_in_first = first_set - second_set
    for node_id, from_state, to_state in only_in_first:
        differences.append({
            "type": "missing_transition",
            "macro_index": macro_index,
            "micro_index": micro_index,
            "location": "second",
            "transition": {
                "nodeId": node_id,
                "fromState": from_state,
                "toState": to_state
            },
            "message": f"Macro {macro_index}, Micro {micro_index}: transition '{node_id}: {from_state}→{to_state}' only in first trace"
        })

    # Find transitions only in second
    only_in_second = second_set - first_set
    for node_id, from_state, to_state in only_in_second:
        differences.append({
            "type": "missing_transition",
            "macro_index": macro_index,
            "micro_index": micro_index,
            "location": "first",
            "transition": {
                "nodeId": node_id,
                "fromState": from_state,
                "toState": to_state
            },
            "message": f"Macro {macro_index}, Micro {micro_index}: transition '{node_id}: {from_state}→{to_state}' only in second trace"
        })

    return differences


def format_diff_report(diff_details: Dict[str, Any], verbose: bool = False) -> str:
    """Format diff details as human-readable report.

    Args:
        diff_details: Output from compare_traces
        verbose: Include detailed difference information

    Returns:
        Formatted string report
    """
    lines = []

    result = diff_details["result"]
    stats = diff_details["stats"]
    differences = diff_details["differences"]

    # Header
    lines.append("=" * 60)
    lines.append("TRACE COMPARISON REPORT")
    lines.append("=" * 60)

    # Statistics
    lines.append(f"First trace:  {stats['first_macros']} macro-steps")
    lines.append(f"Second trace: {stats['second_macros']} macro-steps")
    lines.append(f"Differences:  {stats['total_differences']}")
    lines.append("")

    # Result
    if result == "equal":
        lines.append("✓ TRACES ARE EQUAL")
        return "\n".join(lines)

    lines.append("✗ TRACES DIFFER")
    lines.append("")

    if not verbose:
        # Summary only
        lines.append(f"Found {len(differences)} difference(s).")
        lines.append("Run with --verbose for detailed diff.")
        return "\n".join(lines)

    # Detailed differences
    lines.append("DETAILED DIFFERENCES:")
    lines.append("-" * 60)

    for i, diff in enumerate(differences, 1):
        lines.append(f"\n[{i}] {diff['message']}")

        if diff['type'] == 'missing_transition' and 'transition' in diff:
            trans = diff['transition']
            lines.append(f"    Transition: {trans['nodeId']}: {trans['fromState']} → {trans['toState']}")

    return "\n".join(lines)


def format_json_diff(diff_details: Dict[str, Any]) -> str:
    """Format diff details as JSON.

    Args:
        diff_details: Output from compare_traces

    Returns:
        JSON string
    """
    return json.dumps(diff_details, indent=2)
