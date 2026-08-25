/* Copyright (c) 2006-2022, Universities Space Research Association (USRA).
*  All rights reserved.
*
* Redistribution and use in source and binary forms, with or without
* modification, are permitted provided that the following conditions are met:
*     * Redistributions of source code must retain the above copyright
*       notice, this list of conditions and the following disclaimer.
*     * Redistributions in binary form must reproduce the above copyright
*       notice, this list of conditions and the following disclaimer in the
*       documentation and/or other materials provided with the distribution.
*     * Neither the name of the Universities Space Research Association nor the
*       names of its contributors may be used to endorse or promote products
*       derived from this software without specific prior written permission.
*
* THIS SOFTWARE IS PROVIDED BY USRA ``AS IS'' AND ANY EXPRESS OR IMPLIED
* WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF
* MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
* DISCLAIMED. IN NO EVENT SHALL USRA BE LIABLE FOR ANY DIRECT, INDIRECT,
* INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
* BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS
* OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
* ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR
* TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE
* USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
*/

#include "StepperPlexilInterface.hh"

#include "Assignable.hh"
#include "Command.hh"
#include "Debug.hh"
#include "Error.hh"
#include "LookupReceiver.hh"
#include "NodeImpl.hh"
#include "NodeConstants.hh"
#include "ParserException.hh"
#include "PlexilExec.hh"
#include "StateCache.hh"
#include "Update.hh"
#include "parsePlan.hh"
#include "plan-utils.hh"
#include "pugixml.hpp"
#include "stricmp.h"

#include <limits>
#include <sstream>
#include <iostream>
#include <unistd.h>
#include <stdexcept>

#ifdef STDC_HEADERS
#include <cstring>
#endif

namespace PLEXIL
{

  // Forward declarations for local functions
  static std::string getText(const State& c);
  static std::string getText(const State& c, const Value& v);
  static State parseCommand(pugi::xml_node const cmd);
  static Value parseOneValue(const std::string& type,
                             const std::string& valStr);
  static Value parseParam(pugi::xml_node const param);
  static void parseParams(pugi::xml_node const root,
                          std::vector<Value>& dest);
  static Value parseResult(pugi::xml_node const valXml);
  static State parseState(pugi::xml_node const elt);
  static Value parseStateValue(pugi::xml_node const stateXml);

  StepperPlexilInterface::StepperPlexilInterface()
    : Dispatcher()
  {
    // Set a default time of 0
    m_states.insert(std::pair<State, Value>(State::timeState(), Value(0.0)));
  }

  void StepperPlexilInterface::printInternalAssignments() {
    ;
  }

  void StepperPlexilInterface::runInitialStep(pugi::xml_node const input)
  {
    checkError(g_exec, "Attempted to run a script without an executive.");
    handleInitialState(input); // steps exec once
  }

  void StepperPlexilInterface::runScriptStep(pugi::xml_node const &input)
  {
    pugi::xml_node scriptElement = input;
    checkParserException(!scriptElement.empty(), "handleInitialState: input "
                         "must be a (possibly empty) InitialState element");
    // state
    if (strcmp(scriptElement.name(), "State") == 0) {
      handleState(scriptElement);
    }
    // command
    else if (strcmp(scriptElement.name(), "Command") == 0) {
      handleCommand(scriptElement);
    }
    // command ack
    else if (strcmp(scriptElement.name(), "CommandAck") == 0) {
      handleCommandAck(scriptElement);
    }
    // command abort
    else if (strcmp(scriptElement.name(), "CommandAbort") == 0) {
      handleCommandAbort(scriptElement);
    }
    // update ack
    else if (strcmp(scriptElement.name(), "UpdateAck") == 0) {
      handleUpdateAck(scriptElement);
    }
    // send plan
    else if (strcmp(scriptElement.name(), "SendPlan") == 0) {
      handleSendPlan(scriptElement);
    }
    // simultaneous
    else if (strcmp(scriptElement.name(), "Simultaneous") == 0) {
      handleSimultaneous(scriptElement);
    }
    // delay
    else if (strcmp(scriptElement.name(), "Delay") == 0) {
      ; // No-op
    }
    // report unknown script element
    else {
      reportParserException("Unknown script element '" << scriptElement.name() << "'");
    }
    // step the exec forward
    g_exec->step(StateCache::currentTime());
    return;
  }

