#!usr/bin/env python3
import argparse

from gendiff.tools.file_readers import read_data_from_file


def main():
    parser = argparse.ArgumentParser(
        description='Compares two configuration files and shows a difference.')
    parser.add_argument('first_file')
    parser.add_argument('second_file')
    parser.add_argument('-f', '--format', metavar='FORMAT',
                        help='set format of output')

    args = parser.parse_args()

    return generate_diff(args.first_file, args.second_file)


def create_diff(prev_data, curr_data):
    diff = {}

    prev_keys = set(prev_data.keys())
    curr_keys = set(curr_data.keys())
    union_keys = curr_keys.union(prev_keys)

    for key in union_keys:
        if key in prev_keys and key in curr_keys:

            if isinstance(prev_data[key], dict) and isinstance(curr_data[key], dict):

                if prev_data[key] == curr_data[key]:
                    diff[key] = {'status': 'same', 'curr_value': curr_data[key]}
                else:
                    diff[key] = {
                        'status': 'changed',
                        'children': create_diff(prev_data[key], curr_data[key])
                    }

            elif prev_data[key] == curr_data[key]:
                diff[key] = {'status': 'same', 'curr_value': curr_data[key]}

            else:
                diff[key] = {
                    'status': 'changed',
                    'pre_value': prev_data[key],
                    'curr_value': curr_data[key]
                }

        elif key in prev_keys:
            diff[key] = {'status': 'removed', 'prev_value': prev_data[key]}

        elif key in curr_keys:
            diff[key] = {'status': 'added', 'curr_value': curr_data[key]}

        else:
            raise Exception('Smth has gone wrong!!!')

    return diff


def stringify_dict(data, base_prefix='', level_space='    '):
    def helper(data_elem, level=1):
        result_list = ['{']
        prefix = level_space * level

        for key in data_elem.keys():
            if not isinstance(data_elem[key], dict):
                value_string = _modify_value_for_output(data_elem[key])
            else:
                value_string = helper(data_elem[key], level + 1)

            result_list.append(f'{base_prefix}{prefix}{level_space}{key}: {value_string}')

        result_list.append(f'{base_prefix}{prefix}' + '}')

        return '\n'.join(result_list)

    return helper(data)


def _modify_value_for_output(value):
    result = value

    if isinstance(value, bool):
        result = str(value).lower()
    elif value is None:
        result = 'null'

    return str(result)


# def _prepare_diff_value_for_output(diff_value):
#     if isinstance(diff_value, dict):
#         diff_value_string = stringify_dict(diff_value)
#     else:
#         diff_value_string = _modify_value_for_output(diff_value)
#
#     return diff_value_string


def gen_atomic_string(prefix, key, status, prev_value_str=None, curr_value_str=None):
    result_list = []

    if status == 'same':
        result_list.append(f'{prefix}    {key}: {curr_value_str}')
    elif status == 'removed':
        result_list.append(f'{prefix}  - {key}: {prev_value_str}')
    elif status == 'added':
        result_list.append(f'{prefix}  + {key}: {curr_value_str}')
    elif status == 'changed':
        result_list.append(f'{prefix}  - {key}: {prev_value_str}')
        result_list.append(f'{prefix}  + {key}: {curr_value_str}')
    else:
        raise Exception('Smth has gone wrong!')

    return result_list


def stringify_diff(diff, level_space='    '):

    def helper(diff_elem, level=0):
        prefix = level_space * level
        result_list = ['{']

        for key in sorted(diff_elem.keys()):
            key_status = diff_elem[key]['status']
            key_prev_value = diff_elem[key].get('prev_value')
            key_curr_value = diff_elem[key].get('curr_value')

            if isinstance(key_prev_value, dict):
                key_prev_value_str = stringify_dict(key_prev_value, prefix)
            else:
                key_prev_value_str = _modify_value_for_output(key_prev_value)

            if 'children' in diff_elem[key]:
                key_status = 'same'
                key_curr_value_str = helper(diff_elem[key]['children'], level + 1)
            elif isinstance(key_curr_value, dict):
                key_curr_value_str = stringify_dict(key_curr_value, prefix)
            else:
                key_curr_value_str = _modify_value_for_output(key_curr_value)

            result_list.extend(gen_atomic_string(prefix, key, key_status, key_prev_value_str, key_curr_value_str))

        result_list.append(prefix + '}')

        return '\n'.join(result_list)

    return helper(diff)


def generate_diff(file_path1, file_path2):
    prev_data = read_data_from_file(file_path1)
    curr_data = read_data_from_file(file_path2)

    # print(stringify_dict(prev_data))

    data_diff = create_diff(prev_data, curr_data)
    # print(data_diff)

    return stringify_diff(data_diff)


if __name__ == '__main__':
    # main()

    print(generate_diff('tests/fixtures/file21.json', 'tests/fixtures/file22.json'))
