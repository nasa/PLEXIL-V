"""Command-line tool for comparing PLEXIL execution traces."""

import click
import sys

from ..parsers.plexil_executive import PlexilExecutiveParser
from ..parsers.maude import MaudeParser
from ..validation import ValidationLevel, LogValidationError
from ..diff import compare_traces, format_diff_report, format_json_diff, DiffResult


@click.command(name='plexilog-diff')
@click.argument('plexil-log', type=click.Path(exists=True))
@click.argument('maude-log', type=click.Path(exists=True))
@click.option('--verbose', '-v', is_flag=True,
              help='Show detailed comparison report')
@click.option('--json', '-j', is_flag=True,
              help='Output in JSON format')
@click.option('--lenient', is_flag=True,
              help='Parse logs in lenient mode (ignore validation errors)')
def main(plexil_log, maude_log, verbose, json, lenient):
    """Compare PLEXIL Executive and Maude/PLEXIL-V execution traces.

    Parses both log files and compares the execution traces for
    differences. By default, outputs "EQ" if equal or a comparison
    report if different. Use --verbose for detailed differences or
    --json for machine-readable JSON format.

    By default, validation is STRICT: logs with errors or missing
    structure will fail before comparison. Use --lenient to compare
    logs that may be malformed.

    Exit codes:
        0 - Traces are equal
        1 - Traces differ
        2 - Parse/validation error

    Examples:
        plexilog-diff executive.log maude.log
        plexilog-diff executive.log maude.log --verbose
        plexilog-diff executive.log maude.log --json
        plexilog-diff faulty1.log faulty2.log --lenient
    """
    plexil_parser = PlexilExecutiveParser()
    maude_parser = MaudeParser()
    validation = ValidationLevel.LENIENT if lenient else ValidationLevel.STRICT

    try:
        # Parse both logs
        with open(plexil_log) as f:
            plexil_trace = plexil_parser.parse(f.read(), validation_level=validation)

        with open(maude_log) as f:
            maude_trace = maude_parser.parse(f.read(), validation_level=validation)

        # Compare traces
        result, diff_details = compare_traces(plexil_trace, maude_trace)

        # Output based on mode
        if json:
            # JSON output mode (always)
            click.echo(format_json_diff(diff_details))
            sys.exit(0 if result == DiffResult.EQUAL else 1)
        elif verbose:
            # Verbose mode: show detailed human-readable comparison report
            report = format_diff_report(diff_details, verbose=True)
            click.echo(report)
            sys.exit(0 if result == DiffResult.EQUAL else 1)
        else:
            # Default mode: "EQ" if equal, comparison report if different
            if result == DiffResult.EQUAL:
                click.echo("EQ")
                sys.exit(0)
            else:
                report = format_diff_report(diff_details, verbose=False)
                click.echo(report)
                sys.exit(1)

    except LogValidationError as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(2)
    except FileNotFoundError as e:
        click.echo(f"Error: File not found: {e.filename}", err=True)
        sys.exit(2)
    except Exception as e:
        click.echo(f"Error comparing traces: {e}", err=True)
        sys.exit(2)


if __name__ == '__main__':
    main()
