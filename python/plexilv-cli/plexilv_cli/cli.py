"""Unified CLI for PLEXIL verification tools."""

import click
from plexilv_run.cli import main as run_command
from plexilv_diff.cli import main as diff_command
from plexilv.plexil.translator.cli import main as plx2maude_command
from plexilv.plexilscript.translator.cli import main as psx2maude_command
from plexilv_log.cli.plexilog import main as plexilog_command
from plexilv_log.cli.plexilog_maude import main as plexilog_maude_command
from plexilv_log.cli.plexilog_diff import main as plexilog_diff_command


@click.group()
@click.version_option()
def main():
    """PLEXIL verification tools.

    This tool provides commands for executing and verifying PLEXIL plans:

    \b
    run (or test)  Execute a PLEXIL plan using the PLEXIL-V formal semantics
    diff           Compare two PLEXIL plans
    plx2maude      Transpile PLEXIL XML to PLEXIL-V Maude format
    psx2maude      Transpile PLEXILScript XML to PLEXIL-V Maude format
    plexilog       Parse PLEXIL Executive logs to JSON
    plexilog-maude Parse PLEXIL-V/Maude logs to JSON
    plexilog-diff  Compare execution logs
    """
    pass


@main.command(name='help')
@click.argument('command', required=False)
def help_command(command):
    """Display help information.

    Show general help, or help for a specific subcommand.

    Examples:

    \b
    plexilv help           Show this help message
    plexilv help run       Show help for the run command
    plexilv help diff      Show help for the diff command
    """
    if command is None:
        # Show main help
        click.echo(main.get_help(click.Context(main)))
    elif command in main.commands:
        # Show help for specific subcommand
        ctx = click.Context(main.commands[command])
        click.echo(main.commands[command].get_help(ctx))
    else:
        click.echo(f"Error: Unknown command '{command}'", err=True)
        click.echo(f"Available commands: {', '.join(sorted(main.commands.keys()))}", err=True)
        raise click.Exit(1)


# Register the run/test command
main.add_command(run_command, name='run')
main.add_command(run_command, name='test')  # Alias for run

# Register the diff command
main.add_command(diff_command, name='diff')

# Register the translator commands
main.add_command(plx2maude_command)
main.add_command(psx2maude_command)

# Register the log processing commands
main.add_command(plexilog_command, name='plexilog')
main.add_command(plexilog_maude_command, name='plexilog-maude')
main.add_command(plexilog_diff_command, name='plexilog-diff')


if __name__ == '__main__':
    main()