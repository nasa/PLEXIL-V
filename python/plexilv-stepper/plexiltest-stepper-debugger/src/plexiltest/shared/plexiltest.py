import ctypes
from enum import Enum, auto
from typing import NamedTuple
from pprint import PrettyPrinter
import re

import xml.etree.ElementTree as ET

from .utils import load_stepper_library
from .interpreters import StepperInterpreter
from .plexil_xml import get_declared_variables

lib = load_stepper_library()

## ctypes types and interfaces
class NodeStateOutcomePair(ctypes.Structure):
    _fields_ = [
        ("outcome", ctypes.c_uint8),
        ("state", ctypes.c_uint8),
    ]

lib.Stepper_new.restype = ctypes.c_void_p
lib.Stepper_new.argtypes = [
    ctypes.c_char_p,
    ctypes.POINTER(ctypes.c_char_p), ctypes.c_int,
    ctypes.POINTER(ctypes.c_char_p), ctypes.c_int
]

lib.Stepper_delete.argtypes = [ctypes.c_void_p]
lib.Stepper_delete.restype = None

lib.Stepper_getNodeStateOutcomes.argtypes = [
    ctypes.c_void_p,
    ctypes.POINTER(ctypes.POINTER(ctypes.c_char_p)),
    ctypes.POINTER(ctypes.c_int)
]
lib.Stepper_getNodeStateOutcomes.restype = ctypes.POINTER(NodeStateOutcomePair)

lib.Stepper_getVariables.argtypes = [
    ctypes.c_void_p,                                  # Stepper* s
    ctypes.POINTER(ctypes.POINTER(ctypes.c_char_p)),  # const char*** varNames
    ctypes.POINTER(ctypes.POINTER(ctypes.c_char_p)),  # const char*** valStrings
    ctypes.POINTER(ctypes.c_char_p),                  # const char** typeStrings
    ctypes.POINTER(ctypes.c_int)                      # int* count
]
lib.Stepper_getVariables.restype = None

lib.Stepper_step.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_size_t]
lib.Stepper_step.restype = ctypes.c_int

lib.Stepper_needsStep.argtypes = [ctypes.c_void_p]
lib.Stepper_needsStep.restype = ctypes.c_bool

lib.Stepper_needsInitialState.argtypes = [ctypes.c_void_p]
lib.Stepper_needsInitialState.restype = ctypes.c_bool

lib.NodeOutcomeEnum_toStringLiteral.argtypes = [ctypes.c_uint8]
lib.NodeOutcomeEnum_toStringLiteral.restype = ctypes.c_char_p

lib.NodeStateEnum_toStringLiteral.argtypes = [ctypes.c_uint8]
lib.NodeStateEnum_toStringLiteral.restype = ctypes.c_char_p

lib.ValueTypeEnum_toStringLiteral.argtypes = [ctypes.c_uint8]
lib.ValueTypeEnum_toStringLiteral.restype = ctypes.c_char_p

lib.charArray_delete.argtypes = [ctypes.c_void_p]
lib.charArray_delete.restype = None

lib.arrayOfCharArray_delete.argtypes = [ctypes.POINTER(ctypes.c_char_p)]
lib.arrayOfCharArray_delete.restype = None


def get_node_names_states_and_outcomes(stepper_ptr):
    node_name_c_strs = ctypes.POINTER(ctypes.c_char_p)()
    count = ctypes.c_int()
    node_state_outcome_pairs = lib.Stepper_getNodeStateOutcomes(stepper_ptr, ctypes.byref(node_name_c_strs), ctypes.byref(count))
    node_names = [node_name_c_strs[i].decode('utf-8') for i in range(count.value)]
    lib.arrayOfCharArray_delete(node_name_c_strs, count)
    node_states = [lib.NodeStateEnum_toStringLiteral(node_state_outcome_pairs[i].state).decode('utf-8') for i in range(count.value)]
    node_outcomes = [lib.NodeOutcomeEnum_toStringLiteral(node_state_outcome_pairs[i].outcome).decode('utf-8') for i in range(count.value)]
    lib.arrayOfNodeStateOutcomePair_delete(node_state_outcome_pairs)
    return [node_names, node_states, node_outcomes]


