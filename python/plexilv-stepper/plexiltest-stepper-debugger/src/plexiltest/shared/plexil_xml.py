import xml.etree.ElementTree as ET
from typing import Dict, Any, List, Union

def get_declared_variables(xml_source: str, is_file: bool = True) -> Dict[str, Dict[str, Any]]:
    """
    Extract declared variables from an XML PLEXIL Plan.

    Args:
        xml_source: A file path or XML string.
        is_file: True if xml_source is a file path.

    Returns:
        A dictionary that maps each variable's name to its details:
        {   <variable's name> :
            {
                "type" : <variable's type>,
                "array_size" : <array variable's size> (0 if scalar)
                "value" : <variable's initial value> (unknown if unspecified)
            }
        }
    """
    if is_file:
        tree = ET.parse(xml_source)
        root = tree.getroot()
    else:
        root = ET.fromstring(xml_source)

    results = {}

    for node in root.findall('.//DeclareVariable') + root.findall('.//DeclareArray'):
        # Get the variable name
        name_node = node.find('Name')
        if name_node is None:
            raise ValueError("Found declared variable without a name.")
        name = name_node.text
        if name in results:
            raise ValueError(f"Found duplicate variable name {name}. " +
                              "Duplicate variable names are not supported.")

        # Get the variable type and string-to-type conversion method using the
        # same type strings as PlexilScript XML. These are slightly different
        # than what the PLEXIL Exec uses.
        type_node = node.find('Type')
        if type_node is None:
            raise ValueError(f"Declared variable {name} does not have a type.")
        type = type_node.text

        if type == 'Real':
            converter = float
        elif type == 'Integer':
            converter = int
        elif type == 'Boolean':
            converter = lambda val: str(val).strip().lower() in ('true', '1')
        else:
            converter = str

        # Get the array size (0 if scalar)
        is_array = (node.tag == 'DeclareArray')
        if is_array:
            size_node = node.find('MaxSize')
            if size_node is None:
                raise ValueError(f"Declared array {name} has no max size.")
            else:
                array_size = int(size_node.text)
        else:
            array_size = 0

        # Get the variable's initial value
        def type_tag(type) :
          return f"{type}Value"

        init_node = node.find('InitialValue')
        initial_value = ["UNKNOWN"] * array_size if is_array else "UNKNOWN"
        if init_node is not None:
            if is_array:
                array_value_node = init_node.find('ArrayValue')
                if array_value_node is not None:
                    prefix_values = []
                    for child in array_value_node.findall(type_tag(type)):
                        if child.text is None:
                            raise ValueError(
                                f"Declared array variable {name} has a " +
                                f"{type_tag(type)} element without a value")
                        prefix_values.append(converter(child.text))
                        if len(prefix_values) > len(initial_value):
                            raise ValueError(
                                f"Declared array variable {name} has too " +
                                f"many {type_tag(type)} elements.")
                        initial_value[:len(prefix_values)] = prefix_values
            else:
                scalar_node = init_node.find(type_tag(type))
                if scalar_node.text is None:
                    raise ValueError(
                                f"Declared variable {name} has a " +
                                f"{type_tag(type)} element without a value.")
                initial_value = converter(scalar_node.text)

        results[name] = {
            "type" : type,
            "array_size" : array_size,
            "value" : initial_value
        }

    return results


