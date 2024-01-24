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


def stringify_dict(data, level_space='    '):
    def helper(data_elem, level=0):
        result_list = ['{']
        prefix = level_space * level

        for key in data_elem.keys():
            if not isinstance(data_elem[key], dict):
                value_string = _modify_values_for_output(data_elem[key])
            else:
                value_string = helper(data_elem[key], level + 1)

            result_list.append(f'{prefix}{level_space}{key}: {value_string}')

        result_list.append(prefix + '}')

        return '\n'.join(result_list)

    return helper(data)


def _modify_values_for_output(value):
    result = value

    if isinstance(value, bool):
        result = str(value).lower()
    elif value is None:
        result = 'null'

    return result


def _generate_elem_result_string(status, key, key_stat):
    if not isinstance(key_stat, dict):
        return [f'    {key}: {key_stat}']

    prev_value = key_stat.get('prev_value', None)
    prev_value = _modify_values_for_output(prev_value)

    curr_value = key_stat.get('curr_value', None)
    curr_value = _modify_values_for_output(curr_value)

    result_list = []

    if key_stat['status'] == 'same':
        result_list.append(f'    {key}: {curr_value}')
    elif key_stat['status'] == 'removed':
        result_list.append(f'  - {key}: {prev_value}')
    elif key_stat['status'] == 'added':
        result_list.append(f'  + {key}: {curr_value}')
    elif key_stat['status'] == 'changed':
        result_list.append(f'  - {key}: {prev_value}')
        result_list.append(f'  + {key}: {curr_value}')
    else:
        raise Exception('Smth has gone wrong!')

    return result_list


# def stringify_diff(diff, level_space='    '):
#     def helper(diff_elem, level=0):
#         prefix = level_space * level
#         result_list = ['{']
#
#         for key in sorted(diff_elem.keys()):
#             if 'children' in diff_elem[key]:
#                 result_list.extend(helper(diff_elem[key]['children'], level + 1))
#             else:
#
#
#             key_result = helper(elem[key], level + 1)
#             result_list.extend(_generate_elem_result_string(key, key_result))
#
#         result_list.append(prefix + '}')
#
#         return '\n'.join(result_list)
#
#     return helper(diff)


def generate_diff(file_path1, file_path2):
    prev_data = read_data_from_file(file_path1)
    curr_data = read_data_from_file(file_path2)

    print(stringify_dict(prev_data))

    # data_diff = create_diff(prev_data, curr_data)
    # print(data_diff)

    # return stringify_diff(data_diff)


if __name__ == '__main__':
    # main()

    print(generate_diff('tests/fixtures/file21.json', 'tests/fixtures/file22.json'))
