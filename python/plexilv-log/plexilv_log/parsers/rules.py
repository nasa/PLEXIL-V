"""Declarative regex patterns for parsing PLEXIL execution logs."""

import re
from typing import Pattern


class PlexilExecutiveRules:
    """Regex patterns for parsing PLEXIL Executive debug logs.

    The PLEXIL Executive outputs verbose debug logs with entries like:
    [PlexilExec:step] ==>Start cycle 1
    [PlexilExec:step][1:0:0] Transitioning Empty node squareRoot 0x... from INACTIVE to WAITING
    [PlexilExec:step] ==>End cycle 1
    """

    # Macro-step boundaries
    CYCLE_START: Pattern = re.compile(
        r'^\[PlexilExec:(?:step|cycle)\] ==>Start cycle (?P<num>\d+)$'
    )

    CYCLE_END: Pattern = re.compile(
        r'^\[PlexilExec:(?:step|cycle)\] ==>End cycle (?P<num>\d+)$'
    )

    # Transition entry
    # [PlexilExec:step][macro:micro:trans] Transitioning [NodeType] node nodeid 0xADDR from STATE to STATE
    TRANSITION: Pattern = re.compile(
        r'^\[PlexilExec:step\]\[(?P<macro>\d+):(?P<micro>\d+):(?P<trans>\d+)\] '
        r'Transitioning( (?P<nodetype>\w+))? node (?P<nodeid>\S+) '
        r'0x[0-9a-fA-F]+ from (?P<from>\w+) to (?P<to>\w+)$'
    )


class MaudeRules:
    """Regex patterns for parsing Maude/PLEXIL-V logs.

    Maude logs have a cleaner format:
    MACRO
        'nodeid from inactive to waiting
     micro
        'nodeid from waiting to executing
     micro
    QuIeScEnCe
    """

    MACRO_START: Pattern = re.compile(r'^\s*MACRO\s*$')

    MICRO_END: Pattern = re.compile(r'^\s*micro\s*$')

    QUIESCENCE: Pattern = re.compile(r'^\s*QuIeScEnCe\s*$')

    # Transition with qualified identifiers
    # Format: 'node1 . 'parent from state to state
    # or: 'node from state to state
    TRANSITION: Pattern = re.compile(
        r'^\s*(?P<nodeid>[\w\.\'\s\-]+?)\s+'
        r'from\s+(?P<from>\w+)\s+'
        r'to\s+(?P<to>\w+)\s*$'
    )
