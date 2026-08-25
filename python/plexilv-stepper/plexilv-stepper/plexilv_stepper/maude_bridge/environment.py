import maude
from typing import Any
from ..models import State, StateEntry, Environment
from .context import TranslatorContext

def register_environment_translators(ctx: TranslatorContext):

    # --- PRMITIVE VALUES ---

    @ctx.encoder(int)
    def encode_int(ctx: TranslatorContext, val: int) -> maude.Term:
        # Find the specific val symbol for Int
        for s in ctx.module.getSymbols():
            if str(s) == "val" and s.arity() == 1 and str(s.domainKind(0)) == "[Int]":
                return s(ctx.module.parseTerm(str(val)))
        # Fallback
        return ctx.module.parseTerm(f"val({val})")

    @ctx.decoder('IntValue')
    def decode_int(ctx: TranslatorContext, term: maude.Term) -> int:
        return int(str(list(term.arguments())[0]))

    @ctx.encoder(float)
    def encode_float(ctx: TranslatorContext, val: float) -> maude.Term:
        # Maude expects floats typically in a specific format like 3.14 (might need to handle scientific notation)
        for s in ctx.module.getSymbols():
            if str(s) == "val" and s.arity() == 1 and str(s.domainKind(0)) == "[Float]":
                # Ensure float has decimal part
                str_val = str(val)
                if '.' not in str_val:
                    str_val += '.0'
                return s(ctx.module.parseTerm(str_val))
        return ctx.module.parseTerm(f"val({val})")

    @ctx.decoder('FloatValue')
    def decode_float(ctx: TranslatorContext, term: maude.Term) -> float:
        return float(str(list(term.arguments())[0]))

    @ctx.encoder(bool)
    def encode_bool(ctx: TranslatorContext, val: bool) -> maude.Term:
        for s in ctx.module.getSymbols():
            if str(s) == "val" and s.arity() == 1 and str(s.domainKind(0)) == "[Bool]":
                return s(ctx.module.parseTerm("true" if val else "false"))
        return ctx.module.parseTerm("val(true)" if val else "val(false)")

    @ctx.decoder('BoolValue')
    def decode_bool(ctx: TranslatorContext, term: maude.Term) -> bool:
        return str(list(term.arguments())[0]) == "true"

    @ctx.encoder(str)
    def encode_str(ctx: TranslatorContext, val: str) -> maude.Term:
        # NOTE: If we get a string, we assume it's for 'StringValue' inside Value.
        # The 'name' of State will be handled explicitly in State encoder to become Qualified.
        for s in ctx.module.getSymbols():
            if str(s) == "val" and s.arity() == 1 and str(s.domainKind(0)) == "[String]":
                return s(ctx.module.parseTerm(f'"{val}"'))
        return ctx.module.parseTerm(f'val("{val}")')

    @ctx.decoder('StringValue')
    def decode_str(ctx: TranslatorContext, term: maude.Term) -> str:
        # Remove surrounding quotes
        val = str(list(term.arguments())[0])
        if val.startswith('"') and val.endswith('"'):
            return val[1:-1]
        return val

    @ctx.encoder(type(None))
    def encode_none(ctx: TranslatorContext, val: None) -> maude.Term:
        return ctx.module.parseTerm('unknown')

    @ctx.decoder('PrimitiveValue') # 'unknown' is of sort PrimitiveValue directly
    def decode_primitive(ctx: TranslatorContext, term: maude.Term) -> None:
        if str(term.symbol()) == 'unknown':
            return None
        raise ValueError(f"Unexpected PrimitiveValue: {term}")


    # --- TUPLE (Arrays / Arguments) ---

    @ctx.encoder(tuple)
    def encode_tuple(ctx: TranslatorContext, val: tuple) -> maude.Term:
        # A tuple generally maps to Arguments in State
        # If it's empty
        if not val:
            return ctx.module.parseTerm('nilarg')

        # Maude uses space `__` for LIST{Value} concatenation
        # We need to find the right append operator
        sym_concat = None
        for s in ctx.module.getSymbols():
            if str(s) == "__" and str(s.getRangeSort()) in ("NeArguments", "[Arguments]", "Arguments"):
                sym_concat = s
                break

        # For simplicity, if we can't find specific append, we can parse or construct
        if len(val) == 1:
             return ctx.to_maude(val[0])

        term = ctx.to_maude(val[0])
        if sym_concat:
             for item in val[1:]:
                 term = sym_concat(term, ctx.to_maude(item))
             return term
        else:
            raise RuntimeError("Could not find concatenation symbol for Arguments")

    @ctx.decoder('Arguments')
    def decode_arguments(ctx: TranslatorContext, term: maude.Term) -> tuple:
        if str(term.symbol()) == 'nilarg':
            return ()

        args_list = []
        def extract(t: maude.Term):
            if str(t.symbol()) == '__':
                for child in t.arguments():
                    extract(child)
            else:
                args_list.append(ctx.from_maude(t))

        extract(term)
        return tuple(args_list)

    @ctx.decoder('NeArguments')
    def decode_nearguments(ctx: TranslatorContext, term: maude.Term) -> tuple:
        return decode_arguments(ctx, term)

    @ctx.decoder('NeList{Value}')
    def decode_nelist_value(ctx: TranslatorContext, term: maude.Term) -> tuple:
        return decode_arguments(ctx, term)

    @ctx.decoder('PrimitiveValue') # 'unknown' is of sort PrimitiveValue directly
    def decode_primitive(ctx: TranslatorContext, term: maude.Term) -> None:
        if str(term.symbol()) == 'unknown':
            return None
        # This fallback catches when a primitive is passed as just PrimitiveValue
        # but we actually want its more specific value or it's genuinely just a wrapper.
        # Generally 'unknown' is the main primitive value directly.
        raise ValueError(f"Unexpected PrimitiveValue: {term}")

    @ctx.decoder('Value')
    def decode_value(ctx: TranslatorContext, term: maude.Term) -> Any:
        # Sometimes Maude typing returns `Value` as the generic sort
        return ctx.from_maude(term)


    # --- STATE AND ENVIRONMENT ---

    @ctx.encoder(State)
    def encode_state(ctx: TranslatorContext, state: State) -> maude.Term:
        # A State is just a concept, but it's used inside StateEntry: Qualified(Arguments)
        raise NotImplementedError("State should be encoded directly within StateEntry")

    @ctx.encoder(StateEntry)
    def encode_state_entry(ctx: TranslatorContext, entry: StateEntry) -> maude.Term:
        # Find _(_):_
        sym_entry = None
        for s in ctx.module.getSymbols():
            # Often operators with spaces are represented simply by the string or need to just be parsed
            if str(s) == '_(_):_':
                sym_entry = s
                break

        if not sym_entry:
            # Another reliable way is to let Maude parse a dummy string and get the symbol
            dummy_term = ctx.module.parseTerm("id('dummy) (nilarg) : val(0)")
            sym_entry = dummy_term.symbol()

        # 1. name -> Qualified (which is a Qid wrapped in 'id' operator, then list)
        q_term = ctx.module.parseTerm(f"id('{entry.state.name})") # Simplified parse approach for Qualified

        # 2. arguments -> Arguments
        args_term = ctx.to_maude(entry.state.arguments)

        # 3. value -> Value
        val_term = ctx.to_maude(entry.value)

        return sym_entry(q_term, args_term, val_term)

    @ctx.decoder('StateEntry')
    def decode_state_entry(ctx: TranslatorContext, term: maude.Term) -> StateEntry:
        args = list(term.arguments())
        q_term, args_term, val_term = args[0], args[1], args[2]

        # Decode Qualified. It's usually `id('name)` or just `'name` depending on context
        q_str = str(q_term)
        if q_str.startswith("id('"):
            name = q_str[4:-1]
        elif q_str.startswith("'"):
            name = q_str[1:]
        else:
            name = q_str

        args_tuple = ctx.from_maude(args_term)
        if not isinstance(args_tuple, tuple):
            args_tuple = (args_tuple,)

        state = State(
            name=name,
            arguments=args_tuple
        )

        return StateEntry(
            state=state,
            value=ctx.from_maude(val_term)
        )

    @ctx.encoder(frozenset)
    def encode_frozenset(ctx: TranslatorContext, env: frozenset) -> maude.Term:
        from ..models import Input

        # Check type to see if we are dealing with Inputs or Environment
        if len(env) > 0 and isinstance(next(iter(env)), Input):
            return encode_inputs(ctx, env)
        return encode_environment(ctx, env)

    def encode_inputs(ctx: TranslatorContext, env: frozenset) -> maude.Term:
        if not env:
            return ctx.module.parseTerm('noInputs')

        sym_concat = None
        for s in ctx.module.getSymbols():
            if str(s) == '__' and str(s.getRangeSort()) in ('Inputs', 'NeInputs', 'Set{Input}', 'NeSet{Input}'):
                sym_concat = s
                break

        if not sym_concat:
            try:
                dummy = ctx.module.parseTerm("noInputs noInputs")
                sym_concat = dummy.symbol()
            except Exception:
                pass

        if not sym_concat:
             raise RuntimeError("Could not find concatenation symbol for Inputs")

        term = None
        for entry in env:
            entry_term = ctx.to_maude(entry)
            if term is None:
                term = entry_term
            else:
                term = sym_concat(term, entry_term)
        return term

    def encode_environment(ctx: TranslatorContext, env: frozenset) -> maude.Term:
        if not env:
            return ctx.module.parseTerm('mtenvironment')

        sym_insert = None
        for s in ctx.module.getSymbols():
            if str(s) == '_,_' and str(s.getRangeSort()) in ('NeEnvironment', 'Environment', '[Environment]', 'Set{Global}', 'NeSet{Global}', 'Set{StateEntry}', 'NeSet{StateEntry}', 'Set`{Global`}', 'NeSet`{Global`}'):
                sym_insert = s
                break

        if not sym_insert:
            # Or parse a dummy insert
            try:
                dummy = ctx.module.parseTerm("mtenvironment , mtenvironment")
                sym_insert = dummy.symbol()
            except Exception:
                pass

        if not sym_insert:
            raise RuntimeError("Could not find insert symbol for Environment")

        term = None
        for entry in env:
            entry_term = ctx.to_maude(entry)
            if term is None:
                term = entry_term
            else:
                # sym_insert might wrap them properly or create a tree
                term = sym_insert(term, entry_term)

        return term

    @ctx.decoder('Environment')
    def decode_environment(ctx: TranslatorContext, term: maude.Term) -> frozenset:
        if str(term.symbol()) == 'mtenvironment':
            return frozenset()

        entries = set()

        def extract(t: maude.Term):
            # Maude sets often have associative _,_ symbol
            sym_name = str(t.symbol()) if hasattr(t, 'symbol') else ""
            if sym_name in ('_,_', '_`,_'):
                for arg in t.arguments():
                    extract(arg)
            else:
                entries.add(ctx.from_maude(t))

        extract(term)
        return frozenset(entries)

    @ctx.decoder('NeEnvironment')
    def decode_ne_environment(ctx: TranslatorContext, term: maude.Term) -> frozenset:
        return decode_environment(ctx, term)