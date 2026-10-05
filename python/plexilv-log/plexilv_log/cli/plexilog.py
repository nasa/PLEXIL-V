"""Command-line tool for parsing PLEXIL Executive logs."""

import click
import sys

from ..parsers.plexil_executive import PlexilExecutiveParser
from ..validation import ValidationLevel, LogValidationError


@click.command(name='plexilog')
@click.argument('log-file', type=click.File('r'), required=False, default='-')
@click.option('--pretty/--compact', default=True,
              help='Pretty-print JSON (default: pretty)')
@click.option('--lenient', is_flag=True,
              help='Parse in lenient mode (ignore validation errors)')
def main(log_file, pretty, lenient):
    """Parse PLEXIL Executive debug logs to JSON.

    Reads PLEXIL Executive debug logs (from plexiltest) and outputs
    structured JSON representing the execution trace to stdout.

    By default, validation is STRICT: logs with ERROR or WARNING entries,
    empty logs, or missing cycle markers will fail with exit code 2.

    Use --lenient to parse logs that may be malformed (exit code 0).

    If LOG_FILE is not provided, reads from stdin.

    Exit codes:
        0 - Success
        1 - Parse error or I/O error
        2 - Validation error (strict mode only)

    Examples:
        plexilog executive.log
        plexilog executive.log > trace.json
        plexilog executive.log --compact
        plexilog --lenient faulty.log
        cat executive.log | plexilog
        plexilog < executive.log
    """
    parser = PlexilExecutiveParser()
    validation = ValidationLevel.LENIENT if lenient else ValidationLevel.STRICT

    try:
        content = log_file.read()
        trace = parser.parse(content, validation_level=validation)
        indent = 2 if pretty else None
        click.echo(trace.to_json(indent=indent))
    except LogValidationError as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(2)  # Exit code 2 for validation errors
    except Exception as e:
        click.echo(f"Error parsing log: {e}", err=True)
        sys.exit(1)  # Exit code 1 for other errors


if __name__ == '__main__':
    main()
