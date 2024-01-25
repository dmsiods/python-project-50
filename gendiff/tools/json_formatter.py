import json


def json_format(diff):
    return json.dumps(diff, sort_keys=True, indent=4)
