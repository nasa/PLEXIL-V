"""Tests for PLEXILScript to PLEXIL-V Maude translator.

Based on PSX2MaudeTests.hs from the Haskell reference implementation.
"""

import pytest
from xsdata.formats.dataclass.parsers import XmlParser
from xsdata.formats.dataclass.parsers.config import ParserConfig

from plexil.plexilscript.v1 import (
    PLEXILScript,
    InitialState,
    Script,
    State,
    Command,
    CommandAck,
    CommandAbort,
    UpdateAck,
    Simultaneous,
    Delay,
    Param,
    TypeValue,
)
from plexilv.plexilscript.translator import translate


@pytest.fixture
def xml_parser():
    """Create an XML parser for PLEXILScript."""
    config = ParserConfig(
        process_xinclude=False,
        fail_on_unknown_properties=False,
    )
    return XmlParser(config=config)


class TestParameter:
    """Test Parameter translation."""

    def test_real_with_dot(self):
        """Real parameter with decimal point."""
        param = Param(value="10.0", type_value=TypeValue.REAL)
        from plexilv.plexilscript.translator.handlers import format_value

        assert format_value(param.value, param.type_value) == "val(10.0)"

    def test_real_without_dot(self):
        """Real parameter without decimal point (needs float cast)."""
        param = Param(value="10", type_value=TypeValue.REAL)
        from plexilv.plexilscript.translator.handlers import format_value

        assert format_value(param.value, param.type_value) == "val(float(10))"

    def test_int(self):
        """Integer parameter."""
        param = Param(value="11", type_value=TypeValue.INT)
        from plexilv.plexilscript.translator.handlers import format_value

        assert format_value(param.value, param.type_value) == "val(11)"

    def test_string(self):
        """String parameter."""
        param = Param(value="Valencia", type_value=TypeValue.STRING)
        from plexilv.plexilscript.translator.handlers import format_value

        assert format_value(param.value, param.type_value) == 'val("Valencia")'

    def test_bool_true_numeric(self):
        """Boolean parameter - true as 1."""
        param = Param(value="1", type_value=TypeValue.BOOL)
        from plexilv.plexilscript.translator.handlers import format_value

        assert format_value(param.value, param.type_value) == "val(true)"

    def test_bool_true_literal(self):
        """Boolean parameter - true as literal."""
        param = Param(value="true", type_value=TypeValue.BOOL)
        from plexilv.plexilscript.translator.handlers import format_value

        assert format_value(param.value, param.type_value) == "val(true)"

    def test_bool_false_literal(self):
        """Boolean parameter - false as literal."""
        param = Param(value="false", type_value=TypeValue.BOOL)
        from plexilv.plexilscript.translator.handlers import format_value

        assert format_value(param.value, param.type_value) == "val(false)"

    def test_unknown_bool(self):
        """Unknown boolean parameter."""
        param = Param(value="UNKNOWN", type_value=TypeValue.BOOL)
        from plexilv.plexilscript.translator.handlers import format_value

        assert format_value(param.value, param.type_value) == "unknown"

    def test_unknown_real(self):
        """Unknown real parameter."""
        param = Param(value="UNKNOWN", type_value=TypeValue.REAL)
        from plexilv.plexilscript.translator.handlers import format_value

        assert format_value(param.value, param.type_value) == "unknown"


