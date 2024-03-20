"""
@pytest.mark.parametrize(
    "input_value, expected_value",
    CLI_TEST_CASES,
)
def test_cli(input_value, expected_value):
    ouput = os.system(input_value)
    if ouput != expected_value:
        raise ValueError(
            error_message(expected=expected_value, got=ouput)
        )
"""
