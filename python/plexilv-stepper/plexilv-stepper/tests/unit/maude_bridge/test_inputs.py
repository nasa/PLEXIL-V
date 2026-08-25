import pytest
import maude

from plexilv_stepper.models import (
    CommandHandle, CommandAbort, CommandAck, CommandResult, StateLookup, UpdateAck
)
from plexilv_stepper.maude_bridge.context import TranslatorContext
from plexilv_stepper.maude_bridge.inputs import register_input_translators

@pytest.fixture
def ctx(maude_module):
    context = TranslatorContext(maude_module)
    from plexilv_stepper.maude_bridge.environment import register_environment_translators
    register_environment_translators(context)
    register_input_translators(context)
    return context

def get_canonical_str(term: maude.Term) -> str:
    """Helper to get a clean unformatted string representation."""
    return term.prettyPrint(maude.PRINT_MIXFIX | maude.PRINT_NUMBER)

def test_encode_decode_command_abort(ctx):
    entry = CommandAbort(identifier="cmd1", arguments=("test", 5), value=False)
    term = ctx.to_maude(entry)

    assert "commandAbort" in get_canonical_str(term)
    assert str(term.getSort()) == 'CommandInput'

    decoded = ctx.from_maude(term)
    assert decoded == entry

def test_encode_decode_command_ack(ctx):
    entry = CommandAck(identifier="cmd2", arguments=(), command_handle=CommandHandle.COMMAND_ACCEPTED)
    term = ctx.to_maude(entry)

    term_str = get_canonical_str(term)
    assert "commandAck" in term_str
    assert "CommandAccepted" in term_str
    assert str(term.getSort()) == 'CommandInput'

    decoded = ctx.from_maude(term)
    assert decoded == entry

def test_encode_decode_command_result(ctx):
    entry = CommandResult(identifier="cmd3", arguments=(True,), value=42.0)
    term = ctx.to_maude(entry)

    assert "commandResult" in get_canonical_str(term)
    assert str(term.getSort()) == 'CommandInput'

    decoded = ctx.from_maude(term)
    assert decoded == entry

def test_encode_decode_state_lookup(ctx):
    entry = StateLookup(identifier="lookup1", arguments=("test_var",), value=None)
    term = ctx.to_maude(entry)

    assert "stateLookup" in get_canonical_str(term)
    assert str(term.getSort()) == 'StateInput'

    decoded = ctx.from_maude(term)
    assert decoded == entry

def test_encode_decode_update_ack(ctx):
    entry = UpdateAck(identifier="update1")
    term = ctx.to_maude(entry)

    assert "updateAck" in get_canonical_str(term)
    assert str(term.getSort()) == 'UpdateInput'

    decoded = ctx.from_maude(term)
    assert decoded == entry

def test_encode_decode_inputs_set(ctx):
    entry1 = CommandAbort(identifier="cmd1", arguments=(), value=1)
    entry2 = UpdateAck(identifier="update1")

    inputs_set = frozenset([entry1, entry2])
    term = ctx.to_maude(inputs_set)

    term_str = get_canonical_str(term)
    assert "commandAbort" in term_str
    assert "updateAck" in term_str

    decoded = ctx.from_maude(term)
    assert decoded == inputs_set

def test_encode_decode_empty_inputs_set(ctx):
    inputs_set = frozenset()

    # In python, frozenset() will map to mtenvironment by default because we cannot infer if it's Environment or Inputs.
    # To cleanly solve this, users usually cast or we check it. However, the requirement didn't specify empty inputs natively needed,
    # but it's good to know `frozenset()` maps to Environment.
    # We will just verify it creates an empty set.
    term = ctx.to_maude(inputs_set)
    assert get_canonical_str(term) in ('mtenvironment', 'noInputs')