class TestCommand:
    """Test Command translation."""

    def test_command_bool(self, xml_parser):
        """Command with bool result."""
        xml = '<Command name="get_bool" type="bool"><Result>1</Result></Command>'
        cmd = xml_parser.from_string(xml, Command)

        from plexilv.plexilscript.translator.handlers import translate_command
        from plexilv.common import IndentedWriter

        writer = IndentedWriter()
        translate_command(cmd, writer)
        output = writer.get_output().strip()

        assert output == "commandResult('get_bool,nilarg,val(true))"

    def test_command_string(self, xml_parser):
        """Command with string result."""
        xml = '<Command name="get_string" type="string"><Result>fred</Result></Command>'
        cmd = xml_parser.from_string(xml, Command)

        from plexilv.plexilscript.translator.handlers import translate_command
        from plexilv.common import IndentedWriter

        writer = IndentedWriter()
        translate_command(cmd, writer)
        output = writer.get_output().strip()

        assert output == 'commandResult(\'get_string,nilarg,val("fred"))'

    def test_command_int(self, xml_parser):
        """Command with int result."""
        xml = '<Command name="get_int" type="int"><Result>0</Result></Command>'
        cmd = xml_parser.from_string(xml, Command)

        from plexilv.plexilscript.translator.handlers import translate_command
        from plexilv.common import IndentedWriter

        writer = IndentedWriter()
        translate_command(cmd, writer)
        output = writer.get_output().strip()

        assert output == "commandResult('get_int,nilarg,val(0))"

    def test_command_real(self, xml_parser):
        """Command with real result."""
        xml = '<Command name="get_real" type="real"><Result>12.345</Result></Command>'
        cmd = xml_parser.from_string(xml, Command)

        from plexilv.plexilscript.translator.handlers import translate_command
        from plexilv.common import IndentedWriter

        writer = IndentedWriter()
        translate_command(cmd, writer)
        output = writer.get_output().strip()

        assert output == "commandResult('get_real,nilarg,val(12.345))"

    def test_command_bool_array(self, xml_parser):
        """Command with bool array result."""
        xml = '<Command name="boolArrayCommand" type="bool-array"><Result>1</Result><Result>1</Result><Result>1</Result></Command>'
        cmd = xml_parser.from_string(xml, Command)

        from plexilv.plexilscript.translator.handlers import translate_command
        from plexilv.common import IndentedWriter

        writer = IndentedWriter()
        translate_command(cmd, writer)
        output = writer.get_output().strip()

        assert (
            output
            == "commandResult('boolArrayCommand,nilarg,array(val(true) # val(true) # val(true)))"
        )

    def test_command_string_array(self, xml_parser):
        """Command with string array result."""
        xml = '<Command name="get_string_aray" type="string-array"><Result>john</Result><Result>paul</Result><Result>george</Result><Result>ringo</Result></Command>'
        cmd = xml_parser.from_string(xml, Command)

        from plexilv.plexilscript.translator.handlers import translate_command
        from plexilv.common import IndentedWriter

        writer = IndentedWriter()
        translate_command(cmd, writer)
        output = writer.get_output().strip()

        assert (
            output
            == 'commandResult(\'get_string_aray,nilarg,array(val("john") # val("paul") # val("george") # val("ringo")))'
        )

    def test_command_int_array(self, xml_parser):
        """Command with int array result."""
        xml = '<Command name="get_int_aray" type="int-array"><Result>1</Result><Result>2</Result><Result>3</Result></Command>'
        cmd = xml_parser.from_string(xml, Command)

        from plexilv.plexilscript.translator.handlers import translate_command
        from plexilv.common import IndentedWriter

        writer = IndentedWriter()
        translate_command(cmd, writer)
        output = writer.get_output().strip()

        assert (
            output
            == "commandResult('get_int_aray,nilarg,array(val(1) # val(2) # val(3)))"
        )

    def test_command_real_array(self, xml_parser):
        """Command with real array result."""
        xml = '<Command name="get_real_aray" type="real-array"><Result>1.1</Result><Result>2.2</Result><Result>3.3</Result></Command>'
        cmd = xml_parser.from_string(xml, Command)

        from plexilv.plexilscript.translator.handlers import translate_command
        from plexilv.common import IndentedWriter

        writer = IndentedWriter()
        translate_command(cmd, writer)
        output = writer.get_output().strip()

        assert (
            output
            == "commandResult('get_real_aray,nilarg,array(val(1.1) # val(2.2) # val(3.3)))"
        )

    def test_command_with_params(self, xml_parser):
        """Command with parameters."""
        xml = '<Command name="get_real" type="real"><Param type="string">param</Param><Result>1.1</Result></Command>'
        cmd = xml_parser.from_string(xml, Command)

        from plexilv.plexilscript.translator.handlers import translate_command
        from plexilv.common import IndentedWriter

        writer = IndentedWriter()
        translate_command(cmd, writer)
        output = writer.get_output().strip()

        assert output == 'commandResult(\'get_real,(val("param")),val(1.1))'


