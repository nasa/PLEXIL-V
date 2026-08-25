import argparse
import re
from antlr4 import *

from ..shared.antlr_generated.PlexilScriptLexer import PlexilScriptLexer
from ..shared.antlr_generated.PlexilScriptParser import PlexilScriptParser
from ..shared import XmlGenerator

def main():
    parser = argparse.ArgumentParser(
        description="Compile a PLEXIL script file to XML.")
    parser.add_argument(
        "input", type=str,
        help="Path to the input file")
    parser.add_argument(
        "-o", "--output", type=str,
        help="Path to an output file")
    parser.add_argument(
        '-c', '--condense', action='store_true',
        help="Condense XML output by removing whitespace between tags")

    args = parser.parse_args()

    with open(args.input, 'r', encoding='utf-8') as file:
        file_content = file.read()

    input_stream = InputStream(file_content)
    input_lexer = PlexilScriptLexer(input_stream)
    input_token_stream = CommonTokenStream(input_lexer)
    input_parser = PlexilScriptParser(input_token_stream)
    input_tree = input_parser.plexilScript()
    xml_visitor = XmlGenerator()

    xml_output = xml_visitor.visit(input_tree)

    if args.condense:
        xml_output = re.sub(r'>\s+<', '><', xml_output)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as file:
            file.write(xml_output)
    else:
        print(xml_output)

if __name__ == '__main__':
    main()