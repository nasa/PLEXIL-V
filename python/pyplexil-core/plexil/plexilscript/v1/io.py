import sys
from pathlib import Path
from xsdata.formats.dataclass.parsers import XmlParser
from xsdata.formats.dataclass.parsers.config import ParserConfig
from xsdata.formats.dataclass.serializers import XmlSerializer
from xsdata.formats.dataclass.serializers.config import SerializerConfig
from .ast import PLEXILScript


def parse_plexilscript_file(input_file: Path, debug: bool = False) -> PLEXILScript:
    """
    Parse a PLEXILScript XML file and return a PLEXILScript object.

    Args:
        input_file: Path to the input PLEXILScript XML file
        debug: Enable debug output

    Returns:
        PLEXILScript object parsed from the XML file

    Raises:
        FileNotFoundError: If the input file doesn't exist
        Exception: If parsing fails
    """
    if not input_file.exists():
        raise FileNotFoundError(f"Input file not found: {input_file}")

    if debug:
        print(f"Parsing file: {input_file}", file=sys.stderr)
        print(f"File size: {input_file.stat().st_size} bytes", file=sys.stderr)

    # Create XML parser with config to ignore unknown properties
    config = ParserConfig(fail_on_unknown_properties=False)
    parser = XmlParser(config=config)

    try:
        # Read and parse the XML file
        with open(input_file, "r", encoding="utf-8") as f:
            xml_content = f.read()

        if debug:
            print(f"XML content length: {len(xml_content)} characters", file=sys.stderr)
            print("Attempting to parse XML...", file=sys.stderr)

        # Parse to PLEXILScript object
        plexil_script = parser.from_string(xml_content, PLEXILScript)

        if debug:
            print("✓ Parsing successful!", file=sys.stderr)
            print(f"PLEXILScript type: {type(plexil_script)}", file=sys.stderr)

            # Print some basic information about the parsed script
            if hasattr(plexil_script, "script") and plexil_script.script:
                print(
                    f"Script elements found: {len(plexil_script.script.choice)}",
                    file=sys.stderr,
                )

            if hasattr(plexil_script, "initial_state") and plexil_script.initial_state:
                print("InitialState found", file=sys.stderr)

        return plexil_script

    except Exception as e:
        if debug:
            print(f"✗ Parsing failed!", file=sys.stderr)
            import traceback

            traceback.print_exc(file=sys.stderr)
        raise Exception(f"Failed to parse PLEXILScript XML: {e}") from e


def serialize_plexilscript(plexil_script: PLEXILScript, debug: bool = False) -> str:
    """
    Serialize a PLEXILScript object back to XML string.

    Args:
        plexil_script: PLEXILScript object to serialize
        debug: Enable debug output

    Returns:
        XML string representation of the PLEXILScript
    """
    if debug:
        print("Serializing PLEXILScript back to XML...", file=sys.stderr)

    # Create serializer with pretty print configuration
    config = SerializerConfig(indent="  ")
    serializer = XmlSerializer(config=config)

    try:
        xml_output = serializer.render(plexil_script)

        if debug:
            print(f"✓ Serialization successful!", file=sys.stderr)
            print(f"Output XML length: {len(xml_output)} characters", file=sys.stderr)

        return xml_output

    except Exception as e:
        if debug:
            print(f"✗ Serialization failed!", file=sys.stderr)
            import traceback

            traceback.print_exc(file=sys.stderr)
        raise Exception(f"Failed to serialize PLEXILScript: {e}") from e
