"""Shared XML parsing utilities for PLEXIL formats."""

from xsdata.formats.dataclass.parsers import XmlParser
from xsdata.formats.dataclass.parsers.config import ParserConfig


def create_parser() -> XmlParser:
    """Create standard XML parser with PLEXIL-compatible configuration.

    Returns:
        XmlParser configured for PLEXIL XML formats
    """
    config = ParserConfig(
        process_xinclude=False,
        fail_on_unknown_properties=False,
    )
    return XmlParser(config=config)