class TestCommandAck:
    """Test CommandAck translation."""

    def test_command_ack(self, xml_parser):
        """CommandAck with parameter."""
        xml = '<CommandAck name="foo" type="string"><Param type="string">fred</Param><Result>COMMAND_SUCCESS</Result></CommandAck>'
        ack = xml_parser.from_string(xml, CommandAck)

        from plexilv.plexilscript.translator.handlers import translate_command_ack
        from plexilv.common import IndentedWriter

        writer = IndentedWriter()
        translate_command_ack(ack, writer)
        output = writer.get_output().strip()

        assert output == 'commandAck(\'foo,(val("fred")),CommandSuccess)'

    def test_command_ack_multiple_params(self, xml_parser):
        """CommandAck with multiple parameters."""
        xml = '<CommandAck name="c2" type="int"><Param type="real">1</Param><Param type="int">10</Param><Result>COMMAND_DENIED</Result></CommandAck>'
        ack = xml_parser.from_string(xml, CommandAck)

        from plexilv.plexilscript.translator.handlers import translate_command_ack
        from plexilv.common import IndentedWriter

        writer = IndentedWriter()
        translate_command_ack(ack, writer)
        output = writer.get_output().strip()

        assert output == "commandAck('c2,(val(float(1)) val(10)),CommandDenied)"


class TestCommandAbort:
    """Test CommandAbort translation."""

    def test_command_abort_bool(self, xml_parser):
        """CommandAbort with bool result."""
        xml = '<CommandAbort name="ReceiveMessage" type="bool"><Param type="string">Foo</Param><Result>1</Result></CommandAbort>'
        abort = xml_parser.from_string(xml, CommandAbort)

        from plexilv.plexilscript.translator.handlers import translate_command_abort
        from plexilv.common import IndentedWriter

        writer = IndentedWriter()
        translate_command_abort(abort, writer)
        output = writer.get_output().strip()

        assert output == 'commandAbort(\'ReceiveMessage,(val("Foo")),val(true))'

    def test_command_abort_int(self, xml_parser):
        """CommandAbort with int result and unknown params."""
        xml = '<CommandAbort name="move_to_waypoint" type="int"><Param type="string">UNKNOWN</Param><Param type="real">4.0</Param><Param type="real">UNKNOWN</Param><Result>1</Result></CommandAbort>'
        abort = xml_parser.from_string(xml, CommandAbort)

        from plexilv.plexilscript.translator.handlers import translate_command_abort
        from plexilv.common import IndentedWriter

        writer = IndentedWriter()
        translate_command_abort(abort, writer)
        output = writer.get_output().strip()

        assert (
            output
            == "commandAbort('move_to_waypoint,(unknown val(4.0) unknown),val(1))"
        )


