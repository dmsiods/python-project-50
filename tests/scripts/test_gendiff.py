from gendiff.scripts.gendiff import generate_diff
import pytest


@pytest.mark.parametrize(
    "file1,file2,file_expected,output_format",
    [
        ('tests/fixtures/file11.json', 'tests/fixtures/file12.json',
         'tests/fixtures/result1.txt', 'stylish'),
        ('tests/fixtures/file11.yml', 'tests/fixtures/file12.yaml',
         'tests/fixtures/result1.txt', 'stylish'),
        ('tests/fixtures/file21.json', 'tests/fixtures/file22.json',
         'tests/fixtures/result2.txt', 'stylish'),
        ('tests/fixtures/file21.json', 'tests/fixtures/file22.json',
         'tests/fixtures/result2_plain.txt', 'plain'),
        ('tests/fixtures/file21.json', 'tests/fixtures/file22.json',
         'tests/fixtures/result2_json.txt', 'json'),
        ('tests/fixtures/file1.json', 'tests/fixtures/file2.json',
         'tests/fixtures/result_stylish', 'stylish'),
        ('tests/fixtures/file1.yml', 'tests/fixtures/file2.yml',
         'tests/fixtures/result_plain', 'plain'),
    ]
)
def test_generate_diff(file1, file2, file_expected, output_format):
    with open(file_expected) as file:
        expected = file.read()

    assert (generate_diff(file1, file2, output_format).strip()
            == expected.strip())
