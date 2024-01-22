from gendiff.scripts.gendiff import generate_diff
import pytest


@pytest.mark.parametrize(
    "file1,file2,file_expected",
    [
        ('tests/fixtures/file11.json', 'tests/fixtures/file12.json', 'tests/fixtures/result1.txt')
    ]
)
def test_generate_diff(file1, file2, file_expected):
    with open(file_expected) as file:
        expected = file.read()

    assert generate_diff('tests/fixtures/file11.json', 'tests/fixtures/file12.json') == expected
