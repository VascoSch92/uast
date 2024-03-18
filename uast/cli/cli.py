import sys
from pathlib import Path

from uast.cli.parser import CliParser
from uast.core.parser import parse


class CommandLineInterface:
    """
    A command-line interface class for executing commands.

    This method initializes a `CliParser` object to parse command-line arguments
    and then executes commands based on the parsed arguments using the `execute_command` function.

    :Methods:
        - `execute() -> None`: Parse command-line arguments and execute corresponding commands.
    """

    @staticmethod
    def execute() -> None:
        """
        The method parses command-line arguments using a `CliParser` object
        and executes commands based on the parsed arguments using the `execute_command` function.

        :return: None
        :rtype: None
        """
        args = CliParser().parse()
        execute_command(args=args)


def execute_command(args) -> None:
    """
    The method executes a command based on the provided command-line arguments.
    It expects the following arguments:

    - `args.source`: The source file to be parsed.
    - `args.print`: The print option to specify the output format.

    If `args.print` is ["schema"], the function prints the schema of the parsed source file and exits.
    If `args.print` is ["json"], the function prints the parsed content in JSON format and exits.
    If `args.print` is not one of the specified options, the function does nothing.

    :param args: The parsed command-line arguments.
    :type args: Any

    :return: None
    :rtype: None

    :raises SystemExit: If an error occurs during parsing or printing.
    """
    source = Path(args.source).absolute()

    if args.print == ["schema"]:
        sys.exit(f"{parse(source=source).schema()}")
    elif args.print == ["json"]:
        sys.exit(f"{parse(source=source).json()}")


def execute_command_line_interface() -> None:
    """
    The method executes the command-line interface by calling the `execute` method
    of the `CommandLineInterface` class.

    :return: None
    :rtype: None
    """
    CommandLineInterface.execute()
