/*
*  Author: Laura Humphrey
*  Date: 2026 March
*
*  Based on the TestExec app's TestExternalInterface implementation.
*/

#ifndef PLEXIL_STEPPER_INTERFACE_HH
#define PLEXIL_STEPPER_INTERFACE_HH

#include "Dispatcher.hh"
#include "State.hh"

#include <iostream>
#include <map>
#include <set>

// Forward reference
namespace pugi
{
  class xml_node;
}

namespace PLEXIL
{

  class StepperPlexilInterface final :
    public Dispatcher
  {
  public:
    StepperPlexilInterface();
    virtual ~StepperPlexilInterface() = default;

    void runInitialStep(pugi::xml_node const input);
    void runScriptStep(pugi::xml_node const &input);

    //
    // Dispatcher API
    //

    virtual void lookupNow(State const &state, LookupReceiver *rcvr);

    // LookupOnChange
    virtual void setThresholds(const State& state, Real hi, Real lo);
    virtual void setThresholds(const State& state, Integer hi, Integer lo);
    virtual void clearThresholds(const State& state);

    // Commands
    virtual void executeCommand(Command *cmd);
    virtual void reportCommandArbitrationFailure(Command *cmd);
    virtual void invokeAbort(Command *cmd);

    // Updates
    virtual void executeUpdate(Update * update);

    // State information
    virtual void printInternalAssignments();

  private:

    typedef std::map<State, Command *> StateCommandMap;
    typedef std::map<State, Value>        StateMap;

    void handleInitialState(pugi::xml_node const input);
    void handleState(pugi::xml_node const elt);
    void handleCommand(pugi::xml_node const elt);
    void handleCommandAck(pugi::xml_node const elt);
    void handleCommandAbort(pugi::xml_node const elt);
    void handleUpdateAck(pugi::xml_node const elt);
    void handleSendPlan(pugi::xml_node const elt);
    void handleSimultaneous(pugi::xml_node const elt);

    std::map<std::string, Update *> m_waitingUpdates;
    StateCommandMap m_executingCommands; //map from state to the command objects
    StateCommandMap m_commandAcks; //map from state to commands awaiting ack
    StateCommandMap m_abortingCommands; // map from state to commands expecting abort ack
    StateMap m_states; //uniquely identified states and their values
  };
}

#endif // PLEXIL_STEPPER_INTERFACE_HH
