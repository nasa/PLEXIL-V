"""Tests for PLEXILScript AST parsing and serialization."""

import pytest
from xsdata.formats.dataclass.parsers import XmlParser
from xsdata.formats.dataclass.parsers.config import ParserConfig
from xsdata.formats.dataclass.serializers import XmlSerializer
from xsdata.formats.dataclass.serializers.config import SerializerConfig

from plexil.plexilscript.v1.ast import (
    PLEXILScript,
    Script,
    InitialState,
    State,
    Command,
    CommandAck,
    CommandAbort,
    UpdateAck,
    Simultaneous,
    SendPlan,
    Delay,
    Param,
    TypeValue,
)

# ====================
# Fixtures
# ====================


@pytest.fixture
def parser():
    """Create XML parser with appropriate config."""
    config = ParserConfig(fail_on_unknown_properties=False)
    return XmlParser(config=config)


@pytest.fixture
def serializer():
    """Create XML serializer with appropriate config."""
    config = SerializerConfig(indent="  ")
    return XmlSerializer(config=config)


# ====================
# Basic Parsing Tests
# ====================


def test_empty_script(parser):
    """Test parsing an empty PLEXILScript."""
    xml = "<PLEXILScript><Script/></PLEXILScript>"
    script = parser.from_string(xml, PLEXILScript)

    assert script is not None
    assert isinstance(script, PLEXILScript)
    assert script.script is not None
    assert len(script.script.choice) == 0
    assert script.initial_state is None


def test_initial_state_only(parser):
    """Test parsing PLEXILScript with only InitialState."""
    xml = """<PLEXILScript>
      <InitialState>
        <State name="x" type="int">
          <Value>5</Value>
        </State>
      </InitialState>
      <Script/>
    </PLEXILScript>"""

    script = parser.from_string(xml, PLEXILScript)

    assert script.initial_state is not None
    assert len(script.initial_state.state) == 1
    assert script.initial_state.state[0].name == "x"
    assert script.initial_state.state[0].type_value == TypeValue.INT
    assert script.initial_state.state[0].value == ["5"]


def test_state_element(parser):
    """Test parsing State element."""
    xml = """<PLEXILScript>
      <Script>
        <State name="temperature" type="real">
          <Value>98.6</Value>
        </State>
      </Script>
    </PLEXILScript>"""

    script = parser.from_string(xml, PLEXILScript)

    assert len(script.script.choice) == 1
    state = script.script.choice[0]
    assert isinstance(state, State)
    assert state.name == "temperature"
    assert state.type_value == TypeValue.REAL
    assert state.value == ["98.6"]


def test_state_with_params(parser):
    """Test parsing State with parameters."""
    xml = """<PLEXILScript>
      <Script>
        <State name="position" type="real">
          <Param type="int">0</Param>
          <Param type="int">1</Param>
          <Value>10.5</Value>
          <Value>20.3</Value>
        </State>
      </Script>
    </PLEXILScript>"""

    script = parser.from_string(xml, PLEXILScript)

    state = script.script.choice[0]
    assert isinstance(state, State)
    assert len(state.param) == 2
    assert state.param[0].value == "0"
    assert state.param[0].type_value == TypeValue.INT
    assert state.param[1].value == "1"
    assert len(state.value) == 2
    assert state.value == ["10.5", "20.3"]


def test_command_element(parser):
    """Test parsing Command element."""
    xml = """<PLEXILScript>
      <Script>
        <Command name="drive" type="int">
          <Result>1</Result>
        </Command>
      </Script>
    </PLEXILScript>"""

    script = parser.from_string(xml, PLEXILScript)

    assert len(script.script.choice) == 1
    cmd = script.script.choice[0]
    assert isinstance(cmd, Command)
    assert cmd.name == "drive"
    assert cmd.type_value == TypeValue.INT
    assert cmd.result == ["1"]


def test_command_with_params(parser):
    """Test parsing Command with parameters."""
    xml = """<PLEXILScript>
      <Script>
        <Command name="setSpeed" type="int">
          <Param type="real">100.5</Param>
          <Result>0</Result>
        </Command>
      </Script>
    </PLEXILScript>"""

    script = parser.from_string(xml, PLEXILScript)

    cmd = script.script.choice[0]
    assert isinstance(cmd, Command)
    assert len(cmd.param) == 1
    assert cmd.param[0].value == "100.5"
    assert cmd.param[0].type_value == TypeValue.REAL


def test_command_ack_element(parser):
    """Test parsing CommandAck element."""
    xml = """<PLEXILScript>
      <Script>
        <CommandAck name="drive" type="string">
          <Result>COMMAND_SENT_TO_SYSTEM</Result>
        </CommandAck>
      </Script>
    </PLEXILScript>"""

    script = parser.from_string(xml, PLEXILScript)

    ack = script.script.choice[0]
    assert isinstance(ack, CommandAck)
    assert ack.name == "drive"
    assert ack.result == ["COMMAND_SENT_TO_SYSTEM"]


