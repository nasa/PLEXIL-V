import maude
from ..models import Input, CommandAbort, CommandAck, CommandHandle, CommandResult, StateLookup, UpdateAck, Inputs
from .context import TranslatorContext

def register_input_translators(ctx: TranslatorContext):

    # --- CommandHandle Enum ---
    @ctx.encoder(CommandHandle)
    def encode_command_handle(ctx: TranslatorContext, val: CommandHandle) -> maude.Term:
        # e.g., 'CommandSentToSystem' directly maps to a zero-arity constructor of the same name
        return ctx.module.parseTerm(val.value)

    @ctx.decoder('CommandHandle')
    def decode_command_handle(ctx: TranslatorContext, term: maude.Term) -> CommandHandle:
        # term string will look like 'CommandSentToSystem'
        val_str = str(term.symbol())
        return CommandHandle(val_str)

    # Helper to parse identifiers (like we do for Environment names)
    def parse_identifier(term: maude.Term) -> str:
        q_str = str(term)
        if q_str.startswith("id('"):
            return q_str[4:-1]
        elif q_str.startswith("'"):
            return q_str[1:]
        return q_str

    def create_identifier(name: str) -> maude.Term:
        return ctx.module.parseTerm(f"id('{name})")

    # --- CommandAbort ---
    @ctx.encoder(CommandAbort)
    def encode_command_abort(ctx: TranslatorContext, entry: CommandAbort) -> maude.Term:
        sym = None
        for s in ctx.module.getSymbols():
            if str(s) == 'commandAbort' and str(s.getRangeSort()) in ('CommandInput', 'Input', '[Input]'):
                sym = s
                break

        if not sym:
            raise RuntimeError("Could not find 'commandAbort' symbol")

        id_term = create_identifier(entry.identifier)
        args_term = ctx.to_maude(entry.arguments)
        val_term = ctx.to_maude(entry.value)
        return sym(id_term, args_term, val_term)

    @ctx.decoder('CommandInput')
    def decode_command_input(ctx: TranslatorContext, term: maude.Term) -> Input:
        sym_name = str(term.symbol())
        args = list(term.arguments())

        def force_tuple(val):
            return val if isinstance(val, tuple) else (val,)

        if sym_name == 'commandAbort':
            return CommandAbort(
                identifier=parse_identifier(args[0]),
                arguments=force_tuple(ctx.from_maude(args[1])),
                value=ctx.from_maude(args[2])
            )
        elif sym_name == 'commandAck':
            return CommandAck(
                identifier=parse_identifier(args[0]),
                arguments=force_tuple(ctx.from_maude(args[1])),
                command_handle=ctx.from_maude(args[2])
            )
        elif sym_name == 'commandResult':
            return CommandResult(
                identifier=parse_identifier(args[0]),
                arguments=force_tuple(ctx.from_maude(args[1])),
                value=ctx.from_maude(args[2])
            )
        raise ValueError(f"Unknown CommandInput symbol: {sym_name}")

    # --- CommandAck ---
    @ctx.encoder(CommandAck)
    def encode_command_ack(ctx: TranslatorContext, entry: CommandAck) -> maude.Term:
        sym = None
        for s in ctx.module.getSymbols():
            if str(s) == 'commandAck' and str(s.getRangeSort()) in ('CommandInput', 'Input', '[Input]'):
                sym = s
                break

        if not sym:
            raise RuntimeError("Could not find 'commandAck' symbol")

        id_term = create_identifier(entry.identifier)
        args_term = ctx.to_maude(entry.arguments)
        handle_term = ctx.to_maude(entry.command_handle)
        return sym(id_term, args_term, handle_term)

    # --- CommandResult ---
    @ctx.encoder(CommandResult)
    def encode_command_result(ctx: TranslatorContext, entry: CommandResult) -> maude.Term:
        sym = None
        for s in ctx.module.getSymbols():
            if str(s) == 'commandResult' and str(s.getRangeSort()) in ('CommandInput', 'Input', '[Input]'):
                sym = s
                break

        if not sym:
            raise RuntimeError("Could not find 'commandResult' symbol")

        id_term = create_identifier(entry.identifier)
        args_term = ctx.to_maude(entry.arguments)
        val_term = ctx.to_maude(entry.value)
        return sym(id_term, args_term, val_term)

    # --- StateLookup ---
    @ctx.encoder(StateLookup)
    def encode_state_lookup(ctx: TranslatorContext, entry: StateLookup) -> maude.Term:
        sym = None
        for s in ctx.module.getSymbols():
            if str(s) == 'stateLookup' and str(s.getRangeSort()) in ('StateInput', 'Input', '[Input]'):
                sym = s
                break

        if not sym:
            raise RuntimeError("Could not find 'stateLookup' symbol")

        id_term = create_identifier(entry.identifier)
        args_term = ctx.to_maude(entry.arguments)
        val_term = ctx.to_maude(entry.value)
        return sym(id_term, args_term, val_term)

    @ctx.decoder('StateInput')
    def decode_state_input(ctx: TranslatorContext, term: maude.Term) -> Input:
        sym_name = str(term.symbol())
        args = list(term.arguments())
        def force_tuple(val):
            return val if isinstance(val, tuple) else (val,)

        if sym_name == 'stateLookup':
            return StateLookup(
                identifier=parse_identifier(args[0]),
                arguments=force_tuple(ctx.from_maude(args[1])),
                value=ctx.from_maude(args[2])
            )
        raise ValueError(f"Unknown StateInput symbol: {sym_name}")

    # --- UpdateAck ---
    @ctx.encoder(UpdateAck)
    def encode_update_ack(ctx: TranslatorContext, entry: UpdateAck) -> maude.Term:
        sym = None
        for s in ctx.module.getSymbols():
            if str(s) == 'updateAck' and str(s.getRangeSort()) in ('UpdateInput', 'Input', '[Input]'):
                sym = s
                break

        if not sym:
            raise RuntimeError("Could not find 'updateAck' symbol")

        id_term = create_identifier(entry.identifier)
        # Note: We omitted ack from python, always default it to true in maude
        ack_term = ctx.module.parseTerm("true")
        return sym(id_term, ack_term)

    @ctx.decoder('UpdateInput')
    def decode_update_input(ctx: TranslatorContext, term: maude.Term) -> Input:
        sym_name = str(term.symbol())
        args = list(term.arguments())
        if sym_name == 'updateAck':
            return UpdateAck(
                identifier=parse_identifier(args[0])
            )
        raise ValueError(f"Unknown UpdateInput symbol: {sym_name}")

    # We should also capture the base 'Input' decoder since Maude might just resolve to 'Input' instead of the subsort
    @ctx.decoder('Input')
    def decode_input(ctx: TranslatorContext, term: maude.Term) -> Input:
        sym_name = str(term.symbol())
        if sym_name in ('commandAbort', 'commandAck', 'commandResult'):
            return decode_command_input(ctx, term)
        elif sym_name == 'stateLookup':
            return decode_state_input(ctx, term)
        elif sym_name == 'updateAck':
            return decode_update_input(ctx, term)
        raise ValueError(f"Unknown Input symbol: {sym_name}")


    # --- Inputs Set ---
    # We already handle `frozenset` based on item type natively if we register it in environment,
    # but the cleanest way is a small type alias or wrapper. Alternatively we just rely on type checking inside the frozenset encoder in context.py.

    # We define `Inputs` decoder here:
    @ctx.decoder('Inputs')
    def decode_inputs(ctx: TranslatorContext, term: maude.Term) -> frozenset:
        if str(term.symbol()) == 'noInputs':
            return frozenset()

        entries = set()

        def extract(t: maude.Term):
            # Inputs set concatenation is `__`
            sym_name = str(t.symbol()) if hasattr(t, 'symbol') else ""
            if sym_name == '__' and str(t.getSort()) in ('Inputs', 'NeInputs', 'Set{Input}', 'NeSet{Input}'):
                for arg in t.arguments():
                    extract(arg)
            else:
                entries.add(ctx.from_maude(t))

        extract(term)
        return frozenset(entries)

    @ctx.decoder('NeInputs')
    def decode_ne_inputs(ctx: TranslatorContext, term: maude.Term) -> frozenset:
        return decode_inputs(ctx, term)
