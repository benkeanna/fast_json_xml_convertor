import json


def _set_dict_item_value(items_dict, item_name, item_value, item_type):
    item_types = {
        'string': str,
        'integer': int,
        'float': float,
        'boolean': bool,
        'list': list,
        'object': dict
    }
    item_type = item_types.get(item_type, None)

    if item_name:
        items_dict[item_name] = item_type(item_value) if item_type else None
    else:
        item_value = item_type(item_value) if item_type else item_value
        items_dict.append(item_value)
    return items_dict


def parse_xml(items_xml, items_dict):
    for item in items_xml:
        item_type = item.get('type')
        item_name = item.get('key')

        if item_type == 'object':
            help_dict = {}
            parse_xml(item, help_dict)
            items_dict = _set_dict_item_value(items_dict, item_name, help_dict, item_type)
        elif item_type == 'list':
            help_list = []
            parse_xml(item, help_list)
            items_dict = _set_dict_item_value(items_dict, item_name, help_list, item_type)
        else:
            item_value = item.get('value')
            items_dict = _set_dict_item_value(items_dict, item_name, item_value, item_type)


def _set_item_list_value(item):
    item_types = {
        str: 'string',
        int: 'integer',
        float: 'float',
        bool: 'boolean',
        list: 'list',
        dict: 'object',
        tuple: 'object'
    }
    try:
        item_type_element = item[1]
    except TypeError:
        item_type_element = item

    item_type = item_types.get(type(item_type_element), None)
    if type(item) == tuple:
        if item[1]:
            tag = '<ITEM key="{}" type="{}" value="{}"/>'.format(item[0], item_type, item[1])
        else:
            tag = '<ITEM key="{}" type="null"/> '.format(item[0])
    else:
        tag = '<ITEM type="{}" value="{}"/> '.format(item_type, str(item).lower())
    return tag


def parse_json_items(json_dict, items_list):
    for item in json_dict.items():
        if type(item[1]) is dict:
            help_list = ['<ITEM key="{}" type="object">'.format(item[0])]  # opening tag
            parse_json_items(item[1], help_list)
            help_list.append('</ITEM>')  # closing tag
            items_list.extend(help_list)

        elif type(item[1]) is list:
            help_list = ['<ITEM key="{}" type="list">'.format(item[0])]  # opening tag
            for inner_item in item[1]:
                if type(inner_item) == dict:
                    # problem that we don't know how many elements will be inside
                    inner_help_list = ['<ITEM type="object">']  # opening tag
                    parse_json_items(inner_item, inner_help_list)
                    inner_help_list.append('</ITEM>')  # closing tag
                    help_list.extend(inner_help_list)
                else:
                    help_list.append(_set_item_list_value(inner_item))
            help_list.append('</ITEM>')  # closing tag
            items_list.extend(help_list)

        else:
            items_list.append(_set_item_list_value(item))


def parse_json(json_dict):
    items_list = ['<ITEM type="object">']
    parse_json_items(json_dict, items_list)
    items_list.append('</ITEM>')

    return '\n'.join(items_list)
