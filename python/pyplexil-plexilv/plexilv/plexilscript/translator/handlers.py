"""Translation handlers for PLEXILScript AST types."""

from .dispatch import translate, walk
from plexilv.common import IndentedWriter
from plexil.plexilscript.v1 import (
    PLEXILScript,
    InitialState,
    Script,
    State,
    Command,
    CommandAck,
    CommandAbort,
    UpdateAck,
    Simultaneous,
    Delay,
    Param,
    TypeValue,
)


def format_value(value_str: str, type_value: TypeValue) -> str:
    """Format a value based on its type for Maude output."""
    if value_str in ("UNKNOWN", "Plexil_Unknown"):
        return "unknown"

    if type_value == TypeValue.BOOL:
        # Handle boolean values
        if value_str in ("1", "true"):
            return "val(true)"
        elif value_str in ("0", "false"):
            return "val(false)"
        else:
            return "unknown"

    elif type_value == TypeValue.REAL:
        # Check if it has a decimal point
        if "." in value_str:
            return f"val({value_str})"
        else:
            # Cast integer representation to float
            return f"val(float({value_str}))"

    elif type_value == TypeValue.INT:
        return f"val({value_str})"

    elif type_value == TypeValue.STRING:
        return f'val("{value_str}")'

    elif type_value == TypeValue.BOOL_ARRAY:
        # Arrays of booleans - parse as space-separated
        parts = value_str.split()
        bool_vals = []
        for p in parts:
            if p in ("1", "true"):
                bool_vals.append("val(true)")
            elif p in ("0", "false"):
                bool_vals.append("val(false)")
        return f"array({' # '.join(bool_vals)})"

    elif type_value == TypeValue.INT_ARRAY:
        parts = value_str.split()
        return f"array({' # '.join(f'val({p})' for p in parts)})"

    elif type_value == TypeValue.REAL_ARRAY:
        parts = value_str.split()
        return f"array({' # '.join(f'val({p})' for p in parts)})"

    elif type_value == TypeValue.STRING_ARRAY:
        parts = value_str.split()
        formatted_parts = ' # '.join(f'val("{p}")' for p in parts)
        return f"array({formatted_parts})"

    return value_str


def format_params(params: list[Param]) -> str:
    """Format parameter list for Maude output."""
    if not params:
        return "nilarg"

    formatted = []
    for param in params:
        formatted.append(format_value(param.value, param.type_value))

    return f"({' '.join(formatted)})"


@translate.register(PLEXILScript)
def translate_plexilscript(node: PLEXILScript, writer: IndentedWriter):
    """Translate PLEXILScript root node to Maude INPUT module."""
    writer.writeln("mod INPUT is")
    writer.indent()
    writer.writeln("protecting PLEXIL-V .")
    writer.writeln("")
    writer.writeln("op input : -> InputGenerator .")
    writer.writeln("eq input = sequenceGenerator(")
    writer.indent()

    # Translate initial state
    if node.initial_state:
        walk(node.initial_state, writer)
    else:
        writer.writeln("noInputs")

    writer.writeln("#")

    # Translate script
    walk(node.script, writer)

    writer.dedent()
    writer.writeln(") .")
    writer.dedent()
    writer.writeln("endm")


@translate.register(InitialState)
def translate_initial_state(node: InitialState, writer: IndentedWriter):
    """Translate InitialState node."""
    if not node.state:
        writer.writeln("noInputs")
    else:
        for i, state in enumerate(node.state):
            walk(state, writer)
            if i < len(node.state) - 1:
                writer.writeln("")


@translate.register(Script)
def translate_script(node: Script, writer: IndentedWriter):
    """Translate Script node."""
    if not node.choice:
        writer.writeln("nilEInputsList")
    else:
        for i, entry in enumerate(node.choice):
            walk(entry, writer)
            if i < len(node.choice) - 1:
                writer.writeln("#")


@translate.register(State)
def translate_state(node: State, writer: IndentedWriter):
    """Translate State lookup."""
    name = node.name or "UNKNOWN"
    params = format_params(node.param)

    # Format value based on type
    if node.type_value in (
        TypeValue.BOOL_ARRAY,
        TypeValue.INT_ARRAY,
        TypeValue.REAL_ARRAY,
        TypeValue.STRING_ARRAY,
    ):
        # Array type - format each element directly based on scalar type
        if node.type_value == TypeValue.BOOL_ARRAY:
            scalar_type = TypeValue.BOOL
        elif node.type_value == TypeValue.INT_ARRAY:
            scalar_type = TypeValue.INT
        elif node.type_value == TypeValue.REAL_ARRAY:
            scalar_type = TypeValue.REAL
        else:  # STRING_ARRAY
            scalar_type = TypeValue.STRING

        values = [format_value(v, scalar_type) for v in node.value]
        value_str = f"array({' # '.join(values)})"
    else:
        # Scalar type - use format_value for proper handling of unknown values
        value_str = format_value(node.value[0], node.type_value) if node.value else "unknown"

    writer.writeln(f"stateLookup('{name},{params},{value_str})")


