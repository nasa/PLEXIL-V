"""Parser for Maude/PLEXIL-V logs."""

from typing import List, Optional, Tuple

from ..models import Trace, Macro, Micro, Transition
from ..validation import validate_log_content, ValidationLevel, LogValidationError
from .rules import MaudeRules


class MaudeParser:
    """Parse Maude/PLEXIL-V logs to JSON-serializable Trace.

    Maude logs have a cleaner structure with explicit MACRO and micro markers.
    Node identifiers may be qualified paths like 'node1 . 'parent, but we
    extract only the local name for now.

    Example input:
        MACRO
            'squareRoot from inactive to waiting
         micro
            'squareRoot from waiting to executing
         micro
        QuIeScEnCe
    """

    def __init__(self):
        self.rules = MaudeRules()

    def parse(self, content: str, validation_level: ValidationLevel = ValidationLevel.STRICT) -> Trace:
        """Parse log content into a Trace.

        Args:
            content: Full log content as string
            validation_level: Validation strictness (STRICT or LENIENT)

        Returns:
            Trace object containing parsed macro-steps

        Raises:
            LogValidationError: If validation_level is STRICT and log is invalid
        """
        # Validate log content if strict mode
        if validation_level == ValidationLevel.STRICT:
            result = validate_log_content(content, 'maude')
            if not result.is_valid:
                error_msg = "Invalid Maude log:\n  " + "\n  ".join(result.errors)
                raise LogValidationError(error_msg)

        lines = content.splitlines()
        macros = self._parse_macros(lines)
        return Trace(macros=macros)

    def _parse_macros(self, lines: List[str]) -> List[Macro]:
        """Parse all macro-steps from lines."""
        macros = []
        i = 0

        while i < len(lines):
            if self.rules.MACRO_START.match(lines[i]):
                macro, consumed = self._parse_macro(lines[i:])
                if macro:
                    macros.append(macro)
                i += consumed
            else:
                i += 1

        return macros

    def _parse_macro(self, lines: List[str]) -> Tuple[Optional[Macro], int]:
        """Parse single macro-step.

        Args:
            lines: Lines starting with MACRO marker

        Returns:
            Tuple of (parsed Macro or None, number of lines consumed)
        """
        if not self.rules.MACRO_START.match(lines[0]):
            return None, 0

        micros = []
        current_transitions = []
        i = 1  # Skip MACRO line

        while i < len(lines):
            line = lines[i]

            # Micro-step end?
            if self.rules.MICRO_END.match(line):
                if current_transitions:
                    micros.append(Micro(transitions=current_transitions))
                    current_transitions = []
                i += 1
                continue

            # Macro end?
            if self.rules.QUIESCENCE.match(line) or self.rules.MACRO_START.match(line):
                if current_transitions:
                    micros.append(Micro(transitions=current_transitions))
                return Macro(micros=micros), i

            # Parse transition
            match = self.rules.TRANSITION.match(line)
            if match:
                transition = self._parse_transition(match)
                if transition:
                    current_transitions.append(transition)

            i += 1

        # End of input
        if current_transitions:
            micros.append(Micro(transitions=current_transitions))

        return Macro(micros=micros), i

    def _parse_transition(self, match) -> Optional[Transition]:
        """Parse a transition from Maude format.

        Args:
            match: Regex match object from TRANSITION pattern

        Returns:
            Transition object or None if parsing fails
        """
        try:
            node_str = match.group('nodeid').strip()

            # Extract local name from qualified path
            # "'node1 . 'lookup8" -> "node1"
            if ' . ' in node_str:
                node_str = node_str.split(' . ')[0].strip()

            # Remove leading quote
            if node_str.startswith("'"):
                node_str = node_str[1:]

            from_state = match.group('from').lower()
            to_state = match.group('to').lower()

            # Normalize state names
            from_state = self._normalize_state(from_state)
            to_state = self._normalize_state(to_state)

            return Transition(
                node_id=node_str,
                from_state=from_state,
                to_state=to_state
            )
        except (ValueError, KeyError, AttributeError):
            return None

    def _normalize_state(self, state: str) -> str:
        """Normalize state name to consistent format.

        Args:
            state: State name from log (may have underscores, uppercase)

        Returns:
            Normalized state name (lowercase, camelCase for iterationEnded)
        """
        # Handle special case: iterationended -> iterationEnded
        if state == 'iterationended':
            return 'iterationEnded'

        return state
