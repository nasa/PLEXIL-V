#include <vector>
#include <string>
#include <iostream>
#include <fstream>
#include <stdexcept>

// Project-specific includes (as in your original)
#include "ExecListenerHub.hh"
#include "StepperPlexilInterface.hh"
#include "StateInfoListener.hh"
#include "planLibrary.hh"
#include "parsePlan.hh"
#include "Logging.hh"
#include "PlexilExec.hh"
#include "Error.hh"
#include "parser-utils.hh"
#include "ParserException.hh"
#include "PlexilSchema.hh"
#include "pugixml.hpp"
#include "NodeImpl.hh"

#include "Stepper.hh"

// Add other required headers as needed

using std::vector;
using std::string;
using namespace PLEXIL;

namespace PLEXIL {

    void cleanup() {
        delete g_exec;
        g_exec = nullptr;
        // LRH -- Why is delete needed for g_exec
        // but results in an error for g_dispatcher?
        g_dispatcher = nullptr;
    }

    Stepper::~Stepper() {
        cleanup();
    }

    Stepper::Stepper(
        const std::string& planName,
        const std::vector<string>& libraryNames,
        const std::vector<string>& libraryPaths)
    {

      setLibraryPaths(libraryPaths);
      g_dispatcher = &m_intf;
      g_exec = makePlexilExec();
      g_exec->setDispatcher(g_dispatcher);
      g_exec->setExecListener(&m_hub);

      m_infoListener = new StateInfoListener();
      m_hub.addListener(m_infoListener);

      // load libraries
      for (const auto& libName : libraryNames) {
        std::string fname = libName;
        if (fname.rfind(".plx") == std::string::npos)
            fname += ".plx";

        Library const *l;
        try {
            l = loadLibraryNode(fname.c_str());
            if (!l) {
                cleanup();
                throw std::runtime_error("Stepper constructor failed because library " + libName + " could not be found");
            }
        }
        catch (ParserException const &e) {
            cleanup();
            throw std::runtime_error("Stepper constructor failed because there was an error reading library " + libName);
        }
      }

      // Load the plan
      pugi::xml_document* planDoc = nullptr;
      try {
          planDoc = loadXmlFile(planName);
          if (!planDoc)
              warn("Error: plan file " << planName << " not found or not readable");
      }
      catch (ParserException const &e) {
          cleanup();
          throw std::runtime_error("Stepper constructor failed because plan file " + planName + " not found or not readable");
      }

      if (!planDoc) {
          cleanup();
          throw std::runtime_error("Stepper constructor failed because plan file " + planName + " not found or not readable");
      }

      NodeImpl* root = nullptr;
      try {
          root = parsePlan(planDoc->document_element());
          m_hub.notifyOfAddPlan(planDoc->document_element());
          delete planDoc;
      }
      catch (ParserException& e) {
          warn("Error parsing plan '" << planName << "':\n" << e.what());
          delete planDoc;
          throw std::runtime_error("Error parsing plan " + planName);
          cleanup();
      }

      if (!g_exec->addPlan(root)) {
          delete root;
          cleanup();
          throw std::runtime_error("Adding plan " + planName + " failed");
      }
    }

    void Stepper::step(const pugi::xml_node& input) {
        if (input.type() != pugi::node_element) {
            reportParserException("step: input must be a pugi::node_element");
        }
        if (!m_tookFirstStep) {
            if (strcmp(input.name(),"InitialState") == 0) {
                m_intf.runInitialStep(input);
                m_tookFirstStep = true;
            }
            else {
                reportParserException("step: first input must be a (possibly "
                                      "empty) InitialState element.");
            }
        }
        else {
            m_intf.runScriptStep(input);
        }
        m_infoListener->clearAssignmentHistory();
        m_infoListener->clearTransitionHistory();
    }

    bool Stepper::needsStep() {
      return g_exec->needsStep();
    }

    bool Stepper::needsInitialState() {
        return !m_tookFirstStep;
    }

    std::map<std::string, NodeStateOutcomePair> Stepper::getNodeInfo() const {
        return m_infoListener->getNodeInfo();
    }

    std::map<std::string, Value> Stepper::getVariableInfo() const {
        return m_infoListener->getVariableInfo();
    }

    std::string nodeInfoToString(const std::map<std::string, NodeStateOutcomePair>& nodeInfo) {
        std::ostringstream oss;
        for (const auto& pair : nodeInfo) {
            oss << pair.first << "\n  " << pair.second.toString() << "\n\n";
        }
        return oss.str();
    }

    std::string variableInfoToString(const std::map<std::string, Value>& variableInfo) {
        std::ostringstream oss;
        for (const auto& pair : variableInfo) {
            oss << pair.first << " = " << pair.second.valueToString() << '\n';
        }
        return oss.str();
    }

    std::string xmlNodeToString(const pugi::xml_node& xmlNode) {
        std::stringstream ss;
        xmlNode.print(ss);
        std::string s = ss.str();
        return s;
    }

}