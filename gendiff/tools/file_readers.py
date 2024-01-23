import json
import yaml


def _get_data_from_json_path(json_path):
    with open(json_path) as file:
        data = json.load(file)

    return data


def _get_data_from_yaml_path(yaml_path):
    with open(yaml_path) as file:
        data = yaml.safe_load(file)

    return data


def read_data_from_file(file_path: str):
    if file_path.endswith('json'):
        data = _get_data_from_json_path(file_path)
    elif file_path.endswith('yaml') or file_path.endswith('yml'):
        data = _get_data_from_yaml_path(file_path)
    else:
        raise Exception('file format is not supported!')

    return data
