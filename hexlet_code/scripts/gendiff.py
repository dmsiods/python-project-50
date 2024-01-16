#!usr/bin/env python3
import argparse
import json


def main():
    parser = argparse.ArgumentParser(
        description='Compares two configuration files and shows a difference.')
    parser.add_argument('first_file')
    parser.add_argument('second_file')
    parser.add_argument('-f', '--format', metavar='FORMAT',
                        help='set format of output')

    args = parser.parse_args()

    generate_diff(args.first_file, args.second_file)


def generate_diff(file_path1, file_path2):
    with open(file_path1) as file:
        old_data = json.load(file)

    with open(file_path2) as file:
        new_data = json.load(file)


if __name__ == '__main__':
    main()
