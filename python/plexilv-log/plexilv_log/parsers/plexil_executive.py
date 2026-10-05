"""Parser for PLEXIL Executive debug logs."""

from typing import List, Optional, Tuple

from ..models import Trace, Macro, Micro, Transition
from ..validation import validate_log_content, ValidationLevel, LogValidationError
from .rules import PlexilExecutiveRules


class PlexilExecutiveParser:
    """Parse PLEXIL Executive debug logs to JSON-serializable Trace.

    The PLEXIL Executive outputs verbose debug logs showing node
    state transitions grouped by macro-step cycles. Each cycle
    contains multiple micro-steps identified by [macro:micro:trans] IDs.

    Example input:
        [PlexilExec:step] ==>Start cycle 1
        [PlexilExec:step][1:0:0] Transitioning Empty node squareRoot 0x... from INACTIVE to WAITING
        [PlexilExec:step][1:1:0] Transitioning Empty node squareRoot 0x... from WAITING to EXECUTING
        [PlexilExec:step] ==>End cycle 1
    """

    def __init__(self):
        self.rules = PlexilExecutiveRules()

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
            result = validate_log_content(content, 'plexil')
            if not result.is_valid:
                error_msg = "Invalid PLEXIL Executive log:\n  " + "\n  ".join(result.errors)
                raise LogValidationError(error_msg)

        lines = content.splitlines()
        macros = self._parse_macros(lines)
        return Trace(macros=macros)

    def _parse_macros(self, lines: List[str]) -> List[Macro]:
        """Parse all macro-steps from lines."""
        macros = []
        i = 0

        while i < len(lines):
            match = self.rules.CYCLE_START.match(lines[i])
            if match:
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
            lines: Lines starting with cycle start marker

        Returns:
            Tuple of (parsed Macro or None, number of lines consumed)
        """
        if not self.rules.CYCLE_START.match(lines[0]):
            return None, 0

        micros = []
        i = 1  # Skip cycle start

        # Group transitions by [macro:micro] ID
        current_micro_transitions = []
        current_macro_id = None
        current_micro_id = None

        while i < len(lines):
            # Check for cycle end
            if self.rules.CYCLE_END.match(lines[i]):
                # Save pending micro
                if current_micro_transitions:
                    micros.append(Micro(transitions=current_micro_transitions))
                return Macro(micros=micros), i + 1

            # Try to parse transition
            match = self.rules.TRANSITION.match(lines[i])
            if match:
                macro_id = match.group('macro')
                micro_id = match.group('micro')

                # New micro-step?
                if macro_id != current_macro_id or micro_id != current_micro_id:
                    if current_micro_transitions:
                        micros.append(Micro(transitions=current_micro_transitions))
                        current_micro_transitions = []
                    current_macro_id = macro_id
                    current_micro_id = micro_id

                # Parse transition
                transition = self._parse_transition(match)
                if transition:
                    current_micro_transitions.append(transition)

            i += 1

        # Macro without proper end
        if current_micro_transitions:
            micros.append(Micro(transitions=current_micro_transitions))
        return Macro(micros=micros), i

    def _parse_transition(self, match) -> Optional[Transition]:
        """Parse a single transition from regex match.

        Args:
            match: Regex match object from TRANSITION pattern

        Returns:
            Transition object or None if parsing fails
        """
        try:
            node_id = match.group('nodeid')
            from_state = match.group('from').lower()
            to_state = match.group('to').lower()

            # Normalize state names (remove underscores, handle special cases)
            from_state = self._normalize_state(from_state)
            to_state = self._normalize_state(to_state)

            return Transition(
                node_id=node_id,
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
        # Remove underscores
        state = state.replace('_', '')

        # Handle special case: ITERATION_ENDED -> iterationEnded
        if state == 'iterationended':
            return 'iterationEnded'

        return state
