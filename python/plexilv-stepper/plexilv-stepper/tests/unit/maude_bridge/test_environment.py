import maude
from plexilv_stepper.maude_bridge.context import TranslatorContext
from plexilv_stepper.models import State, StateEntry
import pytest

@pytest.fixture
def ctx(maude_module):
    context = TranslatorContext(maude_module)
    from plexilv_stepper.maude_bridge.environment import register_environment_translators
    register_environment_translators(context)
    return context

def get_canonical_str(term: maude.Term) -> str:
    """Helper to get a clean unformatted string representation."""
    return term.prettyPrint(maude.PRINT_MIXFIX | maude.PRINT_NUMBER)

def test_encode_decode_primitives(ctx):
    # Test Int
    term_int = ctx.to_maude(42)
    assert get_canonical_str(term_int) == 'val(42)'
    assert str(term_int.getSort()) == 'IntValue'
    assert ctx.from_maude(term_int) == 42

    # Test Bool True
    term_bool_true = ctx.to_maude(True)
    assert get_canonical_str(term_bool_true) == 'val(true)'
    assert str(term_bool_true.getSort()) == 'BoolValue'
    assert ctx.from_maude(term_bool_true) is True

    # Test Bool False
    term_bool_false = ctx.to_maude(False)
    assert get_canonical_str(term_bool_false) == 'val(false)'
    assert str(term_bool_false.getSort()) == 'BoolValue'
    assert ctx.from_maude(term_bool_false) is False

    # Test Float
    term_float = ctx.to_maude(3.5)
    assert get_canonical_str(term_float) == 'val(3.5)'
    assert str(term_float.getSort()) == 'FloatValue'
    assert ctx.from_maude(term_float) == 3.5

    # Test String
    term_str = ctx.to_maude("test")
    assert get_canonical_str(term_str) == 'val("test")'
    assert str(term_str.getSort()) == 'StringValue'
    assert ctx.from_maude(term_str) == "test"

    # Test Empty String
    term_empty_str = ctx.to_maude("")
    assert get_canonical_str(term_empty_str) == 'val("")'
    assert str(term_empty_str.getSort()) == 'StringValue'
    assert ctx.from_maude(term_empty_str) == ""

    # Test None
    term_none = ctx.to_maude(None)
    assert get_canonical_str(term_none) == 'unknown'
    assert str(term_none.symbol()) == 'unknown'
    assert ctx.from_maude(term_none) is None

def test_encode_decode_tuple(ctx):
    py_tuple = (1, 2.5, "hello")
    term_tuple = ctx.to_maude(py_tuple)
    # Ensure it's rendered as space-separated primitive values (Maude may add parens for associativity)
    assert get_canonical_str(term_tuple) == '(val(1) val(2.5)) val("hello")'
    decoded = ctx.from_maude(term_tuple)
    assert decoded == py_tuple

    # Empty tuple
    term_empty = ctx.to_maude(())
    assert get_canonical_str(term_empty) == 'nilarg'
    assert ctx.from_maude(term_empty) == ()

def test_encode_decode_state_entry(ctx):
    state = State(name="temperature", arguments=(1,))
    entry = StateEntry(state=state, value=98.25)

    term_entry = ctx.to_maude(entry)
    # Scientific notation is often output internally for floats by Maude wrapper
    assert get_canonical_str(term_entry) == "id('temperature)(val(1)): val(9.825e+1)"
    assert str(term_entry.getSort()) == 'StateEntry'

    decoded = ctx.from_maude(term_entry)
    assert decoded == entry

def test_encode_decode_environment(ctx):
    state1 = State(name="temp", arguments=())
    entry1 = StateEntry(state=state1, value=100)

    state2 = State(name="status", arguments=("engine",))
    entry2 = StateEntry(state=state2, value=True)

    env = frozenset([entry1, entry2])

    term_env = ctx.to_maude(env)

    # Set representations can be unordered in strings
    term_str = get_canonical_str(term_env)
    assert "id('temp)(nilarg): val(100)" in term_str
    assert "id('status)(val(\"engine\")): val(true)" in term_str
    assert "," in term_str # Set items separated by comma

    # The sort should be Environment or NeEnvironment
    decoded = ctx.from_maude(term_env)
    assert decoded == env

    # Empty environment
    term_empty = ctx.to_maude(frozenset())
    assert get_canonical_str(term_empty) == 'mtenvironment'
    assert ctx.from_maude(term_empty) == frozenset()
