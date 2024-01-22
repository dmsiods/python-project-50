from gendiff.scripts.gendiff import generate_diff
from pytest import fixture


@fixture(name='result1')
def _result1():
    with open('tests/fixtures/result1.txt') as result_file:
        result = result_file.read()

    return result


def test_generate_diff(result1):
    assert generate_diff('tests/fixtures/file11.json', 'tests/fixtures/file12.json') == result1
