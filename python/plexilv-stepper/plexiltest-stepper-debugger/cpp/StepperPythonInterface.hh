#ifndef STEPPER_PYTHON_INTERFACE_HH
#define STEPPER_PYTHON_INTERFACE_HH

#include "Stepper.hh"

extern "C" {

  /// Define C interfaces to Stepper methods

  /// Methods for Stepper creation and deletion
  Stepper* Stepper_new(
    const char* planName,
    const char** libraryNames, int numNames,
    const char** libraryPaths, int numPaths
  );
  void Stepper_delete(Stepper* s);

  /// Methods for running a Stepper
  /**
   * @brief Runs one step of the Stepper given a script input.
   *
   * Note that a Stepper's first step must be over an "initial state" XML node
   * element, which can be empty. If a Stepper's associated PLEXIL Executive is
   * able to execute another macro step without an external script input, that
   * step can be taken by sending in a "delay" XML node element.
   *
   * @param s A Stepper instance
   * @param scriptInput An initial-state element or top-level script element
   * @param errorMessage C-style string pointer to return an error message
   * @param maxMessageLength Maximum length of the error message string
   * @return Error code:
   *         0 - No error,
   *         1 - No step taken due to issue with scriptInput,
   *         2 - Unrecoverable error in PLEXIL Exec,
   *         3 - Unknown error (assume unrecoverable)
   */
  int Stepper_step(Stepper* s, const char* scriptInput, char* errorMessage, const size_t maxMessageLength);

  /**
   * @brief Whether PLEXIL Exec can take a macro step without a script input.
   */
  bool Stepper_needsStep(Stepper* s);

  /**
   * @brief Whether PLEXIL Exec has yet to receive an initial state.
   */
  bool Stepper_needsInitialState(Stepper* s);

  /// Methods to get data out of the Stepper
  const Value* Stepper_getVariableValues(
    const Stepper* s,
    int* count
  );

  void Stepper_getVariables(
    const Stepper* s,
    const char*** varNames,
    const char*** valStrings,
    const char** typeStrings,
    int* count
  );

  const NodeStateOutcomePair* Stepper_getNodeStateOutcomes(
    const Stepper* s,
    const char*** nodeNames,
    int* count
  );

  /// Methods to convert enum values to string literals.
  // Since these return string literals and do not call 'new' or 'malloc',
  // their memory cannot be manually freed/deleted.
  const char* NodeOutcomeEnum_toStringLiteral(NodeOutcome val);
  const char* NodeStateEnum_toStringLiteral(NodeState val);
  const char* ValueTypeEnum_toStringLiteral(ValueType val);

  /// Methods to free memory
  void charArray_delete(char* charArray);
  void arrayOfCharArray_delete(char** nodeNames, int count);
  void arrayOfNodeStateOutcomePair_delete(NodeStateOutcomePair* pairs, int count);
}

#endif // STEPPER_PYTHON_INTERFACE_HH