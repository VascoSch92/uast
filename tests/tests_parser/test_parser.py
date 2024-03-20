from typing import List

import pytest

from tests.utils import error_message
from uast.core.parser import (
    parse,
    _parse_tree,
)


def test_parse_tree(tree_sample) -> None:
    tree = _parse_tree(source=tree_sample[0])
    for tree_value, expected_value in zip(tree, tree_sample[1]):
        if tree_value != expected_value:
            raise ValueError(
                error_message(expected=expected_value, got=tree_value)
            )


def test_parser(parse_sample) -> None:
    tree = parse(source=parse_sample[0])
    if isinstance(tree, List):
        for tree_value, expected_value in zip(tree, parse_sample[1]):
            if tree_value != expected_value:
                raise ValueError(
                    error_message(expected=expected_value, got=tree_value)
                )
    else:
        if tree != parse_sample[1]:
            raise ValueError(
                error_message(expected=parse_sample[1], got=tree)
            )


@pytest.mark.parametrize(
    "source, error",
    [
        ("tests", NotImplementedError),
        ("README.md", ValueError),
        (0, ValueError),
    ]
)
def test_parser_error(source, error) -> None:
    with pytest.raises(error):
        _ = parse(source=source)
