from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum


@dataclass(kw_only=True)
class Delay:
    """Delay element - empty marker for script timing."""

    pass


@dataclass(kw_only=True)
class SendPlan:
    file: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )


@dataclass(kw_only=True)
class UpdateAck:
    name: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )


class TypeValue(Enum):
    BOOL = "bool"
    REAL = "real"
    INT = "int"
    STRING = "string"
    BOOL_ARRAY = "bool-array"
    REAL_ARRAY = "real-array"
    INT_ARRAY = "int-array"
    STRING_ARRAY = "string-array"


@dataclass(kw_only=True)
class Param:
    value: str = field(default="")
    type_value: None | TypeValue = field(
        default=None,
        metadata={
            "name": "type",
            "type": "Attribute",
        },
    )


@dataclass(kw_only=True)
class State:
    param: list[Param] = field(
        default_factory=list,
        metadata={
            "name": "Param",
            "type": "Element",
        },
    )
    value: list[str] = field(
        default_factory=list,
        metadata={
            "name": "Value",
            "type": "Element",
            "namespace": "",
            "min_occurs": 1,
        },
    )
    name: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    type_value: None | TypeValue = field(
        default=None,
        metadata={
            "name": "type",
            "type": "Attribute",
        },
    )


@dataclass(kw_only=True)
class CommandType:
    class Meta:
        name = "command-type"

    param: list[Param] = field(
        default_factory=list,
        metadata={
            "name": "Param",
            "type": "Element",
        },
    )
    result: list[str] = field(
        default_factory=list,
        metadata={
            "name": "Result",
            "type": "Element",
            "namespace": "",
            "min_occurs": 1,
        },
    )
    name: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    type_value: None | TypeValue = field(
        default=None,
        metadata={
            "name": "type",
            "type": "Attribute",
        },
    )


@dataclass(kw_only=True)
class Command(CommandType):
    pass


@dataclass(kw_only=True)
class CommandAbort(CommandType):
    pass


@dataclass(kw_only=True)
class CommandAck(CommandType):
    pass


@dataclass(kw_only=True)
class InitialState:
    state: list[State] = field(
        default_factory=list,
        metadata={
            "name": "State",
            "type": "Element",
        },
    )


@dataclass(kw_only=True)
class Simultaneous:
    choice: list[State | UpdateAck | Command | CommandAck | CommandAbort] = field(
        default_factory=list,
        metadata={
            "type": "Elements",
            "choices": (
                {
                    "name": "State",
                    "type": State,
                },
                {
                    "name": "UpdateAck",
                    "type": UpdateAck,
                },
                {
                    "name": "Command",
                    "type": Command,
                },
                {
                    "name": "CommandAck",
                    "type": CommandAck,
                },
                {
                    "name": "CommandAbort",
                    "type": CommandAbort,
                },
            ),
        },
    )


@dataclass(kw_only=True)
class Script:
    choice: list[
        State
        | UpdateAck
        | Command
        | CommandAck
        | CommandAbort
        | Simultaneous
        | SendPlan
        | Delay
    ] = field(
        default_factory=list,
        metadata={
            "type": "Elements",
            "choices": (
                {
                    "name": "State",
                    "type": State,
                },
                {
                    "name": "UpdateAck",
                    "type": UpdateAck,
                },
                {
                    "name": "Command",
                    "type": Command,
                },
                {
                    "name": "CommandAck",
                    "type": CommandAck,
                },
                {
                    "name": "CommandAbort",
                    "type": CommandAbort,
                },
                {
                    "name": "Simultaneous",
                    "type": Simultaneous,
                },
                {
                    "name": "SendPlan",
                    "type": SendPlan,
                },
                {
                    "name": "Delay",
                    "type": Delay,
                },
            ),
        },
    )


@dataclass(kw_only=True)
class PLEXILScript:
    class Meta:
        name = "PLEXILScript"

    initial_state: None | InitialState = field(
        default=None,
        metadata={
            "name": "InitialState",
            "type": "Element",
        },
    )
    script: Script = field(
        metadata={
            "name": "Script",
            "type": "Element",
        }
    )
