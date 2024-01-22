#!usr/bin/env python3
import argparse
import json


def main():
    parser = argparse.ArgumentParser(
        description='Compares two configuration files and shows a difference.')
    parser.add_argument('--first_file', default='data/file1.json')
    parser.add_argument('--second_file', default='data/file2.json')
    parser.add_argument('-f', '--format', metavar='FORMAT',
                        help='set format of output')

    args = parser.parse_args()

    return generate_diff(args.first_file, args.second_file)


def _get_json_by_path(json_path):
    with open(json_path) as file:
        data = json.load(file)

    return data


def generate_diff(file_path1, file_path2):
    old_data = _get_json_by_path(file_path1)
    new_data = _get_json_by_path(file_path2)

    old_keys = set(old_data.keys())
    new_keys = set(new_data.keys())

    union_keys = new_keys.union(old_keys)
    changed_value_keys, same_value_keys = set(), set()

    for key in union_keys:
        if key in old_keys and key in new_keys:
            if old_data[key] == new_data[key]:
                same_value_keys.add(key)
            else:
                changed_value_keys.add(key)

    removed_value_keys = old_keys.difference(new_keys)
    added_value_keys = new_keys.difference(old_keys)

    sorted_union_keys = sorted(union_keys)
    result_list = ['{']

    for key in sorted_union_keys:
        if key in same_value_keys:
            result_list.append(f'    {key}: {str(old_data[key]).lower()}')
        elif key in removed_value_keys:
            result_list.append(f'  - {key}: {str(old_data[key]).lower()}')
        elif key in added_value_keys:
            result_list.append(f'  + {key}: {str(new_data[key]).lower()}')
        elif key in changed_value_keys:
            result_list.append(f'  - {key}: {str(old_data[key]).lower()}')
            result_list.append(f'  + {key}: {str(new_data[key]).lower()}')
        else:
            raise Exception('Smth has gone wrong!')

    result_list.append('}')

    return '\n'.join(result_list)


if __name__ == '__main__':
    main()