def get_variable_names_and_values(stepper_ptr):
    var_name_c_strs = ctypes.POINTER(ctypes.c_char_p)()
    var_val_c_strs = ctypes.POINTER(ctypes.c_char_p)()
    MAX_LITERAL_LEN = 100
    var_type_c_strs_buffer = (ctypes.c_char_p * MAX_LITERAL_LEN)()
    count = ctypes.c_int()
    lib.Stepper_getVariables(stepper_ptr,
                             ctypes.byref(var_name_c_strs),
                             ctypes.byref(var_val_c_strs),
                             var_type_c_strs_buffer,
                             ctypes.byref(count))
    var_names = [var_name_c_strs[i].decode('utf-8') for i in range(count.value)]
    var_vals = [var_val_c_strs[i].decode('utf-8') for i in range(count.value)]
    var_types = [var_type_c_strs_buffer[i].decode('utf-8') for i in range(count.value)]
    lib.arrayOfCharArray_delete(var_name_c_strs, count.value)
    lib.arrayOfCharArray_delete(var_val_c_strs, count.value)
    return [var_names, var_vals, var_types]


## Python class and auxiliary functions
class ExecutiveParsingError(Exception):
    pass


class ExecutiveError(Exception):
    pass


class MultipleInitialStateError(Exception):
    pass


class NodeStateEnum(Enum):
    NO_NODE_STATE = auto()
    INACTIVE_STATE = auto()
    WAITING_STATE = auto()
    EXECUTING_STATE = auto()
    ITERATION_ENDED_STATE = auto()
    FINISHED_STATE = auto()
    FAILING_STATE = auto()
    FINISHING_STATE = auto()
    UNDEFINED_STATE = auto()

    @property
    def short_name(self):
        if self.name.endswith('_STATE'):
            return self.name[:-6]
        return self.name

    def __str__(self):
        return self.short_name

    def __repr__(self):
        return self.__str__()


class NodeOutcomeEnum(Enum):
    NO_OUTCOME = auto()
    SUCCESS_OUTCOME = auto()
    FAILURE_OUTCOME = auto()
    SKIPPED_OUTCOME = auto()
    INTERRUPTED_OUTCOME = auto()
    UNDEFINED_OUTCOME = auto()

    @property
    def short_name(self):
        if self.name.endswith('_OUTCOME') and not self.name.startswith('NO'):
            return self.name[:-8]
        return self.name

    def __str__(self):
        return self.short_name

    def __repr__(self):
        return self.__str__()


class NodeStateOutcomePair(NamedTuple):
    state: NodeStateEnum
    outcome: NodeOutcomeEnum

    @classmethod
    def from_strings(cls, state_str, outcome_str):
        state = NodeStateEnum[state_str]
        outcome = NodeOutcomeEnum[outcome_str]
        return cls(state, outcome)

    def __str__(self):
        return f"({self.state}, {self.outcome})"

    def __repr__(self):
        return self.__str__()


