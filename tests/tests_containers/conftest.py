from _pytest.python import Metafunc

from tests.utils import generate_samples
from tests.tests_containers.test_cases import (
    DICT_TEST_CASES,
    SCHEMA_TEST_CASES,
    CLASS_INSTANCES_TEST_CASES,
    SCRIPT_PROPERTY_TEST_CASES,
    CLASS_PROPERTIES_TEST_CASES,
    METHOD_INSTANCES_TEST_CASES,
    SCRIPT_INSTANCES_TEST_CASES,
    METHOD_PROPERTIES_TEST_CASES,
    VARIABLE_INSTANCES_TEST_CASES,
)


def pytest_generate_tests(metafunc: Metafunc) -> None:
    if "variable_sample" in metafunc.fixturenames:
        samples = generate_samples(test_cases=VARIABLE_INSTANCES_TEST_CASES)
        metafunc.parametrize(
            argnames="variable_sample",
            argvalues=samples,
            ids=[f"sample - {sample[1]['name']}" for sample in samples],
        )

    if "method_sample" in metafunc.fixturenames:
        samples = generate_samples(test_cases=METHOD_INSTANCES_TEST_CASES)
        metafunc.parametrize(
            argnames="method_sample",
            argvalues=samples,
            ids=[f"sample - {sample[1]['name']}" for sample in samples],
        )

    if "method_property_sample" in metafunc.fixturenames:
        samples = generate_samples(test_cases=METHOD_PROPERTIES_TEST_CASES)
        metafunc.parametrize(
            argnames="method_property_sample",
            argvalues=samples,
            ids=[f"sample - {idx}" for idx, _ in enumerate(samples)],
        )

    if "class_sample" in metafunc.fixturenames:
        samples = generate_samples(test_cases=CLASS_INSTANCES_TEST_CASES)
        metafunc.parametrize(
            argnames="class_sample",
            argvalues=samples,
            ids=[f"sample - {sample[1]['name']}" for sample in samples],
        )

    if "class_property_sample" in metafunc.fixturenames:
        samples = generate_samples(test_cases=CLASS_PROPERTIES_TEST_CASES)
        metafunc.parametrize(
            argnames="class_property_sample",
            argvalues=samples,
            ids=[f"sample - {idx}" for idx, _ in enumerate(samples)],
        )

    if "script_sample" in metafunc.fixturenames:
        samples = generate_samples(test_cases=SCRIPT_INSTANCES_TEST_CASES)
        metafunc.parametrize(
            argnames="script_sample",
            argvalues=samples,
            ids=[f"sample - {sample[1]['name']}" for sample in samples],
        )

    if "script_property_sample" in metafunc.fixturenames:
        samples = generate_samples(test_cases=SCRIPT_PROPERTY_TEST_CASES)
        metafunc.parametrize(
            argnames="script_property_sample",
            argvalues=samples,
            ids=[f"sample - {idx}" for idx, _ in enumerate(samples)],
        )

    if "dict_sample" in metafunc.fixturenames:
        samples = generate_samples(test_cases=DICT_TEST_CASES)
        metafunc.parametrize(
            argnames="dict_sample",
            argvalues=samples,
            ids=[f"sample - {idx}" for idx, _ in enumerate(samples)],
        )

    if "schema_sample" in metafunc.fixturenames:
        samples = generate_samples(test_cases=SCHEMA_TEST_CASES)
        metafunc.parametrize(
            argnames="schema_sample",
            argvalues=samples,
            ids=[f"sample - {idx}" for idx, _ in enumerate(samples)],
        )
