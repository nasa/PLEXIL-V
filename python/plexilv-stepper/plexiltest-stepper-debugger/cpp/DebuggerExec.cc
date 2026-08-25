/* Debugger-Exec.cc
*  Author: Laura Humphrey
*  Date: 2026 March
*/

#include "lifecycle-utils.h"
#include "Logging.hh"

#include <fstream>
#include <string>
#include <iostream>

#include <cstring>

using std::endl;
using std::set;
using std::string;
using std::vector;

using namespace PLEXIL;

static int run(int argc, char** argv);

int main(int argc, char** argv)
{
  int result = run(argc, argv);
  plexilRunFinalizers();
  return result;
}

int run(int argc, char** argv)
{
  string scriptName("error");
  string planName("error");
  vector<string> libraryNames;
  vector<string> libraryPaths;
  string
    usage("Usage: Debugger -s <script> -p <plan>\n\
                        [-l <library-file>]*     (no default)\n\
                        [-L <library-dir>]*      (default .)\n");

  /// If not enough command line parameters, print usage
  if (argc < 5) {
    if (argc >= 2 && strcmp(argv[1], "-h") == 0) {
      // print usage and exit
      std::cout << usage << std::endl;
      return 0;
    }
    warn("Not enough arguments.\n At least the -p and -s arguments must be provided.\n" << usage);
    return 2;
  }

  /// Parse command line parameters
  for (int i = 1; i < argc; ++i) {
    if (strcmp(argv[i], "-p") == 0) {
      if (argc == (++i)) {
        warn("Missing argument to the " << argv[i-1] << " option.\n"
             << usage);
        return 2;
      }
      planName = argv[i];
    }
    else if (strcmp(argv[i], "-s") == 0) {
      if (argc == (++i)) {
        warn("Missing argument to the " << argv[i-1] << " option.\n"
             << usage);
        return 2;
      }
      scriptName = argv[i];
    }
    else if (strcmp(argv[i], "-l") == 0) {
      if (argc == (++i)) {
        warn("Missing argument to the " << argv[i-1] << " option.\n"
             << usage);
        return 2;
      }
      libraryNames.push_back(argv[i]);
    }
    else if (strcmp(argv[i], "-L") == 0) {
      if (argc == (++i)) {
        warn("Missing argument to the " << argv[i-1] << " option.\n"
             << usage);
        return 2;
      }
      libraryPaths.push_back(argv[i]);
    }
    else if (strcmp(argv[i], "-log") == 0) {
      if (argc == (++i)) {
        warn("Missing argument to the " << argv[i-1] << " option.\n"
             << usage);
        return 2;
      }
      Logging::ENABLE_LOGGING = 1;
      Logging::set_log_file_name(argv[i]);
    }
    else if (strcmp(argv[i], "-eprompt") == 0)
      Logging::ENABLE_E_PROMPT = 1;
    else if (strcmp(argv[i], "-wprompt") == 0)
      Logging::ENABLE_W_PROMPT = 1;
    else {
      warn("Unknown option '" << argv[i] << "'.  " << usage);
      return 2;
    }
  }

  /// If no plan or script supplied, error out
  if (scriptName == "error") {
    warn("No -s option found.\n" << usage);
    return 2;
  }
  if (planName == "error") {
    warn("No -p option found.\n" << usage);
    return 2;
  }

  if (Logging::ENABLE_LOGGING) {

#ifdef __linux__
    Logging::print_to_log(argv, argc);
#endif
#ifdef __APPLE__
    string cmd = "user command: ";
    for (int i = 1; i < argc; ++i)
      cmd = cmd + argv[i] + " ";

    Logging::print_to_log(cmd.c_str());
#endif
  }

  /// Set library paths
  setLibraryPaths(libraryPaths);

  /// Create Debugger object
  // Debugger s(scriptName, planName, libraryNames, libraryPaths);
  Debugger s(planName, libraryNames, libraryPaths);

  /// Step through the plan
  std::cout << std::endl << "********** Running initial step **********\n" << std::endl;
  // s.step();
  std::cout << "----- Nodes -----" << std::endl;
  std::cout << nodeInfoToString(s.getNodeInfo()) << std::endl;
  std::cout << "----- Variables -----" << std::endl;
  std::cout << variableInfoToString(s.getVariableInfo()) << std::endl;

  while (s.execNeedsStep()) {
    std::cout << std::endl << "********** Press ENTER to continue **********" << std::endl;
    std::cin.get();
    // s.step();
    std::cout << "----- Nodes -----" << std::endl;
    std::cout << nodeInfoToString(s.getNodeInfo()) << std::endl;
    std::cout << "----- Variables -----" << std::endl;
    std::cout << variableInfoToString(s.getVariableInfo()) << std::endl;
  }

  return 0;
}

