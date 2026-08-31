"""IndentedWriter class for managing indented output."""


class IndentedWriter:
    """Handles nested formatting with manual indentation control."""

    def __init__(self, indent_str: str = "  "):
        self.indent_str = indent_str
        self.level = 0
        self.lines: list[str] = []
        self.current_line: list[str] = []

    def indent(self):
        """Increase indentation level."""
        self.level += 1

    def dedent(self):
        """Decrease indentation level."""
        if self.level > 0:
            self.level -= 1

    def write(self, text: str):
        """Write text to the current line without newline."""
        self.current_line.append(text)

    def writeln(self, text: str = ""):
        """Write text with newline, applying current indentation."""
        if text or self.current_line:
            line_content = "".join(self.current_line) + text
            if line_content.strip():  # Only indent non-empty lines
                self.lines.append(self.indent_str * self.level + line_content)
            else:
                self.lines.append("")
            self.current_line = []
        else:
            self.lines.append("")

    def blank_line(self):
        """Add a blank line."""
        self.writeln()

    def get_output(self) -> str:
        """Return the complete buffered output."""
        # Flush any remaining content
        if self.current_line:
            self.writeln()
        return "\n".join(self.lines)

    def clear(self):
        """Clear all buffered output."""
        self.lines = []
        self.current_line = []
        self.level = 0
