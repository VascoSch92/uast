from typing import Any, Dict, List, Tuple


def error_message(expected: Any, got: Any) -> str:
    """
    Return an error message in the format "Expected: <expected>. Got <got>" comparing the expected value with
    the actual value.

    :param expected: The expected value.
    :type expected: Any
    :param got: The actual value.
    :type got: Any

    :return: A string containing the error message.
    :rtype: str
    """
    return f"Expected: {expected}. Got {got}."


def generate_samples(test_cases: Dict) -> List[Tuple]:
    """
    Generate sample test cases from a dictionary of input and expected values.

    :param test_cases: A dictionary containing input and expected values.
    :type test_cases: Dict

    :return: A list of tuples where each tuple contains an input value and its corresponding expected value.
    :rtype: List[Tuple]

    Example:
    >>> test_cases = {"input_value": [1, 2, 3], "expected_value": [10, 20, 30]}
    >>> generate_samples(test_cases)
    [(1, 10), (2, 20), (3, 30)]
    """
    return list((input, expected) for input, expected in zip(test_cases["input_value"], test_cases["expected_value"]))

def lists_are_equal(a: List, b: List) -> bool:

    if len(a) != len(b):
        return False
    for element_a, element_b in zip(a, b):
        if element_a != element_b:
            return False
    return True