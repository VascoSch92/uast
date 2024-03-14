import ast
from typing import Dict, List

from _pytest.python import Metafunc

from tests.tests_ast_parsers.test_cases import (
    CLASS_TEST_CASES,
    VALUE_TEST_CASES,
    IMPORT_TEST_CASES,
    METHOD_TEST_CASES,
    ARGUMENT_TEST_CASES,
    ANNOTATION_TEST_CASES,
    ASSIGNMENT_TEST_CASES,
    IMPORT_FROM_TEST_CASES,
    ANNOTATE_ASSIGNMENT_TEST_CASES,
)


def _generate_samples(test_cases: Dict, attribute: str = "") -> List:
    """
    Generate sample input-output pairs from test cases.

    :param test_cases: A dictionary containing test cases where
        "input_values" key holds the Python code snippets of input values (as strings) and
        "expected_values" key holds the expected output values as a list.
    :type test_cases: dict

    :param attribute: Optional. The attribute name to extract from each test case.
        If not provided, the whole test case branch will be used.
    :type attribute: str

    :return: A list of tuples representing input-output pairs generated
        from the test cases. Each tuple contains an input value and its corresponding
        expected output value.
    :rtype: list
    """
    test_cases_tree = ast.parse(test_cases["input_values"])

    input_values = [
        branch.__getattribute__(attribute)
        if attribute else branch
        for branch in test_cases_tree.body
    ]
    expected_values = test_cases["expected_values"]

    return [(input, expected) for input, expected in zip(input_values, expected_values)]


def pytest_generate_tests(metafunc: Metafunc):
    if "annotation_sample" in metafunc.fixturenames:
        samples = _generate_samples(test_cases=ANNOTATION_TEST_CASES, attribute="annotation")
        metafunc.parametrize(
            argnames="annotation_sample",
            argvalues=samples,
            ids=[f"sample - {sample[1]}" for sample in samples],
        )

    if "value_sample" in metafunc.fixturenames:
        samples = _generate_samples(test_cases=VALUE_TEST_CASES, attribute="value")
        metafunc.parametrize(
            argnames="value_sample",
            argvalues=samples,
            ids=[f"sample - {sample[1]}" for sample in samples],
        )

    if "annotate_assignment_sample" in metafunc.fixturenames:
        samples = _generate_samples(test_cases=ANNOTATE_ASSIGNMENT_TEST_CASES)
        metafunc.parametrize(
            argnames="annotate_assignment_sample",
            argvalues=samples,
            ids=[f"sample - {sample[1].name}" for sample in samples],
        )

    if "assignment_sample" in metafunc.fixturenames:
        samples = _generate_samples(test_cases=ASSIGNMENT_TEST_CASES)
        metafunc.parametrize(
            argnames="assignment_sample",
            argvalues=samples,
            ids=[f"sample - {sample[1][0].name}" for sample in samples],
        )

    if "method_sample" in metafunc.fixturenames:
        samples = _generate_samples(test_cases=METHOD_TEST_CASES)
        metafunc.parametrize(
            argnames="method_sample",
            argvalues=samples,
            ids=[f"sample - {sample[1]}" for sample in samples],
        )

    if "argument_sample" in metafunc.fixturenames:
        samples = _generate_samples(test_cases=ARGUMENT_TEST_CASES, attribute="args")
        metafunc.parametrize(
            argnames="argument_sample",
            argvalues=samples,
            ids=[f"sample - {idx}" for idx in range(len(samples))],
        )

    if "class_sample" in metafunc.fixturenames:
        samples = _generate_samples(test_cases=CLASS_TEST_CASES)
        metafunc.parametrize(
            argnames="class_sample",
            argvalues=samples,
            ids=[f"sample - {sample[0].name}" for sample in samples],
        )

    if "import_from_sample" in metafunc.fixturenames:
        samples = _generate_samples(test_cases=IMPORT_FROM_TEST_CASES)
        metafunc.parametrize(
            argnames="import_from_sample",
            argvalues=samples,
            ids=[f"{sample[1].__repr__()}" for sample in samples],
        )

    if "import_sample" in metafunc.fixturenames:
        samples = _generate_samples(test_cases=IMPORT_TEST_CASES)
        metafunc.parametrize(
            argnames="import_sample",
            argvalues=samples,
            ids=[f"{sample[1].__repr__()}" for sample in samples],
        )
