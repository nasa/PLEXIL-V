import pytest
from plexil.core.v1.ast import (
    # Logical operators
    And,
    Or,
    Xor,
    Not,
    # Comparison operators
    Eqnumeric,
    Nenumeric,
    Gt,
    Lt,
    Ge,
    Le,
    Eqboolean,
    Neboolean,
    Eqstring,
    Nestring,
    # Arithmetic operators
    Add,
    Sub,
    Mul,
    Div,
    Mod,
    # Unary numeric functions
    Abs,
    Sqrt,
    Ceil,
    Floor,
    Round,
    Trunc,
    RealToInt,
    # N-ary numeric functions
    Max,
    Min,
    # Known test
    IsKnown,
)

# ====================
# Logical Operators
# ====================


def test_and_two_operands(translate_xml):
    xml = (
        "<AND><BooleanValue>true</BooleanValue><BooleanValue>false</BooleanValue></AND>"
    )
    assert translate_xml(xml, And) == "_and_(const(val(true)),const(val(false)))"


def test_and_three_operands(translate_xml):
    xml = "<AND><BooleanValue>true</BooleanValue><BooleanValue>true</BooleanValue><BooleanValue>false</BooleanValue></AND>"
    assert (
        translate_xml(xml, And)
        == "_and_(_and_(const(val(true)),const(val(true))),const(val(false)))"
    )


def test_or_two_operands(translate_xml):
    xml = "<OR><BooleanValue>true</BooleanValue><BooleanValue>false</BooleanValue></OR>"
    assert translate_xml(xml, Or) == "_or_(const(val(true)),const(val(false)))"


def test_or_three_operands(translate_xml):
    xml = "<OR><BooleanValue>true</BooleanValue><BooleanValue>false</BooleanValue><BooleanValue>true</BooleanValue></OR>"
    assert (
        translate_xml(xml, Or)
        == "_or_(_or_(const(val(true)),const(val(false))),const(val(true)))"
    )


def test_xor_two_operands(translate_xml):
    xml = (
        "<XOR><BooleanValue>true</BooleanValue><BooleanValue>false</BooleanValue></XOR>"
    )
    assert translate_xml(xml, Xor) == "_xor_(const(val(true)),const(val(false)))"


def test_xor_three_operands(translate_xml):
    xml = "<XOR><BooleanValue>true</BooleanValue><BooleanValue>true</BooleanValue><BooleanValue>false</BooleanValue></XOR>"
    assert (
        translate_xml(xml, Xor)
        == "_xor_(_xor_(const(val(true)),const(val(true))),const(val(false)))"
    )


def test_not_operator(translate_xml):
    xml = "<NOT><BooleanValue>false</BooleanValue></NOT>"
    assert translate_xml(xml, Not) == "not_(const(val(false)))"


# ====================
# Equality Operators
# ====================


def test_eq_boolean(translate_xml):
    xml = "<EQBoolean><BooleanValue>true</BooleanValue><BooleanValue>false</BooleanValue></EQBoolean>"
    assert translate_xml(xml, Eqboolean) == "_equ_(const(val(true)),const(val(false)))"


def test_ne_boolean(translate_xml):
    xml = "<NEBoolean><BooleanValue>true</BooleanValue><BooleanValue>false</BooleanValue></NEBoolean>"
    assert translate_xml(xml, Neboolean) == "_nequ_(const(val(true)),const(val(false)))"


def test_eq_numeric(translate_xml):
    xml = "<EQNumeric><IntegerValue>3</IntegerValue><IntegerValue>4</IntegerValue></EQNumeric>"
    assert translate_xml(xml, Eqnumeric) == "_equ_(const(val(3)),const(val(4)))"


def test_ne_numeric(translate_xml):
    xml = "<NENumeric><IntegerValue>3</IntegerValue><IntegerValue>4</IntegerValue></NENumeric>"
    assert translate_xml(xml, Nenumeric) == "_nequ_(const(val(3)),const(val(4)))"


def test_eq_string(translate_xml):
    xml = (
        "<EQString><StringValue>a</StringValue><StringValue>b</StringValue></EQString>"
    )
    assert translate_xml(xml, Eqstring) == '_equ_(const(val("a")),const(val("b")))'


def test_ne_string(translate_xml):
    xml = (
        "<NEString><StringValue>a</StringValue><StringValue>b</StringValue></NEString>"
    )
    assert translate_xml(xml, Nestring) == '_nequ_(const(val("a")),const(val("b")))'


# ====================
# Comparison Operators
# ====================


def test_gt_operator(translate_xml):
    xml = "<GT><IntegerValue>5</IntegerValue><IntegerValue>3</IntegerValue></GT>"
    assert translate_xml(xml, Gt) == "_>_(const(val(5)),const(val(3)))"


def test_lt_operator(translate_xml):
    xml = "<LT><IntegerValue>3</IntegerValue><IntegerValue>5</IntegerValue></LT>"
    assert translate_xml(xml, Lt) == "_<_(const(val(3)),const(val(5)))"


def test_ge_operator(translate_xml):
    xml = (
        "<GE><RealVariable>speedPref</RealVariable><IntegerValue>0</IntegerValue></GE>"
    )
    assert translate_xml(xml, Ge) == "_>=_(var('speedPref),const(val(0)))"


