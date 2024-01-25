def _format_value_for_output(value):
    result = value

    if isinstance(value, bool):
        result = str(value).lower()
    elif value is None:
        result = 'null'

    return str(result)


def _stringify_dict(data, base_prefix='', space_pattern='    '):

    def helper(data_elem, level=1):
        result_list = ['{']
        level_prefix = space_pattern * level

        for key in data_elem.keys():
            if not isinstance(data_elem[key], dict):
                value_string = _format_value_for_output(data_elem[key])
            else:
                value_string = helper(data_elem[key], level + 1)

            result = f'{base_prefix}{level_prefix}{space_pattern}{key}:' \
                     f' {value_string}'
            result_list.append(result)

        result_list.append(f'{base_prefix}{level_prefix}' + '}')

        return '\n'.join(result_list)

    return helper(data)


def _gen_atomic_string(
        level_prefix,
        key,
        status,
        prev_value_str=None,
        curr_value_str=None
):
    result_list = []

    if status == 'same':
        result_list.append(f'{level_prefix}    {key}: {curr_value_str}')
    elif status == 'removed':
        result_list.append(f'{level_prefix}  - {key}: {prev_value_str}')
    elif status == 'added':
        result_list.append(f'{level_prefix}  + {key}: {curr_value_str}')
    elif status == 'changed':
        result_list.append(f'{level_prefix}  - {key}: {prev_value_str}')
        result_list.append(f'{level_prefix}  + {key}: {curr_value_str}')
    else:
        raise Exception('Smth has gone wrong!')

    return result_list


def stylish_format(diff, space_pattern='    '):

    def helper(diff_elem, level=0):
        level_prefix = space_pattern * level
        result_list = ['{']

        for key in sorted(diff_elem.keys()):
            key_status = diff_elem[key]['status']
            key_prev_value = diff_elem[key].get('prev_value')
            key_curr_value = diff_elem[key].get('curr_value')

            if isinstance(key_prev_value, dict):
                key_prev_value_str = _stringify_dict(
                    key_prev_value, level_prefix
                )
            else:
                key_prev_value_str = _format_value_for_output(key_prev_value)

            if 'children' in diff_elem[key]:
                key_status = 'same'
                key_curr_value_str = helper(
                    diff_elem[key]['children'],
                    level + 1
                )
            elif isinstance(key_curr_value, dict):
                key_curr_value_str = _stringify_dict(
                    key_curr_value,
                    level_prefix
                )
            else:
                key_curr_value_str = _format_value_for_output(key_curr_value)

            atomic_result = _gen_atomic_string(
                level_prefix,
                key,
                key_status,
                key_prev_value_str,
                key_curr_value_str
            )
            result_list.extend(atomic_result)

        result_list.append(level_prefix + '}')

        return '\n'.join(result_list)

    return helper(diff)


__all__ = 'stylish_format',
