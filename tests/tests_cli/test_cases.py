from uast.__version__ import __version__

CLI_TEST_CASES = [
    (
        "python uast/__init__.py tests/utils.py --p json",
        "bla",
    ),
    (
        "python uast/__init__.py tests/utils.py --p schema",
        "bla",
    ),
    (
        "python uast/__init__.py --version",
        f"uast: v{__version__}",
    ),
]
