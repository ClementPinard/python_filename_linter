import pytest

from python_filename_linter.main import to_snake_case


@pytest.mark.parametrize(
    "test_input,expected",
    [
        ("A_A", "a_a"),
        ("helloDear", "hello_dear"),
        ("__ThisIsATest__", "__this_is_atest__"),
    ],
)
def test_eval(test_input, expected):
    assert to_snake_case(test_input) == expected
