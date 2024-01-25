#!usr/bin/env python3
import argparse

from gendiff.tools.file_readers import read_data_from_file
from gendiff.tools.stylish_formatter import stylish_format


def main():
    parser = argparse.ArgumentParser(
        description='Compares two configuration files and shows a difference.')
    parser.add_argument('first_file')
    parser.add_argument('second_file')
    parser.add_argument('-f', '--format', default='stylish', metavar='FORMAT',
                        help='set format of output')

    args = parser.parse_args()

    return generate_diff(args.first_file, args.second_file, args.format)


def create_diff(prev_data, curr_data):
    diff = {}

    prev_keys = set(prev_data.keys())
    curr_keys = set(curr_data.keys())
    union_keys = curr_keys.union(prev_keys)

    for key in union_keys:
        if key in prev_keys and key in curr_keys:

            if (isinstance(prev_data[key], dict)
                    and isinstance(curr_data[key], dict)):

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
                    'prev_value': prev_data[key],
                    'curr_value': curr_data[key]
                }

        elif key in prev_keys:
            diff[key] = {'status': 'removed', 'prev_value': prev_data[key]}

        elif key in curr_keys:
            diff[key] = {'status': 'added', 'curr_value': curr_data[key]}

        else:
            raise Exception('Smth has gone wrong!!!')

    return diff


def generate_diff(file_path1, file_path2, output_format='stylish'):
    prev_data = read_data_from_file(file_path1)
    curr_data = read_data_from_file(file_path2)

    data_diff = create_diff(prev_data, curr_data)

    diff_string = ''

    if output_format == 'stylish':
        diff_string = stylish_format(data_diff)

    return diff_string


if __name__ == '__main__':
    main()