@translate.register(Command)
def translate_command(node: Command, writer: IndentedWriter):
    """Translate Command result."""
    name = node.name or "UNKNOWN"
    params = format_params(node.param)

    # Format result value based on type
    if node.type_value in (
        TypeValue.BOOL_ARRAY,
        TypeValue.INT_ARRAY,
        TypeValue.REAL_ARRAY,
        TypeValue.STRING_ARRAY,
    ):
        # Array result
        if node.type_value == TypeValue.BOOL_ARRAY:
            values = [format_value(v, TypeValue.BOOL) for v in node.result]
        elif node.type_value == TypeValue.INT_ARRAY:
            values = [format_value(v, TypeValue.INT) for v in node.result]
        elif node.type_value == TypeValue.REAL_ARRAY:
            values = [format_value(v, TypeValue.REAL) for v in node.result]
        else:  # STRING_ARRAY
            values = [f'val("{v}")' for v in node.result]
        result_str = f"array({' # '.join(values)})"
    elif node.type_value == TypeValue.STRING:
        result_str = f'val("{node.result[0]}")' if node.result else 'val("")'
    elif node.type_value == TypeValue.BOOL:
        val = node.result[0] if node.result else "false"
        bool_val = "true" if val in ("1", "true") else "false"
        result_str = f"val({bool_val})"
    elif node.type_value == TypeValue.REAL:
        result_str = f"val({node.result[0]})" if node.result else "val(0.0)"
    else:  # INT
        result_str = f"val({node.result[0]})" if node.result else "val(0)"

    writer.writeln(f"commandResult('{name},{params},{result_str})")


@translate.register(CommandAck)
def translate_command_ack(node: CommandAck, writer: IndentedWriter):
    """Translate CommandAck."""
    name = node.name or "UNKNOWN"
    params = format_params(node.param)

    # The result field contains the command handle status
    handle = node.result[0] if node.result else "COMMAND_DENIED"
    # Map XML status to Maude format
    handle_map = {
        "COMMAND_DENIED": "CommandDenied",
        "COMMAND_ACCEPTED": "CommandAccepted",
        "COMMAND_SENT_TO_SYSTEM": "CommandSentToSystem",
        "COMMAND_RCVD_BY_SYSTEM": "CommandReceivedBySystem",
        "COMMAND_SUCCESS": "CommandSuccess",
        "COMMAND_FAILED": "CommandFailed",
    }
    handle_str = handle_map.get(handle, handle)

    writer.writeln(f"commandAck('{name},{params},{handle_str})")


@translate.register(CommandAbort)
def translate_command_abort(node: CommandAbort, writer: IndentedWriter):
    """Translate CommandAbort."""
    name = node.name or "UNKNOWN"
    params = format_params(node.param)

    # Format result value based on type
    if node.type_value == TypeValue.BOOL:
        val = node.result[0] if node.result else "false"
        bool_val = "true" if val in ("1", "true") else "false"
        result_str = f"val({bool_val})"
    elif node.type_value == TypeValue.STRING:
        result_str = f'val("{node.result[0]}")' if node.result else 'val("")'
    elif node.type_value == TypeValue.REAL:
        result_str = f"val({node.result[0]})" if node.result else "val(0.0)"
    else:  # INT
        result_str = f"val({node.result[0]})" if node.result else "val(0)"

    writer.writeln(f"commandAbort('{name},{params},{result_str})")


@translate.register(UpdateAck)
def translate_update_ack(node: UpdateAck, writer: IndentedWriter):
    """Translate UpdateAck."""
    name = node.name or "UNKNOWN"
    writer.writeln(f"updateAck('{name},true)")


@translate.register(Simultaneous)
def translate_simultaneous(node: Simultaneous, writer: IndentedWriter):
    """Translate Simultaneous entries."""
    for entry in node.choice:
        walk(entry, writer)


@translate.register(Delay)
def translate_delay(node: Delay, writer: IndentedWriter):
    """Translate Delay (empty element)."""
    writer.writeln("noInputs")