class TestState:
    """Test State lookup translation."""

    def test_state_int_array(self):
        """State with int array value."""
        state = State(
            name="st", param=[], value=["1", "2", "3"], type_value=TypeValue.INT_ARRAY
        )

        from plexilv.plexilscript.translator.handlers import translate_state
        from plexilv.common import IndentedWriter

        writer = IndentedWriter()
        translate_state(state, writer)
        output = writer.get_output().strip()

        assert output == "stateLookup('st,nilarg,array(val(1) # val(2) # val(3)))"

    def test_state_int(self):
        """State with int value."""
        state = State(name="st", param=[], value=["1"], type_value=TypeValue.INT)

        from plexilv.plexilscript.translator.handlers import translate_state
        from plexilv.common import IndentedWriter

        writer = IndentedWriter()
        translate_state(state, writer)
        output = writer.get_output().strip()

        assert output == "stateLookup('st,nilarg,val(1))"

    def test_state_string(self):
        """State with string value."""
        state = State(name="st", param=[], value=["one"], type_value=TypeValue.STRING)

        from plexilv.plexilscript.translator.handlers import translate_state
        from plexilv.common import IndentedWriter

        writer = IndentedWriter()
        translate_state(state, writer)
        output = writer.get_output().strip()

        assert output == 'stateLookup(\'st,nilarg,val("one"))'

    def test_state_with_params(self):
        """State with parameters."""
        state = State(
            name="st",
            param=[
                Param(value="1", type_value=TypeValue.REAL),
                Param(value="10", type_value=TypeValue.INT),
            ],
            value=["one", "two"],
            type_value=TypeValue.STRING,
        )

        from plexilv.plexilscript.translator.handlers import translate_state
        from plexilv.common import IndentedWriter

        writer = IndentedWriter()
        translate_state(state, writer)
        output = writer.get_output().strip()

        assert output == 'stateLookup(\'st,(val(float(1)) val(10)),val("one"))'

    def test_state_plexil_unknown_real(self):
        """State with Plexil_Unknown real value."""
        state = State(name="foo", param=[], value=["Plexil_Unknown"], type_value=TypeValue.REAL)

        from plexilv.plexilscript.translator.handlers import translate_state
        from plexilv.common import IndentedWriter

        writer = IndentedWriter()
        translate_state(state, writer)
        output = writer.get_output().strip()

        assert output == "stateLookup('foo,nilarg,unknown)"

    def test_state_plexil_unknown_int(self):
        """State with Plexil_Unknown int value."""
        state = State(name="bar", param=[], value=["Plexil_Unknown"], type_value=TypeValue.INT)

        from plexilv.plexilscript.translator.handlers import translate_state
        from plexilv.common import IndentedWriter

        writer = IndentedWriter()
        translate_state(state, writer)
        output = writer.get_output().strip()

        assert output == "stateLookup('bar,nilarg,unknown)"

    def test_state_plexil_unknown_bool(self):
        """State with Plexil_Unknown bool value."""
        state = State(name="baz", param=[], value=["Plexil_Unknown"], type_value=TypeValue.BOOL)

        from plexilv.plexilscript.translator.handlers import translate_state
        from plexilv.common import IndentedWriter

        writer = IndentedWriter()
        translate_state(state, writer)
        output = writer.get_output().strip()

        assert output == "stateLookup('baz,nilarg,unknown)"

    def test_state_plexil_unknown_string(self):
        """State with Plexil_Unknown string value."""
        state = State(name="qux", param=[], value=["Plexil_Unknown"], type_value=TypeValue.STRING)

        from plexilv.plexilscript.translator.handlers import translate_state
        from plexilv.common import IndentedWriter

        writer = IndentedWriter()
        translate_state(state, writer)
        output = writer.get_output().strip()

        assert output == "stateLookup('qux,nilarg,unknown)"


class TestUpdateAck:
    """Test UpdateAck translation."""

    def test_update_ack(self, xml_parser):
        """UpdateAck element."""
        xml = '<UpdateAck name="array8"/>'
        ack = xml_parser.from_string(xml, UpdateAck)

        from plexilv.plexilscript.translator.handlers import translate_update_ack
        from plexilv.common import IndentedWriter

        writer = IndentedWriter()
        translate_update_ack(ack, writer)
        output = writer.get_output().strip()

        assert output == "updateAck('array8,true)"


