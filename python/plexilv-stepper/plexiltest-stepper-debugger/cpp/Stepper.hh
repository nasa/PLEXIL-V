#ifndef PLEXIL_STEPPER_HH
#define PLEXIL_STEPPER_HH

#include <vector>
#include <string>
#include <iostream>
#include <fstream>

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

// Add other required headers as needed

using std::vector;
using std::string;
using namespace PLEXIL;

namespace PLEXIL {

    class Stepper {
    private:
        StepperPlexilInterface m_intf;
        std::unique_ptr<PlexilExec> m_exec;
        ExecListenerHub m_hub;
        StateInfoListener* m_infoListener;
        bool m_tookFirstStep = false;

    public:
        Stepper(
            const string& planName,
            const vector<string>& libraryNames,
            const vector<string>& libraryPaths);
        ~Stepper();

        void step(const pugi::xml_node& scriptInput);
        bool needsStep();
        bool needsInitialState();

        std::map<std::string, NodeStateOutcomePair> getNodeInfo() const;
        std::map<std::string, Value> getVariableInfo() const;
    };

    std::string nodeInfoToString(const std::map<std::string, NodeStateOutcomePair>& nodeInfo);
    std::string variableInfoToString(const std::map<std::string, Value>& variableInfo);
    std::string xmlNodeToString(const pugi::xml_node& xmlNode);

}

#endif // PLEXIL_STEPPER_HH