  void StepperPlexilInterface::handleInitialState(pugi::xml_node const input)
  {
    checkParserException(strcmp(input.name(), "InitialState") == 0,
                         "handleInitialState: input must be a (possibly empty) "
                         "InitialState element");
    pugi::xml_node state = input.first_child();
    if (state.type() != pugi::node_pcdata) {
      while (state) {
        State st = parseState(state);
        Value value = parseStateValue(state);
        debugMsg("Stepper:stepperOutput",
                 "Creating initial state " << st << " = " << value);
        m_states[st] = value;
        StateCache::instance().lookupReturn(st, value);
        state = state.next_sibling();
      }
    }
    g_exec->step(StateCache::currentTime());
  }

  void StepperPlexilInterface::handleState(pugi::xml_node const elt)
  {
    State st = parseState(elt);
    Value value = parseStateValue(elt);
    debugMsg("Stepper:stepperOutput",
             "Processing event: " << st << " = " << value);
    m_states[st] = value;
    StateCache::instance().lookupReturn(st, value);
  }

  void StepperPlexilInterface::handleCommand(pugi::xml_node const elt)
  {
    State command = parseCommand(elt);
    Value value = parseResult(elt);
    debugMsg("Stepper:stepperOutput",
             "Sending command result " << getText(command, value));
    StateCommandMap::iterator it =
      m_executingCommands.find(command);
    checkParserException(it != m_executingCommands.end(),
                         "No currently executing command " << getText(command));
    commandReturn(it->second, value);
    m_executingCommands.erase(it);
  }

  void StepperPlexilInterface::handleCommandAck(pugi::xml_node const elt)
  {
    State command = parseCommand(elt);
    // Ack should be string value
    Value value = parseResult(elt);
    CommandHandleValue handle = NO_COMMAND_HANDLE;
    std::string const *str = nullptr;
    if (value.getValuePointer(str))
      handle = parseCommandHandleValue(*str);
    debugMsg("Stepper:stepperOutput",
             "Sending command ACK " << getText(command, value));
    StateCommandMap::iterator it = m_commandAcks.find(command);
    checkParserException(it != m_commandAcks.end(),
                         "No command waiting for acknowledgement " << getText(command));
    commandHandleReturn(it->second, handle);
  }

  void StepperPlexilInterface::handleCommandAbort(pugi::xml_node const elt)
  {
    State command = parseCommand(elt);
    Value value = parseResult(elt);
    checkParserException(value.valueType() == BOOLEAN_TYPE,
                         "CommmandAbort value must be Boolean");
    Boolean ack;
    checkParserException(value.getValue(ack),
                         "CommmandAbort value must not be unknown");

    debugMsg("Stepper:stepperOutput",
             "Sending abort ACK " << getText(command, value));
    StateCommandMap::iterator it =
      m_abortingCommands.find(command);
    checkParserException(it != m_abortingCommands.end(),
                         "No abort waiting for acknowledgement " << getText(command));
    debugMsg("Stepper:stepperOutput",
             "Acknowledging abort into " << it->second);
    commandAbortAcknowledge(it->second, ack);
    m_abortingCommands.erase(it);
  }

  void StepperPlexilInterface::handleUpdateAck(pugi::xml_node const elt)
  {
    std::string name(elt.attribute("name").value());
    debugMsg("Stepper:stepperOutput", "Sending update ACK " << name);
    std::map<std::string, Update*>::iterator it = m_waitingUpdates.find(name);
    checkParserException(it != m_waitingUpdates.end(),
                         "No update from node " << name << " waiting for acknowledgement.");
    it->second->acknowledge(true);
    m_waitingUpdates.erase(it);
  }

