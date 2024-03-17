from uast.cli.cli import execute_command_line_interface
from uast.core.parser import parse  # noqa: F401


def main() -> None:
    """Entry point for the command line interface."""
    execute_command_line_interface()


if __name__ == "__main__":
    main()
