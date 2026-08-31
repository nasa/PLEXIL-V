from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
from typing import ForwardRef, Any


@dataclass(kw_only=True)
class ArrayVariable:
    value: str = field(default="")


class AtomicTypeValues(Enum):
    INTEGER = "Integer"
    REAL = "Real"
    BOOLEAN = "Boolean"
    STRING = "String"


@dataclass(kw_only=True)
class BooleanValue:
    value: bool = field()


@dataclass(kw_only=True)
class BooleanVariable:
    value: str = field(default="")


@dataclass(kw_only=True)
class Comment:
    value: str = field(default="")
    file_name: None | str = field(
        default=None,
        metadata={
            "name": "FileName",
            "type": "Attribute",
        },
    )
    line_no: None | int = field(
        default=None,
        metadata={
            "name": "LineNo",
            "type": "Attribute",
        },
    )
    col_no: None | int = field(
        default=None,
        metadata={
            "name": "ColNo",
            "type": "Attribute",
        },
    )
    epx: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )


@dataclass(kw_only=True)
class DeclareMutex:
    name: DeclareMutex.Name = field(
        metadata={
            "name": "Name",
            "type": "Element",
            "namespace": "",
        }
    )
    file_name: None | str = field(
        default=None,
        metadata={
            "name": "FileName",
            "type": "Attribute",
        },
    )
    line_no: None | int = field(
        default=None,
        metadata={
            "name": "LineNo",
            "type": "Attribute",
        },
    )
    col_no: None | int = field(
        default=None,
        metadata={
            "name": "ColNo",
            "type": "Attribute",
        },
    )
    epx: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )

    @dataclass(kw_only=True)
    class Name:
        value: str = field(default="")
        file_name: None | str = field(
            default=None,
            metadata={
                "name": "FileName",
                "type": "Attribute",
            },
        )
        line_no: None | int = field(
            default=None,
            metadata={
                "name": "LineNo",
                "type": "Attribute",
            },
        )
        col_no: None | int = field(
            default=None,
            metadata={
                "name": "ColNo",
                "type": "Attribute",
            },
        )
        epx: None | str = field(
            default=None,
            metadata={
                "type": "Attribute",
            },
        )


@dataclass(kw_only=True)
class IntegerValue:
    value: int = field()


@dataclass(kw_only=True)
class IntegerVariable:
    value: str = field(default="")


@dataclass(kw_only=True)
class LookupNow:
    name: Name = field(
        metadata={
            "name": "Name",
            "type": "Element",
        }
    )
    arguments: None | Arguments = field(
        default=None,
        metadata={
            "name": "Arguments",
            "type": "Element",
        },
    )
    file_name: None | str = field(
        default=None,
        metadata={
            "name": "FileName",
            "type": "Attribute",
        },
    )
    line_no: None | int = field(
        default=None,
        metadata={
            "name": "LineNo",
            "type": "Attribute",
        },
    )
    col_no: None | int = field(
        default=None,
        metadata={
            "name": "ColNo",
            "type": "Attribute",
        },
    )
    epx: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )


@dataclass(kw_only=True)
class LookupOnChange:
    name: Name = field(
        metadata={
            "name": "Name",
            "type": "Element",
        }
    )
    tolerance: None | Tolerance = field(
        default=None,
        metadata={
            "name": "Tolerance",
            "type": "Element",
        },
    )
    arguments: None | Arguments = field(
        default=None,
        metadata={
            "name": "Arguments",
            "type": "Element",
        },
    )
    file_name: None | str = field(
        default=None,
        metadata={
            "name": "FileName",
            "type": "Attribute",
        },
    )
    line_no: None | int = field(
        default=None,
        metadata={
            "name": "LineNo",
            "type": "Attribute",
        },
    )
    col_no: None | int = field(
        default=None,
        metadata={
            "name": "ColNo",
            "type": "Attribute",
        },
    )
    epx: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )


class NcnameOrEmptyValue(Enum):
    VALUE = ""


class NodeCommandHandleValueValue(Enum):
    COMMAND_SENT_TO_SYSTEM = "COMMAND_SENT_TO_SYSTEM"
    COMMAND_ACCEPTED = "COMMAND_ACCEPTED"
    COMMAND_DENIED = "COMMAND_DENIED"
    COMMAND_RCVD_BY_SYSTEM = "COMMAND_RCVD_BY_SYSTEM"
    COMMAND_FAILED = "COMMAND_FAILED"
    COMMAND_SUCCESS = "COMMAND_SUCCESS"
    COMMAND_ABORTED = "COMMAND_ABORTED"
    COMMAND_ABORT_FAILED = "COMMAND_ABORT_FAILED"
    COMMAND_INTERFACE_ERROR = "COMMAND_INTERFACE_ERROR"


class NodeFailureValueValue(Enum):
    PRE_CONDITION_FAILED = "PRE_CONDITION_FAILED"
    POST_CONDITION_FAILED = "POST_CONDITION_FAILED"
    INVARIANT_CONDITION_FAILED = "INVARIANT_CONDITION_FAILED"
    PARENT_FAILED = "PARENT_FAILED"
    PARENT_EXITED = "PARENT_EXITED"
    EXITED = "EXITED"


@dataclass(kw_only=True)
class NodeId:
    value: str = field(default="")
    generated: None | bool = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    file_name: None | str = field(
        default=None,
        metadata={
            "name": "FileName",
            "type": "Attribute",
        },
    )
    line_no: None | int = field(
        default=None,
        metadata={
            "name": "LineNo",
            "type": "Attribute",
        },
    )
    col_no: None | int = field(
        default=None,
        metadata={
            "name": "ColNo",
            "type": "Attribute",
        },
    )
    epx: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )


class NodeOutcomeValueValue(Enum):
    SUCCESS = "SUCCESS"
    FAILURE = "FAILURE"
    SKIPPED = "SKIPPED"
    INTERRUPTED = "INTERRUPTED"


class NodeRefDir(Enum):
    PARENT = "parent"
    SIBLING = "sibling"
    CHILD = "child"
    SELF = "self"


class NodeStateValueValue(Enum):
    WAITING = "WAITING"
    EXECUTING = "EXECUTING"
    FINISHING = "FINISHING"
    FAILING = "FAILING"
    ITERATION_ENDED = "ITERATION_ENDED"
    FINISHED = "FINISHED"
    INACTIVE = "INACTIVE"


class NodeTypeValue(Enum):
    NODE_LIST = "NodeList"
    COMMAND = "Command"
    ASSIGNMENT = "Assignment"
    UPDATE = "Update"
    EMPTY = "Empty"
    LIBRARY_NODE_CALL = "LibraryNodeCall"


class ParameterTypeValues(Enum):
    INTEGER = "Integer"
    REAL = "Real"
    BOOLEAN = "Boolean"
    STRING = "String"
    ANY = "Any"


@dataclass(kw_only=True)
class RealValue:
    value: float = field()


@dataclass(kw_only=True)
class RealVariable:
    value: str = field(default="")


@dataclass(kw_only=True)
class StringValue:
    value: str = field(default="")


@dataclass(kw_only=True)
class StringVariable:
    value: str = field(default="")


class TimepointValue(Enum):
    START = "START"
    END = "END"


@dataclass(kw_only=True)
class UsingMutex:
    name: list[UsingMutex.Name] = field(
        default_factory=list,
        metadata={
            "name": "Name",
            "type": "Element",
            "namespace": "",
            "min_occurs": 1,
        },
    )
    file_name: None | str = field(
        default=None,
        metadata={
            "name": "FileName",
            "type": "Attribute",
        },
    )
    line_no: None | int = field(
        default=None,
        metadata={
            "name": "LineNo",
            "type": "Attribute",
        },
    )
    col_no: None | int = field(
        default=None,
        metadata={
            "name": "ColNo",
            "type": "Attribute",
        },
    )
    epx: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )

    @dataclass(kw_only=True)
    class Name:
        value: str = field(default="")
        file_name: None | str = field(
            default=None,
            metadata={
                "name": "FileName",
                "type": "Attribute",
            },
        )
        line_no: None | int = field(
            default=None,
            metadata={
                "name": "LineNo",
                "type": "Attribute",
            },
        )
        col_no: None | int = field(
            default=None,
            metadata={
                "name": "ColNo",
                "type": "Attribute",
            },
        )
        epx: None | str = field(
            default=None,
            metadata={
                "type": "Attribute",
            },
        )


@dataclass(kw_only=True)
class ArrayValue:
    choice: list[IntegerValue | RealValue | BooleanValue | StringValue] = field(
        default_factory=list,
        metadata={
            "type": "Elements",
            "choices": (
                {
                    "name": "IntegerValue",
                    "type": IntegerValue,
                },
                {
                    "name": "RealValue",
                    "type": RealValue,
                },
                {
                    "name": "BooleanValue",
                    "type": BooleanValue,
                },
                {
                    "name": "StringValue",
                    "type": StringValue,
                },
            ),
        },
    )
    type_value: AtomicTypeValues = field(
        metadata={
            "name": "Type",
            "type": "Attribute",
        }
    )
    file_name: None | str = field(
        default=None,
        metadata={
            "name": "FileName",
            "type": "Attribute",
        },
    )
    line_no: None | int = field(
        default=None,
        metadata={
            "name": "LineNo",
            "type": "Attribute",
        },
    )
    col_no: None | int = field(
        default=None,
        metadata={
            "name": "ColNo",
            "type": "Attribute",
        },
    )
    epx: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )


@dataclass(kw_only=True)
class Concat:
    choice: list[
        StringVariable
        | StringValue
        | Concat
        | LookupOnChange
        | LookupNow
        | ArrayElement
    ] = field(
        default_factory=list,
        metadata={
            "type": "Elements",
            "choices": (
                {
                    "name": "StringVariable",
                    "type": StringVariable,
                },
                {
                    "name": "StringValue",
                    "type": StringValue,
                },
                {
                    "name": "Concat",
                    "type": ForwardRef("Concat"),
                },
                {
                    "name": "LookupOnChange",
                    "type": ForwardRef("LookupOnChange"),
                },
                {
                    "name": "LookupNow",
                    "type": ForwardRef("LookupNow"),
                },
                {
                    "name": "ArrayElement",
                    "type": ForwardRef("ArrayElement"),
                },
            ),
        },
    )
    file_name: None | str = field(
        default=None,
        metadata={
            "name": "FileName",
            "type": "Attribute",
        },
    )
    line_no: None | int = field(
        default=None,
        metadata={
            "name": "LineNo",
            "type": "Attribute",
        },
    )
    col_no: None | int = field(
        default=None,
        metadata={
            "name": "ColNo",
            "type": "Attribute",
        },
    )
    epx: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )


@dataclass(kw_only=True)
class Eqstring:
    class Meta:
        name = "EQString"

    choice: list[
        StringVariable
        | StringValue
        | Concat
        | LookupOnChange
        | LookupNow
        | ArrayElement
    ] = field(
        default_factory=list,
        metadata={
            "type": "Elements",
            "choices": (
                {
                    "name": "StringVariable",
                    "type": StringVariable,
                    "max_occurs": 2,
                },
                {
                    "name": "StringValue",
                    "type": StringValue,
                    "max_occurs": 2,
                },
                {
                    "name": "Concat",
                    "type": ForwardRef("Concat"),
                    "max_occurs": 2,
                },
                {
                    "name": "LookupOnChange",
                    "type": ForwardRef("LookupOnChange"),
                    "max_occurs": 2,
                },
                {
                    "name": "LookupNow",
                    "type": ForwardRef("LookupNow"),
                    "max_occurs": 2,
                },
                {
                    "name": "ArrayElement",
                    "type": ForwardRef("ArrayElement"),
                    "max_occurs": 2,
                },
            ),
            "max_occurs": 2,
        },
    )
    file_name: None | str = field(
        default=None,
        metadata={
            "name": "FileName",
            "type": "Attribute",
        },
    )
    line_no: None | int = field(
        default=None,
        metadata={
            "name": "LineNo",
            "type": "Attribute",
        },
    )
    col_no: None | int = field(
        default=None,
        metadata={
            "name": "ColNo",
            "type": "Attribute",
        },
    )
    epx: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )


@dataclass(kw_only=True)
class Nestring:
    class Meta:
        name = "NEString"

    choice: list[
        StringVariable
        | StringValue
        | Concat
        | LookupOnChange
        | LookupNow
        | ArrayElement
    ] = field(
        default_factory=list,
        metadata={
            "type": "Elements",
            "choices": (
                {
                    "name": "StringVariable",
                    "type": StringVariable,
                    "max_occurs": 2,
                },
                {
                    "name": "StringValue",
                    "type": StringValue,
                    "max_occurs": 2,
                },
                {
                    "name": "Concat",
                    "type": ForwardRef("Concat"),
                    "max_occurs": 2,
                },
                {
                    "name": "LookupOnChange",
                    "type": ForwardRef("LookupOnChange"),
                    "max_occurs": 2,
                },
                {
                    "name": "LookupNow",
                    "type": ForwardRef("LookupNow"),
                    "max_occurs": 2,
                },
                {
                    "name": "ArrayElement",
                    "type": ForwardRef("ArrayElement"),
                    "max_occurs": 2,
                },
            ),
            "max_occurs": 2,
        },
    )
    file_name: None | str = field(
        default=None,
        metadata={
            "name": "FileName",
            "type": "Attribute",
        },
    )
    line_no: None | int = field(
        default=None,
        metadata={
            "name": "LineNo",
            "type": "Attribute",
        },
    )
    col_no: None | int = field(
        default=None,
        metadata={
            "name": "ColNo",
            "type": "Attribute",
        },
    )
    epx: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )


@dataclass(kw_only=True)
class NodeCommandHandleValue:
    value: NodeCommandHandleValueValue = field()


@dataclass(kw_only=True)
class NodeFailureValue:
    value: NodeFailureValueValue = field()


@dataclass(kw_only=True)
class NodeOutcomeValue:
    value: NodeOutcomeValueValue = field()


@dataclass(kw_only=True)
class NodeRef:
    value: str | NcnameOrEmptyValue = field(default="")
    dir: None | NodeRefDir = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    file_name: None | str = field(
        default=None,
        metadata={
            "name": "FileName",
            "type": "Attribute",
        },
    )
    line_no: None | int = field(
        default=None,
        metadata={
            "name": "LineNo",
            "type": "Attribute",
        },
    )
    col_no: None | int = field(
        default=None,
        metadata={
            "name": "ColNo",
            "type": "Attribute",
        },
    )
    epx: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )


@dataclass(kw_only=True)
class NodeStateValue:
    value: NodeStateValueValue = field()


@dataclass(kw_only=True)
class Parameter:
    name: None | str = field(
        default=None,
        metadata={
            "name": "Name",
            "type": "Element",
            "namespace": "",
        },
    )
    type_value: ParameterTypeValues = field(
        metadata={
            "name": "Type",
            "type": "Element",
            "namespace": "",
        }
    )
    max_size: None | int = field(
        default=None,
        metadata={
            "name": "MaxSize",
            "type": "Element",
            "namespace": "",
        },
    )
    file_name: None | str = field(
        default=None,
        metadata={
            "name": "FileName",
            "type": "Attribute",
        },
    )
    line_no: None | int = field(
        default=None,
        metadata={
            "name": "LineNo",
            "type": "Attribute",
        },
    )
    col_no: None | int = field(
        default=None,
        metadata={
            "name": "ColNo",
            "type": "Attribute",
        },
    )
    epx: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )


@dataclass(kw_only=True)
class Return:
    class Meta:
        nillable = True

    name: None | str = field(
        default=None,
        metadata={
            "name": "Name",
            "type": "Element",
            "namespace": "",
        },
    )
    type_value: None | AtomicTypeValues = field(
        default=None,
        metadata={
            "name": "Type",
            "type": "Element",
            "namespace": "",
            "required": True,
        },
    )
    max_size: None | int = field(
        default=None,
        metadata={
            "name": "MaxSize",
            "type": "Element",
            "namespace": "",
        },
    )
    file_name: None | str = field(
        default=None,
        metadata={
            "name": "FileName",
            "type": "Attribute",
        },
    )
    line_no: None | int = field(
        default=None,
        metadata={
            "name": "LineNo",
            "type": "Attribute",
        },
    )
    col_no: None | int = field(
        default=None,
        metadata={
            "name": "ColNo",
            "type": "Attribute",
        },
    )
    epx: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )


@dataclass(kw_only=True)
class Timepoint:
    value: TimepointValue = field()


@dataclass(kw_only=True)
class AllKnown:
    class Meta:
        name = "ALL_KNOWN"

    choice: None | ArrayValue | ArrayVariable | LookupOnChange | LookupNow = field(
        default=None,
        metadata={
            "type": "Elements",
            "choices": (
                {
                    "name": "ArrayValue",
                    "type": ArrayValue,
                },
                {
                    "name": "ArrayVariable",
                    "type": ArrayVariable,
                },
                {
                    "name": "LookupOnChange",
                    "type": ForwardRef("LookupOnChange"),
                },
                {
                    "name": "LookupNow",
                    "type": ForwardRef("LookupNow"),
                },
            ),
        },
    )
    file_name: None | str = field(
        default=None,
        metadata={
            "name": "FileName",
            "type": "Attribute",
        },
    )
    line_no: None | int = field(
        default=None,
        metadata={
            "name": "LineNo",
            "type": "Attribute",
        },
    )
    col_no: None | int = field(
        default=None,
        metadata={
            "name": "ColNo",
            "type": "Attribute",
        },
    )
    epx: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )


@dataclass(kw_only=True)
class AnyKnown:
    class Meta:
        name = "ANY_KNOWN"

    choice: None | ArrayValue | ArrayVariable | LookupOnChange | LookupNow = field(
        default=None,
        metadata={
            "type": "Elements",
            "choices": (
                {
                    "name": "ArrayValue",
                    "type": ArrayValue,
                },
                {
                    "name": "ArrayVariable",
                    "type": ArrayVariable,
                },
                {
                    "name": "LookupOnChange",
                    "type": ForwardRef("LookupOnChange"),
                },
                {
                    "name": "LookupNow",
                    "type": ForwardRef("LookupNow"),
                },
            ),
        },
    )
    file_name: None | str = field(
        default=None,
        metadata={
            "name": "FileName",
            "type": "Attribute",
        },
    )
    line_no: None | int = field(
        default=None,
        metadata={
            "name": "LineNo",
            "type": "Attribute",
        },
    )
    col_no: None | int = field(
        default=None,
        metadata={
            "name": "ColNo",
            "type": "Attribute",
        },
    )
    epx: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )


@dataclass(kw_only=True)
class ArrayRhs:
    class Meta:
        name = "ArrayRHS"

    choice: None | ArrayValue | ArrayVariable | LookupOnChange | LookupNow = field(
        default=None,
        metadata={
            "type": "Elements",
            "choices": (
                {
                    "name": "ArrayValue",
                    "type": ArrayValue,
                },
                {
                    "name": "ArrayVariable",
                    "type": ArrayVariable,
                },
                {
                    "name": "LookupOnChange",
                    "type": LookupOnChange,
                },
                {
                    "name": "LookupNow",
                    "type": LookupNow,
                },
            ),
        },
    )
    file_name: None | str = field(
        default=None,
        metadata={
            "name": "FileName",
            "type": "Attribute",
        },
    )
    line_no: None | int = field(
        default=None,
        metadata={
            "name": "LineNo",
            "type": "Attribute",
        },
    )
    col_no: None | int = field(
        default=None,
        metadata={
            "name": "ColNo",
            "type": "Attribute",
        },
    )
    epx: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )


@dataclass(kw_only=True)
class DeclareArray:
    name: str = field(
        metadata={
            "name": "Name",
            "type": "Element",
            "namespace": "",
        }
    )
    type_value: AtomicTypeValues = field(
        metadata={
            "name": "Type",
            "type": "Element",
            "namespace": "",
        }
    )
    max_size: None | int = field(
        default=None,
        metadata={
            "name": "MaxSize",
            "type": "Element",
            "namespace": "",
        },
    )
    initial_value: None | DeclareArray.InitialValue = field(
        default=None,
        metadata={
            "name": "InitialValue",
            "type": "Element",
            "namespace": "",
        },
    )
    file_name: None | str = field(
        default=None,
        metadata={
            "name": "FileName",
            "type": "Attribute",
        },
    )
    line_no: None | int = field(
        default=None,
        metadata={
            "name": "LineNo",
            "type": "Attribute",
        },
    )
    col_no: None | int = field(
        default=None,
        metadata={
            "name": "ColNo",
            "type": "Attribute",
        },
    )
    epx: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )

    @dataclass(kw_only=True)
    class InitialValue:
        choice: (
            None
            | ArrayValue
            | ArrayVariable
            | IntegerValue
            | RealValue
            | BooleanValue
            | StringValue
        ) = field(
            default=None,
            metadata={
                "type": "Elements",
                "choices": (
                    {
                        "name": "ArrayValue",
                        "type": ArrayValue,
                    },
                    {
                        "name": "ArrayVariable",
                        "type": ArrayVariable,
                    },
                    {
                        "name": "IntegerValue",
                        "type": IntegerValue,
                    },
                    {
                        "name": "RealValue",
                        "type": RealValue,
                    },
                    {
                        "name": "BooleanValue",
                        "type": BooleanValue,
                    },
                    {
                        "name": "StringValue",
                        "type": StringValue,
                    },
                ),
            },
        )


@dataclass(kw_only=True)
class Eqarray:
    class Meta:
        name = "EQArray"

    choice: list[ArrayValue | ArrayVariable | LookupOnChange | LookupNow] = field(
        default_factory=list,
        metadata={
            "type": "Elements",
            "choices": (
                {
                    "name": "ArrayValue",
                    "type": ArrayValue,
                    "max_occurs": 2,
                },
                {
                    "name": "ArrayVariable",
                    "type": ArrayVariable,
                    "max_occurs": 2,
                },
                {
                    "name": "LookupOnChange",
                    "type": ForwardRef("LookupOnChange"),
                    "max_occurs": 2,
                },
                {
                    "name": "LookupNow",
                    "type": ForwardRef("LookupNow"),
                    "max_occurs": 2,
                },
            ),
            "max_occurs": 2,
        },
    )
    file_name: None | str = field(
        default=None,
        metadata={
            "name": "FileName",
            "type": "Attribute",
        },
    )
    line_no: None | int = field(
        default=None,
        metadata={
            "name": "LineNo",
            "type": "Attribute",
        },
    )
    col_no: None | int = field(
        default=None,
        metadata={
            "name": "ColNo",
            "type": "Attribute",
        },
    )
    epx: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )


@dataclass(kw_only=True)
class Nearray:
    class Meta:
        name = "NEArray"

    choice: list[ArrayValue | ArrayVariable | LookupOnChange | LookupNow] = field(
        default_factory=list,
        metadata={
            "type": "Elements",
            "choices": (
                {
                    "name": "ArrayValue",
                    "type": ArrayValue,
                    "max_occurs": 2,
                },
                {
                    "name": "ArrayVariable",
                    "type": ArrayVariable,
                    "max_occurs": 2,
                },
                {
                    "name": "LookupOnChange",
                    "type": ForwardRef("LookupOnChange"),
                    "max_occurs": 2,
                },
                {
                    "name": "LookupNow",
                    "type": ForwardRef("LookupNow"),
                    "max_occurs": 2,
                },
            ),
            "max_occurs": 2,
        },
    )
    file_name: None | str = field(
        default=None,
        metadata={
            "name": "FileName",
            "type": "Attribute",
        },
    )
    line_no: None | int = field(
        default=None,
        metadata={
            "name": "LineNo",
            "type": "Attribute",
        },
    )
    col_no: None | int = field(
        default=None,
        metadata={
            "name": "ColNo",
            "type": "Attribute",
        },
    )
    epx: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )


@dataclass(kw_only=True)
class NodeTimepointValue:
    node_id_or_node_ref: None | NodeId | NodeRef = field(
        default=None,
        metadata={
            "type": "Elements",
            "choices": (
                {
                    "name": "NodeId",
                    "type": NodeId,
                },
                {
                    "name": "NodeRef",
                    "type": NodeRef,
                },
            ),
        },
    )
    node_state_value: NodeStateValue = field(
        metadata={
            "name": "NodeStateValue",
            "type": "Element",
        }
    )
    timepoint: Timepoint = field(
        metadata={
            "name": "Timepoint",
            "type": "Element",
        }
    )
    file_name: None | str = field(
        default=None,
        metadata={
            "name": "FileName",
            "type": "Attribute",
        },
    )
    line_no: None | int = field(
        default=None,
        metadata={
            "name": "LineNo",
            "type": "Attribute",
        },
    )
    col_no: None | int = field(
        default=None,
        metadata={
            "name": "ColNo",
            "type": "Attribute",
        },
    )
    epx: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )


@dataclass(kw_only=True)
class Strlen:
    class Meta:
        name = "STRLEN"

    choice: (
        None
        | StringVariable
        | StringValue
        | Concat
        | LookupOnChange
        | LookupNow
        | ArrayElement
    ) = field(
        default=None,
        metadata={
            "type": "Elements",
            "choices": (
                {
                    "name": "StringVariable",
                    "type": StringVariable,
                },
                {
                    "name": "StringValue",
                    "type": StringValue,
                },
                {
                    "name": "Concat",
                    "type": Concat,
                },
                {
                    "name": "LookupOnChange",
                    "type": ForwardRef("LookupOnChange"),
                },
                {
                    "name": "LookupNow",
                    "type": ForwardRef("LookupNow"),
                },
                {
                    "name": "ArrayElement",
                    "type": ForwardRef("ArrayElement"),
                },
            ),
        },
    )
    file_name: None | str = field(
        default=None,
        metadata={
            "name": "FileName",
            "type": "Attribute",
        },
    )
    line_no: None | int = field(
        default=None,
        metadata={
            "name": "LineNo",
            "type": "Attribute",
        },
    )
    col_no: None | int = field(
        default=None,
        metadata={
            "name": "ColNo",
            "type": "Attribute",
        },
    )
    epx: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )


@dataclass(kw_only=True)
class StateDeclaration:
    name: str = field(
        metadata={
            "name": "Name",
            "type": "Element",
            "namespace": "",
        }
    )
    return_value: None | Return = field(
        metadata={
            "name": "Return",
            "type": "Element",
        }
    )
    parameter: list[Parameter] = field(
        default_factory=list,
        metadata={
            "name": "Parameter",
            "type": "Element",
        },
    )
    any_parameters: None | object = field(
        default=None,
        metadata={
            "name": "AnyParameters",
            "type": "Element",
            "namespace": "",
        },
    )
    file_name: None | str = field(
        default=None,
        metadata={
            "name": "FileName",
            "type": "Attribute",
        },
    )
    line_no: None | int = field(
        default=None,
        metadata={
            "name": "LineNo",
            "type": "Attribute",
        },
    )
    col_no: None | int = field(
        default=None,
        metadata={
            "name": "ColNo",
            "type": "Attribute",
        },
    )
    epx: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )


@dataclass(kw_only=True)
class UnaryArrayOperator:
    choice: None | ArrayValue | ArrayVariable | LookupOnChange | LookupNow = field(
        default=None,
        metadata={
            "type": "Elements",
            "choices": (
                {
                    "name": "ArrayValue",
                    "type": ArrayValue,
                },
                {
                    "name": "ArrayVariable",
                    "type": ArrayVariable,
                },
                {
                    "name": "LookupOnChange",
                    "type": ForwardRef("LookupOnChange"),
                },
                {
                    "name": "LookupNow",
                    "type": ForwardRef("LookupNow"),
                },
            ),
        },
    )
    file_name: None | str = field(
        default=None,
        metadata={
            "name": "FileName",
            "type": "Attribute",
        },
    )
    line_no: None | int = field(
        default=None,
        metadata={
            "name": "LineNo",
            "type": "Attribute",
        },
    )
    col_no: None | int = field(
        default=None,
        metadata={
            "name": "ColNo",
            "type": "Attribute",
        },
    )
    epx: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )


@dataclass(kw_only=True)
class NodeReference:
    class Meta:
        name = "node-reference"

    node_id_or_node_ref: None | NodeId | NodeRef = field(
        default=None,
        metadata={
            "type": "Elements",
            "choices": (
                {
                    "name": "NodeId",
                    "type": NodeId,
                },
                {
                    "name": "NodeRef",
                    "type": NodeRef,
                },
            ),
        },
    )
    file_name: None | str = field(
        default=None,
        metadata={
            "name": "FileName",
            "type": "Attribute",
        },
    )
    line_no: None | int = field(
        default=None,
        metadata={
            "name": "LineNo",
            "type": "Attribute",
        },
    )
    col_no: None | int = field(
        default=None,
        metadata={
            "name": "ColNo",
            "type": "Attribute",
        },
    )
    epx: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )


@dataclass(kw_only=True)
class ArrayMaxSize(UnaryArrayOperator):
    pass


@dataclass(kw_only=True)
class ArraySize(UnaryArrayOperator):
    pass


@dataclass(kw_only=True)
class Executing(NodeReference):
    pass


@dataclass(kw_only=True)
class Failed(NodeReference):
    pass


@dataclass(kw_only=True)
class Finished(NodeReference):
    pass


@dataclass(kw_only=True)
class Inactive(NodeReference):
    pass


@dataclass(kw_only=True)
class IterationEnded(NodeReference):
    pass


@dataclass(kw_only=True)
class NoChildFailed(NodeReference):
    pass


@dataclass(kw_only=True)
class NodeCommandHandleVariable(NodeReference):
    pass


@dataclass(kw_only=True)
class NodeFailureVariable(NodeReference):
    pass


@dataclass(kw_only=True)
class NodeOutcomeVariable(NodeReference):
    pass


@dataclass(kw_only=True)
class NodeStateVariable(NodeReference):
    pass


@dataclass(kw_only=True)
class NumericComparisonType:
    choice: list[
        Add
        | Sub
        | Mul
        | Div
        | Mod
        | Max
        | Min
        | Sqrt
        | Abs
        | Ceil
        | Floor
        | Round
        | Trunc
        | RealToInt
        | IntegerVariable
        | RealVariable
        | IntegerValue
        | RealValue
        | NodeTimepointValue
        | ArraySize
        | ArrayMaxSize
        | LookupOnChange
        | LookupNow
        | ArrayElement
        | Strlen
    ] = field(
        default_factory=list,
        metadata={
            "type": "Elements",
            "choices": (
                {
                    "name": "ADD",
                    "type": ForwardRef("Add"),
                    "max_occurs": 2,
                },
                {
                    "name": "SUB",
                    "type": ForwardRef("Sub"),
                    "max_occurs": 2,
                },
                {
                    "name": "MUL",
                    "type": ForwardRef("Mul"),
                    "max_occurs": 2,
                },
                {
                    "name": "DIV",
                    "type": ForwardRef("Div"),
                    "max_occurs": 2,
                },
                {
                    "name": "MOD",
                    "type": ForwardRef("Mod"),
                    "max_occurs": 2,
                },
                {
                    "name": "MAX",
                    "type": ForwardRef("Max"),
                    "max_occurs": 2,
                },
                {
                    "name": "MIN",
                    "type": ForwardRef("Min"),
                    "max_occurs": 2,
                },
                {
                    "name": "SQRT",
                    "type": ForwardRef("Sqrt"),
                    "max_occurs": 2,
                },
                {
                    "name": "ABS",
                    "type": ForwardRef("Abs"),
                    "max_occurs": 2,
                },
                {
                    "name": "CEIL",
                    "type": ForwardRef("Ceil"),
                    "max_occurs": 2,
                },
                {
                    "name": "FLOOR",
                    "type": ForwardRef("Floor"),
                    "max_occurs": 2,
                },
                {
                    "name": "ROUND",
                    "type": ForwardRef("Round"),
                    "max_occurs": 2,
                },
                {
                    "name": "TRUNC",
                    "type": ForwardRef("Trunc"),
                    "max_occurs": 2,
                },
                {
                    "name": "REAL_TO_INT",
                    "type": ForwardRef("RealToInt"),
                    "max_occurs": 2,
                },
                {
                    "name": "IntegerVariable",
                    "type": IntegerVariable,
                    "max_occurs": 2,
                },
                {
                    "name": "RealVariable",
                    "type": RealVariable,
                    "max_occurs": 2,
                },
                {
                    "name": "IntegerValue",
                    "type": IntegerValue,
                    "max_occurs": 2,
                },
                {
                    "name": "RealValue",
                    "type": RealValue,
                    "max_occurs": 2,
                },
                {
                    "name": "NodeTimepointValue",
                    "type": NodeTimepointValue,
                    "max_occurs": 2,
                },
                {
                    "name": "ArraySize",
                    "type": ForwardRef("ArraySize"),
                    "max_occurs": 2,
                },
                {
                    "name": "ArrayMaxSize",
                    "type": ForwardRef("ArrayMaxSize"),
                    "max_occurs": 2,
                },
                {
                    "name": "LookupOnChange",
                    "type": ForwardRef("LookupOnChange"),
                    "max_occurs": 2,
                },
                {
                    "name": "LookupNow",
                    "type": ForwardRef("LookupNow"),
                    "max_occurs": 2,
                },
                {
                    "name": "ArrayElement",
                    "type": ForwardRef("ArrayElement"),
                    "max_occurs": 2,
                },
                {
                    "name": "STRLEN",
                    "type": ForwardRef("Strlen"),
                    "max_occurs": 2,
                },
            ),
            "max_occurs": 2,
        },
    )
    file_name: None | str = field(
        default=None,
        metadata={
            "name": "FileName",
            "type": "Attribute",
        },
    )
    line_no: None | int = field(
        default=None,
        metadata={
            "name": "LineNo",
            "type": "Attribute",
        },
    )
    col_no: None | int = field(
        default=None,
        metadata={
            "name": "ColNo",
            "type": "Attribute",
        },
    )
    epx: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )


@dataclass(kw_only=True)
class PostconditionFailed(NodeReference):
    pass


@dataclass(kw_only=True)
class Skipped(NodeReference):
    pass


@dataclass(kw_only=True)
class Succeeded(NodeReference):
    pass


@dataclass(kw_only=True)
class UnaryNumericExpression:
    choice: (
        None
        | Add
        | Sub
        | Mul
        | Div
        | Mod
        | Max
        | Min
        | Sqrt
        | Abs
        | Ceil
        | Floor
        | Round
        | Trunc
        | RealToInt
        | IntegerVariable
        | RealVariable
        | IntegerValue
        | RealValue
        | NodeTimepointValue
        | ArraySize
        | ArrayMaxSize
        | LookupOnChange
        | LookupNow
        | ArrayElement
        | Strlen
    ) = field(
        default=None,
        metadata={
            "type": "Elements",
            "choices": (
                {
                    "name": "ADD",
                    "type": ForwardRef("Add"),
                },
                {
                    "name": "SUB",
                    "type": ForwardRef("Sub"),
                },
                {
                    "name": "MUL",
                    "type": ForwardRef("Mul"),
                },
                {
                    "name": "DIV",
                    "type": ForwardRef("Div"),
                },
                {
                    "name": "MOD",
                    "type": ForwardRef("Mod"),
                },
                {
                    "name": "MAX",
                    "type": ForwardRef("Max"),
                },
                {
                    "name": "MIN",
                    "type": ForwardRef("Min"),
                },
                {
                    "name": "SQRT",
                    "type": ForwardRef("Sqrt"),
                },
                {
                    "name": "ABS",
                    "type": ForwardRef("Abs"),
                },
                {
                    "name": "CEIL",
                    "type": ForwardRef("Ceil"),
                },
                {
                    "name": "FLOOR",
                    "type": ForwardRef("Floor"),
                },
                {
                    "name": "ROUND",
                    "type": ForwardRef("Round"),
                },
                {
                    "name": "TRUNC",
                    "type": ForwardRef("Trunc"),
                },
                {
                    "name": "REAL_TO_INT",
                    "type": ForwardRef("RealToInt"),
                },
                {
                    "name": "IntegerVariable",
                    "type": IntegerVariable,
                },
                {
                    "name": "RealVariable",
                    "type": RealVariable,
                },
                {
                    "name": "IntegerValue",
                    "type": IntegerValue,
                },
                {
                    "name": "RealValue",
                    "type": RealValue,
                },
                {
                    "name": "NodeTimepointValue",
                    "type": NodeTimepointValue,
                },
                {
                    "name": "ArraySize",
                    "type": ForwardRef("ArraySize"),
                },
                {
                    "name": "ArrayMaxSize",
                    "type": ForwardRef("ArrayMaxSize"),
                },
                {
                    "name": "LookupOnChange",
                    "type": ForwardRef("LookupOnChange"),
                },
                {
                    "name": "LookupNow",
                    "type": ForwardRef("LookupNow"),
                },
                {
                    "name": "ArrayElement",
                    "type": ForwardRef("ArrayElement"),
                },
                {
                    "name": "STRLEN",
                    "type": ForwardRef("Strlen"),
                },
            ),
        },
    )
    file_name: None | str = field(
        default=None,
        metadata={
            "name": "FileName",
            "type": "Attribute",
        },
    )
    line_no: None | int = field(
        default=None,
        metadata={
            "name": "LineNo",
            "type": "Attribute",
        },
    )
    col_no: None | int = field(
        default=None,
        metadata={
            "name": "ColNo",
            "type": "Attribute",
        },
    )
    epx: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )


@dataclass(kw_only=True)
class Waiting(NodeReference):
    pass


@dataclass(kw_only=True)
class Abs(UnaryNumericExpression):
    class Meta:
        name = "ABS"


@dataclass(kw_only=True)
class Ceil(UnaryNumericExpression):
    class Meta:
        name = "CEIL"


@dataclass(kw_only=True)
class Eqinternal:
    class Meta:
        name = "EQInternal"

    choice: list[
        NodeStateVariable
        | NodeStateValue
        | NodeOutcomeVariable
        | NodeOutcomeValue
        | NodeFailureVariable
        | NodeFailureValue
        | NodeCommandHandleVariable
        | NodeCommandHandleValue
    ] = field(
        default_factory=list,
        metadata={
            "type": "Elements",
            "choices": (
                {
                    "name": "NodeStateVariable",
                    "type": NodeStateVariable,
                    "max_occurs": 2,
                },
                {
                    "name": "NodeStateValue",
                    "type": NodeStateValue,
                    "max_occurs": 2,
                },
                {
                    "name": "NodeOutcomeVariable",
                    "type": NodeOutcomeVariable,
                    "max_occurs": 2,
                },
                {
                    "name": "NodeOutcomeValue",
                    "type": NodeOutcomeValue,
                    "max_occurs": 2,
                },
                {
                    "name": "NodeFailureVariable",
                    "type": NodeFailureVariable,
                    "max_occurs": 2,
                },
                {
                    "name": "NodeFailureValue",
                    "type": NodeFailureValue,
                    "max_occurs": 2,
                },
                {
                    "name": "NodeCommandHandleVariable",
                    "type": NodeCommandHandleVariable,
                    "max_occurs": 2,
                },
                {
                    "name": "NodeCommandHandleValue",
                    "type": NodeCommandHandleValue,
                    "max_occurs": 2,
                },
            ),
            "max_occurs": 2,
        },
    )
    file_name: None | str = field(
        default=None,
        metadata={
            "name": "FileName",
            "type": "Attribute",
        },
    )
    line_no: None | int = field(
        default=None,
        metadata={
            "name": "LineNo",
            "type": "Attribute",
        },
    )
    col_no: None | int = field(
        default=None,
        metadata={
            "name": "ColNo",
            "type": "Attribute",
        },
    )
    epx: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )


@dataclass(kw_only=True)
class Eqnumeric(NumericComparisonType):
    class Meta:
        name = "EQNumeric"


@dataclass(kw_only=True)
class Floor(UnaryNumericExpression):
    class Meta:
        name = "FLOOR"


@dataclass(kw_only=True)
class Ge(NumericComparisonType):
    class Meta:
        name = "GE"


@dataclass(kw_only=True)
class Gt(NumericComparisonType):
    class Meta:
        name = "GT"


@dataclass(kw_only=True)
class Le(NumericComparisonType):
    class Meta:
        name = "LE"


@dataclass(kw_only=True)
class Lt(NumericComparisonType):
    class Meta:
        name = "LT"


@dataclass(kw_only=True)
class Neinternal:
    class Meta:
        name = "NEInternal"

    choice: list[
        NodeStateVariable
        | NodeStateValue
        | NodeOutcomeVariable
        | NodeOutcomeValue
        | NodeFailureVariable
        | NodeFailureValue
        | NodeCommandHandleVariable
        | NodeCommandHandleValue
    ] = field(
        default_factory=list,
        metadata={
            "type": "Elements",
            "choices": (
                {
                    "name": "NodeStateVariable",
                    "type": NodeStateVariable,
                    "max_occurs": 2,
                },
                {
                    "name": "NodeStateValue",
                    "type": NodeStateValue,
                    "max_occurs": 2,
                },
                {
                    "name": "NodeOutcomeVariable",
                    "type": NodeOutcomeVariable,
                    "max_occurs": 2,
                },
                {
                    "name": "NodeOutcomeValue",
                    "type": NodeOutcomeValue,
                    "max_occurs": 2,
                },
                {
                    "name": "NodeFailureVariable",
                    "type": NodeFailureVariable,
                    "max_occurs": 2,
                },
                {
                    "name": "NodeFailureValue",
                    "type": NodeFailureValue,
                    "max_occurs": 2,
                },
                {
                    "name": "NodeCommandHandleVariable",
                    "type": NodeCommandHandleVariable,
                    "max_occurs": 2,
                },
                {
                    "name": "NodeCommandHandleValue",
                    "type": NodeCommandHandleValue,
                    "max_occurs": 2,
                },
            ),
            "max_occurs": 2,
        },
    )
    file_name: None | str = field(
        default=None,
        metadata={
            "name": "FileName",
            "type": "Attribute",
        },
    )
    line_no: None | int = field(
        default=None,
        metadata={
            "name": "LineNo",
            "type": "Attribute",
        },
    )
    col_no: None | int = field(
        default=None,
        metadata={
            "name": "ColNo",
            "type": "Attribute",
        },
    )
    epx: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )


@dataclass(kw_only=True)
class Nenumeric(NumericComparisonType):
    class Meta:
        name = "NENumeric"


@dataclass(kw_only=True)
class RealToInt(UnaryNumericExpression):
    class Meta:
        name = "REAL_TO_INT"


@dataclass(kw_only=True)
class Round(UnaryNumericExpression):
    class Meta:
        name = "ROUND"


@dataclass(kw_only=True)
class Sqrt(UnaryNumericExpression):
    class Meta:
        name = "SQRT"


@dataclass(kw_only=True)
class Trunc(UnaryNumericExpression):
    class Meta:
        name = "TRUNC"


@dataclass(kw_only=True)
class BinaryNumericExpression:
    choice: list[
        Add
        | Sub
        | Mul
        | Div
        | Mod
        | Max
        | Min
        | Sqrt
        | Abs
        | Ceil
        | Floor
        | Round
        | Trunc
        | RealToInt
        | IntegerVariable
        | RealVariable
        | IntegerValue
        | RealValue
        | NodeTimepointValue
        | ArraySize
        | ArrayMaxSize
        | LookupOnChange
        | LookupNow
        | ArrayElement
        | Strlen
    ] = field(
        default_factory=list,
        metadata={
            "type": "Elements",
            "choices": (
                {
                    "name": "ADD",
                    "type": ForwardRef("Add"),
                    "max_occurs": 2,
                },
                {
                    "name": "SUB",
                    "type": ForwardRef("Sub"),
                    "max_occurs": 2,
                },
                {
                    "name": "MUL",
                    "type": ForwardRef("Mul"),
                    "max_occurs": 2,
                },
                {
                    "name": "DIV",
                    "type": ForwardRef("Div"),
                    "max_occurs": 2,
                },
                {
                    "name": "MOD",
                    "type": ForwardRef("Mod"),
                    "max_occurs": 2,
                },
                {
                    "name": "MAX",
                    "type": ForwardRef("Max"),
                    "max_occurs": 2,
                },
                {
                    "name": "MIN",
                    "type": ForwardRef("Min"),
                    "max_occurs": 2,
                },
                {
                    "name": "SQRT",
                    "type": Sqrt,
                    "max_occurs": 2,
                },
                {
                    "name": "ABS",
                    "type": Abs,
                    "max_occurs": 2,
                },
                {
                    "name": "CEIL",
                    "type": Ceil,
                    "max_occurs": 2,
                },
                {
                    "name": "FLOOR",
                    "type": Floor,
                    "max_occurs": 2,
                },
                {
                    "name": "ROUND",
                    "type": Round,
                    "max_occurs": 2,
                },
                {
                    "name": "TRUNC",
                    "type": Trunc,
                    "max_occurs": 2,
                },
                {
                    "name": "REAL_TO_INT",
                    "type": RealToInt,
                    "max_occurs": 2,
                },
                {
                    "name": "IntegerVariable",
                    "type": IntegerVariable,
                    "max_occurs": 2,
                },
                {
                    "name": "RealVariable",
                    "type": RealVariable,
                    "max_occurs": 2,
                },
                {
                    "name": "IntegerValue",
                    "type": IntegerValue,
                    "max_occurs": 2,
                },
                {
                    "name": "RealValue",
                    "type": RealValue,
                    "max_occurs": 2,
                },
                {
                    "name": "NodeTimepointValue",
                    "type": NodeTimepointValue,
                    "max_occurs": 2,
                },
                {
                    "name": "ArraySize",
                    "type": ForwardRef("ArraySize"),
                    "max_occurs": 2,
                },
                {
                    "name": "ArrayMaxSize",
                    "type": ForwardRef("ArrayMaxSize"),
                    "max_occurs": 2,
                },
                {
                    "name": "LookupOnChange",
                    "type": ForwardRef("LookupOnChange"),
                    "max_occurs": 2,
                },
                {
                    "name": "LookupNow",
                    "type": ForwardRef("LookupNow"),
                    "max_occurs": 2,
                },
                {
                    "name": "ArrayElement",
                    "type": ForwardRef("ArrayElement"),
                    "max_occurs": 2,
                },
                {
                    "name": "STRLEN",
                    "type": ForwardRef("Strlen"),
                    "max_occurs": 2,
                },
            ),
            "max_occurs": 2,
        },
    )
    file_name: None | str = field(
        default=None,
        metadata={
            "name": "FileName",
            "type": "Attribute",
        },
    )
    line_no: None | int = field(
        default=None,
        metadata={
            "name": "LineNo",
            "type": "Attribute",
        },
    )
    col_no: None | int = field(
        default=None,
        metadata={
            "name": "ColNo",
            "type": "Attribute",
        },
    )
    epx: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )


@dataclass(kw_only=True)
class NaryBooleanOperator:
    choice: list[
        BooleanVariable
        | BooleanValue
        | Or
        | Xor
        | And
        | Not
        | Eqboolean
        | Eqnumeric
        | Eqinternal
        | Eqstring
        | Eqarray
        | Neboolean
        | Nenumeric
        | Neinternal
        | Nestring
        | Nearray
        | Gt
        | Ge
        | Lt
        | Le
        | IsKnown
        | AllKnown
        | AnyKnown
        | Executing
        | Finished
        | Inactive
        | IterationEnded
        | Waiting
        | NoChildFailed
        | Failed
        | Skipped
        | Succeeded
        | PostconditionFailed
        | LookupOnChange
        | LookupNow
        | ArrayElement
    ] = field(
        default_factory=list,
        metadata={
            "type": "Elements",
            "choices": (
                {
                    "name": "BooleanVariable",
                    "type": BooleanVariable,
                },
                {
                    "name": "BooleanValue",
                    "type": BooleanValue,
                },
                {
                    "name": "OR",
                    "type": ForwardRef("Or"),
                },
                {
                    "name": "XOR",
                    "type": ForwardRef("Xor"),
                },
                {
                    "name": "AND",
                    "type": ForwardRef("And"),
                },
                {
                    "name": "NOT",
                    "type": ForwardRef("Not"),
                },
                {
                    "name": "EQBoolean",
                    "type": ForwardRef("Eqboolean"),
                },
                {
                    "name": "EQNumeric",
                    "type": ForwardRef("Eqnumeric"),
                },
                {
                    "name": "EQInternal",
                    "type": Eqinternal,
                },
                {
                    "name": "EQString",
                    "type": ForwardRef("Eqstring"),
                },
                {
                    "name": "EQArray",
                    "type": ForwardRef("Eqarray"),
                },
                {
                    "name": "NEBoolean",
                    "type": ForwardRef("Neboolean"),
                },
                {
                    "name": "NENumeric",
                    "type": ForwardRef("Nenumeric"),
                },
                {
                    "name": "NEInternal",
                    "type": Neinternal,
                },
                {
                    "name": "NEString",
                    "type": ForwardRef("Nestring"),
                },
                {
                    "name": "NEArray",
                    "type": ForwardRef("Nearray"),
                },
                {
                    "name": "GT",
                    "type": ForwardRef("Gt"),
                },
                {
                    "name": "GE",
                    "type": ForwardRef("Ge"),
                },
                {
                    "name": "LT",
                    "type": ForwardRef("Lt"),
                },
                {
                    "name": "LE",
                    "type": ForwardRef("Le"),
                },
                {
                    "name": "IsKnown",
                    "type": ForwardRef("IsKnown"),
                },
                {
                    "name": "ALL_KNOWN",
                    "type": ForwardRef("AllKnown"),
                },
                {
                    "name": "ANY_KNOWN",
                    "type": ForwardRef("AnyKnown"),
                },
                {
                    "name": "Executing",
                    "type": Executing,
                },
                {
                    "name": "Finished",
                    "type": Finished,
                },
                {
                    "name": "Inactive",
                    "type": Inactive,
                },
                {
                    "name": "IterationEnded",
                    "type": IterationEnded,
                },
                {
                    "name": "Waiting",
                    "type": Waiting,
                },
                {
                    "name": "NoChildFailed",
                    "type": NoChildFailed,
                },
                {
                    "name": "Failed",
                    "type": Failed,
                },
                {
                    "name": "Skipped",
                    "type": Skipped,
                },
                {
                    "name": "Succeeded",
                    "type": Succeeded,
                },
                {
                    "name": "PostconditionFailed",
                    "type": PostconditionFailed,
                },
                {
                    "name": "LookupOnChange",
                    "type": ForwardRef("LookupOnChange"),
                },
                {
                    "name": "LookupNow",
                    "type": ForwardRef("LookupNow"),
                },
                {
                    "name": "ArrayElement",
                    "type": ForwardRef("ArrayElement"),
                },
            ),
        },
    )
    file_name: None | str = field(
        default=None,
        metadata={
            "name": "FileName",
            "type": "Attribute",
        },
    )
    line_no: None | int = field(
        default=None,
        metadata={
            "name": "LineNo",
            "type": "Attribute",
        },
    )
    col_no: None | int = field(
        default=None,
        metadata={
            "name": "ColNo",
            "type": "Attribute",
        },
    )
    epx: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )


@dataclass(kw_only=True)
class And(NaryBooleanOperator):
    class Meta:
        name = "AND"


@dataclass(kw_only=True)
class Div(BinaryNumericExpression):
    class Meta:
        name = "DIV"


@dataclass(kw_only=True)
class Mod(BinaryNumericExpression):
    class Meta:
        name = "MOD"


@dataclass(kw_only=True)
class Or(NaryBooleanOperator):
    class Meta:
        name = "OR"


@dataclass(kw_only=True)
class Xor(NaryBooleanOperator):
    class Meta:
        name = "XOR"


@dataclass(kw_only=True)
class NaryNumericExpression:
    choice: list[
        Add
        | Sub
        | Mul
        | Div
        | Mod
        | Max
        | Min
        | Sqrt
        | Abs
        | Ceil
        | Floor
        | Round
        | Trunc
        | RealToInt
        | IntegerVariable
        | RealVariable
        | IntegerValue
        | RealValue
        | NodeTimepointValue
        | ArraySize
        | ArrayMaxSize
        | LookupOnChange
        | LookupNow
        | ArrayElement
        | Strlen
    ] = field(
        default_factory=list,
        metadata={
            "type": "Elements",
            "choices": (
                {
                    "name": "ADD",
                    "type": ForwardRef("Add"),
                },
                {
                    "name": "SUB",
                    "type": ForwardRef("Sub"),
                },
                {
                    "name": "MUL",
                    "type": ForwardRef("Mul"),
                },
                {
                    "name": "DIV",
                    "type": Div,
                },
                {
                    "name": "MOD",
                    "type": Mod,
                },
                {
                    "name": "MAX",
                    "type": ForwardRef("Max"),
                },
                {
                    "name": "MIN",
                    "type": ForwardRef("Min"),
                },
                {
                    "name": "SQRT",
                    "type": Sqrt,
                },
                {
                    "name": "ABS",
                    "type": Abs,
                },
                {
                    "name": "CEIL",
                    "type": Ceil,
                },
                {
                    "name": "FLOOR",
                    "type": Floor,
                },
                {
                    "name": "ROUND",
                    "type": Round,
                },
                {
                    "name": "TRUNC",
                    "type": Trunc,
                },
                {
                    "name": "REAL_TO_INT",
                    "type": RealToInt,
                },
                {
                    "name": "IntegerVariable",
                    "type": IntegerVariable,
                },
                {
                    "name": "RealVariable",
                    "type": RealVariable,
                },
                {
                    "name": "IntegerValue",
                    "type": IntegerValue,
                },
                {
                    "name": "RealValue",
                    "type": RealValue,
                },
                {
                    "name": "NodeTimepointValue",
                    "type": NodeTimepointValue,
                },
                {
                    "name": "ArraySize",
                    "type": ForwardRef("ArraySize"),
                },
                {
                    "name": "ArrayMaxSize",
                    "type": ForwardRef("ArrayMaxSize"),
                },
                {
                    "name": "LookupOnChange",
                    "type": ForwardRef("LookupOnChange"),
                },
                {
                    "name": "LookupNow",
                    "type": ForwardRef("LookupNow"),
                },
                {
                    "name": "ArrayElement",
                    "type": ForwardRef("ArrayElement"),
                },
                {
                    "name": "STRLEN",
                    "type": ForwardRef("Strlen"),
                },
            ),
        },
    )
    file_name: None | str = field(
        default=None,
        metadata={
            "name": "FileName",
            "type": "Attribute",
        },
    )
    line_no: None | int = field(
        default=None,
        metadata={
            "name": "LineNo",
            "type": "Attribute",
        },
    )
    col_no: None | int = field(
        default=None,
        metadata={
            "name": "ColNo",
            "type": "Attribute",
        },
    )
    epx: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )


@dataclass(kw_only=True)
class Add(NaryNumericExpression):
    class Meta:
        name = "ADD"


@dataclass(kw_only=True)
class Max(NaryNumericExpression):
    class Meta:
        name = "MAX"


@dataclass(kw_only=True)
class Min(NaryNumericExpression):
    class Meta:
        name = "MIN"


@dataclass(kw_only=True)
class Mul(NaryNumericExpression):
    class Meta:
        name = "MUL"


@dataclass(kw_only=True)
class Sub(NaryNumericExpression):
    class Meta:
        name = "SUB"


@dataclass(kw_only=True)
class ArrayElement:
    choice: None | ArrayValue | ArrayVariable | LookupOnChange | LookupNow | str = (
        field(
            default=None,
            metadata={
                "type": "Elements",
                "choices": (
                    {
                        "name": "ArrayValue",
                        "type": ArrayValue,
                    },
                    {
                        "name": "ArrayVariable",
                        "type": ArrayVariable,
                    },
                    {
                        "name": "LookupOnChange",
                        "type": ForwardRef("LookupOnChange"),
                    },
                    {
                        "name": "LookupNow",
                        "type": ForwardRef("LookupNow"),
                    },
                    {
                        "name": "Name",
                        "type": str,
                        "namespace": "",
                    },
                ),
            },
        )
    )
    index: ArrayElement.Index = field(
        metadata={
            "name": "Index",
            "type": "Element",
            "namespace": "",
        }
    )
    file_name: None | str = field(
        default=None,
        metadata={
            "name": "FileName",
            "type": "Attribute",
        },
    )
    line_no: None | int = field(
        default=None,
        metadata={
            "name": "LineNo",
            "type": "Attribute",
        },
    )
    col_no: None | int = field(
        default=None,
        metadata={
            "name": "ColNo",
            "type": "Attribute",
        },
    )
    epx: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )

    @dataclass(kw_only=True)
    class Index:
        choice: (
            None
            | Add
            | Sub
            | Mul
            | Div
            | Mod
            | Max
            | Min
            | Sqrt
            | Abs
            | Ceil
            | Floor
            | Round
            | Trunc
            | RealToInt
            | IntegerVariable
            | RealVariable
            | IntegerValue
            | RealValue
            | NodeTimepointValue
            | ArraySize
            | ArrayMaxSize
            | LookupOnChange
            | LookupNow
            | ArrayElement
            | Strlen
        ) = field(
            default=None,
            metadata={
                "type": "Elements",
                "choices": (
                    {
                        "name": "ADD",
                        "type": Add,
                    },
                    {
                        "name": "SUB",
                        "type": Sub,
                    },
                    {
                        "name": "MUL",
                        "type": Mul,
                    },
                    {
                        "name": "DIV",
                        "type": Div,
                    },
                    {
                        "name": "MOD",
                        "type": Mod,
                    },
                    {
                        "name": "MAX",
                        "type": Max,
                    },
                    {
                        "name": "MIN",
                        "type": Min,
                    },
                    {
                        "name": "SQRT",
                        "type": Sqrt,
                    },
                    {
                        "name": "ABS",
                        "type": Abs,
                    },
                    {
                        "name": "CEIL",
                        "type": Ceil,
                    },
                    {
                        "name": "FLOOR",
                        "type": Floor,
                    },
                    {
                        "name": "ROUND",
                        "type": Round,
                    },
                    {
                        "name": "TRUNC",
                        "type": Trunc,
                    },
                    {
                        "name": "REAL_TO_INT",
                        "type": RealToInt,
                    },
                    {
                        "name": "IntegerVariable",
                        "type": IntegerVariable,
                    },
                    {
                        "name": "RealVariable",
                        "type": RealVariable,
                    },
                    {
                        "name": "IntegerValue",
                        "type": IntegerValue,
                    },
                    {
                        "name": "RealValue",
                        "type": RealValue,
                    },
                    {
                        "name": "NodeTimepointValue",
                        "type": NodeTimepointValue,
                    },
                    {
                        "name": "ArraySize",
                        "type": ArraySize,
                    },
                    {
                        "name": "ArrayMaxSize",
                        "type": ArrayMaxSize,
                    },
                    {
                        "name": "LookupOnChange",
                        "type": ForwardRef("LookupOnChange"),
                    },
                    {
                        "name": "LookupNow",
                        "type": ForwardRef("LookupNow"),
                    },
                    {
                        "name": "ArrayElement",
                        "type": ForwardRef("ArrayElement"),
                    },
                    {
                        "name": "STRLEN",
                        "type": Strlen,
                    },
                ),
            },
        )
        file_name: None | str = field(
            default=None,
            metadata={
                "name": "FileName",
                "type": "Attribute",
            },
        )
        line_no: None | int = field(
            default=None,
            metadata={
                "name": "LineNo",
                "type": "Attribute",
            },
        )
        col_no: None | int = field(
            default=None,
            metadata={
                "name": "ColNo",
                "type": "Attribute",
            },
        )
        epx: None | str = field(
            default=None,
            metadata={
                "type": "Attribute",
            },
        )