def test_command_abort_element(parser):
    """Test parsing CommandAbort element."""
    xml = """<PLEXILScript>
      <Script>
        <CommandAbort name="move" type="int">
          <Result>-1</Result>
        </CommandAbort>
      </Script>
    </PLEXILScript>"""

    script = parser.from_string(xml, PLEXILScript)

    abort = script.script.choice[0]
    assert isinstance(abort, CommandAbort)
    assert abort.name == "move"


def test_update_ack_element(parser):
    """Test parsing UpdateAck element."""
    xml = """<PLEXILScript>
      <Script>
        <UpdateAck name="x"/>
      </Script>
    </PLEXILScript>"""

    script = parser.from_string(xml, PLEXILScript)

    ack = script.script.choice[0]
    assert isinstance(ack, UpdateAck)
    assert ack.name == "x"


def test_send_plan_element(parser):
    """Test parsing SendPlan element."""
    xml = """<PLEXILScript>
      <Script>
        <SendPlan file="test-plan.plx"/>
      </Script>
    </PLEXILScript>"""

    script = parser.from_string(xml, PLEXILScript)

    send_plan = script.script.choice[0]
    assert isinstance(send_plan, SendPlan)
    assert send_plan.file == "test-plan.plx"


def test_delay_element_empty(parser):
    """Test parsing empty Delay element."""
    xml = """<PLEXILScript>
      <Script>
        <Delay/>
      </Script>
    </PLEXILScript>"""

    script = parser.from_string(xml, PLEXILScript)

    delay = script.script.choice[0]
    assert isinstance(delay, Delay)


def test_delay_element_ignores_content(parser):
    """Test that Delay ignores any content (non-standard usage in some files)."""
    xml = """<PLEXILScript>
      <Script>
        <Delay>5</Delay>
      </Script>
    </PLEXILScript>"""

    script = parser.from_string(xml, PLEXILScript)

    # Should parse as Delay, content is ignored
    delay = script.script.choice[0]
    assert isinstance(delay, Delay)


def test_simultaneous_element(parser):
    """Test parsing Simultaneous block."""
    xml = """<PLEXILScript>
      <Script>
        <Simultaneous>
          <State name="s1" type="int">
            <Value>1</Value>
          </State>
          <Command name="c1" type="int">
            <Result>2</Result>
          </Command>
        </Simultaneous>
      </Script>
    </PLEXILScript>"""

    script = parser.from_string(xml, PLEXILScript)

    assert len(script.script.choice) == 1
    simul = script.script.choice[0]
    assert isinstance(simul, Simultaneous)
    assert len(simul.choice) == 2
    assert isinstance(simul.choice[0], State)
    assert isinstance(simul.choice[1], Command)


# ====================
# Document Order Tests
# ====================


def test_document_order_preserved(parser):
    """Test that document order is preserved in Script.choice."""
    xml = """<PLEXILScript>
      <Script>
        <Command name="first" type="int">
          <Result>1</Result>
        </Command>
        <State name="second" type="int">
          <Value>2</Value>
        </State>
        <UpdateAck name="third"/>
        <CommandAck name="fourth" type="int">
          <Result>4</Result>
        </CommandAck>
        <State name="fifth" type="int">
          <Value>5</Value>
        </State>
      </Script>
    </PLEXILScript>"""

    script = parser.from_string(xml, PLEXILScript)

    assert len(script.script.choice) == 5

    # Verify exact document order
    assert isinstance(script.script.choice[0], Command)
    assert script.script.choice[0].name == "first"

    assert isinstance(script.script.choice[1], State)
    assert script.script.choice[1].name == "second"

    assert isinstance(script.script.choice[2], UpdateAck)
    assert script.script.choice[2].name == "third"

    assert isinstance(script.script.choice[3], CommandAck)
    assert script.script.choice[3].name == "fourth"

    assert isinstance(script.script.choice[4], State)
    assert script.script.choice[4].name == "fifth"


def test_simultaneous_order_preserved(parser):
    """Test that document order is preserved in Simultaneous.choice."""
    xml = """<PLEXILScript>
      <Script>
        <Simultaneous>
          <UpdateAck name="first"/>
          <State name="second" type="bool">
            <Value>true</Value>
          </State>
          <Command name="third" type="int">
            <Result>3</Result>
          </Command>
          <CommandAbort name="fourth" type="int">
            <Result>4</Result>
          </CommandAbort>
        </Simultaneous>
      </Script>
    </PLEXILScript>"""

    script = parser.from_string(xml, PLEXILScript)

    simul = script.script.choice[0]
    assert len(simul.choice) == 4

    # Verify exact document order
    assert isinstance(simul.choice[0], UpdateAck)
    assert isinstance(simul.choice[1], State)
    assert isinstance(simul.choice[2], Command)
    assert isinstance(simul.choice[3], CommandAbort)


