import maude
from typing import Dict, Type, Callable, Any

class TranslatorContext:
    def __init__(self, module: maude.Module):
        self.module = module
        self._encoders: Dict[Type, Callable] = {}
        self._decoders: Dict[str, Callable] = {}

    def encoder(self, py_type: Type):
        """Decorator to register a Python -> Maude translator."""
        def decorator(func):
            self._encoders[py_type] = func
            return func
        return decorator

    def decoder(self, maude_sort: str):
        """Decorator to register a Maude -> Python translator."""
        def decorator(func):
            self._decoders[maude_sort] = func
            return func
        return decorator

    def to_maude(self, obj: Any) -> maude.Term:
        """Translates a Python object to a Maude term compositionally."""
        py_type = type(obj)
        if py_type not in self._encoders:
            raise ValueError(f"No encoder registered for Python type: {py_type}")
        return self._encoders[py_type](self, obj)

    def from_maude(self, term: maude.Term) -> Any:
        """Translates a Maude term to a Python object compositionally."""
        sort_name = term.getSort().name() if hasattr(term.getSort(), 'name') else str(term.getSort())

        if sort_name in self._decoders:
            return self._decoders[sort_name](self, term)

        # Strip brackets if it's a kind, e.g. [Arguments] -> Arguments or NeArguments depending on what's registered
        if sort_name.startswith('[') and sort_name.endswith(']'):
            stripped = sort_name[1:-1]
            if stripped in self._decoders:
                return self._decoders[stripped](self, term)
            # Try Ne variants commonly used in Maude
            if f"Ne{stripped}" in self._decoders:
                return self._decoders[f"Ne{stripped}"](self, term)

        # Fallback to checking if we have a decoder for a supersort
        # This is useful if the sort is IntValue but we only registered PrimitiveValue (though we register specifically usually)
        for registered_sort in self._decoders:
            try:
                maude_sort = self.module.findSort(registered_sort)
                if maude_sort and term.getSort() <= maude_sort:
                    return self._decoders[registered_sort](self, term)
            except Exception:
                pass

        raise ValueError(f"No decoder registered for Maude sort: {sort_name}")