def test_le_operator(translate_xml):
    xml = "<LE><IntegerValue>3</IntegerValue><IntegerValue>5</IntegerValue></LE>"
    assert translate_xml(xml, Le) == "_<=_(const(val(3)),const(val(5)))"


# ====================
# Arithmetic Operators
# ====================


def test_add_two_operands(translate_xml):
    xml = "<ADD><IntegerValue>3</IntegerValue><IntegerValue>4</IntegerValue></ADD>"
    assert translate_xml(xml, Add) == "_+_(const(val(3)),const(val(4)))"


def test_add_three_operands(translate_xml):
    xml = "<ADD><IntegerValue>1</IntegerValue><IntegerValue>2</IntegerValue><IntegerValue>3</IntegerValue></ADD>"
    assert (
        translate_xml(xml, Add) == "_+_(_+_(const(val(1)),const(val(2))),const(val(3)))"
    )


def test_sub_two_operands(translate_xml):
    xml = "<SUB><IntegerValue>10</IntegerValue><IntegerValue>3</IntegerValue></SUB>"
    assert translate_xml(xml, Sub) == "_-_(const(val(10)),const(val(3)))"


def test_mul_two_operands(translate_xml):
    xml = "<MUL><IntegerValue>3</IntegerValue><IntegerValue>4</IntegerValue></MUL>"
    assert translate_xml(xml, Mul) == "_*_(const(val(3)),const(val(4)))"


def test_mul_three_operands(translate_xml):
    xml = "<MUL><IntegerValue>2</IntegerValue><IntegerValue>3</IntegerValue><IntegerValue>4</IntegerValue></MUL>"
    assert (
        translate_xml(xml, Mul) == "_*_(_*_(const(val(2)),const(val(3))),const(val(4)))"
    )


def test_div_operator(translate_xml):
    xml = "<DIV><IntegerValue>10</IntegerValue><IntegerValue>2</IntegerValue></DIV>"
    assert translate_xml(xml, Div) == "_/_(const(val(10)),const(val(2)))"


def test_mod_operator(translate_xml):
    xml = "<MOD><IntegerValue>10</IntegerValue><IntegerValue>3</IntegerValue></MOD>"
    assert translate_xml(xml, Mod) == "_rem_(const(val(10)),const(val(3)))"


# ====================
# Unary Numeric Functions
# ====================


def test_abs_function(translate_xml):
    xml = "<ABS><IntegerValue>-5</IntegerValue></ABS>"
    assert translate_xml(xml, Abs) == "func(absp,const(val(-5)))"


def test_sqrt_function(translate_xml):
    xml = "<SQRT><RealValue>16.0</RealValue></SQRT>"
    assert translate_xml(xml, Sqrt) == "func(sqrt,const(val(16.0)))"


def test_ceil_function(translate_xml):
    xml = "<CEIL><RealValue>3.2</RealValue></CEIL>"
    assert translate_xml(xml, Ceil) == "func(ceiling,const(val(3.2)))"


def test_floor_function(translate_xml):
    xml = "<FLOOR><RealValue>3.8</RealValue></FLOOR>"
    assert translate_xml(xml, Floor) == "func(floor,const(val(3.8)))"


def test_round_function(translate_xml):
    xml = "<ROUND><RealValue>3.5</RealValue></ROUND>"
    assert translate_xml(xml, Round) == "func(round,const(val(3.5)))"


def test_trunc_function(translate_xml):
    xml = "<TRUNC><RealValue>3.9</RealValue></TRUNC>"
    assert translate_xml(xml, Trunc) == "func(trunc,const(val(3.9)))"


def test_real_to_int_function(translate_xml):
    xml = "<RealToInt><RealValue>3.7</RealValue></RealToInt>"
    assert translate_xml(xml, RealToInt) == "func(real-to-int,const(val(3.7)))"


# ====================
# N-ary Numeric Functions
# ====================


def test_max_two_operands(translate_xml):
    xml = "<MAX><IntegerValue>5</IntegerValue><IntegerValue>3</IntegerValue></MAX>"
    assert translate_xml(xml, Max) == "_max_(const(val(5)),const(val(3)))"


def test_max_three_operands(translate_xml):
    xml = "<MAX><IntegerValue>5</IntegerValue><IntegerValue>3</IntegerValue><IntegerValue>7</IntegerValue></MAX>"
    assert (
        translate_xml(xml, Max)
        == "_max_(_max_(const(val(5)),const(val(3))),const(val(7)))"
    )


def test_min_two_operands(translate_xml):
    xml = "<MIN><IntegerValue>5</IntegerValue><IntegerValue>3</IntegerValue></MIN>"
    assert translate_xml(xml, Min) == "_min_(const(val(5)),const(val(3)))"


def test_min_three_operands(translate_xml):
    xml = "<MIN><IntegerValue>5</IntegerValue><IntegerValue>3</IntegerValue><IntegerValue>7</IntegerValue></MIN>"
    assert (
        translate_xml(xml, Min)
        == "_min_(_min_(const(val(5)),const(val(3))),const(val(7)))"
    )


# ====================
# Known Test
# ====================


def test_is_known(translate_xml):
    xml = "<IsKnown><BooleanValue>true</BooleanValue></IsKnown>"
    assert translate_xml(xml, IsKnown) == "isKnown(const(val(true)))"
