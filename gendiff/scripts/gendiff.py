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


def _get_data_statistic(old_data, new_data):
    statistic = {
        'union_keys': {},
        'changed': {},
        'same': {},
        'removed': {},
        'added': {},
    }

    old_keys = set(old_data.keys())
    new_keys = set(new_data.keys())

    statistic['union_keys'] = new_keys.union(old_keys)

    for key in statistic['union_keys']:
        if key in old_keys and key in new_keys:
            if old_data[key] == new_data[key]:
                statistic['same'][key] = new_data[key]
            else:
                statistic['changed'][key] = {'old': old_data[key], 'new': new_data[key]}
        elif key in old_keys:
            statistic['removed'][key] = old_data[key]
        else:
            statistic['added'][key] = new_data[key]

    return statistic


def _generate_result_string(statistic):
    result_list = ['{']

    for key in sorted(statistic['union_keys']):
        if key in statistic['same']:
            val = str(statistic['same'][key]).lower()
            result_list.append(f'    {key}: {val}')
        elif key in statistic['removed']:
            val = str(statistic['removed'][key]).lower()
            result_list.append(f'  - {key}: {val}')
        elif key in statistic['added']:
            val = str(statistic['added'][key]).lower()
            result_list.append(f'  + {key}: {val}')
        elif key in statistic['changed']:
            old_val = str(statistic['changed'][key]['old']).lower()
            new_val = str(statistic['changed'][key]['new']).lower()
            result_list.append(f'  - {key}: {old_val}')
            result_list.append(f'  + {key}: {new_val}')
        else:
            raise Exception('Smth has gone wrong!')

    result_list.append('}')

    return '\n'.join(result_list)


def generate_diff(file_path1, file_path2):
    old_data = _get_json_by_path(file_path1)
    new_data = _get_json_by_path(file_path2)

    statistic = _get_data_statistic(old_data, new_data)

    return _generate_result_string(statistic)


if __name__ == '__main__':
    main()