def get_state_declarations(xml_source: str, is_file: bool = True) -> Dict[str, Dict[str, Any]]:
    """
    Parses a PLEXIL Plan XML and extracts StateDeclarations, including their return types
    and parameter specifications.

    Args:
        xml_source: A file path or an XML string.
        is_file: True if xml_source is a file path, False if it's an XML string.

    Returns:
        A dictionary mapping the StateDeclaration Name to its details:
        {
            "StateName": {
                "return_type": "type-string",
                "parameters": [{"name": "param_name", "type": "param_type"}, ...],
                "any_parameters": bool
            }
        }
    """
    if is_file:
        tree = ET.parse(xml_source)
        root = tree.getroot()
    else:
        root = ET.fromstring(xml_source)

    state_map = {}

    for state_decl in root.findall('.//StateDeclaration'):
        name_node = state_decl.find('Name')
        if name_node is None or not name_node.text:
            continue

        state_name = name_node.text.strip()

        # --- Extract Return Type ---
        state_type = "unknown" # Fallback
        type_node = state_decl.find('./Return/Type')
        if type_node is not None and type_node.text:
            state_type = type_node.text.strip()
            # If MaxSize is present, it's an array
            if state_decl.find('./Return/MaxSize') is not None:
                state_type += "-array"

        # --- Extract Parameters ---
        parameters: List[Dict[str, str]] = []
        for param_node in state_decl.findall('Parameter'):
            p_name_node = param_node.find('Name')
            p_type_node = param_node.find('Type')

            p_name = p_name_node.text.strip() if (p_name_node is not None and p_name_node.text) else None

            if p_type_node is not None and p_type_node.text:
                p_type = p_type_node.text.strip()
                if param_node.find('MaxSize') is not None:
                    p_type += "-array"

                parameters.append({
                    "name": p_name,
                    "type": p_type
                })

        # --- Check for AnyParameters flag ---
        any_parameters = state_decl.find('AnyParameters') is not None

        # --- Save to Map ---
        state_map[state_name] = {
            "return_type": state_type,
            "parameters": parameters,
            "any_parameters": any_parameters
        }

    return state_map


def parse_bool(val: str) -> bool:
    """Convert an XML string boolean to a Python bool."""
    if not val:
        return False
    return val.strip().lower() in ('true', '1')

def parse_int(val: str) -> int:
    """Convert an XML string integer to a Python int."""
    return int(val.strip())

def parse_real(val: str) -> float:
    """Convert an XML string real to a Python float."""
    return float(val.strip())

def parse_string(val: str) -> str:
    """Convert an XML string to a Python str."""
    return str(val) if val is not None else ""

# Map the PLEXIL base types to their respective parsing functions
_TYPE_PARSERS = {
    'bool': parse_bool,
    'int': parse_int,
    'real': parse_real,
    'string': parse_string
}

def convert_type(value: str, type_attr: str) -> Any:
    """
    Translates a single XML string value to the appropriate Python type
    based on the PLEXIL schema type attribute.
    """
    if not type_attr:
        return value # Default to returning the raw string if no type is provided

    # Handle arrays (assuming array elements are passed in one at a time,
    # or you are mapping this over multiple <Value> elements)
    is_array = type_attr.endswith('-array')
    base_type = type_attr.replace('-array', '') if is_array else type_attr

    if base_type not in _TYPE_PARSERS:
        raise ValueError(f"Unknown PLEXIL type: {type_attr}")

    parser = _TYPE_PARSERS[base_type]

    # Note: If the XML represents arrays as a single comma/space-separated string inside
    # one <Value> tag, you would split it here. However, your schema uses
    # maxOccurs="unbounded" for <Value>, meaning arrays are likely multiple <Value> tags.
    # Therefore, this function converts individual values.
    return parser(value)

def extract_node_values(node: ET.Element) -> Union[Any, List[Any]]:
    """
    Extracts and converts all <Value> or <Result> child elements of a given node
    (like <State>, <Param>, or <Command>) based on the node's 'type' attribute.
    """
    type_attr = node.get('type', 'string')

    # In the schema, values are either in <Value> or <Result> tags, or text in <Param>
    value_nodes = node.findall('Value') or node.findall('Result')

    # If there are no sub-elements, it might be a <Param> containing direct text
    if not value_nodes:
        text = node.text or ""
        return convert_type(text, type_attr)

    # Convert all extracted text nodes
    converted_values = [convert_type(v.text or "", type_attr) for v in value_nodes]

    # If the schema explicitly says it's an array, or if there's more than one value, return a list
    if type_attr.endswith('-array') or len(converted_values) > 1:
        return converted_values

    # Otherwise, return the single scalar value
    return converted_values[0] if converted_values else None