  void StepperPlexilInterface::handleSendPlan(pugi::xml_node const elt)
  {
    const char* filename = elt.attribute("file").value();
    checkError(strlen(filename) > 0,
               "SendPlan element has no file attribute");

    pugi::xml_document* doc = new pugi::xml_document();
    pugi::xml_parse_result parseResult = doc->load_file(filename);
    assertTrueMsg(parseResult.status == pugi::status_ok,
                  "Error parsing plan file " << elt.attribute("file").value()
                  << ": " << parseResult.description());

    debugMsg("Stepper:stepperOutput",
             "Sending plan from file " << elt.attribute("file").value());
    NodeImpl *root = nullptr;
    try {
      root = parsePlan(doc->document_element().child("PlexilPlan"));
    }
    catch (ParserException const &e) {
      std::cerr << "Error parsing plan XML: \n" << e.what() << std::endl;
    }
    if (root)
      g_exec->addPlan(root);
  }

  void StepperPlexilInterface::handleSimultaneous(pugi::xml_node const elt)
  {
    debugMsg("Stepper:stepperOutput", "Processing simultaneous event(s)");
    pugi::xml_node item = elt.first_child();
    while (!item.empty()) {
      // ignore text element (e.g. from <Script> </Script>)
      if (item.type() == pugi::node_pcdata) {
        //debugMsg("Test:verboseTestOutput", " Ignoring XML PCDATA");
      }
      // state
      else if (strcmp(item.name(), "State") == 0) {
        handleState(item);
      }
      // command
      else if (strcmp(item.name(), "Command") == 0) {
        handleCommand(item);
      }
      // command ack
      else if (strcmp(item.name(), "CommandAck") == 0) {
        handleCommandAck(item);
      }
      // command abort
      else if (strcmp(item.name(), "CommandAbort") == 0) {
        handleCommandAbort(item);
      }
      // update ack
      else if (strcmp(item.name(), "UpdateAck") == 0) {
        handleUpdateAck(item);
      }
      // report unknown script element
      else {
        reportParserException("Unknown script element '" << item.name()
                              << "' inside <Simultaneous>");
        return;
      }
      item = item.next_sibling();
    }
    debugMsg("Stepper:stepperOutput", "End simultaneous event(s)");
  }

  //
  // Script parsing utilities
  //

  static State parseStateInternal(pugi::xml_node const elt)
  {
    checkParserException(!elt.attribute("name").empty(),
                         "No name attribute in " << elt.name() << " element.");
    State result(elt.attribute("name").value());
    std::vector<Value> parms;
    parseParams(elt, parms);
    size_t n = parms.size();
    if (n) {
      result.setParameterCount(n);
      for (size_t i = 0; i < n; ++i)
        result.setParameter(i, parms[i]);
    }
    return result;
  }

  static State parseState(pugi::xml_node const elt)
  {
    checkParserException(strcmp(elt.name(), "State") == 0,
                         "Expected <State> element. Found '" << elt.name() << "'");
    return parseStateInternal(elt);
  }

  // Parses all command-like elements: Command, CommandAck, CommandAbort.
  static State parseCommand(pugi::xml_node const cmd)
  {
    checkParserException(strcmp(cmd.name(), "Command") == 0 ||
                         strcmp(cmd.name(), "CommandAck") == 0 ||
                         strcmp(cmd.name(), "CommandAbort") == 0,
                         "Expected <Command> element.  Found '" << cmd.name() << "'");
    return parseStateInternal(cmd);
  }

