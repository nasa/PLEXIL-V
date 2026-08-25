"""Command-line interface for plexilv-stepper."""

import os
import sys
from pathlib import Path
from pprint import PrettyPrinter

import click

from plexilv_stepper.plexilvtest import PLEXILVTest


def pprint_state(state):
    pp = PrettyPrinter(indent=4, width=80, compact=False)
    print("Stepper Status: ", end="")
    pp.pprint(state)


def pause():
    input("\n> Press Enter to continue...")


@click.command()
@click.option(
    "-p",
    "--plan",
    required=True,
    type=click.Path(exists=True, path_type=Path),
    help="Path to PLEXIL plan file (.plx or .maude)",
)
@click.option(
    "-s",
    "--script",
    required=True,
    type=click.Path(exists=True, path_type=Path),
    help="Path to PLEXIL script file (.psx or .maude)",
)
@click.option(
    "--plexilv-home",
    type=click.Path(exists=True, file_okay=False, dir_okay=True, path_type=Path),
    help="Path to PLEXIL-V repository root (overrides $PLEXILV_HOME)",
)
def main(
    plan: Path,
    script: Path,
    plexilv_home: Path | None,
) -> None:
    """Execute PLEXIL plan step-by-step using the formal semantics of PLEXIL-V.
    """
    try:
        home_path = str(plexilv_home) if plexilv_home else os.environ.get("PLEXILV_HOME", "")
        if not home_path:
            click.echo("Error: PLEXILV_HOME environment variable is not set and --plexilv-home was not provided.", err=True)
            sys.exit(1)

        stepper = PLEXILVTest(plexilv_home=home_path, plan=str(plan), script=str(script))

        print("\n********** Initial state **********")
        state = stepper.get_current_state()
        pprint_state(state)
        pause()

        while stepper.needs_step():
            stepper.step()
            print("\n********** Next state **********")
            state = stepper.get_current_state()
            pprint_state(state)
            pause()

    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


if __name__ == "__main__":
    main()