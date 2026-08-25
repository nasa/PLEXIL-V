from antlr4 import FileStream, CommonTokenStream, InputStream
from antlr4.error.ErrorListener import ErrorListener

# Import the generated classes
from .antlr_generated.PlexilScriptLexer import PlexilScriptLexer
from .antlr_generated.PlexilScriptParser import PlexilScriptParser
from .antlr_generated.PlexilScriptVisitor import PlexilScriptVisitor


class ScriptParsingError(Exception):
    pass


class ScriptErrorListener(ErrorListener):
    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        raise ScriptParsingError(f"line_{line},col_{column}: {msg}")


class XmlGenerator(PlexilScriptVisitor):
    """
    "Compiles" a script in PlexilScript grammar to XML.

    This class implements the visitor pattern over an ANTLR-generated parse
    tree, overriding 'visit<X>' methods for all rules <X> in the PlexilScript
    grammar. Each visitor method returns XML elements that conform to the
    PLEXIL XML schema for scripts.
    """

    def __init__(self):
        super().__init__()
        self._indent_level = 0

    def _increase_indent(self):
        self._indent_level += 1

    def _decrease_indent(self):
        self._indent_level -= 1

    def _indent(self, str):
        return self._indent_level * '  ' + str

    #  plexilScript : elements EOF ;
    def visitPlexilScript(self, ctx: PlexilScriptParser.PlexilScriptContext):
        xml_out = '<PLEXILScript>\n'
        self._increase_indent()
        if ctx.elements():
            xml_out += self.visit(ctx.elements())
        self._decrease_indent()
        xml_out += '</PLEXILScript>'
        return xml_out

    # elements : element* ;
    def visitElements(self, ctx: PlexilScriptParser.ElementsContext):
        xml_out = ''
        for el in ctx.element():
            xml_str = self.visit(el)
            if xml_str:
                xml_out += xml_str
        return xml_out

    # initialState : 'initial-state' LBRACE elements RBRACE ;
    def visitInitialState(self, ctx:PlexilScriptParser.InitialStateContext):
        xml_out = ''
        if ctx.elements().element():
            xml_out += self._indent('<InitialState>\n')
            self._increase_indent()
            xml_out += self.visit(ctx.elements())
            self._decrease_indent()
            xml_out += self._indent('</InitialState>\n')
            return xml_out
        else:
            xml_out += self._indent('<InitialState/>\n')
        return xml_out

    # simultaneous : 'simultaneous' LBRACE elements RBRACE ;
    def visitSimultaneous(self, ctx:PlexilScriptParser.SimultaneousContext):
        xml_out = self._indent('<Simultaneous>\n')

        self._increase_indent()
        if ctx.elements():
            xml_out += self.visit(ctx.elements())
        self._decrease_indent()

        xml_out += self._indent('</Simultaneous>\n')
        return xml_out

    # script : 'script' LBRACE elements RBRACE ;
    def visitScript(self, ctx:PlexilScriptParser.ScriptContext):
        xml_out = ''
        if ctx.elements().element():
            xml_out += self._indent('<Script>\n')
            self._increase_indent()
            xml_out += self.visit(ctx.elements())
            self._decrease_indent()
            xml_out += self._indent('</Script>\n')
            return xml_out
        else:
            xml_out += self._indent('<Script/>\n')
        return xml_out

    # updateAck : 'update-ack' ID SEMI ;
    def visitUpdateAck(self, ctx:PlexilScriptParser.UpdateAckContext):
        id = ctx.ID()
        xml_out = self._indent(f'<UpdateAck name="{id}"/>\n')
        return xml_out

    # stateDef : 'state' ID parameters EQUALS values COLON type SEMI
    def visitStateDef(self, ctx: PlexilScriptParser.StateDefContext):
        name = ctx.ID().getText()
        data_type = ctx.type_().getText()
        xml_out = self._indent(f'<State name="{name}" type="{data_type}">\n')

        self._increase_indent()
        if ctx.parameters():
            xml_out += self.visit(ctx.parameters())
        if ctx.values():
            xml_out += self.visit(ctx.values())
        self._decrease_indent()

        xml_out += self._indent('</State>\n')
        return xml_out

    # functionCall : 'function-call' ID parameters EQUALS values COLON type SEMI ;
    # I think this has been removed
    # def visitFunctionCall(self, ctx:PlexilScriptParser.FunctionCallContext):
    #     name = ctx.ID().getText()
    #     data_type = ctx.type_().getText()
    #     xml_out = self._indent(f'<FunctionCall name="{name}" type="{data_type}">\n')
    #     return self.visitChildren(ctx)

    # 'command' ID parameters EQUALS results COLON type SEMI ;
    def visitCommand(self, ctx:PlexilScriptParser.CommandContext):
        name = ctx.ID().getText()
        data_type = ctx.type_().getText()
        xml_out = self._indent(f'<Command name="{name}" type="{data_type}">\n')

        self._increase_indent()
        if ctx.parameters():
            xml_out += self.visit(ctx.parameters())
        if ctx.results():
            xml_out += self.visit(ctx.results())
        self._decrease_indent()

        xml_out += self._indent(f'</Command>\n')
        return xml_out

    # commandAbort : 'command-abort' ID parameters EQUALS results COLON type SEMI ;
    def visitCommandAbort(self, ctx:PlexilScriptParser.CommandAbortContext):
        name = ctx.ID().getText()
        data_type = ctx.type_().getText()
        xml_out = self._indent(f'<CommandAbort name="{name}" type="{data_type}">\n')

        self._increase_indent()
        if ctx.parameters():
            xml_out += self.visit(ctx.parameters())
        if ctx.results():
            xml_out += self.visit(ctx.results())
        self._decrease_indent()

        xml_out += self._indent(f'</CommandAbort>\n')
        return xml_out

    # commandAck : 'command-ack' ID parameters EQUALS results COLON type SEMI ;
    def visitCommandAck(self, ctx:PlexilScriptParser.CommandAckContext):
        name = ctx.ID().getText()
        data_type = ctx.type_().getText()
        xml_out = self._indent(f'<CommandAck name="{name}" type="{data_type}">\n')

        self._increase_indent()
        if ctx.parameters():
            xml_out += self.visit(ctx.parameters())
        if ctx.results():
            xml_out += self.visit(ctx.results())
        self._decrease_indent()

        xml_out += self._indent(f'</CommandAck>\n')
        return xml_out

    # commandAccepted : 'command-accepted' ID parameters SEMI ;
    def visitCommandAccepted(self, ctx:PlexilScriptParser.CommandAcceptedContext):
        name = ctx.ID().getText()
        xml_out = self._indent(f'<CommandAck name="{name}">\n')

        self._increase_indent()
        if ctx.parameters():
            xml_out += self.visit(ctx.parameters())
        xml_out += self._indent(f'<Result>COMMAND_ACCEPTED</Result>\n')
        self._decrease_indent()

        xml_out += self._indent(f'</CommandAck>\n')
        return xml_out

    # commandDenied : 'command-denied' ID parameters SEMI ;
    def visitCommandDenied(self, ctx:PlexilScriptParser.CommandDeniedContext):
        name = ctx.ID().getText()
        xml_out = self._indent(f'<CommandAck name="{name}">\n')

        self._increase_indent()
        if ctx.parameters():
            xml_out += self.visit(ctx.parameters())
        xml_out += self._indent(f'<Result>COMMAND_DENIED</Result>\n')
        self._decrease_indent()

        xml_out += self._indent(f'</CommandAck>\n')
        return xml_out

    # commandSentToSystem : 'command-sent-to-system' ID parameters SEMI ;
    def visitCommandSentToSystem(self, ctx:PlexilScriptParser.CommandSentToSystemContext):
        name = ctx.ID().getText()
        xml_out = self._indent(f'<CommandAck name="{name}">\n')

        self._increase_indent()
        if ctx.parameters():
            xml_out += self.visit(ctx.parameters())
        xml_out += self._indent(f'<Result>COMMAND_SENT_TO_SYSTEM</Result>\n')
        self._decrease_indent()

        xml_out += self._indent(f'</CommandAck>\n')
        return xml_out

    # commandRcvdBySystem : 'command-rcvd-by-system' ID parameters SEMI ;
    def visitCommandRcvdBySystem(self, ctx:PlexilScriptParser.CommandRcvdBySystemContext):
        name = ctx.ID().getText()
        xml_out = self._indent(f'<CommandAck name="{name}">\n')

        self._increase_indent()
        if ctx.parameters():
            xml_out += self.visit(ctx.parameters())
        xml_out += self._indent(f'<Result>COMMAND_RCVD_BY_SYSTEM</Result>\n')
        self._decrease_indent()

        xml_out += self._indent(f'</CommandAck>\n')
        return xml_out

    # commandSuccess : 'command-success' ID parameters SEMI ;
    def visitCommandSuccess(self, ctx:PlexilScriptParser.CommandSuccessContext):
        name = ctx.ID().getText()
        xml_out = self._indent(f'<CommandAck name="{name}" type="string">\n')

        self._increase_indent()
        if ctx.parameters():
            xml_out += self.visit(ctx.parameters())
        xml_out += self._indent(f'<Result>COMMAND_SUCCESS</Result>\n')
        self._decrease_indent()

        xml_out += self._indent(f'</CommandAck>\n')
        return xml_out

    # commandFailed : 'command-failed' ID parameters SEMI ;
    def visitCommandFailed(self, ctx:PlexilScriptParser.CommandFailedContext):
        name = ctx.ID().getText()
        xml_out = self._indent(f'<CommandAck name="{name}">\n')

        self._increase_indent()
        if ctx.parameters():
            xml_out += self.visit(ctx.parameters())
        xml_out += self._indent(f'<Result>COMMAND_FAILED</Result>\n')
        self._decrease_indent()

        xml_out += self._indent(f'</CommandAck>\n')
        return xml_out

    # delay : 'delay' SEMI ;
    def visitDelay(self, ctx: PlexilScriptParser.DelayContext):
        return self._indent(f'<Delay/>\n')

    # parameters : LPAREN (parameter (COMMA parameter)*)? RPAREN ;
    def visitParameters(self, ctx: PlexilScriptParser.ParametersContext):
        xml_out = ''
        for param in ctx.parameter():
            t = param.type_().getText()
            xml_out += self._indent(f'<Param type="{t}">{self.visit(param)}</Param>\n')
        return xml_out

    # parameter : value COLON type ;
    def visitParameter(self, ctx: PlexilScriptParser.ParameterContext):
        return self.visit(ctx.value())

    # values : value | LPAREN value (COMMA value)* RPAREN ;
    def visitValues(self, ctx:PlexilScriptParser.ValuesContext):
        xml_out = ''
        for val_ctx in ctx.value():
            xml_out += self._indent('<Value>')
            xml_out += self.visit(val_ctx)
            xml_out += '</Value>\n'
        return xml_out

    # results : value | LPAREN value (COMMA value)* RPAREN ;
    def visitResults(self, ctx:PlexilScriptParser.ResultsContext):
        xml_out = ''
        for val_ctx in ctx.value():
            xml_out += self._indent('<Result>')
            xml_out += self.visit(val_ctx)
            xml_out += '</Result>\n'
        return xml_out

    # value : 'true' | 'false' | UNKNOWN | STRING | NUMBER ;
    def visitValue(self, ctx:PlexilScriptParser.ValueContext):
        text = ctx.getText()
        if ctx.UNKNOWN() is not None:
            return 'Plexil_Unknown'
        elif ctx.STRING() is not None:
            return text.strip('"')
        else:
            return text


