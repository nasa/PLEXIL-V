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


#include "Debug.hh"
#include "Error.hh"
#include "ExecListener.hh"
#include "ExecListenerFactory.hh"
#include "NodeImpl.hh"
#include "CommandNode.hh"
#include "CommandImpl.hh"
#include "NodeTransition.hh"
#include "StateInfoListener.hh"
#include "NodeVariableMap.hh"
#include "Expression.hh"

#include "pugixml.hpp"

#include <iomanip> // for setprecision

namespace PLEXIL
{

  StateInfoListener::StateInfoListener()
    : m_assignments(), m_transitions()
  {
  }

  StateInfoListener::StateInfoListener (pugi::xml_node const xml)
    : ExecListener(xml)
  {
  }

  StateInfoListener::~StateInfoListener() = default;

  // For now, use the DebugMsg facilities (really intended for debugging the
  // *executive* and not plans) to display messages of interest.  Later, a more
  // structured approach including listener filters and a different user
  // interface may be in order.

  void StateInfoListener::implementNotifyNodeTransition(NodeTransition const &trans)
  {
    assertTrueMsg(trans.node,
                  "StateInfoListener:implementNotifyNodeTransition: not a node");
    NodeImpl *node = dynamic_cast<NodeImpl *>(trans.node);
    if (node->getType() == NodeType_Command) {
      if (CommandNode* cmd_node = dynamic_cast<CommandNode*>(trans.node)) {
        if (cmd_node->getCommand()->isActive() && cmd_node->getCommand()->getDest()) {
          m_variableInfo[cmd_node->getCommand()->getDest()->getName()] =
            cmd_node->getCommand()->getDest()->toValue();
        }
      }
    }
    m_transitions.push_back(trans);
    m_nodeInfo[node->getNodeId()] = NodeStateOutcomePair(node->getOutcome(), node->getState());
  }

  void StateInfoListener::implementNotifyAssignment(Expression const *dest,
                                                    std::string const &destName,
                                                    Value const &value)
  {
    m_assignments.push_back(AssignmentRecord(dest, destName, value));
    m_variableInfo[destName] = value;
  }

  std::map<std::string, NodeStateOutcomePair> StateInfoListener::getNodeInfo() {
    return m_nodeInfo;
  }

  std::map<std::string, Value> StateInfoListener::getVariableInfo() {
    return m_variableInfo;
  }

  void StateInfoListener::clearTransitionHistory() {
    m_transitions.clear();
  }

  void StateInfoListener::clearAssignmentHistory() {
    m_assignments.clear();
  }

  ExecListener *makeStateInfoListener()
  {
    return new StateInfoListener();
  }

} // namespace PLEXIL

extern "C"
void initStateInfoListener()
{
  REGISTER_EXEC_LISTENER(PLEXIL::StateInfoListener, "StateInfoListener");
}
