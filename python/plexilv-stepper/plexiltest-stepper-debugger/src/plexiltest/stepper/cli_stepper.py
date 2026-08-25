from os import path
from pprint import PrettyPrinter
import argparse

from ..shared import PLEXILTest
from ..shared import extract_elements_from_script
from ..shared import convert_script_element_to_xml
from ..shared import ExecutiveParsingError
from ..shared import ExecutiveError
from ..shared import MultipleInitialStateError
from ..shared import ScriptParsingError


def main():
    parser = argparse.ArgumentParser(description="PLEXIL Test Stepper")
    parser.add_argument("-p","--plan",
                        help="Path to the compiled plan file (.plx)",
                        type=str,
                        required=True)
    parser.add_argument("-s","--script",
                        help="Path to the compiled or uncompiled script file"
                             "(.pst or .psx)",
                        type=str,
                        required=True)
    parser.add_argument("--library_names",
                        type=str,
                        help="An optional list of compiled plan library"
                             "files (.plx)",
                        nargs="+",
                        default=[])
    parser.add_argument("--library_paths",
                        type=str,
                        nargs="+",
                        default=[],
                        help="An optional list of plan library directories "
                             "ordered by search priority")

    args = parser.parse_args()

    plan = args.plan
    script = args.script
    library_names = args.library_names
    library_paths = args.library_paths

    if not path.isfile(script):
        print("Cannot find script file: " + script)
        exit
    if not path.isfile(plan):
        print(f"Cannot find plan file: {plan}. "
              f"Did you forget to compile it with plexilc?")
        exit

    def wait_for_input():
        input("\n> Press Enter to continue...")
        print("")

    def run_step(item):
        try:
            plexiltest.step(convert_script_element_to_xml(item))
        except MultipleInitialStateError:
            print(f"Initial state error: Multiple initial states are not allowed.\n")
            raise MultipleInitialStateError
        except ScriptParsingError as e:
            print(f"Script error: Ill-formatted input - \n{e}\n")
            raise e
        except ExecutiveParsingError as e:
            print(f"Executive Parsing error: Rejected input - {e}.\n")
            raise e
        except ExecutiveError as e:
            print(f"Executive error: Something failed in the PLEXIL Exec - {e}.\n")
            raise e
        except Exception as e:
            print(f"Error: Some unanticipated error occurred - {e}.\n")
            raise e

    plexiltest = PLEXILTest(plan, library_names, library_paths)
    try:
        initial_state, script_elements = extract_elements_from_script(script)
    except ScriptParsingError as e:
        print(f"\nScript error: \n{e}\n")
        print("********** EXITING **********")
        return

    print("\n********** Initial state **********")
    if initial_state:
        try:
            run_step(initial_state)
        except:
            return
    else:
        plexiltest.step('<InitialState/>')
    print(f"{plexiltest.pprint_str()}")
    wait_for_input()

    for element in script_elements:
        print("================================")
        print(element)
        print("================================\n")
        try:
            run_step(element)
        except:
            print("********** EXITING **********")
            return
        print("********** Next state **********")
        print(plexiltest.pprint_str())
        wait_for_input()

    while plexiltest.needs_step():
        run_step('<Delay/>')
        print("********** Next state **********")
        print(plexiltest.pprint_str())
        wait_for_input()

    print("********** Done! **********\n")

if __name__ == "__main__":
    main()