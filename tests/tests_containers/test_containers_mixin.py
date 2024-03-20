import pytest

from tests.utils import error_message
from uast.core.containers.containers import Method, Variable
from uast.core.containers.containers_mixin import (
    equality_between_containers,
    _equality_between_dictionaries,
)


@pytest.mark.parametrize(
    "a, b, expected_output",
    [
        ({}, {}, True),
        ({"a": 1}, {}, False),
        ({"a": 1}, {"a": 1}, True),
    ]
)
def test_equality_between_dictionaries(a, b, expected_output) -> None:
    if _equality_between_dictionaries(a=a, b=b) != expected_output:
        raise ValueError(
            error_message(
                expected=expected_output,
                got=_equality_between_dictionaries(a=a, b=b),
            )
        )


@pytest.mark.parametrize(
    "a, b, _type, expected_output",
    [
        (Variable(name=""), Variable(name=""), Variable, True),
        (Method(name="123"), Method(name=""), Method, False),
        (Variable(name="a"), Method(name="a"), Variable, False),
    ]
)
def test_equality_between_containers(a, b, _type,  expected_output) -> None:
    if equality_between_containers(a=a, b=b, _type=_type) != expected_output:
        raise ValueError(
            error_message(
                expected=expected_output,
                got=equality_between_containers(a=a, b=b, _type=_type),
            )
        )
