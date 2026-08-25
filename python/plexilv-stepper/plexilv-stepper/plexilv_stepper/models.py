from dataclasses import dataclass
from typing import Tuple, Any, FrozenSet

@dataclass(frozen=True)
class State:
    name: str
    arguments: Tuple[Any, ...]

@dataclass(frozen=True)
class StateEntry:
    state: State
    value: Any

Environment = FrozenSet[StateEntry]

class Input:
    """Base class for external Inputs"""
    pass

from enum import Enum

@dataclass(frozen=True)
class CommandAbort(Input):
    identifier: str
    arguments: Tuple[Any, ...]
    value: Any

class CommandHandle(Enum):
    COMMAND_SENT_TO_SYSTEM = "CommandSentToSystem"
    COMMAND_ACCEPTED = "CommandAccepted"
    COMMAND_RCVD_BY_SYSTEM = "CommandRcvdBySystem"
    COMMAND_FAILED = "CommandFailed"
    COMMAND_DENIED = "CommandDenied"
    COMMAND_SUCCESS = "CommandSuccess"
    COMMAND_INTERFACE_ERROR = "CommandInterfaceError"
    COMMAND_HANDLE_MAX = "CommandHandleMax"

@dataclass(frozen=True)
class CommandAck(Input):
    identifier: str
    arguments: Tuple[Any, ...]
    command_handle: CommandHandle

@dataclass(frozen=True)
class CommandResult(Input):
    identifier: str
    arguments: Tuple[Any, ...]
    value: Any

@dataclass(frozen=True)
class StateLookup(Input):
    identifier: str
    arguments: Tuple[Any, ...]
    value: Any

@dataclass(frozen=True)
class UpdateAck(Input):
    identifier: str
    # 'ack' field removed per request, assumed to be True/UPDATE_SUCCESS

Inputs = FrozenSet[Input]
