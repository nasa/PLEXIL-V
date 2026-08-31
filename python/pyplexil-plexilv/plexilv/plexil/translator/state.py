"""TranspilerContext for managing AST traversal state and symbol tables."""

from typing import Any
from plexil.core.v1.ast import PlexilPlan


class TranspilerContext:
    """Maintains AST stack and symbol table during transpilation."""

    def __init__(self, libraries: dict[str, PlexilPlan] | None = None):
        # AST Stack: list of parent nodes to allow children to reference parent data
        self.ast_stack: list[Any] = []

        # Symbol Table: stack of dictionaries for nested variable scoping
        self.symbol_table: list[dict[str, Any]] = [{}]

        # Library registry: maps library names to PlexilPlan ASTs
        self.libraries: dict[str, PlexilPlan] = libraries or {}

    def push_node(self, node: Any):
        """Push a node onto the AST stack."""
        self.ast_stack.append(node)

    def pop_node(self):
        """Pop a node from the AST stack."""
        if self.ast_stack:
            return self.ast_stack.pop()
        return None

    def current_node(self) -> Any:
        """Get the current node without popping."""
        if self.ast_stack:
            return self.ast_stack[-1]
        return None

    def parent_node(self) -> Any:
        """Get the parent of the current node."""
        if len(self.ast_stack) >= 2:
            return self.ast_stack[-2]
        return None

    def push_scope(self):
        """Create a new variable scope."""
        self.symbol_table.append({})

    def pop_scope(self):
        """Exit the current variable scope."""
        if len(self.symbol_table) > 1:
            self.symbol_table.pop()

    def declare_variable(self, name: str, var_type: str, value: Any = None):
        """Declare a variable in the current scope."""
        self.symbol_table[-1][name] = {"type": var_type, "value": value}

    def lookup_variable(self, name: str) -> dict[str, Any] | None:
        """Look up a variable in the symbol table (searches from current to outer scopes)."""
        for scope in reversed(self.symbol_table):
            if name in scope:
                return scope[name]
        return None

    def is_in_scope(self, name: str) -> bool:
        """Check if a variable is declared in any scope."""
        return self.lookup_variable(name) is not None
