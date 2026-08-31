import pytest
from xsdata.formats.dataclass.parsers import XmlParser
from xsdata.formats.dataclass.parsers.config import ParserConfig
from plexil.core.v1.ast import PlexilPlan
from plexilv.plexil.translator.dispatch import translate as translate_node, walk
from plexilv.common import IndentedWriter
from plexilv.plexil.translator.state import TranspilerContext
from plexilv.plexil.translator import translate


def normalize_whitespace(text: str) -> str:
    """Remove all whitespace except inside double quotes.

    This makes tests immune to single-line vs multi-line formatting differences
    while preserving whitespace in string literals.

    Examples:
        >>> normalize_whitespace('library(\\n  "hello world",\\n  foo\\n)')
        'library("hello world",foo)'
    """
    result = []
    inside_quotes = False

    for char in text:
        if char == '"':
            inside_quotes = not inside_quotes
            result.append(char)
        elif inside_quotes:
            # Preserve all characters including whitespace inside quotes
            result.append(char)
        elif not char.isspace():
            # Outside quotes, skip whitespace
            result.append(char)

    return ''.join(result)


@pytest.fixture
def translate_xml():
    """Fixture that provides a helper function to translate XML snippets."""

    def _translate(xml_input, node_class):
        parser = XmlParser()
        writer = IndentedWriter()
        context = TranspilerContext()

        value = parser.from_string(xml_input, node_class)
        walk(value, writer, context)

        return writer.get_output().strip()

    return _translate


@pytest.fixture
def translate_xml_with_libraries():
    """Translate XML fragment to PLEXIL-V with library support.

    Usage:
        result = translate_xml_with_libraries(
            main_xml,
            Node,
            libraries={'libName': library_xml}
        )
    """

    def _translate(
        xml_str: str, result_type: type, libraries: dict[str, str] | None = None
    ):
        from plexil.core.v1.ast import PlexilPlan as PP, Node, Node

        config = ParserConfig(
            process_xinclude=False,
            fail_on_unknown_properties=False,
        )
        parser = XmlParser(config=config)

        # Parse main node directly as Node (or result_type)
        parsed_main = parser.from_string(xml_str, result_type)

        # Parse library nodes as Node and wrap in PlexilPlan structure
        library_asts = {}
        if libraries:
            for lib_name, lib_xml in libraries.items():
                # Parse library node directly as Node
                lib_node = parser.from_string(lib_xml, Node)

                # Wrap in PlexilPlan
                lib_plan = PP(node=lib_node)
                library_asts[lib_name] = lib_plan

        # Transpile with libraries
        writer = IndentedWriter()
        context = TranspilerContext(libraries=library_asts)
        walk(parsed_main, writer, context)
        return writer.get_output().strip()

    return _translate
