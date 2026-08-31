"""Condition translation handlers"""

from ..dispatch import translate, walk
from plexilv.common import IndentedWriter
from ..state import TranspilerContext
from ._helpers import *
from plexil.core.v1 import *


@translate.register(StartCondition)
def _(node: StartCondition, writer: IndentedWriter, context: TranspilerContext):
    """Translate start condition."""
    translate_condition("startc", node, writer, context)


@translate.register(EndCondition)
def _(node: EndCondition, writer: IndentedWriter, context: TranspilerContext):
    """Translate end condition."""
    translate_condition("endc", node, writer, context)


@translate.register(PreCondition)
def _(node: PreCondition, writer: IndentedWriter, context: TranspilerContext):
    """Translate pre-condition."""
    translate_condition("pre", node, writer, context)


@translate.register(PostCondition)
def _(node: PostCondition, writer: IndentedWriter, context: TranspilerContext):
    """Translate post-condition."""
    translate_condition("post", node, writer, context)


@translate.register(InvariantCondition)
def _(node: InvariantCondition, writer: IndentedWriter, context: TranspilerContext):
    """Translate invariant condition."""
    translate_condition("inv", node, writer, context)


@translate.register(RepeatCondition)
def _(node: RepeatCondition, writer: IndentedWriter, context: TranspilerContext):
    """Translate repeat condition."""
    translate_condition("repeatc", node, writer, context)


@translate.register(ExitCondition)
def _(node: ExitCondition, writer: IndentedWriter, context: TranspilerContext):
    """Translate exit condition."""
    translate_condition("exitc", node, writer, context)


@translate.register(SkipCondition)
def _(node: SkipCondition, writer: IndentedWriter, context: TranspilerContext):
    """Translate skip condition."""
    translate_condition("skip", node, writer, context)