class PLEXILTest(StepperInterpreter):
    _nodes = {}
    _vars = {}
    _stepper_ptr = None
    _err_code = 0
    _err_string = None

    def __init__(self, plan, library_names=[], library_paths=[]):

        utf_library_names = [name.encode('utf-8') for name in library_names]
        utf_library_paths = [path.encode('utf-8') for path in library_paths]

        library_names_arr = (ctypes.c_char_p * len(utf_library_names))(*utf_library_names)
        library_paths_arr = (ctypes.c_char_p * len(utf_library_paths))(*utf_library_paths)
        self._stepper_ptr = lib.Stepper_new(plan.encode('utf-8'),
                                            library_names_arr, len(library_names_arr),
                                            library_paths_arr, len(library_paths_arr))
        if self._stepper_ptr is None:
            raise RuntimeError("Received null pointer during construction of Stepper")
        with open(plan, 'r', encoding='utf-8') as f:
            xml_string = f.read()
        root = ET.fromstring(xml_string)
        node_names = [nodeid.text for nodeid in root.findall('.//NodeId')]
        for node_name in node_names:
            self._nodes[node_name] = NodeStateOutcomePair(
                                        NodeStateEnum.INACTIVE_STATE,
                                        NodeOutcomeEnum.NO_OUTCOME)
        vars = get_declared_variables(plan)
        self._vars = vars

    def needs_initial_state(self):
        return lib.Stepper_needsInitialState(self._stepper_ptr)

    def needs_step(self):
        return lib.Stepper_needsStep(self._stepper_ptr)

    def step(self, script_input):
        max_error_len = 1024
        error_buffer = ctypes.create_string_buffer(max_error_len)
        self._err_code = lib.Stepper_step(
            self._stepper_ptr,
            script_input.encode('utf-8'),
            error_buffer,
            max_error_len
        )
        if self._err_code > 0:
            self._err_string = error_buffer.value.decode('utf-8')
            if self._err_code == 1:
                raise ExecutiveParsingError(self._err_string)
            if self._err_code == 2:
                raise ExecutiveError(self._err_string)
            if self._err_code > 2:
                raise Exception(self._err_string)

        [var_names, val_strs, type_strs] = get_variable_names_and_values(self._stepper_ptr)

        def converter(type_str: str):
            if "real" in type_str.lower():
                return float
            elif "boolean" in type_str.lower():
                return lambda val: str(val).strip().lower() in ('true', '1')
            elif "integer" in type_str.lower():
                converter = int
            else:
                converter = str
            return converter

        def convert(val_str, type_str):
            if 'unknown' in val_str.lower():
                return 'UNKNOWN'
            else:
                return converter(type_str)(val_str)

        def get_name_and_array_index(var_name: str):
            pattern = r"^([a-zA-Z][a-zA-Z0-9_\-.]+)(?:\[(\d+)\])?\s*$"
            match = re.search(pattern, var_name)
            if match:
                name = match.group(1)
                index = int(match.group(2)) if match.group(2) else None
                return name, index
            else:
                return var_name, None

        def get_array(val_str: str, type_str: str):
            match = re.search(r"^#\((.*?)\)$", val_str.strip(), re.DOTALL)
            if match:
                array_content = match.group(1)
                return [convert(i, type_str) for i in array_content.split()]
            return None

        for var_name, val_str, type_str in zip(var_names, val_strs, type_strs):
            if var_name not in self._vars:
                raise ValueError(
                    f"Received update for variable{var_name}, which was not" +
                    f"in the plan's declared variable list")

            declared_type = self._vars[var_name]["type"].lower()
            declared_length = self._vars[var_name]["array_size"]

            if declared_type not in type_str.lower():
                raise ValueError(
                    f"Received variable {var_name} has type {type_str} " +
                    f"different than declared type {declared_type}")

            # Value received from PLEXIL Exec is a whole array
            if "array_type" in type_str.lower():
                arr = get_array(val_str, type_str)
                if len(arr) > declared_length:
                    raise ValueError(
                        f"Received array {arr} with length larger than " +
                        f"declared length {declared_length}")
                self._vars[var_name]["value"][:len(arr)-1] = arr
            else:
                name, array_index = get_name_and_array_index(var_name)
                if array_index is not None:
                    # Value received from PLEXIL Exec is an array element
                    if declared_length == 0:
                        raise ValueError(
                            f"Received array element for non-array variable" +
                            f"{var_name}")
                    if array_index >= declared_length:
                        raise ValueError(
                            f"Received array element for index {array_index} " +
                            f"greater than array length {declared_length}")
                    self._vars[name]["value"][array_index] = \
                        convert(val_str, type_str)
                else:
                    if declared_length > 0:
                        raise ValueError(
                            f"Received scalar for array variable {var_name}")
                    self._vars[name]["value"] = convert(val_str, type_str)

        [node_names, node_states, node_outcomes] = get_node_names_states_and_outcomes(self._stepper_ptr)
        for node_name, node_state, node_outcome in zip(node_names, node_states, node_outcomes):
            self._nodes[node_name] = NodeStateOutcomePair.from_strings(node_state, node_outcome)

    @property
    def err_code(self):
        return self._err_code

    @property
    def err_string(self):
        return None if self._err_code == 0 else self._err_string

    @property
    def nodes(self):
        return self._nodes

    @property
    def variables(self):
        return self._vars

    def get_current_state(self) -> dict:
        flattened_variables = {key: inner_dict['value'] for key, inner_dict
                               in self.variables.items()}
        return {
            "nodes" : self.nodes,
            "variables" : flattened_variables,
        }

    def pprint_str(self):
        pp = PrettyPrinter(indent=4, width=80, compact=False)
        state = self.get_current_state()
        nodes_str = '\n'.join(f"  {k}: {pp.pformat(v)}"
                          for k, v in state["nodes"].items())
        vars_str = '\n'.join(f"  {k}: {pp.pformat(v)}"
                         for k, v in state["variables"].items())
        return 'Nodes:\n' + nodes_str + '\n\nVariables:\n' + vars_str

    def _delete_stepper_ptr(self):
        if self._stepper_ptr:
            lib.Stepper_delete(self._stepper_ptr)
            self._stepper_ptr = None

    def __del__(self):
        if getattr(self, '_stepper_ptr', None):
            self._delete_stepper_ptr()