  static Value parseResult(pugi::xml_node const cmd)
  {
    pugi::xml_node resXml = cmd.child("Result");
    checkParserException(!resXml.empty(), "No Result child in <" << cmd.name() << "> element.");
    checkParserException(!resXml.first_child().empty(), "Empty Result child in <" << cmd.name() << "> element.");
    checkParserException(!resXml.empty(), "No Result child in <" << cmd.name() << "> element.");
    checkParserException(!cmd.attribute("type").empty(),
                         "No type attribute in <" << cmd.name() << "> element.");
    std::string type(cmd.attribute("type").value());

    // read in the initiial values and parameters
    if (type.rfind("array") == std::string::npos) {
      // Not an array
      return parseOneValue(type, resXml.child_value());
    }
    else {
      std::vector<Value> values;
      while (!resXml.empty()) {
        values.push_back(parseOneValue(type, resXml.child_value()));
        resXml = resXml.next_sibling();
      }
      return Value(values);
    }
  }

  static void parseParams(pugi::xml_node const root,
                          std::vector<Value>& dest)
  {
    size_t n = std::distance(root.begin(), root.end());
    if (!n)
      return; // no parameters

    dest.reserve(n);
    pugi::xml_node param = root.child("Param");
    while (!param.empty()) {
      dest.push_back(parseParam(param));
      param = param.next_sibling("Param");
    }
  }

  static Value parseParam(pugi::xml_node const param)
  {
    checkParserException(!param.first_child().empty()
                         || strcmp(param.attribute("type").value(), "string") == 0,
                         "Empty Param child in <" << param.parent().name() << "> element.");
    std::string type(param.attribute("type").value());
    std::string val(param.child_value());
    if (val == "UNKNOWN") {
      // Create a typed unknown
      ValueType t = UNKNOWN_TYPE;
      if (type == "int")
        t = INTEGER_TYPE;
      else if (type == "real")
        t = REAL_TYPE;
      else if (type == "bool")
        t = BOOLEAN_TYPE;
      else if (type == "string")
        t = STRING_TYPE;
      return Value(t);
    }
    else if (type == "int") {
      Integer value;
      std::istringstream str(val);
      str >> value;
      return Value(value);
    }
    else if (type == "real") {
      Real value;
      std::istringstream str(val);
      str >> value;
      return Value(value);
    }
    else if (type == "bool") {
      bool value;
      std::istringstream str(val);
      str >> value;
      return Value(value);
    }
    // string case
    else if (param.first_child().empty()) {
      return Value("");
    }
    else {
      return Value(param.child_value());
    }
  }

  static Value parseStateValue(pugi::xml_node const stateXml)
  {
    // read in values
    std::string type(stateXml.attribute("type").value());
    checkParserException(!type.empty(),
                         "No type attribute in <" << stateXml.name() << "> element");

    pugi::xml_node valXml = stateXml.child("Value");
    checkParserException(valXml,
                         "No <Value> element in <"  << stateXml.name() << "> element");
    if (type.rfind("array") == std::string::npos) {
      // Not an array
      return parseOneValue(type, valXml.child_value());
    }
    else {
      std::vector<Value> values;
      while (!valXml.empty()) {
        values.push_back(parseOneValue(type, valXml.child_value()));
        valXml = valXml.next_sibling();
      }
      return Value(values);
    }
  }

  // parse in value
  static Value parseOneValue(const std::string& type,
                             const std::string& valStr)
  {
    // Unknown
    if (0 == stricmp(valStr.c_str(), "Plexil_Unknown")) return Value();

    // string or string-array
    else if (type.find("string") == 0) {
      return Value(valStr);
    }
    // int, int-array
    else if (type.find("int") == 0) {
      Integer value;
      std::istringstream ss(valStr);
      ss >> value;
      return Value(value);
    }
    // real, real-array
    else if (type.find("real") == 0) {
      Real value;
      std::istringstream ss(valStr);
      ss >> value;
      return Value(value);
    }
    // bool or bool-array
    else if (type.find("bool") == 0) {
      if (0 == stricmp(valStr.c_str(), "true"))
        return Value(true);
      else if (0 == stricmp(valStr.c_str(), "false"))
        return Value(false);
      else {
        bool value;
        std::istringstream ss(valStr);
        ss >> value;
        return Value(value);
      }
    }
    else {
      reportParserException("Unknown type attribute \"" << type << "\"");
      return Value();
    }
  }