@dataclass(kw_only=True)
class IsKnown:
    choice: (
        None
        | BooleanVariable
        | BooleanValue
        | Or
        | Xor
        | And
        | Not
        | Eqboolean
        | Eqnumeric
        | Eqinternal
        | Eqstring
        | Eqarray
        | Neboolean
        | Nenumeric
        | Neinternal
        | Nestring
        | Nearray
        | Gt
        | Ge
        | Lt
        | Le
        | IsKnown
        | AllKnown
        | AnyKnown
        | Executing
        | Finished
        | Inactive
        | IterationEnded
        | Waiting
        | NoChildFailed
        | Failed
        | Skipped
        | Succeeded
        | PostconditionFailed
        | Add
        | Sub
        | Mul
        | Div
        | Mod
        | Max
        | Min
        | Sqrt
        | Abs
        | Ceil
        | Floor
        | Round
        | Trunc
        | RealToInt
        | IntegerVariable
        | RealVariable
        | IntegerValue
        | RealValue
        | NodeTimepointValue
        | ArraySize
        | ArrayMaxSize
        | StringVariable
        | StringValue
        | Concat
        | ArrayValue
        | ArrayVariable
        | LookupOnChange
        | LookupNow
        | ArrayElement
        | NodeStateVariable
        | NodeOutcomeVariable
        | NodeCommandHandleVariable
    ) = field(
        default=None,
        metadata={
            "type": "Elements",
            "choices": (
                {
                    "name": "BooleanVariable",
                    "type": BooleanVariable,
                },
                {
                    "name": "BooleanValue",
                    "type": BooleanValue,
                },
                {
                    "name": "OR",
                    "type": Or,
                },
                {
                    "name": "XOR",
                    "type": Xor,
                },
                {
                    "name": "AND",
                    "type": And,
                },
                {
                    "name": "NOT",
                    "type": ForwardRef("Not"),
                },
                {
                    "name": "EQBoolean",
                    "type": ForwardRef("Eqboolean"),
                },
                {
                    "name": "EQNumeric",
                    "type": Eqnumeric,
                },
                {
                    "name": "EQInternal",
                    "type": Eqinternal,
                },
                {
                    "name": "EQString",
                    "type": ForwardRef("Eqstring"),
                },
                {
                    "name": "EQArray",
                    "type": ForwardRef("Eqarray"),
                },
                {
                    "name": "NEBoolean",
                    "type": ForwardRef("Neboolean"),
                },
                {
                    "name": "NENumeric",
                    "type": Nenumeric,
                },
                {
                    "name": "NEInternal",
                    "type": Neinternal,
                },
                {
                    "name": "NEString",
                    "type": ForwardRef("Nestring"),
                },
                {
                    "name": "NEArray",
                    "type": ForwardRef("Nearray"),
                },
                {
                    "name": "GT",
                    "type": Gt,
                },
                {
                    "name": "GE",
                    "type": Ge,
                },
                {
                    "name": "LT",
                    "type": Lt,
                },
                {
                    "name": "LE",
                    "type": Le,
                },
                {
                    "name": "IsKnown",
                    "type": ForwardRef("IsKnown"),
                },
                {
                    "name": "ALL_KNOWN",
                    "type": ForwardRef("AllKnown"),
                },
                {
                    "name": "ANY_KNOWN",
                    "type": ForwardRef("AnyKnown"),
                },
                {
                    "name": "Executing",
                    "type": Executing,
                },
                {
                    "name": "Finished",
                    "type": Finished,
                },
                {
                    "name": "Inactive",
                    "type": Inactive,
                },
                {
                    "name": "IterationEnded",
                    "type": IterationEnded,
                },
                {
                    "name": "Waiting",
                    "type": Waiting,
                },
                {
                    "name": "NoChildFailed",
                    "type": NoChildFailed,
                },
                {
                    "name": "Failed",
                    "type": Failed,
                },
                {
                    "name": "Skipped",
                    "type": Skipped,
                },
                {
                    "name": "Succeeded",
                    "type": Succeeded,
                },
                {
                    "name": "PostconditionFailed",
                    "type": PostconditionFailed,
                },
                {
                    "name": "ADD",
                    "type": Add,
                },
                {
                    "name": "SUB",
                    "type": Sub,
                },
                {
                    "name": "MUL",
                    "type": Mul,
                },
                {
                    "name": "DIV",
                    "type": Div,
                },
                {
                    "name": "MOD",
                    "type": Mod,
                },
                {
                    "name": "MAX",
                    "type": Max,
                },
                {
                    "name": "MIN",
                    "type": Min,
                },
                {
                    "name": "SQRT",
                    "type": Sqrt,
                },
                {
                    "name": "ABS",
                    "type": Abs,
                },
                {
                    "name": "CEIL",
                    "type": Ceil,
                },
                {
                    "name": "FLOOR",
                    "type": Floor,
                },
                {
                    "name": "ROUND",
                    "type": Round,
                },
                {
                    "name": "TRUNC",
                    "type": Trunc,
                },
                {
                    "name": "REAL_TO_INT",
                    "type": RealToInt,
                },
                {
                    "name": "IntegerVariable",
                    "type": IntegerVariable,
                },
                {
                    "name": "RealVariable",
                    "type": RealVariable,
                },
                {
                    "name": "IntegerValue",
                    "type": IntegerValue,
                },
                {
                    "name": "RealValue",
                    "type": RealValue,
                },
                {
                    "name": "NodeTimepointValue",
                    "type": NodeTimepointValue,
                },
                {
                    "name": "ArraySize",
                    "type": ArraySize,
                },
                {
                    "name": "ArrayMaxSize",
                    "type": ArrayMaxSize,
                },
                {
                    "name": "StringVariable",
                    "type": StringVariable,
                },
                {
                    "name": "StringValue",
                    "type": StringValue,
                },
                {
                    "name": "Concat",
                    "type": ForwardRef("Concat"),
                },
                {
                    "name": "ArrayValue",
                    "type": ArrayValue,
                },
                {
                    "name": "ArrayVariable",
                    "type": ArrayVariable,
                },
                {
                    "name": "LookupOnChange",
                    "type": ForwardRef("LookupOnChange"),
                },
                {
                    "name": "LookupNow",
                    "type": ForwardRef("LookupNow"),
                },
                {
                    "name": "ArrayElement",
                    "type": ForwardRef("ArrayElement"),
                },
                {
                    "name": "NodeStateVariable",
                    "type": NodeStateVariable,
                },
                {
                    "name": "NodeOutcomeVariable",
                    "type": NodeOutcomeVariable,
                },
                {
                    "name": "NodeCommandHandleVariable",
                    "type": NodeCommandHandleVariable,
                },
            ),
        },
    )
    file_name: None | str = field(
        default=None,
        metadata={
            "name": "FileName",
            "type": "Attribute",
        },
    )
    line_no: None | int = field(
        default=None,
        metadata={
            "name": "LineNo",
            "type": "Attribute",
        },
    )
    col_no: None | int = field(
        default=None,
        metadata={
            "name": "ColNo",
            "type": "Attribute",
        },
    )
    epx: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )


@dataclass(kw_only=True)
class DeclareVariable:
    name: str = field(
        metadata={
            "name": "Name",
            "type": "Element",
            "namespace": "",
        }
    )
    type_value: AtomicTypeValues = field(
        metadata={
            "name": "Type",
            "type": "Element",
            "namespace": "",
        }
    )
    initial_value: None | DeclareVariable.InitialValue = field(
        default=None,
        metadata={
            "name": "InitialValue",
            "type": "Element",
            "namespace": "",
        },
    )
    file_name: None | str = field(
        default=None,
        metadata={
            "name": "FileName",
            "type": "Attribute",
        },
    )
    line_no: None | int = field(
        default=None,
        metadata={
            "name": "LineNo",
            "type": "Attribute",
        },
    )
    col_no: None | int = field(
        default=None,
        metadata={
            "name": "ColNo",
            "type": "Attribute",
        },
    )
    epx: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )

    @dataclass(kw_only=True)
    class InitialValue:
        choice: (
            None
            | IntegerVariable
            | RealVariable
            | BooleanVariable
            | StringVariable
            | ArrayVariable
            | ArrayElement
            | IntegerValue
            | RealValue
            | BooleanValue
            | StringValue
        ) = field(
            default=None,
            metadata={
                "type": "Elements",
                "choices": (
                    {
                        "name": "IntegerVariable",
                        "type": IntegerVariable,
                    },
                    {
                        "name": "RealVariable",
                        "type": RealVariable,
                    },
                    {
                        "name": "BooleanVariable",
                        "type": BooleanVariable,
                    },
                    {
                        "name": "StringVariable",
                        "type": StringVariable,
                    },
                    {
                        "name": "ArrayVariable",
                        "type": ArrayVariable,
                    },
                    {
                        "name": "ArrayElement",
                        "type": ArrayElement,
                    },
                    {
                        "name": "IntegerValue",
                        "type": IntegerValue,
                    },
                    {
                        "name": "RealValue",
                        "type": RealValue,
                    },
                    {
                        "name": "BooleanValue",
                        "type": BooleanValue,
                    },
                    {
                        "name": "StringValue",
                        "type": StringValue,
                    },
                ),
            },
        )
        file_name: None | str = field(
            default=None,
            metadata={
                "name": "FileName",
                "type": "Attribute",
            },
        )
        line_no: None | int = field(
            default=None,
            metadata={
                "name": "LineNo",
                "type": "Attribute",
            },
        )
        col_no: None | int = field(
            default=None,
            metadata={
                "name": "ColNo",
                "type": "Attribute",
            },
        )
        epx: None | str = field(
            default=None,
            metadata={
                "type": "Attribute",
            },
        )


@dataclass(kw_only=True)
class Not:
    class Meta:
        name = "NOT"

    choice: (
        None
        | BooleanVariable
        | BooleanValue
        | Or
        | Xor
        | And
        | Not
        | Eqboolean
        | Eqnumeric
        | Eqinternal
        | Eqstring
        | Eqarray
        | Neboolean
        | Nenumeric
        | Neinternal
        | Nestring
        | Nearray
        | Gt
        | Ge
        | Lt
        | Le
        | IsKnown
        | AllKnown
        | AnyKnown
        | Executing
        | Finished
        | Inactive
        | IterationEnded
        | Waiting
        | NoChildFailed
        | Failed
        | Skipped
        | Succeeded
        | PostconditionFailed
        | LookupOnChange
        | LookupNow
        | ArrayElement
    ) = field(
        default=None,
        metadata={
            "type": "Elements",
            "choices": (
                {
                    "name": "BooleanVariable",
                    "type": BooleanVariable,
                },
                {
                    "name": "BooleanValue",
                    "type": BooleanValue,
                },
                {
                    "name": "OR",
                    "type": Or,
                },
                {
                    "name": "XOR",
                    "type": Xor,
                },
                {
                    "name": "AND",
                    "type": And,
                },
                {
                    "name": "NOT",
                    "type": ForwardRef("Not"),
                },
                {
                    "name": "EQBoolean",
                    "type": ForwardRef("Eqboolean"),
                },
                {
                    "name": "EQNumeric",
                    "type": Eqnumeric,
                },
                {
                    "name": "EQInternal",
                    "type": Eqinternal,
                },
                {
                    "name": "EQString",
                    "type": ForwardRef("Eqstring"),
                },
                {
                    "name": "EQArray",
                    "type": ForwardRef("Eqarray"),
                },
                {
                    "name": "NEBoolean",
                    "type": ForwardRef("Neboolean"),
                },
                {
                    "name": "NENumeric",
                    "type": Nenumeric,
                },
                {
                    "name": "NEInternal",
                    "type": Neinternal,
                },
                {
                    "name": "NEString",
                    "type": ForwardRef("Nestring"),
                },
                {
                    "name": "NEArray",
                    "type": ForwardRef("Nearray"),
                },
                {
                    "name": "GT",
                    "type": Gt,
                },
                {
                    "name": "GE",
                    "type": Ge,
                },
                {
                    "name": "LT",
                    "type": Lt,
                },
                {
                    "name": "LE",
                    "type": Le,
                },
                {
                    "name": "IsKnown",
                    "type": IsKnown,
                },
                {
                    "name": "ALL_KNOWN",
                    "type": AllKnown,
                },
                {
                    "name": "ANY_KNOWN",
                    "type": AnyKnown,
                },
                {
                    "name": "Executing",
                    "type": Executing,
                },
                {
                    "name": "Finished",
                    "type": Finished,
                },
                {
                    "name": "Inactive",
                    "type": Inactive,
                },
                {
                    "name": "IterationEnded",
                    "type": IterationEnded,
                },
                {
                    "name": "Waiting",
                    "type": Waiting,
                },
                {
                    "name": "NoChildFailed",
                    "type": NoChildFailed,
                },
                {
                    "name": "Failed",
                    "type": Failed,
                },
                {
                    "name": "Skipped",
                    "type": Skipped,
                },
                {
                    "name": "Succeeded",
                    "type": Succeeded,
                },
                {
                    "name": "PostconditionFailed",
                    "type": PostconditionFailed,
                },
                {
                    "name": "LookupOnChange",
                    "type": ForwardRef("LookupOnChange"),
                },
                {
                    "name": "LookupNow",
                    "type": ForwardRef("LookupNow"),
                },
                {
                    "name": "ArrayElement",
                    "type": ForwardRef("ArrayElement"),
                },
            ),
        },
    )
    file_name: None | str = field(
        default=None,
        metadata={
            "name": "FileName",
            "type": "Attribute",
        },
    )
    line_no: None | int = field(
        default=None,
        metadata={
            "name": "LineNo",
            "type": "Attribute",
        },
    )
    col_no: None | int = field(
        default=None,
        metadata={
            "name": "ColNo",
            "type": "Attribute",
        },
    )
    epx: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )


@dataclass(kw_only=True)
class Name:
    choice: (
        None
        | StringVariable
        | StringValue
        | Concat
        | LookupOnChange
        | LookupNow
        | ArrayElement
    ) = field(
        default=None,
        metadata={
            "type": "Elements",
            "choices": (
                {
                    "name": "StringVariable",
                    "type": StringVariable,
                },
                {
                    "name": "StringValue",
                    "type": StringValue,
                },
                {
                    "name": "Concat",
                    "type": Concat,
                },
                {
                    "name": "LookupOnChange",
                    "type": LookupOnChange,
                },
                {
                    "name": "LookupNow",
                    "type": LookupNow,
                },
                {
                    "name": "ArrayElement",
                    "type": ArrayElement,
                },
            ),
        },
    )
    file_name: None | str = field(
        default=None,
        metadata={
            "name": "FileName",
            "type": "Attribute",
        },
    )
    line_no: None | int = field(
        default=None,
        metadata={
            "name": "LineNo",
            "type": "Attribute",
        },
    )
    col_no: None | int = field(
        default=None,
        metadata={
            "name": "ColNo",
            "type": "Attribute",
        },
    )
    epx: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )


@dataclass(kw_only=True)
class NumericRhs:
    class Meta:
        name = "NumericRHS"

    choice: (
        None
        | Add
        | Sub
        | Mul
        | Div
        | Mod
        | Max
        | Min
        | Sqrt
        | Abs
        | Ceil
        | Floor
        | Round
        | Trunc
        | RealToInt
        | IntegerVariable
        | RealVariable
        | IntegerValue
        | RealValue
        | NodeTimepointValue
        | ArraySize
        | ArrayMaxSize
        | LookupOnChange
        | LookupNow
        | ArrayElement
        | Strlen
    ) = field(
        default=None,
        metadata={
            "type": "Elements",
            "choices": (
                {
                    "name": "ADD",
                    "type": Add,
                },
                {
                    "name": "SUB",
                    "type": Sub,
                },
                {
                    "name": "MUL",
                    "type": Mul,
                },
                {
                    "name": "DIV",
                    "type": Div,
                },
                {
                    "name": "MOD",
                    "type": Mod,
                },
                {
                    "name": "MAX",
                    "type": Max,
                },
                {
                    "name": "MIN",
                    "type": Min,
                },
                {
                    "name": "SQRT",
                    "type": Sqrt,
                },
                {
                    "name": "ABS",
                    "type": Abs,
                },
                {
                    "name": "CEIL",
                    "type": Ceil,
                },
                {
                    "name": "FLOOR",
                    "type": Floor,
                },
                {
                    "name": "ROUND",
                    "type": Round,
                },
                {
                    "name": "TRUNC",
                    "type": Trunc,
                },
                {
                    "name": "REAL_TO_INT",
                    "type": RealToInt,
                },
                {
                    "name": "IntegerVariable",
                    "type": IntegerVariable,
                },
                {
                    "name": "RealVariable",
                    "type": RealVariable,
                },
                {
                    "name": "IntegerValue",
                    "type": IntegerValue,
                },
                {
                    "name": "RealValue",
                    "type": RealValue,
                },
                {
                    "name": "NodeTimepointValue",
                    "type": NodeTimepointValue,
                },
                {
                    "name": "ArraySize",
                    "type": ArraySize,
                },
                {
                    "name": "ArrayMaxSize",
                    "type": ArrayMaxSize,
                },
                {
                    "name": "LookupOnChange",
                    "type": LookupOnChange,
                },
                {
                    "name": "LookupNow",
                    "type": LookupNow,
                },
                {
                    "name": "ArrayElement",
                    "type": ArrayElement,
                },
                {
                    "name": "STRLEN",
                    "type": Strlen,
                },
            ),
        },
    )
    file_name: None | str = field(
        default=None,
        metadata={
            "name": "FileName",
            "type": "Attribute",
        },
    )
    line_no: None | int = field(
        default=None,
        metadata={
            "name": "LineNo",
            "type": "Attribute",
        },
    )
    col_no: None | int = field(
        default=None,
        metadata={
            "name": "ColNo",
            "type": "Attribute",
        },
    )
    epx: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )


@dataclass(kw_only=True)
class StringRhs:
    class Meta:
        name = "StringRHS"

    choice: (
        None
        | StringVariable
        | StringValue
        | Concat
        | LookupOnChange
        | LookupNow
        | ArrayElement
    ) = field(
        default=None,
        metadata={
            "type": "Elements",
            "choices": (
                {
                    "name": "StringVariable",
                    "type": StringVariable,
                },
                {
                    "name": "StringValue",
                    "type": StringValue,
                },
                {
                    "name": "Concat",
                    "type": Concat,
                },
                {
                    "name": "LookupOnChange",
                    "type": LookupOnChange,
                },
                {
                    "name": "LookupNow",
                    "type": LookupNow,
                },
                {
                    "name": "ArrayElement",
                    "type": ArrayElement,
                },
            ),
        },
    )
    file_name: None | str = field(
        default=None,
        metadata={
            "name": "FileName",
            "type": "Attribute",
        },
    )
    line_no: None | int = field(
        default=None,
        metadata={
            "name": "LineNo",
            "type": "Attribute",
        },
    )
    col_no: None | int = field(
        default=None,
        metadata={
            "name": "ColNo",
            "type": "Attribute",
        },
    )
    epx: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )


@dataclass(kw_only=True)
class Tolerance:
    choice: (
        None
        | Add
        | Sub
        | Mul
        | Div
        | Mod
        | Max
        | Min
        | Sqrt
        | Abs
        | Ceil
        | Floor
        | Round
        | Trunc
        | RealToInt
        | IntegerVariable
        | RealVariable
        | IntegerValue
        | RealValue
        | NodeTimepointValue
        | ArraySize
        | ArrayMaxSize
        | LookupOnChange
        | LookupNow
        | ArrayElement
        | Strlen
    ) = field(
        default=None,
        metadata={
            "type": "Elements",
            "choices": (
                {
                    "name": "ADD",
                    "type": Add,
                },
                {
                    "name": "SUB",
                    "type": Sub,
                },
                {
                    "name": "MUL",
                    "type": Mul,
                },
                {
                    "name": "DIV",
                    "type": Div,
                },
                {
                    "name": "MOD",
                    "type": Mod,
                },
                {
                    "name": "MAX",
                    "type": Max,
                },
                {
                    "name": "MIN",
                    "type": Min,
                },
                {
                    "name": "SQRT",
                    "type": Sqrt,
                },
                {
                    "name": "ABS",
                    "type": Abs,
                },
                {
                    "name": "CEIL",
                    "type": Ceil,
                },
                {
                    "name": "FLOOR",
                    "type": Floor,
                },
                {
                    "name": "ROUND",
                    "type": Round,
                },
                {
                    "name": "TRUNC",
                    "type": Trunc,
                },
                {
                    "name": "REAL_TO_INT",
                    "type": RealToInt,
                },
                {
                    "name": "IntegerVariable",
                    "type": IntegerVariable,
                },
                {
                    "name": "RealVariable",
                    "type": RealVariable,
                },
                {
                    "name": "IntegerValue",
                    "type": IntegerValue,
                },
                {
                    "name": "RealValue",
                    "type": RealValue,
                },
                {
                    "name": "NodeTimepointValue",
                    "type": NodeTimepointValue,
                },
                {
                    "name": "ArraySize",
                    "type": ArraySize,
                },
                {
                    "name": "ArrayMaxSize",
                    "type": ArrayMaxSize,
                },
                {
                    "name": "LookupOnChange",
                    "type": LookupOnChange,
                },
                {
                    "name": "LookupNow",
                    "type": LookupNow,
                },
                {
                    "name": "ArrayElement",
                    "type": ArrayElement,
                },
                {
                    "name": "STRLEN",
                    "type": Strlen,
                },
            ),
        },
    )
    file_name: None | str = field(
        default=None,
        metadata={
            "name": "FileName",
            "type": "Attribute",
        },
    )
    line_no: None | int = field(
        default=None,
        metadata={
            "name": "LineNo",
            "type": "Attribute",
        },
    )
    col_no: None | int = field(
        default=None,
        metadata={
            "name": "ColNo",
            "type": "Attribute",
        },
    )
    epx: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )


@dataclass(kw_only=True)
class Eqboolean:
    class Meta:
        name = "EQBoolean"

    choice: list[
        BooleanVariable
        | BooleanValue
        | Or
        | Xor
        | And
        | Not
        | Eqboolean
        | Eqnumeric
        | Eqinternal
        | Eqstring
        | Eqarray
        | Neboolean
        | Nenumeric
        | Neinternal
        | Nestring
        | Nearray
        | Gt
        | Ge
        | Lt
        | Le
        | IsKnown
        | AllKnown
        | AnyKnown
        | Executing
        | Finished
        | Inactive
        | IterationEnded
        | Waiting
        | NoChildFailed
        | Failed
        | Skipped
        | Succeeded
        | PostconditionFailed
        | LookupOnChange
        | LookupNow
        | ArrayElement
    ] = field(
        default_factory=list,
        metadata={
            "type": "Elements",
            "choices": (
                {
                    "name": "BooleanVariable",
                    "type": BooleanVariable,
                    "max_occurs": 2,
                },
                {
                    "name": "BooleanValue",
                    "type": BooleanValue,
                    "max_occurs": 2,
                },
                {
                    "name": "OR",
                    "type": Or,
                    "max_occurs": 2,
                },
                {
                    "name": "XOR",
                    "type": Xor,
                    "max_occurs": 2,
                },
                {
                    "name": "AND",
                    "type": And,
                    "max_occurs": 2,
                },
                {
                    "name": "NOT",
                    "type": Not,
                    "max_occurs": 2,
                },
                {
                    "name": "EQBoolean",
                    "type": ForwardRef("Eqboolean"),
                    "max_occurs": 2,
                },
                {
                    "name": "EQNumeric",
                    "type": Eqnumeric,
                    "max_occurs": 2,
                },
                {
                    "name": "EQInternal",
                    "type": Eqinternal,
                    "max_occurs": 2,
                },
                {
                    "name": "EQString",
                    "type": ForwardRef("Eqstring"),
                    "max_occurs": 2,
                },
                {
                    "name": "EQArray",
                    "type": ForwardRef("Eqarray"),
                    "max_occurs": 2,
                },
                {
                    "name": "NEBoolean",
                    "type": ForwardRef("Neboolean"),
                    "max_occurs": 2,
                },
                {
                    "name": "NENumeric",
                    "type": Nenumeric,
                    "max_occurs": 2,
                },
                {
                    "name": "NEInternal",
                    "type": Neinternal,
                    "max_occurs": 2,
                },
                {
                    "name": "NEString",
                    "type": ForwardRef("Nestring"),
                    "max_occurs": 2,
                },
                {
                    "name": "NEArray",
                    "type": ForwardRef("Nearray"),
                    "max_occurs": 2,
                },
                {
                    "name": "GT",
                    "type": Gt,
                    "max_occurs": 2,
                },
                {
                    "name": "GE",
                    "type": Ge,
                    "max_occurs": 2,
                },
                {
                    "name": "LT",
                    "type": Lt,
                    "max_occurs": 2,
                },
                {
                    "name": "LE",
                    "type": Le,
                    "max_occurs": 2,
                },
                {
                    "name": "IsKnown",
                    "type": IsKnown,
                    "max_occurs": 2,
                },
                {
                    "name": "ALL_KNOWN",
                    "type": AllKnown,
                    "max_occurs": 2,
                },
                {
                    "name": "ANY_KNOWN",
                    "type": AnyKnown,
                    "max_occurs": 2,
                },
                {
                    "name": "Executing",
                    "type": Executing,
                    "max_occurs": 2,
                },
                {
                    "name": "Finished",
                    "type": Finished,
                    "max_occurs": 2,
                },
                {
                    "name": "Inactive",
                    "type": Inactive,
                    "max_occurs": 2,
                },
                {
                    "name": "IterationEnded",
                    "type": IterationEnded,
                    "max_occurs": 2,
                },
                {
                    "name": "Waiting",
                    "type": Waiting,
                    "max_occurs": 2,
                },
                {
                    "name": "NoChildFailed",
                    "type": NoChildFailed,
                    "max_occurs": 2,
                },
                {
                    "name": "Failed",
                    "type": Failed,
                    "max_occurs": 2,
                },
                {
                    "name": "Skipped",
                    "type": Skipped,
                    "max_occurs": 2,
                },
                {
                    "name": "Succeeded",
                    "type": Succeeded,
                    "max_occurs": 2,
                },
                {
                    "name": "PostconditionFailed",
                    "type": PostconditionFailed,
                    "max_occurs": 2,
                },
                {
                    "name": "LookupOnChange",
                    "type": ForwardRef("LookupOnChange"),
                    "max_occurs": 2,
                },
                {
                    "name": "LookupNow",
                    "type": ForwardRef("LookupNow"),
                    "max_occurs": 2,
                },
                {
                    "name": "ArrayElement",
                    "type": ForwardRef("ArrayElement"),
                    "max_occurs": 2,
                },
            ),
            "max_occurs": 2,
        },
    )
    file_name: None | str = field(
        default=None,
        metadata={
            "name": "FileName",
            "type": "Attribute",
        },
    )
    line_no: None | int = field(
        default=None,
        metadata={
            "name": "LineNo",
            "type": "Attribute",
        },
    )
    col_no: None | int = field(
        default=None,
        metadata={
            "name": "ColNo",
            "type": "Attribute",
        },
    )
    epx: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )


@dataclass(kw_only=True)
class In:
    declare_variable_or_declare_array: list[DeclareVariable | DeclareArray] = field(
        default_factory=list,
        metadata={
            "type": "Elements",
            "choices": (
                {
                    "name": "DeclareVariable",
                    "type": DeclareVariable,
                },
                {
                    "name": "DeclareArray",
                    "type": DeclareArray,
                },
            ),
        },
    )
    file_name: None | str = field(
        default=None,
        metadata={
            "name": "FileName",
            "type": "Attribute",
        },
    )
    line_no: None | int = field(
        default=None,
        metadata={
            "name": "LineNo",
            "type": "Attribute",
        },
    )
    col_no: None | int = field(
        default=None,
        metadata={
            "name": "ColNo",
            "type": "Attribute",
        },
    )
    epx: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )


@dataclass(kw_only=True)
class InOut:
    declare_variable_or_declare_array: list[DeclareVariable | DeclareArray] = field(
        default_factory=list,
        metadata={
            "type": "Elements",
            "choices": (
                {
                    "name": "DeclareVariable",
                    "type": DeclareVariable,
                },
                {
                    "name": "DeclareArray",
                    "type": DeclareArray,
                },
            ),
        },
    )
    file_name: None | str = field(
        default=None,
        metadata={
            "name": "FileName",
            "type": "Attribute",
        },
    )
    line_no: None | int = field(
        default=None,
        metadata={
            "name": "LineNo",
            "type": "Attribute",
        },
    )
    col_no: None | int = field(
        default=None,
        metadata={
            "name": "ColNo",
            "type": "Attribute",
        },
    )
    epx: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )


@dataclass(kw_only=True)
class VariableDeclarations:
    declare_variable_or_declare_array_or_declare_mutex: list[
        DeclareVariable | DeclareArray | DeclareMutex
    ] = field(
        default_factory=list,
        metadata={
            "type": "Elements",
            "choices": (
                {
                    "name": "DeclareVariable",
                    "type": DeclareVariable,
                },
                {
                    "name": "DeclareArray",
                    "type": DeclareArray,
                },
                {
                    "name": "DeclareMutex",
                    "type": DeclareMutex,
                },
            ),
        },
    )
    file_name: None | str = field(
        default=None,
        metadata={
            "name": "FileName",
            "type": "Attribute",
        },
    )
    line_no: None | int = field(
        default=None,
        metadata={
            "name": "LineNo",
            "type": "Attribute",
        },
    )
    col_no: None | int = field(
        default=None,
        metadata={
            "name": "ColNo",
            "type": "Attribute",
        },
    )
    epx: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )


@dataclass(kw_only=True)
class Interface:
    in_value: None | In = field(
        default=None,
        metadata={
            "name": "In",
            "type": "Element",
        },
    )
    in_out: None | InOut = field(
        default=None,
        metadata={
            "name": "InOut",
            "type": "Element",
        },
    )
    file_name: None | str = field(
        default=None,
        metadata={
            "name": "FileName",
            "type": "Attribute",
        },
    )
    line_no: None | int = field(
        default=None,
        metadata={
            "name": "LineNo",
            "type": "Attribute",
        },
    )
    col_no: None | int = field(
        default=None,
        metadata={
            "name": "ColNo",
            "type": "Attribute",
        },
    )
    epx: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )


@dataclass(kw_only=True)
class Neboolean:
    class Meta:
        name = "NEBoolean"

    choice: list[
        BooleanVariable
        | BooleanValue
        | Or
        | Xor
        | And
        | Not
        | Eqboolean
        | Eqnumeric
        | Eqinternal
        | Eqstring
        | Eqarray
        | Neboolean
        | Nenumeric
        | Neinternal
        | Nestring
        | Nearray
        | Gt
        | Ge
        | Lt
        | Le
        | IsKnown
        | AllKnown
        | AnyKnown
        | Executing
        | Finished
        | Inactive
        | IterationEnded
        | Waiting
        | NoChildFailed
        | Failed
        | Skipped
        | Succeeded
        | PostconditionFailed
        | LookupOnChange
        | LookupNow
        | ArrayElement
    ] = field(
        default_factory=list,
        metadata={
            "type": "Elements",
            "choices": (
                {
                    "name": "BooleanVariable",
                    "type": BooleanVariable,
                    "max_occurs": 2,
                },
                {
                    "name": "BooleanValue",
                    "type": BooleanValue,
                    "max_occurs": 2,
                },
                {
                    "name": "OR",
                    "type": Or,
                    "max_occurs": 2,
                },
                {
                    "name": "XOR",
                    "type": Xor,
                    "max_occurs": 2,
                },
                {
                    "name": "AND",
                    "type": And,
                    "max_occurs": 2,
                },
                {
                    "name": "NOT",
                    "type": Not,
                    "max_occurs": 2,
                },
                {
                    "name": "EQBoolean",
                    "type": Eqboolean,
                    "max_occurs": 2,
                },
                {
                    "name": "EQNumeric",
                    "type": Eqnumeric,
                    "max_occurs": 2,
                },
                {
                    "name": "EQInternal",
                    "type": Eqinternal,
                    "max_occurs": 2,
                },
                {
                    "name": "EQString",
                    "type": Eqstring,
                    "max_occurs": 2,
                },
                {
                    "name": "EQArray",
                    "type": Eqarray,
                    "max_occurs": 2,
                },
                {
                    "name": "NEBoolean",
                    "type": ForwardRef("Neboolean"),
                    "max_occurs": 2,
                },
                {
                    "name": "NENumeric",
                    "type": Nenumeric,
                    "max_occurs": 2,
                },
                {
                    "name": "NEInternal",
                    "type": Neinternal,
                    "max_occurs": 2,
                },
                {
                    "name": "NEString",
                    "type": ForwardRef("Nestring"),
                    "max_occurs": 2,
                },
                {
                    "name": "NEArray",
                    "type": ForwardRef("Nearray"),
                    "max_occurs": 2,
                },
                {
                    "name": "GT",
                    "type": Gt,
                    "max_occurs": 2,
                },
                {
                    "name": "GE",
                    "type": Ge,
                    "max_occurs": 2,
                },
                {
                    "name": "LT",
                    "type": Lt,
                    "max_occurs": 2,
                },
                {
                    "name": "LE",
                    "type": Le,
                    "max_occurs": 2,
                },
                {
                    "name": "IsKnown",
                    "type": IsKnown,
                    "max_occurs": 2,
                },
                {
                    "name": "ALL_KNOWN",
                    "type": AllKnown,
                    "max_occurs": 2,
                },
                {
                    "name": "ANY_KNOWN",
                    "type": AnyKnown,
                    "max_occurs": 2,
                },
                {
                    "name": "Executing",
                    "type": Executing,
                    "max_occurs": 2,
                },
                {
                    "name": "Finished",
                    "type": Finished,
                    "max_occurs": 2,
                },
                {
                    "name": "Inactive",
                    "type": Inactive,
                    "max_occurs": 2,
                },
                {
                    "name": "IterationEnded",
                    "type": IterationEnded,
                    "max_occurs": 2,
                },
                {
                    "name": "Waiting",
                    "type": Waiting,
                    "max_occurs": 2,
                },
                {
                    "name": "NoChildFailed",
                    "type": NoChildFailed,
                    "max_occurs": 2,
                },
                {
                    "name": "Failed",
                    "type": Failed,
                    "max_occurs": 2,
                },
                {
                    "name": "Skipped",
                    "type": Skipped,
                    "max_occurs": 2,
                },
                {
                    "name": "Succeeded",
                    "type": Succeeded,
                    "max_occurs": 2,
                },
                {
                    "name": "PostconditionFailed",
                    "type": PostconditionFailed,
                    "max_occurs": 2,
                },
                {
                    "name": "LookupOnChange",
                    "type": ForwardRef("LookupOnChange"),
                    "max_occurs": 2,
                },
                {
                    "name": "LookupNow",
                    "type": ForwardRef("LookupNow"),
                    "max_occurs": 2,
                },
                {
                    "name": "ArrayElement",
                    "type": ForwardRef("ArrayElement"),
                    "max_occurs": 2,
                },
            ),
            "max_occurs": 2,
        },
    )
    file_name: None | str = field(
        default=None,
        metadata={
            "name": "FileName",
            "type": "Attribute",
        },
    )
    line_no: None | int = field(
        default=None,
        metadata={
            "name": "LineNo",
            "type": "Attribute",
        },
    )
    col_no: None | int = field(
        default=None,
        metadata={
            "name": "ColNo",
            "type": "Attribute",
        },
    )
    epx: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )


@dataclass(kw_only=True)
class Arguments:
    choice: list[
        BooleanVariable
        | BooleanValue
        | Or
        | Xor
        | And
        | Not
        | Eqboolean
        | Eqnumeric
        | Eqinternal
        | Eqstring
        | Eqarray
        | Neboolean
        | Nenumeric
        | Neinternal
        | Nestring
        | Nearray
        | Gt
        | Ge
        | Lt
        | Le
        | IsKnown
        | AllKnown
        | AnyKnown
        | Executing
        | Finished
        | Inactive
        | IterationEnded
        | Waiting
        | NoChildFailed
        | Failed
        | Skipped
        | Succeeded
        | PostconditionFailed
        | Add
        | Sub
        | Mul
        | Div
        | Mod
        | Max
        | Min
        | Sqrt
        | Abs
        | Ceil
        | Floor
        | Round
        | Trunc
        | RealToInt
        | IntegerVariable
        | RealVariable
        | IntegerValue
        | RealValue
        | NodeTimepointValue
        | ArraySize
        | ArrayMaxSize
        | StringVariable
        | StringValue
        | Concat
        | ArrayValue
        | ArrayVariable
        | LookupOnChange
        | LookupNow
        | ArrayElement
    ] = field(
        default_factory=list,
        metadata={
            "type": "Elements",
            "choices": (
                {
                    "name": "BooleanVariable",
                    "type": BooleanVariable,
                },
                {
                    "name": "BooleanValue",
                    "type": BooleanValue,
                },
                {
                    "name": "OR",
                    "type": Or,
                },
                {
                    "name": "XOR",
                    "type": Xor,
                },
                {
                    "name": "AND",
                    "type": And,
                },
                {
                    "name": "NOT",
                    "type": Not,
                },
                {
                    "name": "EQBoolean",
                    "type": Eqboolean,
                },
                {
                    "name": "EQNumeric",
                    "type": Eqnumeric,
                },
                {
                    "name": "EQInternal",
                    "type": Eqinternal,
                },
                {
                    "name": "EQString",
                    "type": Eqstring,
                },
                {
                    "name": "EQArray",
                    "type": Eqarray,
                },
                {
                    "name": "NEBoolean",
                    "type": Neboolean,
                },
                {
                    "name": "NENumeric",
                    "type": Nenumeric,
                },
                {
                    "name": "NEInternal",
                    "type": Neinternal,
                },
                {
                    "name": "NEString",
                    "type": Nestring,
                },
                {
                    "name": "NEArray",
                    "type": Nearray,
                },
                {
                    "name": "GT",
                    "type": Gt,
                },
                {
                    "name": "GE",
                    "type": Ge,
                },
                {
                    "name": "LT",
                    "type": Lt,
                },
                {
                    "name": "LE",
                    "type": Le,
                },
                {
                    "name": "IsKnown",
                    "type": IsKnown,
                },
                {
                    "name": "ALL_KNOWN",
                    "type": AllKnown,
                },
                {
                    "name": "ANY_KNOWN",
                    "type": AnyKnown,
                },
                {
                    "name": "Executing",
                    "type": Executing,
                },
                {
                    "name": "Finished",
                    "type": Finished,
                },
                {
                    "name": "Inactive",
                    "type": Inactive,
                },
                {
                    "name": "IterationEnded",
                    "type": IterationEnded,
                },
                {
                    "name": "Waiting",
                    "type": Waiting,
                },
                {
                    "name": "NoChildFailed",
                    "type": NoChildFailed,
                },
                {
                    "name": "Failed",
                    "type": Failed,
                },
                {
                    "name": "Skipped",
                    "type": Skipped,
                },
                {
                    "name": "Succeeded",
                    "type": Succeeded,
                },
                {
                    "name": "PostconditionFailed",
                    "type": PostconditionFailed,
                },
                {
                    "name": "ADD",
                    "type": Add,
                },
                {
                    "name": "SUB",
                    "type": Sub,
                },
                {
                    "name": "MUL",
                    "type": Mul,
                },
                {
                    "name": "DIV",
                    "type": Div,
                },
                {
                    "name": "MOD",
                    "type": Mod,
                },
                {
                    "name": "MAX",
                    "type": Max,
                },
                {
                    "name": "MIN",
                    "type": Min,
                },
                {
                    "name": "SQRT",
                    "type": Sqrt,
                },
                {
                    "name": "ABS",
                    "type": Abs,
                },
                {
                    "name": "CEIL",
                    "type": Ceil,
                },
                {
                    "name": "FLOOR",
                    "type": Floor,
                },
                {
                    "name": "ROUND",
                    "type": Round,
                },
                {
                    "name": "TRUNC",
                    "type": Trunc,
                },
                {
                    "name": "REAL_TO_INT",
                    "type": RealToInt,
                },
                {
                    "name": "IntegerVariable",
                    "type": IntegerVariable,
                },
                {
                    "name": "RealVariable",
                    "type": RealVariable,
                },
                {
                    "name": "IntegerValue",
                    "type": IntegerValue,
                },
                {
                    "name": "RealValue",
                    "type": RealValue,
                },
                {
                    "name": "NodeTimepointValue",
                    "type": NodeTimepointValue,
                },
                {
                    "name": "ArraySize",
                    "type": ArraySize,
                },
                {
                    "name": "ArrayMaxSize",
                    "type": ArrayMaxSize,
                },
                {
                    "name": "StringVariable",
                    "type": StringVariable,
                },
                {
                    "name": "StringValue",
                    "type": StringValue,
                },
                {
                    "name": "Concat",
                    "type": Concat,
                },
                {
                    "name": "ArrayValue",
                    "type": ArrayValue,
                },
                {
                    "name": "ArrayVariable",
                    "type": ArrayVariable,
                },
                {
                    "name": "LookupOnChange",
                    "type": LookupOnChange,
                },
                {
                    "name": "LookupNow",
                    "type": LookupNow,
                },
                {
                    "name": "ArrayElement",
                    "type": ArrayElement,
                },
            ),
        },
    )
    file_name: None | str = field(
        default=None,
        metadata={
            "name": "FileName",
            "type": "Attribute",
        },
    )
    line_no: None | int = field(
        default=None,
        metadata={
            "name": "LineNo",
            "type": "Attribute",
        },
    )
    col_no: None | int = field(
        default=None,
        metadata={
            "name": "ColNo",
            "type": "Attribute",
        },
    )
    epx: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )


@dataclass(kw_only=True)
class Assume:
    choice: (
        None
        | BooleanVariable
        | BooleanValue
        | Or
        | Xor
        | And
        | Not
        | Eqboolean
        | Eqnumeric
        | Eqinternal
        | Eqstring
        | Eqarray
        | Neboolean
        | Nenumeric
        | Neinternal
        | Nestring
        | Nearray
        | Gt
        | Ge
        | Lt
        | Le
        | IsKnown
        | AllKnown
        | AnyKnown
        | Executing
        | Finished
        | Inactive
        | IterationEnded
        | Waiting
        | NoChildFailed
        | Failed
        | Skipped
        | Succeeded
        | PostconditionFailed
        | LookupOnChange
        | LookupNow
        | ArrayElement
    ) = field(
        default=None,
        metadata={
            "type": "Elements",
            "choices": (
                {
                    "name": "BooleanVariable",
                    "type": BooleanVariable,
                },
                {
                    "name": "BooleanValue",
                    "type": BooleanValue,
                },
                {
                    "name": "OR",
                    "type": Or,
                },
                {
                    "name": "XOR",
                    "type": Xor,
                },
                {
                    "name": "AND",
                    "type": And,
                },
                {
                    "name": "NOT",
                    "type": Not,
                },
                {
                    "name": "EQBoolean",
                    "type": Eqboolean,
                },
                {
                    "name": "EQNumeric",
                    "type": Eqnumeric,
                },
                {
                    "name": "EQInternal",
                    "type": Eqinternal,
                },
                {
                    "name": "EQString",
                    "type": Eqstring,
                },
                {
                    "name": "EQArray",
                    "type": Eqarray,
                },
                {
                    "name": "NEBoolean",
                    "type": Neboolean,
                },
                {
                    "name": "NENumeric",
                    "type": Nenumeric,
                },
                {
                    "name": "NEInternal",
                    "type": Neinternal,
                },
                {
                    "name": "NEString",
                    "type": Nestring,
                },
                {
                    "name": "NEArray",
                    "type": Nearray,
                },
                {
                    "name": "GT",
                    "type": Gt,
                },
                {
                    "name": "GE",
                    "type": Ge,
                },
                {
                    "name": "LT",
                    "type": Lt,
                },
                {
                    "name": "LE",
                    "type": Le,
                },
                {
                    "name": "IsKnown",
                    "type": IsKnown,
                },
                {
                    "name": "ALL_KNOWN",
                    "type": AllKnown,
                },
                {
                    "name": "ANY_KNOWN",
                    "type": AnyKnown,
                },
                {
                    "name": "Executing",
                    "type": Executing,
                },
                {
                    "name": "Finished",
                    "type": Finished,
                },
                {
                    "name": "Inactive",
                    "type": Inactive,
                },
                {
                    "name": "IterationEnded",
                    "type": IterationEnded,
                },
                {
                    "name": "Waiting",
                    "type": Waiting,
                },
                {
                    "name": "NoChildFailed",
                    "type": NoChildFailed,
                },
                {
                    "name": "Failed",
                    "type": Failed,
                },
                {
                    "name": "Skipped",
                    "type": Skipped,
                },
                {
                    "name": "Succeeded",
                    "type": Succeeded,
                },
                {
                    "name": "PostconditionFailed",
                    "type": PostconditionFailed,
                },
                {
                    "name": "LookupOnChange",
                    "type": LookupOnChange,
                },
                {
                    "name": "LookupNow",
                    "type": LookupNow,
                },
                {
                    "name": "ArrayElement",
                    "type": ArrayElement,
                },
            ),
        },
    )
    file_name: None | str = field(
        default=None,
        metadata={
            "name": "FileName",
            "type": "Attribute",
        },
    )
    line_no: None | int = field(
        default=None,
        metadata={
            "name": "LineNo",
            "type": "Attribute",
        },
    )
    col_no: None | int = field(
        default=None,
        metadata={
            "name": "ColNo",
            "type": "Attribute",
        },
    )
    epx: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )


@dataclass(kw_only=True)
class BooleanRhs:
    class Meta:
        name = "BooleanRHS"

    choice: (
        None
        | BooleanVariable
        | BooleanValue
        | Or
        | Xor
        | And
        | Not
        | Eqboolean
        | Eqnumeric
        | Eqinternal
        | Eqstring
        | Eqarray
        | Neboolean
        | Nenumeric
        | Neinternal
        | Nestring
        | Nearray
        | Gt
        | Ge
        | Lt
        | Le
        | IsKnown
        | AllKnown
        | AnyKnown
        | Executing
        | Finished
        | Inactive
        | IterationEnded
        | Waiting
        | NoChildFailed
        | Failed
        | Skipped
        | Succeeded
        | PostconditionFailed
        | LookupOnChange
        | LookupNow
        | ArrayElement
    ) = field(
        default=None,
        metadata={
            "type": "Elements",
            "choices": (
                {
                    "name": "BooleanVariable",
                    "type": BooleanVariable,
                },
                {
                    "name": "BooleanValue",
                    "type": BooleanValue,
                },
                {
                    "name": "OR",
                    "type": Or,
                },
                {
                    "name": "XOR",
                    "type": Xor,
                },
                {
                    "name": "AND",
                    "type": And,
                },
                {
                    "name": "NOT",
                    "type": Not,
                },
                {
                    "name": "EQBoolean",
                    "type": Eqboolean,
                },
                {
                    "name": "EQNumeric",
                    "type": Eqnumeric,
                },
                {
                    "name": "EQInternal",
                    "type": Eqinternal,
                },
                {
                    "name": "EQString",
                    "type": Eqstring,
                },
                {
                    "name": "EQArray",
                    "type": Eqarray,
                },
                {
                    "name": "NEBoolean",
                    "type": Neboolean,
                },
                {
                    "name": "NENumeric",
                    "type": Nenumeric,
                },
                {
                    "name": "NEInternal",
                    "type": Neinternal,
                },
                {
                    "name": "NEString",
                    "type": Nestring,
                },
                {
                    "name": "NEArray",
                    "type": Nearray,
                },
                {
                    "name": "GT",
                    "type": Gt,
                },
                {
                    "name": "GE",
                    "type": Ge,
                },
                {
                    "name": "LT",
                    "type": Lt,
                },
                {
                    "name": "LE",
                    "type": Le,
                },
                {
                    "name": "IsKnown",
                    "type": IsKnown,
                },
                {
                    "name": "ALL_KNOWN",
                    "type": AllKnown,
                },
                {
                    "name": "ANY_KNOWN",
                    "type": AnyKnown,
                },
                {
                    "name": "Executing",
                    "type": Executing,
                },
                {
                    "name": "Finished",
                    "type": Finished,
                },
                {
                    "name": "Inactive",
                    "type": Inactive,
                },
                {
                    "name": "IterationEnded",
                    "type": IterationEnded,
                },
                {
                    "name": "Waiting",
                    "type": Waiting,
                },
                {
                    "name": "NoChildFailed",
                    "type": NoChildFailed,
                },
                {
                    "name": "Failed",
                    "type": Failed,
                },
                {
                    "name": "Skipped",
                    "type": Skipped,
                },
                {
                    "name": "Succeeded",
                    "type": Succeeded,
                },
                {
                    "name": "PostconditionFailed",
                    "type": PostconditionFailed,
                },
                {
                    "name": "LookupOnChange",
                    "type": LookupOnChange,
                },
                {
                    "name": "LookupNow",
                    "type": LookupNow,
                },
                {
                    "name": "ArrayElement",
                    "type": ArrayElement,
                },
            ),
        },
    )
    file_name: None | str = field(
        default=None,
        metadata={
            "name": "FileName",
            "type": "Attribute",
        },
    )
    line_no: None | int = field(
        default=None,
        metadata={
            "name": "LineNo",
            "type": "Attribute",
        },
    )
    col_no: None | int = field(
        default=None,
        metadata={
            "name": "ColNo",
            "type": "Attribute",
        },
    )
    epx: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )


@dataclass(kw_only=True)
class ConditionType:
    choice: (
        None
        | BooleanVariable
        | BooleanValue
        | Or
        | Xor
        | And
        | Not
        | Eqboolean
        | Eqnumeric
        | Eqinternal
        | Eqstring
        | Eqarray
        | Neboolean
        | Nenumeric
        | Neinternal
        | Nestring
        | Nearray
        | Gt
        | Ge
        | Lt
        | Le
        | IsKnown
        | AllKnown
        | AnyKnown
        | Executing
        | Finished
        | Inactive
        | IterationEnded
        | Waiting
        | NoChildFailed
        | Failed
        | Skipped
        | Succeeded
        | PostconditionFailed
        | LookupOnChange
        | LookupNow
        | ArrayElement
    ) = field(
        default=None,
        metadata={
            "type": "Elements",
            "choices": (
                {
                    "name": "BooleanVariable",
                    "type": BooleanVariable,
                },
                {
                    "name": "BooleanValue",
                    "type": BooleanValue,
                },
                {
                    "name": "OR",
                    "type": Or,
                },
                {
                    "name": "XOR",
                    "type": Xor,
                },
                {
                    "name": "AND",
                    "type": And,
                },
                {
                    "name": "NOT",
                    "type": Not,
                },
                {
                    "name": "EQBoolean",
                    "type": Eqboolean,
                },
                {
                    "name": "EQNumeric",
                    "type": Eqnumeric,
                },
                {
                    "name": "EQInternal",
                    "type": Eqinternal,
                },
                {
                    "name": "EQString",
                    "type": Eqstring,
                },
                {
                    "name": "EQArray",
                    "type": Eqarray,
                },
                {
                    "name": "NEBoolean",
                    "type": Neboolean,
                },
                {
                    "name": "NENumeric",
                    "type": Nenumeric,
                },
                {
                    "name": "NEInternal",
                    "type": Neinternal,
                },
                {
                    "name": "NEString",
                    "type": Nestring,
                },
                {
                    "name": "NEArray",
                    "type": Nearray,
                },
                {
                    "name": "GT",
                    "type": Gt,
                },
                {
                    "name": "GE",
                    "type": Ge,
                },
                {
                    "name": "LT",
                    "type": Lt,
                },
                {
                    "name": "LE",
                    "type": Le,
                },
                {
                    "name": "IsKnown",
                    "type": IsKnown,
                },
                {
                    "name": "ALL_KNOWN",
                    "type": AllKnown,
                },
                {
                    "name": "ANY_KNOWN",
                    "type": AnyKnown,
                },
                {
                    "name": "Executing",
                    "type": Executing,
                },
                {
                    "name": "Finished",
                    "type": Finished,
                },
                {
                    "name": "Inactive",
                    "type": Inactive,
                },
                {
                    "name": "IterationEnded",
                    "type": IterationEnded,
                },
                {
                    "name": "Waiting",
                    "type": Waiting,
                },
                {
                    "name": "NoChildFailed",
                    "type": NoChildFailed,
                },
                {
                    "name": "Failed",
                    "type": Failed,
                },
                {
                    "name": "Skipped",
                    "type": Skipped,
                },
                {
                    "name": "Succeeded",
                    "type": Succeeded,
                },
                {
                    "name": "PostconditionFailed",
                    "type": PostconditionFailed,
                },
                {
                    "name": "LookupOnChange",
                    "type": LookupOnChange,
                },
                {
                    "name": "LookupNow",
                    "type": LookupNow,
                },
                {
                    "name": "ArrayElement",
                    "type": ArrayElement,
                },
            ),
        },
    )
    file_name: None | str = field(
        default=None,
        metadata={
            "name": "FileName",
            "type": "Attribute",
        },
    )
    line_no: None | int = field(
        default=None,
        metadata={
            "name": "LineNo",
            "type": "Attribute",
        },
    )
    col_no: None | int = field(
        default=None,
        metadata={
            "name": "ColNo",
            "type": "Attribute",
        },
    )
    epx: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )


@dataclass(kw_only=True)
class Desire:
    choice: (
        None
        | BooleanVariable
        | BooleanValue
        | Or
        | Xor
        | And
        | Not
        | Eqboolean
        | Eqnumeric
        | Eqinternal
        | Eqstring
        | Eqarray
        | Neboolean
        | Nenumeric
        | Neinternal
        | Nestring
        | Nearray
        | Gt
        | Ge
        | Lt
        | Le
        | IsKnown
        | AllKnown
        | AnyKnown
        | Executing
        | Finished
        | Inactive
        | IterationEnded
        | Waiting
        | NoChildFailed
        | Failed
        | Skipped
        | Succeeded
        | PostconditionFailed
        | LookupOnChange
        | LookupNow
        | ArrayElement
    ) = field(
        default=None,
        metadata={
            "type": "Elements",
            "choices": (
                {
                    "name": "BooleanVariable",
                    "type": BooleanVariable,
                },
                {
                    "name": "BooleanValue",
                    "type": BooleanValue,
                },
                {
                    "name": "OR",
                    "type": Or,
                },
                {
                    "name": "XOR",
                    "type": Xor,
                },
                {
                    "name": "AND",
                    "type": And,
                },
                {
                    "name": "NOT",
                    "type": Not,
                },
                {
                    "name": "EQBoolean",
                    "type": Eqboolean,
                },
                {
                    "name": "EQNumeric",
                    "type": Eqnumeric,
                },
                {
                    "name": "EQInternal",
                    "type": Eqinternal,
                },
                {
                    "name": "EQString",
                    "type": Eqstring,
                },
                {
                    "name": "EQArray",
                    "type": Eqarray,
                },
                {
                    "name": "NEBoolean",
                    "type": Neboolean,
                },
                {
                    "name": "NENumeric",
                    "type": Nenumeric,
                },
                {
                    "name": "NEInternal",
                    "type": Neinternal,
                },
                {
                    "name": "NEString",
                    "type": Nestring,
                },
                {
                    "name": "NEArray",
                    "type": Nearray,
                },
                {
                    "name": "GT",
                    "type": Gt,
                },
                {
                    "name": "GE",
                    "type": Ge,
                },
                {
                    "name": "LT",
                    "type": Lt,
                },
                {
                    "name": "LE",
                    "type": Le,
                },
                {
                    "name": "IsKnown",
                    "type": IsKnown,
                },
                {
                    "name": "ALL_KNOWN",
                    "type": AllKnown,
                },
                {
                    "name": "ANY_KNOWN",
                    "type": AnyKnown,
                },
                {
                    "name": "Executing",
                    "type": Executing,
                },
                {
                    "name": "Finished",
                    "type": Finished,
                },
                {
                    "name": "Inactive",
                    "type": Inactive,
                },
                {
                    "name": "IterationEnded",
                    "type": IterationEnded,
                },
                {
                    "name": "Waiting",
                    "type": Waiting,
                },
                {
                    "name": "NoChildFailed",
                    "type": NoChildFailed,
                },
                {
                    "name": "Failed",
                    "type": Failed,
                },
                {
                    "name": "Skipped",
                    "type": Skipped,
                },
                {
                    "name": "Succeeded",
                    "type": Succeeded,
                },
                {
                    "name": "PostconditionFailed",
                    "type": PostconditionFailed,
                },
                {
                    "name": "LookupOnChange",
                    "type": LookupOnChange,
                },
                {
                    "name": "LookupNow",
                    "type": LookupNow,
                },
                {
                    "name": "ArrayElement",
                    "type": ArrayElement,
                },
            ),
        },
    )
    file_name: None | str = field(
        default=None,
        metadata={
            "name": "FileName",
            "type": "Attribute",
        },
    )
    line_no: None | int = field(
        default=None,
        metadata={
            "name": "LineNo",
            "type": "Attribute",
        },
    )
    col_no: None | int = field(
        default=None,
        metadata={
            "name": "ColNo",
            "type": "Attribute",
        },
    )
    epx: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )


@dataclass(kw_only=True)
class Expect:
    choice: (
        None
        | BooleanVariable
        | BooleanValue
        | Or
        | Xor
        | And
        | Not
        | Eqboolean
        | Eqnumeric
        | Eqinternal
        | Eqstring
        | Eqarray
        | Neboolean
        | Nenumeric
        | Neinternal
        | Nestring
        | Nearray
        | Gt
        | Ge
        | Lt
        | Le
        | IsKnown
        | AllKnown
        | AnyKnown
        | Executing
        | Finished
        | Inactive
        | IterationEnded
        | Waiting
        | NoChildFailed
        | Failed
        | Skipped
        | Succeeded
        | PostconditionFailed
        | LookupOnChange
        | LookupNow
        | ArrayElement
    ) = field(
        default=None,
        metadata={
            "type": "Elements",
            "choices": (
                {
                    "name": "BooleanVariable",
                    "type": BooleanVariable,
                },
                {
                    "name": "BooleanValue",
                    "type": BooleanValue,
                },
                {
                    "name": "OR",
                    "type": Or,
                },
                {
                    "name": "XOR",
                    "type": Xor,
                },
                {
                    "name": "AND",
                    "type": And,
                },
                {
                    "name": "NOT",
                    "type": Not,
                },
                {
                    "name": "EQBoolean",
                    "type": Eqboolean,
                },
                {
                    "name": "EQNumeric",
                    "type": Eqnumeric,
                },
                {
                    "name": "EQInternal",
                    "type": Eqinternal,
                },
                {
                    "name": "EQString",
                    "type": Eqstring,
                },
                {
                    "name": "EQArray",
                    "type": Eqarray,
                },
                {
                    "name": "NEBoolean",
                    "type": Neboolean,
                },
                {
                    "name": "NENumeric",
                    "type": Nenumeric,
                },
                {
                    "name": "NEInternal",
                    "type": Neinternal,
                },
                {
                    "name": "NEString",
                    "type": Nestring,
                },
                {
                    "name": "NEArray",
                    "type": Nearray,
                },
                {
                    "name": "GT",
                    "type": Gt,
                },
                {
                    "name": "GE",
                    "type": Ge,
                },
                {
                    "name": "LT",
                    "type": Lt,
                },
                {
                    "name": "LE",
                    "type": Le,
                },
                {
                    "name": "IsKnown",
                    "type": IsKnown,
                },
                {
                    "name": "ALL_KNOWN",
                    "type": AllKnown,
                },
                {
                    "name": "ANY_KNOWN",
                    "type": AnyKnown,
                },
                {
                    "name": "Executing",
                    "type": Executing,
                },
                {
                    "name": "Finished",
                    "type": Finished,
                },
                {
                    "name": "Inactive",
                    "type": Inactive,
                },
                {
                    "name": "IterationEnded",
                    "type": IterationEnded,
                },
                {
                    "name": "Waiting",
                    "type": Waiting,
                },
                {
                    "name": "NoChildFailed",
                    "type": NoChildFailed,
                },
                {
                    "name": "Failed",
                    "type": Failed,
                },
                {
                    "name": "Skipped",
                    "type": Skipped,
                },
                {
                    "name": "Succeeded",
                    "type": Succeeded,
                },
                {
                    "name": "PostconditionFailed",
                    "type": PostconditionFailed,
                },
                {
                    "name": "LookupOnChange",
                    "type": LookupOnChange,
                },
                {
                    "name": "LookupNow",
                    "type": LookupNow,
                },
                {
                    "name": "ArrayElement",
                    "type": ArrayElement,
                },
            ),
        },
    )
    file_name: None | str = field(
        default=None,
        metadata={
            "name": "FileName",
            "type": "Attribute",
        },
    )
    line_no: None | int = field(
        default=None,
        metadata={
            "name": "LineNo",
            "type": "Attribute",
        },
    )
    col_no: None | int = field(
        default=None,
        metadata={
            "name": "ColNo",
            "type": "Attribute",
        },
    )
    epx: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )


@dataclass(kw_only=True)
class LibraryNodeCall:
    node_id: NodeId = field(
        metadata={
            "name": "NodeId",
            "type": "Element",
        }
    )
    alias: list[LibraryNodeCall.Alias] = field(
        default_factory=list,
        metadata={
            "name": "Alias",
            "type": "Element",
            "namespace": "",
        },
    )
    file_name: None | str = field(
        default=None,
        metadata={
            "name": "FileName",
            "type": "Attribute",
        },
    )
    line_no: None | int = field(
        default=None,
        metadata={
            "name": "LineNo",
            "type": "Attribute",
        },
    )
    col_no: None | int = field(
        default=None,
        metadata={
            "name": "ColNo",
            "type": "Attribute",
        },
    )
    epx: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )

    @dataclass(kw_only=True)
    class Alias:
        node_parameter: str = field(
            metadata={
                "name": "NodeParameter",
                "type": "Element",
                "namespace": "",
            }
        )
        choice: (
            None
            | BooleanVariable
            | BooleanValue
            | Or
            | Xor
            | And
            | Not
            | Eqboolean
            | Eqnumeric
            | Eqinternal
            | Eqstring
            | Eqarray
            | Neboolean
            | Nenumeric
            | Neinternal
            | Nestring
            | Nearray
            | Gt
            | Ge
            | Lt
            | Le
            | IsKnown
            | AllKnown
            | AnyKnown
            | Executing
            | Finished
            | Inactive
            | IterationEnded
            | Waiting
            | NoChildFailed
            | Failed
            | Skipped
            | Succeeded
            | PostconditionFailed
            | Add
            | Sub
            | Mul
            | Div
            | Mod
            | Max
            | Min
            | Sqrt
            | Abs
            | Ceil
            | Floor
            | Round
            | Trunc
            | RealToInt
            | IntegerVariable
            | RealVariable
            | IntegerValue
            | RealValue
            | NodeTimepointValue
            | ArraySize
            | ArrayMaxSize
            | StringVariable
            | StringValue
            | Concat
            | ArrayValue
            | ArrayVariable
            | LookupOnChange
            | LookupNow
            | ArrayElement
        ) = field(
            default=None,
            metadata={
                "type": "Elements",
                "choices": (
                    {
                        "name": "BooleanVariable",
                        "type": BooleanVariable,
                    },
                    {
                        "name": "BooleanValue",
                        "type": BooleanValue,
                    },
                    {
                        "name": "OR",
                        "type": Or,
                    },
                    {
                        "name": "XOR",
                        "type": Xor,
                    },
                    {
                        "name": "AND",
                        "type": And,
                    },
                    {
                        "name": "NOT",
                        "type": Not,
                    },
                    {
                        "name": "EQBoolean",
                        "type": Eqboolean,
                    },
                    {
                        "name": "EQNumeric",
                        "type": Eqnumeric,
                    },
                    {
                        "name": "EQInternal",
                        "type": Eqinternal,
                    },
                    {
                        "name": "EQString",
                        "type": Eqstring,
                    },
                    {
                        "name": "EQArray",
                        "type": Eqarray,
                    },
                    {
                        "name": "NEBoolean",
                        "type": Neboolean,
                    },
                    {
                        "name": "NENumeric",
                        "type": Nenumeric,
                    },
                    {
                        "name": "NEInternal",
                        "type": Neinternal,
                    },
                    {
                        "name": "NEString",
                        "type": Nestring,
                    },
                    {
                        "name": "NEArray",
                        "type": Nearray,
                    },
                    {
                        "name": "GT",
                        "type": Gt,
                    },
                    {
                        "name": "GE",
                        "type": Ge,
                    },
                    {
                        "name": "LT",
                        "type": Lt,
                    },
                    {
                        "name": "LE",
                        "type": Le,
                    },
                    {
                        "name": "IsKnown",
                        "type": IsKnown,
                    },
                    {
                        "name": "ALL_KNOWN",
                        "type": AllKnown,
                    },
                    {
                        "name": "ANY_KNOWN",
                        "type": AnyKnown,
                    },
                    {
                        "name": "Executing",
                        "type": Executing,
                    },
                    {
                        "name": "Finished",
                        "type": Finished,
                    },
                    {
                        "name": "Inactive",
                        "type": Inactive,
                    },
                    {
                        "name": "IterationEnded",
                        "type": IterationEnded,
                    },
                    {
                        "name": "Waiting",
                        "type": Waiting,
                    },
                    {
                        "name": "NoChildFailed",
                        "type": NoChildFailed,
                    },
                    {
                        "name": "Failed",
                        "type": Failed,
                    },
                    {
                        "name": "Skipped",
                        "type": Skipped,
                    },
                    {
                        "name": "Succeeded",
                        "type": Succeeded,
                    },
                    {
                        "name": "PostconditionFailed",
                        "type": PostconditionFailed,
                    },
                    {
                        "name": "ADD",
                        "type": Add,
                    },
                    {
                        "name": "SUB",
                        "type": Sub,
                    },
                    {
                        "name": "MUL",
                        "type": Mul,
                    },
                    {
                        "name": "DIV",
                        "type": Div,
                    },
                    {
                        "name": "MOD",
                        "type": Mod,
                    },
                    {
                        "name": "MAX",
                        "type": Max,
                    },
                    {
                        "name": "MIN",
                        "type": Min,
                    },
                    {
                        "name": "SQRT",
                        "type": Sqrt,
                    },
                    {
                        "name": "ABS",
                        "type": Abs,
                    },
                    {
                        "name": "CEIL",
                        "type": Ceil,
                    },
                    {
                        "name": "FLOOR",
                        "type": Floor,
                    },
                    {
                        "name": "ROUND",
                        "type": Round,
                    },
                    {
                        "name": "TRUNC",
                        "type": Trunc,
                    },
                    {
                        "name": "REAL_TO_INT",
                        "type": RealToInt,
                    },
                    {
                        "name": "IntegerVariable",
                        "type": IntegerVariable,
                    },
                    {
                        "name": "RealVariable",
                        "type": RealVariable,
                    },
                    {
                        "name": "IntegerValue",
                        "type": IntegerValue,
                    },
                    {
                        "name": "RealValue",
                        "type": RealValue,
                    },
                    {
                        "name": "NodeTimepointValue",
                        "type": NodeTimepointValue,
                    },
                    {
                        "name": "ArraySize",
                        "type": ArraySize,
                    },
                    {
                        "name": "ArrayMaxSize",
                        "type": ArrayMaxSize,
                    },
                    {
                        "name": "StringVariable",
                        "type": StringVariable,
                    },
                    {
                        "name": "StringValue",
                        "type": StringValue,
                    },
                    {
                        "name": "Concat",
                        "type": Concat,
                    },
                    {
                        "name": "ArrayValue",
                        "type": ArrayValue,
                    },
                    {
                        "name": "ArrayVariable",
                        "type": ArrayVariable,
                    },
                    {
                        "name": "LookupOnChange",
                        "type": LookupOnChange,
                    },
                    {
                        "name": "LookupNow",
                        "type": LookupNow,
                    },
                    {
                        "name": "ArrayElement",
                        "type": ArrayElement,
                    },
                ),
            },
        )
        file_name: None | str = field(
            default=None,
            metadata={
                "name": "FileName",
                "type": "Attribute",
            },
        )
        line_no: None | int = field(
            default=None,
            metadata={
                "name": "LineNo",
                "type": "Attribute",
            },
        )
        col_no: None | int = field(
            default=None,
            metadata={
                "name": "ColNo",
                "type": "Attribute",
            },
        )
        epx: None | str = field(
            default=None,
            metadata={
                "type": "Attribute",
            },
        )


@dataclass(kw_only=True)
class LibraryNodeDeclaration:
    name: str = field(
        metadata={
            "name": "Name",
            "type": "Element",
            "namespace": "",
        }
    )
    interface: None | Interface = field(
        default=None,
        metadata={
            "name": "Interface",
            "type": "Element",
        },
    )
    file_name: None | str = field(
        default=None,
        metadata={
            "name": "FileName",
            "type": "Attribute",
        },
    )
    line_no: None | int = field(
        default=None,
        metadata={
            "name": "LineNo",
            "type": "Attribute",
        },
    )
    col_no: None | int = field(
        default=None,
        metadata={
            "name": "ColNo",
            "type": "Attribute",
        },
    )
    epx: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )


@dataclass(kw_only=True)
class Resource:
    resource_name: Resource.ResourceName = field(
        metadata={
            "name": "ResourceName",
            "type": "Element",
            "namespace": "",
        }
    )
    resource_upper_bound: None | Resource.ResourceUpperBound = field(
        default=None,
        metadata={
            "name": "ResourceUpperBound",
            "type": "Element",
            "namespace": "",
        },
    )
    resource_release_at_termination: None | Resource.ResourceReleaseAtTermination = (
        field(
            default=None,
            metadata={
                "name": "ResourceReleaseAtTermination",
                "type": "Element",
                "namespace": "",
            },
        )
    )
    file_name: None | str = field(
        default=None,
        metadata={
            "name": "FileName",
            "type": "Attribute",
        },
    )
    line_no: None | int = field(
        default=None,
        metadata={
            "name": "LineNo",
            "type": "Attribute",
        },
    )
    col_no: None | int = field(
        default=None,
        metadata={
            "name": "ColNo",
            "type": "Attribute",
        },
    )
    epx: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )

    @dataclass(kw_only=True)
    class ResourceName:
        choice: (
            None
            | StringVariable
            | StringValue
            | Concat
            | LookupOnChange
            | LookupNow
            | ArrayElement
        ) = field(
            default=None,
            metadata={
                "type": "Elements",
                "choices": (
                    {
                        "name": "StringVariable",
                        "type": StringVariable,
                    },
                    {
                        "name": "StringValue",
                        "type": StringValue,
                    },
                    {
                        "name": "Concat",
                        "type": Concat,
                    },
                    {
                        "name": "LookupOnChange",
                        "type": LookupOnChange,
                    },
                    {
                        "name": "LookupNow",
                        "type": LookupNow,
                    },
                    {
                        "name": "ArrayElement",
                        "type": ArrayElement,
                    },
                ),
            },
        )
        file_name: None | str = field(
            default=None,
            metadata={
                "name": "FileName",
                "type": "Attribute",
            },
        )
        line_no: None | int = field(
            default=None,
            metadata={
                "name": "LineNo",
                "type": "Attribute",
            },
        )
        col_no: None | int = field(
            default=None,
            metadata={
                "name": "ColNo",
                "type": "Attribute",
            },
        )
        epx: None | str = field(
            default=None,
            metadata={
                "type": "Attribute",
            },
        )

    @dataclass(kw_only=True)
    class ResourceUpperBound:
        choice: (
            None
            | Add
            | Sub
            | Mul
            | Div
            | Mod
            | Max
            | Min
            | Sqrt
            | Abs
            | Ceil
            | Floor
            | Round
            | Trunc
            | RealToInt
            | IntegerVariable
            | RealVariable
            | IntegerValue
            | RealValue
            | NodeTimepointValue
            | ArraySize
            | ArrayMaxSize
            | LookupOnChange
            | LookupNow
            | ArrayElement
            | Strlen
        ) = field(
            default=None,
            metadata={
                "type": "Elements",
                "choices": (
                    {
                        "name": "ADD",
                        "type": Add,
                    },
                    {
                        "name": "SUB",
                        "type": Sub,
                    },
                    {
                        "name": "MUL",
                        "type": Mul,
                    },
                    {
                        "name": "DIV",
                        "type": Div,
                    },
                    {
                        "name": "MOD",
                        "type": Mod,
                    },
                    {
                        "name": "MAX",
                        "type": Max,
                    },
                    {
                        "name": "MIN",
                        "type": Min,
                    },
                    {
                        "name": "SQRT",
                        "type": Sqrt,
                    },
                    {
                        "name": "ABS",
                        "type": Abs,
                    },
                    {
                        "name": "CEIL",
                        "type": Ceil,
                    },
                    {
                        "name": "FLOOR",
                        "type": Floor,
                    },
                    {
                        "name": "ROUND",
                        "type": Round,
                    },
                    {
                        "name": "TRUNC",
                        "type": Trunc,
                    },
                    {
                        "name": "REAL_TO_INT",
                        "type": RealToInt,
                    },
                    {
                        "name": "IntegerVariable",
                        "type": IntegerVariable,
                    },
                    {
                        "name": "RealVariable",
                        "type": RealVariable,
                    },
                    {
                        "name": "IntegerValue",
                        "type": IntegerValue,
                    },
                    {
                        "name": "RealValue",
                        "type": RealValue,
                    },
                    {
                        "name": "NodeTimepointValue",
                        "type": NodeTimepointValue,
                    },
                    {
                        "name": "ArraySize",
                        "type": ArraySize,
                    },
                    {
                        "name": "ArrayMaxSize",
                        "type": ArrayMaxSize,
                    },
                    {
                        "name": "LookupOnChange",
                        "type": LookupOnChange,
                    },
                    {
                        "name": "LookupNow",
                        "type": LookupNow,
                    },
                    {
                        "name": "ArrayElement",
                        "type": ArrayElement,
                    },
                    {
                        "name": "STRLEN",
                        "type": Strlen,
                    },
                ),
            },
        )
        file_name: None | str = field(
            default=None,
            metadata={
                "name": "FileName",
                "type": "Attribute",
            },
        )
        line_no: None | int = field(
            default=None,
            metadata={
                "name": "LineNo",
                "type": "Attribute",
            },
        )
        col_no: None | int = field(
            default=None,
            metadata={
                "name": "ColNo",
                "type": "Attribute",
            },
        )
        epx: None | str = field(
            default=None,
            metadata={
                "type": "Attribute",
            },
        )

    @dataclass(kw_only=True)
    class ResourceReleaseAtTermination:
        choice: (
            None
            | BooleanVariable
            | BooleanValue
            | Or
            | Xor
            | And
            | Not
            | Eqboolean
            | Eqnumeric
            | Eqinternal
            | Eqstring
            | Eqarray
            | Neboolean
            | Nenumeric
            | Neinternal
            | Nestring
            | Nearray
            | Gt
            | Ge
            | Lt
            | Le
            | IsKnown
            | AllKnown
            | AnyKnown
            | Executing
            | Finished
            | Inactive
            | IterationEnded
            | Waiting
            | NoChildFailed
            | Failed
            | Skipped
            | Succeeded
            | PostconditionFailed
            | LookupOnChange
            | LookupNow
            | ArrayElement
        ) = field(
            default=None,
            metadata={
                "type": "Elements",
                "choices": (
                    {
                        "name": "BooleanVariable",
                        "type": BooleanVariable,
                    },
                    {
                        "name": "BooleanValue",
                        "type": BooleanValue,
                    },
                    {
                        "name": "OR",
                        "type": Or,
                    },
                    {
                        "name": "XOR",
                        "type": Xor,
                    },
                    {
                        "name": "AND",
                        "type": And,
                    },
                    {
                        "name": "NOT",
                        "type": Not,
                    },
                    {
                        "name": "EQBoolean",
                        "type": Eqboolean,
                    },
                    {
                        "name": "EQNumeric",
                        "type": Eqnumeric,
                    },
                    {
                        "name": "EQInternal",
                        "type": Eqinternal,
                    },
                    {
                        "name": "EQString",
                        "type": Eqstring,
                    },
                    {
                        "name": "EQArray",
                        "type": Eqarray,
                    },
                    {
                        "name": "NEBoolean",
                        "type": Neboolean,
                    },
                    {
                        "name": "NENumeric",
                        "type": Nenumeric,
                    },
                    {
                        "name": "NEInternal",
                        "type": Neinternal,
                    },
                    {
                        "name": "NEString",
                        "type": Nestring,
                    },
                    {
                        "name": "NEArray",
                        "type": Nearray,
                    },
                    {
                        "name": "GT",
                        "type": Gt,
                    },
                    {
                        "name": "GE",
                        "type": Ge,
                    },
                    {
                        "name": "LT",
                        "type": Lt,
                    },
                    {
                        "name": "LE",
                        "type": Le,
                    },
                    {
                        "name": "IsKnown",
                        "type": IsKnown,
                    },
                    {
                        "name": "ALL_KNOWN",
                        "type": AllKnown,
                    },
                    {
                        "name": "ANY_KNOWN",
                        "type": AnyKnown,
                    },
                    {
                        "name": "Executing",
                        "type": Executing,
                    },
                    {
                        "name": "Finished",
                        "type": Finished,
                    },
                    {
                        "name": "Inactive",
                        "type": Inactive,
                    },
                    {
                        "name": "IterationEnded",
                        "type": IterationEnded,
                    },
                    {
                        "name": "Waiting",
                        "type": Waiting,
                    },
                    {
                        "name": "NoChildFailed",
                        "type": NoChildFailed,
                    },
                    {
                        "name": "Failed",
                        "type": Failed,
                    },
                    {
                        "name": "Skipped",
                        "type": Skipped,
                    },
                    {
                        "name": "Succeeded",
                        "type": Succeeded,
                    },
                    {
                        "name": "PostconditionFailed",
                        "type": PostconditionFailed,
                    },
                    {
                        "name": "LookupOnChange",
                        "type": LookupOnChange,
                    },
                    {
                        "name": "LookupNow",
                        "type": LookupNow,
                    },
                    {
                        "name": "ArrayElement",
                        "type": ArrayElement,
                    },
                ),
            },
        )
        file_name: None | str = field(
            default=None,
            metadata={
                "name": "FileName",
                "type": "Attribute",
            },
        )
        line_no: None | int = field(
            default=None,
            metadata={
                "name": "LineNo",
                "type": "Attribute",
            },
        )
        col_no: None | int = field(
            default=None,
            metadata={
                "name": "ColNo",
                "type": "Attribute",
            },
        )
        epx: None | str = field(
            default=None,
            metadata={
                "type": "Attribute",
            },
        )