# ====================
# Type Tests
# ====================


@pytest.mark.parametrize(
    "type_str,type_enum",
    [
        ("bool", TypeValue.BOOL),
        ("int", TypeValue.INT),
        ("real", TypeValue.REAL),
        ("string", TypeValue.STRING),
        ("bool-array", TypeValue.BOOL_ARRAY),
        ("int-array", TypeValue.INT_ARRAY),
        ("real-array", TypeValue.REAL_ARRAY),
        ("string-array", TypeValue.STRING_ARRAY),
    ],
)
def test_type_values(parser, type_str, type_enum):
    """Test all type enumeration values."""
    xml = f"""<PLEXILScript>
      <Script>
        <State name="test" type="{type_str}">
          <Value>dummy</Value>
        </State>
      </Script>
    </PLEXILScript>"""

    script = parser.from_string(xml, PLEXILScript)

    state = script.script.choice[0]
    assert state.type_value == type_enum


# ====================
# Round-trip Tests
# ====================


def test_roundtrip_simple(parser, serializer):
    """Test parsing and serializing a simple script."""
    original_xml = """<PLEXILScript>
      <Script>
        <State name="x" type="int">
          <Value>42</Value>
        </State>
      </Script>
    </PLEXILScript>"""

    # Parse
    script = parser.from_string(original_xml, PLEXILScript)

    # Serialize
    output_xml = serializer.render(script)

    # Parse again
    script2 = parser.from_string(output_xml, PLEXILScript)

    # Compare
    assert script == script2


def test_roundtrip_complex(parser, serializer):
    """Test round-trip with complex script."""
    original_xml = """<PLEXILScript>
      <InitialState>
        <State name="flag" type="bool">
          <Value>true</Value>
        </State>
      </InitialState>
      <Script>
        <Command name="cmd1" type="int">
          <Param type="string">arg1</Param>
          <Result>0</Result>
        </Command>
        <State name="s1" type="real">
          <Value>3.14</Value>
        </State>
        <Simultaneous>
          <UpdateAck name="ack1"/>
          <State name="s2" type="int">
            <Value>99</Value>
          </State>
        </Simultaneous>
        <CommandAck name="cmd2" type="string">
          <Result>SUCCESS</Result>
        </CommandAck>
      </Script>
    </PLEXILScript>"""

    # Parse
    script = parser.from_string(original_xml, PLEXILScript)

    # Serialize
    output_xml = serializer.render(script)

    # Parse again
    script2 = parser.from_string(output_xml, PLEXILScript)

    # Compare
    assert script == script2


# ====================
# Edge Cases
# ====================


def test_multiple_values(parser):
    """Test State with multiple values."""
    xml = """<PLEXILScript>
      <Script>
        <State name="array" type="int-array">
          <Value>1</Value>
          <Value>2</Value>
          <Value>3</Value>
        </State>
      </Script>
    </PLEXILScript>"""

    script = parser.from_string(xml, PLEXILScript)

    state = script.script.choice[0]
    assert len(state.value) == 3
    assert state.value == ["1", "2", "3"]


def test_multiple_results(parser):
    """Test Command with multiple results."""
    xml = """<PLEXILScript>
      <Script>
        <Command name="multi" type="int-array">
          <Result>10</Result>
          <Result>20</Result>
        </Command>
      </Script>
    </PLEXILScript>"""

    script = parser.from_string(xml, PLEXILScript)

    cmd = script.script.choice[0]
    assert len(cmd.result) == 2
    assert cmd.result == ["10", "20"]


def test_nested_simultaneous_blocks(parser):
    """Test multiple Simultaneous blocks in sequence."""
    xml = """<PLEXILScript>
      <Script>
        <Simultaneous>
          <State name="s1" type="int">
            <Value>1</Value>
          </State>
        </Simultaneous>
        <State name="between" type="int">
          <Value>99</Value>
        </State>
        <Simultaneous>
          <State name="s2" type="int">
            <Value>2</Value>
          </State>
        </Simultaneous>
      </Script>
    </PLEXILScript>"""

    script = parser.from_string(xml, PLEXILScript)

    assert len(script.script.choice) == 3
    assert isinstance(script.script.choice[0], Simultaneous)
    assert isinstance(script.script.choice[1], State)
    assert script.script.choice[1].name == "between"
    assert isinstance(script.script.choice[2], Simultaneous)
