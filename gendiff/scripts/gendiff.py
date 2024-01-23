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


def _get_data_statistic(old_data, new_data):
    statistic = {}

    old_keys = set(old_data.keys())
    new_keys = set(new_data.keys())
    union_keys = new_keys.union(old_keys)

    for key in union_keys:
        if key in old_keys and key in new_keys:
            if old_data[key] == new_data[key]:
                statistic[key] = {'status': 'same', 'curr_value': new_data[key]}
            else:
                statistic[key] = {
                    'status': 'changed',
                    'prev_value': old_data[key],
                    'curr_value': new_data[key],
                }
        elif key in old_keys:
            statistic[key] = {'status': 'removed', 'prev_value': old_data[key]}
        else:
            statistic[key] = {'status': 'added', 'curr_value': new_data[key]}

    return statistic


def _modify_values_for_output(value):
    result = value

    if isinstance(value, bool):
        result = str(value).lower()
    elif value is None:
        result = 'null'

    return result


def _generate_result_string(statistic):
    result_list = ['{']

    for key in sorted(statistic.keys()):
        prev_value = statistic[key].get('prev_value', None)
        prev_value = _modify_values_for_output(prev_value)

        curr_value = statistic[key].get('curr_value', None)
        curr_value = _modify_values_for_output(curr_value)

        if statistic[key]['status'] == 'same':
            result_list.append(f'    {key}: {curr_value}')
        elif statistic[key]['status'] == 'removed':
            result_list.append(f'  - {key}: {prev_value}')
        elif statistic[key]['status'] == 'added':
            result_list.append(f'  + {key}: {curr_value}')
        elif statistic[key]['status'] == 'changed':
            result_list.append(f'  - {key}: {prev_value}')
            result_list.append(f'  + {key}: {curr_value}')
        else:
            raise Exception('Smth has gone wrong!')

    result_list.append('}')

    return '\n'.join(result_list)


def generate_diff(file_path1, file_path2):
    old_data = read_data_from_file(file_path1)
    new_data = read_data_from_file(file_path2)

    statistic = _get_data_statistic(old_data, new_data)

    return _generate_result_string(statistic)


if __name__ == '__main__':
    main()
