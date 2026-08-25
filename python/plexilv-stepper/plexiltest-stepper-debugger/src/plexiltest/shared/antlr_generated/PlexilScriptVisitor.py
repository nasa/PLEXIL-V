# Generated from PlexilScript.g4 by ANTLR 4.13.1
from antlr4 import *
if "." in __name__:
    from .PlexilScriptParser import PlexilScriptParser
else:
    from PlexilScriptParser import PlexilScriptParser

# This class defines a complete generic visitor for a parse tree produced by PlexilScriptParser.

class PlexilScriptVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by PlexilScriptParser#plexilScript.
    def visitPlexilScript(self, ctx:PlexilScriptParser.PlexilScriptContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PlexilScriptParser#elements.
    def visitElements(self, ctx:PlexilScriptParser.ElementsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PlexilScriptParser#element.
    def visitElement(self, ctx:PlexilScriptParser.ElementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PlexilScriptParser#initialState.
    def visitInitialState(self, ctx:PlexilScriptParser.InitialStateContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PlexilScriptParser#simultaneous.
    def visitSimultaneous(self, ctx:PlexilScriptParser.SimultaneousContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PlexilScriptParser#script.
    def visitScript(self, ctx:PlexilScriptParser.ScriptContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PlexilScriptParser#updateAck.
    def visitUpdateAck(self, ctx:PlexilScriptParser.UpdateAckContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PlexilScriptParser#stateDef.
    def visitStateDef(self, ctx:PlexilScriptParser.StateDefContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PlexilScriptParser#functionCall.
    def visitFunctionCall(self, ctx:PlexilScriptParser.FunctionCallContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PlexilScriptParser#command.
    def visitCommand(self, ctx:PlexilScriptParser.CommandContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PlexilScriptParser#commandAbort.
    def visitCommandAbort(self, ctx:PlexilScriptParser.CommandAbortContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PlexilScriptParser#commandAck.
    def visitCommandAck(self, ctx:PlexilScriptParser.CommandAckContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PlexilScriptParser#commandAccepted.
    def visitCommandAccepted(self, ctx:PlexilScriptParser.CommandAcceptedContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PlexilScriptParser#commandDenied.
    def visitCommandDenied(self, ctx:PlexilScriptParser.CommandDeniedContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PlexilScriptParser#commandSentToSystem.
    def visitCommandSentToSystem(self, ctx:PlexilScriptParser.CommandSentToSystemContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PlexilScriptParser#commandRcvdBySystem.
    def visitCommandRcvdBySystem(self, ctx:PlexilScriptParser.CommandRcvdBySystemContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PlexilScriptParser#commandSuccess.
    def visitCommandSuccess(self, ctx:PlexilScriptParser.CommandSuccessContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PlexilScriptParser#commandFailed.
    def visitCommandFailed(self, ctx:PlexilScriptParser.CommandFailedContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PlexilScriptParser#delay.
    def visitDelay(self, ctx:PlexilScriptParser.DelayContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PlexilScriptParser#parameters.
    def visitParameters(self, ctx:PlexilScriptParser.ParametersContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PlexilScriptParser#parameter.
    def visitParameter(self, ctx:PlexilScriptParser.ParameterContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PlexilScriptParser#values.
    def visitValues(self, ctx:PlexilScriptParser.ValuesContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PlexilScriptParser#results.
    def visitResults(self, ctx:PlexilScriptParser.ResultsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PlexilScriptParser#value.
    def visitValue(self, ctx:PlexilScriptParser.ValueContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PlexilScriptParser#type.
    def visitType(self, ctx:PlexilScriptParser.TypeContext):
        return self.visitChildren(ctx)



del PlexilScriptParser