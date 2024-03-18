import argparse

from uast.__version__ import __version__


class CliParser:
    """
    Command-line argument parser for the program.

    The class provides methods to parse command-line arguments and configure an ArgumentParser object
    with specific settings for the program.
    """

    def parse(self) -> argparse.Namespace:
        """
        Parse command-line arguments and return the parsed namespace.

        :return: Parsed command-line arguments stored as a namespace.
        :rtype: argparse.Namespace
        """
        parser = self.create_parser()

        parser = self.add_version_command(parser=parser)
        parser = self.add_source_to_parser(parser=parser)
        parser = self.add_print_option_to_parser(parser=parser)

        namespace = parser.parse_args()
        return namespace

    @staticmethod
    def create_parser() -> argparse.ArgumentParser:
        """
        Create and return an ArgumentParser object for parsing command-line arguments.

        :return: An ArgumentParser object configured with the following settings:
        :rtype: argparse.ArgumentParser
        """
        return argparse.ArgumentParser(
            prog="uast",
            description="DESCRIPTION",
            epilog="For help with a specific command, see: `sequence help <command>`",
        )

    @staticmethod
    def add_version_command(parser: argparse.ArgumentParser) -> argparse.ArgumentParser:
        """
        Add a version command to the given ArgumentParser object.

        :param parser: An ArgumentParser object to which the version command will be added.
        :type parser: argparse.ArgumentParser

        :return: The modified ArgumentParser object with the version command added.
        :rtype: argparse.ArgumentParser

        .. note::
            The version command adds an argument '-v' or '--version' to the parser,
            which, when specified, displays the version information of the program.
        """
        parser.add_argument(
            "-v",
            "--version",
            action="version",
            version=f"{parser.prog}: v{__version__}",
            help="Display the version information.",
        )
        return parser

    @staticmethod
    def add_source_to_parser(parser: argparse.ArgumentParser) -> argparse.ArgumentParser:
        """
        Add a source argument to the given ArgumentParser object.

        :param parser: An ArgumentParser object to which the source argument will be added.
        :type parser: argparse.ArgumentParser

        :return: The modified ArgumentParser object with the source argument added.
        :rtype: argparse.ArgumentParser

        This method adds an optional positional argument 'source' to the parser,
        which specifies the source to parse.
        """
        parser.add_argument("source", type=str, nargs="?", help="Source to parse")
        return parser

    @staticmethod
    def add_print_option_to_parser(parser: argparse.ArgumentParser) -> argparse.ArgumentParser:
        """
        Add a print option to the given ArgumentParser object.

        :param parser: An ArgumentParser object to which the print option will be added.
        :type parser: argparse.ArgumentParser

        :return: The modified ArgumentParser object with the print option added.
        :rtype: argparse.ArgumentParser

        This method adds an optional argument `-p` or `--print` to the parser,
        which specifies what information to print.

        :Notes:

        - The print option allows the user to specify what information to print.
        - It accept one of the following values: `schema` and `json`.
        """
        parser.add_argument("-p", "--print", nargs="+", choices=["schema", "json"], help="Print option")
        return parser