class ScriptElementExtractor(PlexilScriptVisitor):
    """
    Extracts text blocks from a script in the PlexilScript grammar.

    This class implements the visitor pattern over an ANTLR-generated parse
    tree, overriding 'visit<X>' methods for all rules <X> in the PlexilScript
    grammar. Each visitor method returns the original text for the rule.
    """
    def __init__(self):
        self.initial_state_element = None
        self.script_sub_elements = []

    def _get_raw_text(self, ctx):
        """Get source text of an arbitrary 'element'"""
        start_idx = ctx.start.start
        stop_idx = ctx.stop.stop
        input_stream = ctx.start.getInputStream()
        return input_stream.getText(start_idx, stop_idx)

    def visitInitialState(self, ctx: PlexilScriptParser.InitialStateContext):
        """Get source text an 'initialState' element"""
        self.initial_state_element = self._get_raw_text(ctx)
        return self.visitChildren(ctx)

    def visitScript(self, ctx: PlexilScriptParser.ScriptContext):
        """Get a list of source text for all sub-elements of a 'script' element"""
        elements_ctx = ctx.elements()
        if elements_ctx:
            for element_ctx in elements_ctx.element():
                element_text = self._get_raw_text(element_ctx)
                self.script_sub_elements.append(element_text)
        return self.visitChildren(ctx)


