from .context import TranslatorContext
from .environment import register_environment_translators
from .inputs import register_input_translators

def register_all_translators(ctx: TranslatorContext):
    register_environment_translators(ctx)
    register_input_translators(ctx)

__all__ = [
    'TranslatorContext',
    'register_environment_translators',
    'register_input_translators',
    'register_all_translators',
]