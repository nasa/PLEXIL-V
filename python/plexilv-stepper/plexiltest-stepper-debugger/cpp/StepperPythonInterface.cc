#include "StepperPythonInterface.hh"
#include "ValueType.hh"
#include "pugixml.hpp"
#include "Error.hh"
#include "ParserException.hh"

#include <cstring>

/// Helper functions
const char* string_toCharArray(const std::string& s) {
    char* cstr = new char[s.size() + 1];
    std::strcpy(cstr, s.c_str());
    return cstr;
}

/// C interface functions
extern "C" {

    Stepper* Stepper_new(
        // const char* scriptName,
        const char* planName,
        const char** libraryNames, const int numNames,
        const char** libraryPaths, const int numPaths)
    {
        std::vector<std::string> names;
        for (int i = 0; i < numNames; ++i)
        names.push_back(libraryNames[i]);
        std::vector<std::string> paths;
        for (int i = 0; i < numPaths; ++i)
        paths.push_back(libraryPaths[i]);
        try {
            return new Stepper(planName, names, paths);
        } catch (const std::exception& ex) {
            return nullptr;
        }
    }

    void Stepper_delete(Stepper* s) {
        delete s;
    }

    int Stepper_step(
        Stepper* s,
        const char* scriptInput,
        char* errorMessage,
        const size_t maxMessageLength)
    {
        Error::doThrowExceptions();
        pugi::xml_document doc;
        pugi::xml_parse_result result = doc.load_string(scriptInput);
        if (result) {
            pugi::xml_node element = doc.document_element();
            try {
                s->step(element);
                return 0;
            }
            catch (const PLEXIL::ParserException& e) {
                if (errorMessage != nullptr) {
                    std::strncpy(errorMessage, e.what(), maxMessageLength - 1);
                }
                return 1; // Invalid script input
            }
            catch (const PLEXIL::Error& e) {
                return 2; // Error in executive
            }
            catch (...) {
                return 3; // Unknown error
            }
        }
        return 3;
    }

    bool Stepper_needsStep(Stepper* s) {
        return s->needsStep();
    }

    bool Stepper_needsInitialState(Stepper* s) {
        return s->needsInitialState();
    }

    const Value* Stepper_getVariableValues(
        const Stepper* s,
        int* count)
    {
        std::map<std::string, Value> m = s->getVariableInfo();
        static std::vector<Value> values;
        values.clear();
        for (const auto& kv : m) {
            values.push_back(kv.second);
        }
        *count = values.size();
        return values.data();
    }

    void Stepper_getVariables(
        const Stepper* s,
        const char*** varNames,
        const char*** valStrings,
        const char** typeStrings,
        int* count)
    {
        std::map<std::string, Value> m = s->getVariableInfo();
        std::vector<std::string> names;
        std::vector<Value> values;
        for (const auto& kv : m) {
            names.push_back(kv.first);
            values.push_back(kv.second);
        }
        *count = values.size();
        *varNames = new const char*[names.size()];
        for (size_t i = 0; i < names.size(); ++i) {
        (*varNames)[i] = string_toCharArray(names[i]);
        }
        *valStrings = new const char*[values.size()];
        for (size_t i = 0; i < values.size(); ++i) {
        (*valStrings)[i] = string_toCharArray(values[i].valueToString());
        }
        for (size_t i = 0; i < values.size(); ++i) {
        typeStrings[i] = ValueTypeEnum_toStringLiteral(values[i].valueType());
        }
    }

    const NodeStateOutcomePair* Stepper_getNodeStateOutcomes(
        const Stepper* s,
        const char*** nodeNames,
        int* count)
    {
        std::map<std::string, NodeStateOutcomePair> m = s->getNodeInfo();
        std::vector<std::string> names;
        std::vector<NodeStateOutcomePair> pairs;
        for (const auto& kv : m) {
            names.push_back(kv.first);
            pairs.push_back(kv.second);
        }
        *nodeNames = new const char*[names.size()];
        for (size_t i = 0; i < names.size(); ++i) {
            (*nodeNames)[i] = string_toCharArray(names[i]);
        }
        *count = pairs.size();
        // Instead of returning pair.data(), use 'new' so that the returned result
        // can be deleted through Python's cytpes interface later. ChatGPT claims
        // this is a better practice for memory management in this case.
        NodeStateOutcomePair* pairArray = new NodeStateOutcomePair[pairs.size()];
        for (size_t i = 0; i < pairs.size(); ++i) {
            pairArray[i] = pairs[i];
        }
        return pairArray;
    }

    const char* ValueTypeEnum_toStringLiteral(ValueType val) {
        switch (val) {
            case UNKNOWN_TYPE:    return "UNKNOWN_TYPE";
            // User scalar types
            case BOOLEAN_TYPE:    return "BOOLEAN_TYPE";
            case INTEGER_TYPE:    return "INTEGER_TYPE";
            case REAL_TYPE:       return "REAL_TYPE";
            case STRING_TYPE:     return "STRING_TYPE";
            case DATE_TYPE:       return "DATE_TYPE";
            case DURATION_TYPE:   return "DURATION_TYPE";
            // User array types
            case BOOLEAN_ARRAY_TYPE:    return "BOOLEAN_ARRAY_TYPE";
            case INTEGER_ARRAY_TYPE:    return "INTEGER_ARRAY_TYPE";
            case REAL_ARRAY_TYPE:       return "REAL_ARRAY_TYPE";
            case STRING_ARRAY_TYPE:     return "STRING_ARRAY_TYPE";
            // Lookup or Command descriptor, mostly for external use
            case STATE_TYPE:    return "STATE_TYPE";
            // Internal types
            case NODE_STATE_TYPE:       return "NODE_STATE_TYPE";
            case OUTCOME_TYPE:          return "OUTCOME_TYPE";
            case FAILURE_TYPE:          return "FAILURE_TYPE";
            case COMMAND_HANDLE_TYPE:   return "COMMAND_HANDLE_TYPE";
            // Undefined
            default:    return "UNDEFINED_VALUE_TYPE";
        }
    }

    const char* NodeOutcomeEnum_toStringLiteral(NodeOutcome val) {
        switch (val) {
            case NO_OUTCOME:        return "NO_OUTCOME";
            case SUCCESS_OUTCOME:   return "SUCCESS_OUTCOME";
            case FAILURE_OUTCOME:   return "FAILURE_OUTCOME";
            case SKIPPED_OUTCOME:   return "SKIPPED_OUTCOME";
            case INTERRUPTED_OUTCOME: return "INTERRUPTED_OUTCOME";
            // case OUTCOME_MAX:       return "OUTCOME_MAX";
            // Undefined
            default:                return "UNDEFINED_OUTCOME";
        }
    }

    const char* NodeStateEnum_toStringLiteral(NodeState val) {
        switch (val) {
            case NO_NODE_STATE:         return "NO_NODE_STATE";
            case INACTIVE_STATE:        return "INACTIVE_STATE";
            case WAITING_STATE:         return "WAITING_STATE";
            case EXECUTING_STATE:       return "EXECUTING_STATE";
            case ITERATION_ENDED_STATE: return "ITERATION_ENDED_STATE";
            case FINISHED_STATE:        return "FINISHED_STATE";
            case FAILING_STATE:         return "FAILING_STATE";
            case FINISHING_STATE:       return "FINISHED_STATE";
            // NODE_STATE_MAX
            // Undefined
            default:                    return "UNDEFINED_STATE";
        }
    }

    void charArray_delete(char* charArray) {
        delete[] charArray;
    }

    void arrayOfCharArray_delete(char** arrOfCharArray, int count) {
        for (int i = 0; i < count; ++i) {
            delete[] arrOfCharArray[i];
        }
        delete[] arrOfCharArray;
    }

    void arrayOfNodeStateOutcomePair_delete(NodeStateOutcomePair* pairs, int count) {
        delete[] pairs;
    }

}