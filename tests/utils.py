from typing import Any


def error_message(expected: Any, got: Any) -> str:
    return f"Expected: {expected}. Got {got}."
