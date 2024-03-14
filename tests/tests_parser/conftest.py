from typing import Dict, List

from _pytest.python import Metafunc

from tests.tests_parser.test_cases import (
    PARSE_TEST_CASE,
    TREE_TEST_CASES,
)


def _generate_samples(test_cases: Dict) -> List:
    return [
        (input, expected)
        for input, expected in zip(test_cases["input_value"], test_cases["expected_value"])
    ]


def pytest_generate_tests(metafunc: Metafunc):
    if "tree_sample" in metafunc.fixturenames:
        samples = _generate_samples(test_cases=TREE_TEST_CASES)
        metafunc.parametrize(
            argnames="tree_sample",
            argvalues=samples,
            ids=[f"sample - {idx}" for idx in range(len(samples))],
        )

    if "parse_sample" in metafunc.fixturenames:
        samples = _generate_samples(test_cases=PARSE_TEST_CASE)
        metafunc.parametrize(
            argnames="parse_sample",
            argvalues=samples,
            ids=[f"sample - {idx}" for idx in range(len(samples))],
        )