  void StepperPlexilInterface::lookupNow(State const &state,
                                        LookupReceiver *rcvr)
  {
    debugMsg("Stepper:stepperOutput", "Looking up immediately " << state);
    StateMap::const_iterator it = m_states.find(state);
    if (it == m_states.end()) {
      debugMsg("Stepper:stepperOutput", "No state found.  Setting UNKNOWN.");
      it = m_states.insert(std::make_pair(state, Value())).first;
    }
    const Value& value = it->second;
    debugMsg("Stepper:stepperOutput", "Returning value " << value);
    rcvr->update(value);
  }

  void StepperPlexilInterface::setThresholds(const State& /* state */,
                                            Real /* highThreshold */,
                                            Real /* lowThreshold */)
  {}

  void StepperPlexilInterface::setThresholds(const State& /* state */,
                                            Integer /* highThreshold */,
                                            Integer /* lowThreshold */)
  {}

  void StepperPlexilInterface::clearThresholds(const State & /* state */)
  {}

  void StepperPlexilInterface::executeCommand(Command *cmd)
  {
    State const& command = cmd->getCommand();

    debugMsg("Stepper:stepperOutput", "Executing " << command);

    // Special handling of the utility commands (a bit of a hack!):
    std::string const & cmdName = command.name();
    if (cmdName == "print") {
      print(command.parameters());
      commandHandleReturn(cmd, COMMAND_SUCCESS);
    }
    else if (cmdName == "pprint") {
      pprint(command.parameters());
      commandHandleReturn(cmd, COMMAND_SUCCESS);
    }
    else if (cmdName == "printToString") {
      commandReturn(cmd, printToString(command.parameters()));
      commandHandleReturn(cmd, COMMAND_SUCCESS);
    }
    else if (cmdName == "pprintToString") {
      commandReturn(cmd, pprintToString(command.parameters()));
      commandHandleReturn(cmd, COMMAND_SUCCESS);
    }
    else {
      // Usual case - set up for scripted ack value
      m_commandAcks[command] = cmd;
      if (cmd->isReturnExpected())
        m_executingCommands[command] = cmd;
    }
  }

  /**
   * @brief Report the failure in the appropriate way for the application.
   */
  void StepperPlexilInterface::reportCommandArbitrationFailure(Command *cmd)
  {
    commandHandleReturn(cmd, COMMAND_DENIED);
  }

  /**
   * @brief Abort one command in execution.
   * @param cmd The command.
   */
  void StepperPlexilInterface::invokeAbort(Command *cmd)
  {
    assertTrue_1(cmd);
    State const &command = cmd->getCommand();
    debugMsg("Stepper:stepperOutput", "Aborting " << command);
    m_abortingCommands[command] = cmd;
  }

  void StepperPlexilInterface::executeUpdate(Update * update)
  {
    debugMsg("Stepper:stepperOutput", "Received update: ");
    Update::PairValueMap const &pairs = update->getPairs();
    for (Update::PairValueMap::const_iterator pairIt = pairs.begin(); pairIt != pairs.end(); ++pairIt)
      debugMsg("Stepper:stepperOutput", " " << pairIt->first << " => " << pairIt->second);
    m_waitingUpdates.insert(std::make_pair(update->getNodeId(), update));
  }

  static std::string getText(const State& c)
  {
    std::ostringstream retval;
    retval << c.name() << "(";
    std::vector<Value>::const_iterator it = c.parameters().begin();
    if (it != c.parameters().end()) {
      retval << *it;
      for (++it; it != c.parameters().end(); ++it)
        retval << ", " << *it;
    }
    retval << ")";
    return retval.str();
  }

  static std::string getText(const State& c, const Value& val)
  {
    std::ostringstream retval;
    retval << getText(c);
    retval << " = ";
    if (val.valueType() == STRING_TYPE)
      retval << "(string)" << val;
    else
      retval << val;
    return retval.str();
  }

}
