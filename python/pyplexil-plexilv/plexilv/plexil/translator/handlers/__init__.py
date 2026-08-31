"""PLEXIL translation handlers.

All handlers are automatically registered when this package is imported.
"""

# Import all handler modules to register their @translate.register decorators
from . import values
from . import expressions
from . import arrays
from . import lookups
from . import predicates
from . import nodes
from . import declarations
from . import actions
from . import conditions

__all__ = [
    "values",
    "expressions",
    "arrays",
    "lookups",
    "predicates",
    "nodes",
    "declarations",
    "actions",
    "conditions",
]