class TestDelay:
    """Test Delay translation."""

    def test_delay(self, xml_parser):
        """Delay element."""
        xml = "<Delay/>"
        delay = xml_parser.from_string(xml, Delay)

        from plexilv.plexilscript.translator.handlers import translate_delay
        from plexilv.common import IndentedWriter

        writer = IndentedWriter()
        translate_delay(delay, writer)
        output = writer.get_output().strip()

        assert output == "noInputs"


class TestScript:
    """Test Script translation."""

    def test_empty_script(self):
        """Empty script translates to nilEInputsList."""
        script = Script(choice=[])

        from plexilv.plexilscript.translator.handlers import translate
        from plexilv.common import IndentedWriter

        writer = IndentedWriter()
        translate(script, writer)
        output = writer.get_output().strip()

        assert output == "nilEInputsList"

    def test_script_with_update_ack(self, xml_parser):
        """Script with UpdateAck entry."""
        xml = '<Script><UpdateAck name="array8"/></Script>'
        script = xml_parser.from_string(xml, Script)

        from plexilv.plexilscript.translator.handlers import translate as trans_script
        from plexilv.common import IndentedWriter

        writer = IndentedWriter()
        trans_script(script, writer)
        output = writer.get_output().strip()

        assert output == "updateAck('array8,true)"


class TestInitialState:
    """Test InitialState translation."""

    def test_empty_initial_state(self):
        """Empty initial state translates to noInputs."""
        initial = InitialState(state=[])

        from plexilv.plexilscript.translator.handlers import translate_initial_state
        from plexilv.common import IndentedWriter

        writer = IndentedWriter()
        translate_initial_state(initial, writer)
        output = writer.get_output().strip()

        assert output == "noInputs"


class TestSimultaneous:
    """Test Simultaneous translation."""

    def test_simultaneous(self, xml_parser):
        """Simultaneous with multiple states."""
        xml = """<Simultaneous>
            <State name="time" type="real"><Value>0.5</Value></State>
            <State name="city" type="string"><Value>Valencia</Value></State>
        </Simultaneous>"""
        sim = xml_parser.from_string(xml, Simultaneous)

        from plexilv.plexilscript.translator.handlers import translate_simultaneous
        from plexilv.common import IndentedWriter

        writer = IndentedWriter()
        translate_simultaneous(sim, writer)
        output = writer.get_output().strip()

        # Should have two state lookups separated by newline
        lines = output.split("\n")
        assert len(lines) == 2
        assert "stateLookup('time,nilarg,val(0.5))" in lines[0]
        assert 'stateLookup(\'city,nilarg,val("Valencia"))' in lines[1]


class TestFullScript:
    """Test full PLEXILScript translation."""

    def test_complete_script(self, xml_parser):
        """Complete PLEXILScript with initial state and script."""
        xml = """<PLEXILScript>
            <InitialState>
                <State name="x" type="int"><Value>5</Value></State>
            </InitialState>
            <Script>
                <UpdateAck name="u1"/>
            </Script>
        </PLEXILScript>"""

        script = xml_parser.from_string(xml, PLEXILScript)
        output = translate(script)

        assert "mod INPUT is" in output
        assert "protecting PLEXIL-V ." in output
        assert "op input : -> InputGenerator ." in output
        assert "eq input = sequenceGenerator(" in output
        assert "stateLookup('x,nilarg,val(5))" in output
        assert "#" in output
        assert "updateAck('u1,true)" in output
        assert ") ." in output
        assert "endm" in output

    def test_minimal_script(self, xml_parser):
        """Minimal PLEXILScript with empty initial state and script."""
        xml = """<PLEXILScript>
            <InitialState/>
            <Script/>
        </PLEXILScript>"""

        script = xml_parser.from_string(xml, PLEXILScript)
        output = translate(script)

        assert "mod INPUT is" in output
        assert "noInputs" in output
        assert "nilEInputsList" in output
        assert "endm" in output
