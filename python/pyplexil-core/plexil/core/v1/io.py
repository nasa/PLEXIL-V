import sys
from pathlib import Path
from xsdata.formats.dataclass.parsers import XmlParser
from xsdata.formats.dataclass.serializers import XmlSerializer
from xsdata.formats.dataclass.serializers.config import SerializerConfig
from .ast import PlexilPlan


def parse_plexil_file(input_file: Path, debug: bool = False) -> PlexilPlan:
    """
    Parse a PLEXIL XML file and return a PlexilPlan object.

    Args:
        input_file: Path to the input PLEXIL XML file
        debug: Enable debug output

    Returns:
        PlexilPlan object parsed from the XML file

    Raises:
        FileNotFoundError: If the input file doesn't exist
        Exception: If parsing fails
    """
    if not input_file.exists():
        raise FileNotFoundError(f"Input file not found: {input_file}")

    if debug:
        print(f"Parsing file: {input_file}", file=sys.stderr)
        print(f"File size: {input_file.stat().st_size} bytes", file=sys.stderr)

    # Create XML parser
    parser = XmlParser()

    try:
        # Read and parse the XML file
        with open(input_file, "r", encoding="utf-8") as f:
            xml_content = f.read()

        if debug:
            print(f"XML content length: {len(xml_content)} characters", file=sys.stderr)
            print("Attempting to parse XML...", file=sys.stderr)

        # Parse to PlexilPlan object
        plexil_plan = parser.from_string(xml_content, PlexilPlan)

        if debug:
            print("✓ Parsing successful!", file=sys.stderr)
            print(f"PlexilPlan type: {type(plexil_plan)}", file=sys.stderr)

            # Print some basic information about the parsed plan
            if hasattr(plexil_plan, "node") and plexil_plan.node:
                print(
                    f"Root node found: {plexil_plan.node.node_id if hasattr(plexil_plan.node, 'node_id') else 'No NodeId'}",
                    file=sys.stderr,
                )

            if (
                hasattr(plexil_plan, "global_declarations")
                and plexil_plan.global_declarations
            ):
                print("GlobalDeclarations found", file=sys.stderr)

        return plexil_plan

    except Exception as e:
        if debug:
            print(f"✗ Parsing failed!", file=sys.stderr)
            import traceback

            traceback.print_exc(file=sys.stderr)
        raise Exception(f"Failed to parse PLEXIL XML: {e}") from e


def serialize_plexil(plexil_plan: PlexilPlan, debug: bool = False) -> str:
    """
    Serialize a PlexilPlan object back to XML string.

    Args:
        plexil_plan: PlexilPlan object to serialize
        debug: Enable debug output

    Returns:
        XML string representation of the PlexilPlan
    """
    if debug:
        print("Serializing PlexilPlan back to XML...", file=sys.stderr)

    # Create serializer with pretty print configuration
    config = SerializerConfig(indent="  ")
    serializer = XmlSerializer(config=config)

    try:
        xml_output = serializer.render(plexil_plan)

        if debug:
            print(f"✓ Serialization successful!", file=sys.stderr)
            print(f"Output XML length: {len(xml_output)} characters", file=sys.stderr)

        return xml_output

    except Exception as e:
        if debug:
            print(f"✗ Serialization failed!", file=sys.stderr)
            import traceback

            traceback.print_exc(file=sys.stderr)
        raise Exception(f"Failed to serialize PlexilPlan: {e}") from e
