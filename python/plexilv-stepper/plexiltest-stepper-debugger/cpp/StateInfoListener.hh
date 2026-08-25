/* Copyright (c) 2006-2021, Universities Space Research Association (USRA).
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

#ifndef PLEXIL_STATE_INFO_LISTENER_HH
#define PLEXIL_STATE_INFO_LISTENER_HH

#include "ExecListener.hh"
#include "NodeTransition.hh"
#include "Value.hh"
#include <sstream>

#include <map>

namespace PLEXIL
{

  // Define custom type
  struct NodeStateOutcomePair {
    NodeOutcome outcome;
    NodeState state;

    NodeStateOutcomePair() = default;
    ~NodeStateOutcomePair() = default;

    NodeStateOutcomePair(NodeOutcome const o,
                         NodeState const s)
      : outcome(o), state(s)
    {};

    std::string toString() const {
      std::ostringstream oss;
      // oss << "State: " << nodeStateName(state) << ", Outcome: " << outcomeName(outcome);
      oss << "(" << nodeStateName(state) << ", " << outcomeName(outcome) << ")";
      return oss.str();
    };
  };

  class StateInfoListener : public ExecListener
  {
  public:
    StateInfoListener();
    StateInfoListener (pugi::xml_node);
    virtual ~StateInfoListener();

    // ExecListener interface methods
    virtual void
    implementNotifyNodeTransition(NodeTransition const &trans) override;

    virtual void
    implementNotifyAssignment(Expression const *dest,
                              std::string const &destName,
                              Value const &value) override;

    // Additional methods and members
    std::map<std::string, NodeStateOutcomePair> getNodeInfo();
    std::map<std::string, Value> getVariableInfo();
    void clearTransitionHistory();
    void clearAssignmentHistory();

  private:

    // Internal data type
    struct AssignmentRecord {
      Value value;
      std::string destName;
      Expression const *dest;

      AssignmentRecord(Expression const *dst,
                       std::string const &name,
                       Value const &val)
        : value(val),
          destName(name),
          dest(dst)
      {}
      // use default destructor, copy constructor, assignment
    };

    std::vector<AssignmentRecord> m_assignments;
    std::vector<NodeTransition> m_transitions;
    std::map<std::string, NodeStateOutcomePair> m_nodeInfo;
    std::map<std::string, Value> m_variableInfo;
  };

  // Factory function now returns pointer to the new type
  ExecListener *makeStateInfoListener();
}

extern "C"
void initStateInfoListener();

#endif // PLEXIL_STATE_INFO_LISTENER_HH