def _get_element_parse_method(parser, pst_input: str):
    clean_text = pst_input.lower().strip()

    prefix_method_pairs = [
        ('initial-state', parser.initialState),
        ('simultaneous', parser.simultaneous),
        ('update-ack', parser.updateAck),
        ('state', parser.stateDef),
        ('command-abort', parser.commandAbort),
        ('command-ack', parser.commandAck),
        ('command-accepted', parser.commandAccepted),
        ('command-denied', parser.commandDenied),
        ('command-sent-to-system', parser.commandSentToSystem),
        ('command-rcvd-by-system', parser.commandRcvdBySystem),
        ('command-success', parser.commandSuccess),
        ('command-failed', parser.commandFailed),
        ('command', parser.command),
        ('delay', parser.delay)
    ]

    for prefix, method in prefix_method_pairs:
        if clean_text.startswith(prefix):
            return method()

    raise ValueError(f"Could not determine PlexilScript element type for: '{pst_input}'")


def extract_elements_from_script(filepath):
    """Extract top-level elements from a script in the PlexilScript grammar.

    Args:
        filepath: Path to a script file in .pst format.

    Returns:
        (initial_state_element, script_sub_elements): A tuple containing the
         string for the 'initial-state' element (including its sub-elements)
         and a list of strings for the sub-elements of the 'script'.
    """
    input_stream = FileStream(filepath, encoding='utf-8')
    lexer = PlexilScriptLexer(input_stream)
    lexer.removeErrorListeners()
    lexer.addErrorListener(ScriptErrorListener())

    token_stream = CommonTokenStream(lexer)
    parser = PlexilScriptParser(token_stream)
    parser.removeErrorListeners()
    parser.addErrorListener(ScriptErrorListener())

    tree = parser.plexilScript()
    extractor = ScriptElementExtractor()
    extractor.visit(tree)
    return extractor.initial_state_element, extractor.script_sub_elements


def is_initial_state_element(pst_input: str):
    """Check whether a string is an 'initial-state' element"""
    if pst_input.lower().strip().startswith('initial-state'):
        return True
    else:
        return False


def convert_script_element_to_xml(input_str):
    """'Compile' an individual PlexilScript grammar element to XML"""
    input_stream = InputStream(input_str)
    lexer = PlexilScriptLexer(input_stream)
    lexer.removeErrorListeners()
    lexer.addErrorListener(ScriptErrorListener())

    token_stream = CommonTokenStream(lexer)
    parser = PlexilScriptParser(token_stream)
    parser.removeErrorListeners()
    parser.addErrorListener(ScriptErrorListener())
    parse_method = _get_element_parse_method(parser, input_str)

    xml_generator = XmlGenerator()
    xml_output = xml_generator.visit(parse_method)

    return xml_output