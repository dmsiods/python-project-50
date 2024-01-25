def _format_value_for_plain_output(value):
    result = value

    if isinstance(value, bool):
        result = str(value).lower()
    elif value is None:
        result = 'null'
    elif isinstance(value, dict):
        result = '[complex value]'
    elif isinstance(value, str):
        result = f"'{value}'"

    return str(result)


def _make_plain_string(path, status, prev_value=None, curr_value=None):
    if status == 'removed':
        plain_string = f"Property {path} was removed"
    elif status == 'added':
        plain_string = f"Property {path} was added with value: {curr_value}"
    elif status == 'changed':
        plain_string = f"Property {path} was updated. From {prev_value}" \
                       f" to {curr_value}"
    else:
        raise Exception('Smth has gone wrong!')

    return plain_string


def plain_format(diff):
    key_result_list = []

    def dfs(diff_elem, path):
        for key in sorted(diff_elem.keys()):
            path.append(key)

            if 'children' in diff_elem[key]:
                dfs(diff_elem[key]['children'], path)
            else:
                key_status = diff_elem[key]['status']

                if key_status != 'same':
                    key_prev_value = diff_elem[key].get('prev_value')
                    key_prev_value = _format_value_for_plain_output(
                        key_prev_value
                    )
                    key_curr_value = diff_elem[key].get('curr_value')
                    key_curr_value = _format_value_for_plain_output(
                        key_curr_value
                    )

                    key_path = '.'.join(path)
                    key_path = f"'{key_path}'"

                    key_result = _make_plain_string(
                        key_path,
                        key_status,
                        key_prev_value,
                        key_curr_value
                    )
                    key_result_list.append(key_result)

            path.pop()

    dfs(diff, [])

    return '\n'.join(key_result_list)


__all__ = 'plain_format',