@dataclass(kw_only=True)
class Update:
    pair: list[Update.Pair] = field(
        default_factory=list,
        metadata={
            "name": "Pair",
            "type": "Element",
            "namespace": "",
        },
    )
    file_name: None | str = field(
        default=None,
        metadata={
            "name": "FileName",
            "type": "Attribute",
        },
    )
    line_no: None | int = field(
        default=None,
        metadata={
            "name": "LineNo",
            "type": "Attribute",
        },
    )
    col_no: None | int = field(
        default=None,
        metadata={
            "name": "ColNo",
            "type": "Attribute",
        },
    )
    epx: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )

    @dataclass(kw_only=True)
    class Pair:
        name: str = field(
            metadata={
                "name": "Name",
                "type": "Element",
                "namespace": "",
            }
        )
        choice: (
            None
            | BooleanVariable
            | BooleanValue
            | Or
            | Xor
            | And
            | Not
            | Eqboolean
            | Eqnumeric
            | Eqinternal
            | Eqstring
            | Eqarray
            | Neboolean
            | Nenumeric
            | Neinternal
            | Nestring
            | Nearray
            | Gt
            | Ge
            | Lt
            | Le
            | IsKnown
            | AllKnown
            | AnyKnown
            | Executing
            | Finished
            | Inactive
            | IterationEnded
            | Waiting
            | NoChildFailed
            | Failed
            | Skipped
            | Succeeded
            | PostconditionFailed
            | Add
            | Sub
            | Mul
            | Div
            | Mod
            | Max
            | Min
            | Sqrt
            | Abs
            | Ceil
            | Floor
            | Round
            | Trunc
            | RealToInt
            | IntegerVariable
            | RealVariable
            | IntegerValue
            | RealValue
            | NodeTimepointValue
            | ArraySize
            | ArrayMaxSize
            | StringVariable
            | StringValue
            | Concat
            | ArrayValue
            | ArrayVariable
            | LookupOnChange
            | LookupNow
            | ArrayElement
        ) = field(
            default=None,
            metadata={
                "type": "Elements",
                "choices": (
                    {
                        "name": "BooleanVariable",
                        "type": BooleanVariable,
                    },
                    {
                        "name": "BooleanValue",
                        "type": BooleanValue,
                    },
                    {
                        "name": "OR",
                        "type": Or,
                    },
                    {
                        "name": "XOR",
                        "type": Xor,
                    },
                    {
                        "name": "AND",
                        "type": And,
                    },
                    {
                        "name": "NOT",
                        "type": Not,
                    },
                    {
                        "name": "EQBoolean",
                        "type": Eqboolean,
                    },
                    {
                        "name": "EQNumeric",
                        "type": Eqnumeric,
                    },
                    {
                        "name": "EQInternal",
                        "type": Eqinternal,
                    },
                    {
                        "name": "EQString",
                        "type": Eqstring,
                    },
                    {
                        "name": "EQArray",
                        "type": Eqarray,
                    },
                    {
                        "name": "NEBoolean",
                        "type": Neboolean,
                    },
                    {
                        "name": "NENumeric",
                        "type": Nenumeric,
                    },
                    {
                        "name": "NEInternal",
                        "type": Neinternal,
                    },
                    {
                        "name": "NEString",
                        "type": Nestring,
                    },
                    {
                        "name": "NEArray",
                        "type": Nearray,
                    },
                    {
                        "name": "GT",
                        "type": Gt,
                    },
                    {
                        "name": "GE",
                        "type": Ge,
                    },
                    {
                        "name": "LT",
                        "type": Lt,
                    },
                    {
                        "name": "LE",
                        "type": Le,
                    },
                    {
                        "name": "IsKnown",
                        "type": IsKnown,
                    },
                    {
                        "name": "ALL_KNOWN",
                        "type": AllKnown,
                    },
                    {
                        "name": "ANY_KNOWN",
                        "type": AnyKnown,
                    },
                    {
                        "name": "Executing",
                        "type": Executing,
                    },
                    {
                        "name": "Finished",
                        "type": Finished,
                    },
                    {
                        "name": "Inactive",
                        "type": Inactive,
                    },
                    {
                        "name": "IterationEnded",
                        "type": IterationEnded,
                    },
                    {
                        "name": "Waiting",
                        "type": Waiting,
                    },
                    {
                        "name": "NoChildFailed",
                        "type": NoChildFailed,
                    },
                    {
                        "name": "Failed",
                        "type": Failed,
                    },
                    {
                        "name": "Skipped",
                        "type": Skipped,
                    },
                    {
                        "name": "Succeeded",
                        "type": Succeeded,
                    },
                    {
                        "name": "PostconditionFailed",
                        "type": PostconditionFailed,
                    },
                    {
                        "name": "ADD",
                        "type": Add,
                    },
                    {
                        "name": "SUB",
                        "type": Sub,
                    },
                    {
                        "name": "MUL",
                        "type": Mul,
                    },
                    {
                        "name": "DIV",
                        "type": Div,
                    },
                    {
                        "name": "MOD",
                        "type": Mod,
                    },
                    {
                        "name": "MAX",
                        "type": Max,
                    },
                    {
                        "name": "MIN",
                        "type": Min,
                    },
                    {
                        "name": "SQRT",
                        "type": Sqrt,
                    },
                    {
                        "name": "ABS",
                        "type": Abs,
                    },
                    {
                        "name": "CEIL",
                        "type": Ceil,
                    },
                    {
                        "name": "FLOOR",
                        "type": Floor,
                    },
                    {
                        "name": "ROUND",
                        "type": Round,
                    },
                    {
                        "name": "TRUNC",
                        "type": Trunc,
                    },
                    {
                        "name": "REAL_TO_INT",
                        "type": RealToInt,
                    },
                    {
                        "name": "IntegerVariable",
                        "type": IntegerVariable,
                    },
                    {
                        "name": "RealVariable",
                        "type": RealVariable,
                    },
                    {
                        "name": "IntegerValue",
                        "type": IntegerValue,
                    },
                    {
                        "name": "RealValue",
                        "type": RealValue,
                    },
                    {
                        "name": "NodeTimepointValue",
                        "type": NodeTimepointValue,
                    },
                    {
                        "name": "ArraySize",
                        "type": ArraySize,
                    },
                    {
                        "name": "ArrayMaxSize",
                        "type": ArrayMaxSize,
                    },
                    {
                        "name": "StringVariable",
                        "type": StringVariable,
                    },
                    {
                        "name": "StringValue",
                        "type": StringValue,
                    },
                    {
                        "name": "Concat",
                        "type": Concat,
                    },
                    {
                        "name": "ArrayValue",
                        "type": ArrayValue,
                    },
                    {
                        "name": "ArrayVariable",
                        "type": ArrayVariable,
                    },
                    {
                        "name": "LookupOnChange",
                        "type": LookupOnChange,
                    },
                    {
                        "name": "LookupNow",
                        "type": LookupNow,
                    },
                    {
                        "name": "ArrayElement",
                        "type": ArrayElement,
                    },
                ),
            },
        )
        file_name: None | str = field(
            default=None,
            metadata={
                "name": "FileName",
                "type": "Attribute",
            },
        )
        line_no: None | int = field(
            default=None,
            metadata={
                "name": "LineNo",
                "type": "Attribute",
            },
        )
        col_no: None | int = field(
            default=None,
            metadata={
                "name": "ColNo",
                "type": "Attribute",
            },
        )
        epx: None | str = field(
            default=None,
            metadata={
                "type": "Attribute",
            },
        )


@dataclass(kw_only=True)
class Assignment:
    choice: (
        None
        | IntegerVariable
        | RealVariable
        | BooleanVariable
        | StringVariable
        | ArrayVariable
        | ArrayElement
    ) = field(
        default=None,
        metadata={
            "type": "Elements",
            "choices": (
                {
                    "name": "IntegerVariable",
                    "type": IntegerVariable,
                },
                {
                    "name": "RealVariable",
                    "type": RealVariable,
                },
                {
                    "name": "BooleanVariable",
                    "type": BooleanVariable,
                },
                {
                    "name": "StringVariable",
                    "type": StringVariable,
                },
                {
                    "name": "ArrayVariable",
                    "type": ArrayVariable,
                },
                {
                    "name": "ArrayElement",
                    "type": ArrayElement,
                },
            ),
        },
    )
    choice_1: None | BooleanRhs | NumericRhs | StringRhs | ArrayRhs = field(
        default=None,
        metadata={
            "type": "Elements",
            "choices": (
                {
                    "name": "BooleanRHS",
                    "type": BooleanRhs,
                },
                {
                    "name": "NumericRHS",
                    "type": NumericRhs,
                },
                {
                    "name": "StringRHS",
                    "type": StringRhs,
                },
                {
                    "name": "ArrayRHS",
                    "type": ArrayRhs,
                },
            ),
        },
    )
    file_name: None | str = field(
        default=None,
        metadata={
            "name": "FileName",
            "type": "Attribute",
        },
    )
    line_no: None | int = field(
        default=None,
        metadata={
            "name": "LineNo",
            "type": "Attribute",
        },
    )
    col_no: None | int = field(
        default=None,
        metadata={
            "name": "ColNo",
            "type": "Attribute",
        },
    )
    epx: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )


@dataclass(kw_only=True)
class EndCondition(ConditionType):
    pass


@dataclass(kw_only=True)
class ExitCondition(ConditionType):
    pass


@dataclass(kw_only=True)
class InvariantCondition(ConditionType):
    pass


@dataclass(kw_only=True)
class PostCondition(ConditionType):
    pass


@dataclass(kw_only=True)
class PreCondition(ConditionType):
    pass


@dataclass(kw_only=True)
class RepeatCondition(ConditionType):
    pass


@dataclass(kw_only=True)
class ResourceList:
    resource: list[Resource] = field(
        default_factory=list,
        metadata={
            "name": "Resource",
            "type": "Element",
        },
    )
    file_name: None | str = field(
        default=None,
        metadata={
            "name": "FileName",
            "type": "Attribute",
        },
    )
    line_no: None | int = field(
        default=None,
        metadata={
            "name": "LineNo",
            "type": "Attribute",
        },
    )
    col_no: None | int = field(
        default=None,
        metadata={
            "name": "ColNo",
            "type": "Attribute",
        },
    )
    epx: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )


@dataclass(kw_only=True)
class SkipCondition(ConditionType):
    pass


@dataclass(kw_only=True)
class StartCondition(ConditionType):
    pass


@dataclass(kw_only=True)
class Command:
    resource_list: None | ResourceList = field(
        default=None,
        metadata={
            "name": "ResourceList",
            "type": "Element",
        },
    )
    choice: (
        None
        | IntegerVariable
        | RealVariable
        | BooleanVariable
        | StringVariable
        | ArrayVariable
        | ArrayElement
    ) = field(
        default=None,
        metadata={
            "type": "Elements",
            "choices": (
                {
                    "name": "IntegerVariable",
                    "type": IntegerVariable,
                },
                {
                    "name": "RealVariable",
                    "type": RealVariable,
                },
                {
                    "name": "BooleanVariable",
                    "type": BooleanVariable,
                },
                {
                    "name": "StringVariable",
                    "type": StringVariable,
                },
                {
                    "name": "ArrayVariable",
                    "type": ArrayVariable,
                },
                {
                    "name": "ArrayElement",
                    "type": ArrayElement,
                },
            ),
        },
    )
    name: Name = field(
        metadata={
            "name": "Name",
            "type": "Element",
        }
    )
    arguments: None | Arguments = field(
        default=None,
        metadata={
            "name": "Arguments",
            "type": "Element",
        },
    )
    file_name: None | str = field(
        default=None,
        metadata={
            "name": "FileName",
            "type": "Attribute",
        },
    )
    line_no: None | int = field(
        default=None,
        metadata={
            "name": "LineNo",
            "type": "Attribute",
        },
    )
    col_no: None | int = field(
        default=None,
        metadata={
            "name": "ColNo",
            "type": "Attribute",
        },
    )
    epx: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )


@dataclass(kw_only=True)
class CommandDeclaration:
    name: str = field(
        metadata={
            "name": "Name",
            "type": "Element",
            "namespace": "",
        }
    )
    return_value: None | Return = field(
        default=None,
        metadata={
            "name": "Return",
            "type": "Element",
        },
    )
    parameter: list[Parameter] = field(
        default_factory=list,
        metadata={
            "name": "Parameter",
            "type": "Element",
        },
    )
    any_parameters: None | object = field(
        default=None,
        metadata={
            "name": "AnyParameters",
            "type": "Element",
            "namespace": "",
        },
    )
    resource_list: None | ResourceList = field(
        default=None,
        metadata={
            "name": "ResourceList",
            "type": "Element",
        },
    )
    file_name: None | str = field(
        default=None,
        metadata={
            "name": "FileName",
            "type": "Attribute",
        },
    )
    line_no: None | int = field(
        default=None,
        metadata={
            "name": "LineNo",
            "type": "Attribute",
        },
    )
    col_no: None | int = field(
        default=None,
        metadata={
            "name": "ColNo",
            "type": "Attribute",
        },
    )
    epx: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )


@dataclass(kw_only=True)
class GlobalDeclarations:
    choice: list[
        CommandDeclaration
        | StateDeclaration
        | LibraryNodeDeclaration
        | DeclareMutex
        | int
    ] = field(
        default_factory=list,
        metadata={
            "type": "Elements",
            "choices": (
                {
                    "name": "CommandDeclaration",
                    "type": CommandDeclaration,
                },
                {
                    "name": "StateDeclaration",
                    "type": StateDeclaration,
                },
                {
                    "name": "LibraryNodeDeclaration",
                    "type": LibraryNodeDeclaration,
                },
                {
                    "name": "DeclareMutex",
                    "type": DeclareMutex,
                },
                {
                    "name": "TimeScalingUnitsSubunits",
                    "type": int,
                    "namespace": "",
                },
            ),
        },
    )
    file_name: None | str = field(
        default=None,
        metadata={
            "name": "FileName",
            "type": "Attribute",
        },
    )
    line_no: None | int = field(
        default=None,
        metadata={
            "name": "LineNo",
            "type": "Attribute",
        },
    )
    col_no: None | int = field(
        default=None,
        metadata={
            "name": "ColNo",
            "type": "Attribute",
        },
    )
    epx: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )


@dataclass(kw_only=True)
class NodeBody:
    choice: None | NodeList | Command | Assignment | Update | LibraryNodeCall = field(
        default=None,
        metadata={
            "type": "Elements",
            "choices": (
                {
                    "name": "NodeList",
                    "type": ForwardRef("NodeList"),
                },
                {
                    "name": "Command",
                    "type": Command,
                },
                {
                    "name": "Assignment",
                    "type": Assignment,
                },
                {
                    "name": "Update",
                    "type": Update,
                },
                {
                    "name": "LibraryNodeCall",
                    "type": LibraryNodeCall,
                },
            ),
        },
    )


@dataclass(kw_only=True)
class NodeActionType:
    assume: None | Assume = field(
        default=None,
        metadata={
            "name": "Assume",
            "type": "Element",
        },
    )
    desire: None | Desire = field(
        default=None,
        metadata={
            "name": "Desire",
            "type": "Element",
        },
    )
    expect: None | Expect = field(
        default=None,
        metadata={
            "name": "Expect",
            "type": "Element",
        },
    )
    variable_declarations: None | VariableDeclarations = field(
        default=None,
        metadata={
            "name": "VariableDeclarations",
            "type": "Element",
        },
    )
    interface: None | Interface = field(
        default=None,
        metadata={
            "name": "Interface",
            "type": "Element",
        },
    )
    using_mutex: None | UsingMutex = field(
        default=None,
        metadata={
            "name": "UsingMutex",
            "type": "Element",
        },
    )
    start_condition: None | StartCondition = field(
        default=None,
        metadata={
            "name": "StartCondition",
            "type": "Element",
        },
    )
    repeat_condition: None | RepeatCondition = field(
        default=None,
        metadata={
            "name": "RepeatCondition",
            "type": "Element",
        },
    )
    pre_condition: None | PreCondition = field(
        default=None,
        metadata={
            "name": "PreCondition",
            "type": "Element",
        },
    )
    post_condition: None | PostCondition = field(
        default=None,
        metadata={
            "name": "PostCondition",
            "type": "Element",
        },
    )
    invariant_condition: None | InvariantCondition = field(
        default=None,
        metadata={
            "name": "InvariantCondition",
            "type": "Element",
        },
    )
    end_condition: None | EndCondition = field(
        default=None,
        metadata={
            "name": "EndCondition",
            "type": "Element",
        },
    )
    exit_condition: None | ExitCondition = field(
        default=None,
        metadata={
            "name": "ExitCondition",
            "type": "Element",
        },
    )
    skip_condition: None | SkipCondition = field(
        default=None,
        metadata={
            "name": "SkipCondition",
            "type": "Element",
        },
    )
    comment: None | Comment = field(
        default=None,
        metadata={
            "name": "Comment",
            "type": "Element",
        },
    )
    priority: None | int = field(
        default=None,
        metadata={
            "name": "Priority",
            "type": "Element",
            "namespace": "",
        },
    )
    node_id: NodeId = field(
        metadata={
            "name": "NodeId",
            "type": "Element",
        }
    )
    node_body: None | NodeBody = field(
        default=None,
        metadata={
            "name": "NodeBody",
            "type": "Element",
        },
    )
    node_type: NodeTypeValue = field(
        metadata={
            "name": "NodeType",
            "type": "Attribute",
        }
    )
    file_name: None | str = field(
        default=None,
        metadata={
            "name": "FileName",
            "type": "Attribute",
        },
    )
    line_no: None | int = field(
        default=None,
        metadata={
            "name": "LineNo",
            "type": "Attribute",
        },
    )
    col_no: None | int = field(
        default=None,
        metadata={
            "name": "ColNo",
            "type": "Attribute",
        },
    )
    epx: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )


@dataclass(kw_only=True)
class Node(NodeActionType):
    pass


@dataclass(kw_only=True)
class NodeList:
    node: list[Node] = field(
        default_factory=list,
        metadata={
            "name": "Node",
            "type": "Element",
        },
    )
    file_name: None | str = field(
        default=None,
        metadata={
            "name": "FileName",
            "type": "Attribute",
        },
    )
    line_no: None | int = field(
        default=None,
        metadata={
            "name": "LineNo",
            "type": "Attribute",
        },
    )
    col_no: None | int = field(
        default=None,
        metadata={
            "name": "ColNo",
            "type": "Attribute",
        },
    )
    epx: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )


@dataclass(kw_only=True)
class PlexilPlan:
    global_declarations: None | GlobalDeclarations = field(
        default=None,
        metadata={
            "name": "GlobalDeclarations",
            "type": "Element",
        },
    )
    node: None | Node = field(
        default=None,
        metadata={
            "name": "Node",
            "type": "Element",
        },
    )
    file_name: None | str = field(
        default=None,
        metadata={
            "name": "FileName",
            "type": "Attribute",
        },
    )
    line_no: None | int = field(
        default=None,
        metadata={
            "name": "LineNo",
            "type": "Attribute",
        },
    )
    col_no: None | int = field(
        default=None,
        metadata={
            "name": "ColNo",
            "type": "Attribute",
        },
    )
    epx: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    w3_org_2001_xmlschema_instance_attributes: dict[str, str] = field(
        default_factory=dict,
        metadata={
            "type": "Attributes",
            "namespace": "http://www.w3.org/2001/XMLSchema-instance",
        },
    )
