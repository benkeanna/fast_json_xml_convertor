import json

from xml.etree.ElementTree import fromstring

from app.parsers import parse_xml, parse_json
from tests.test_data import xml_string, json_string


def test_parse_xml():
    my_xml = fromstring(xml_string)
    items_dict = {}
    parse_xml(my_xml, items_dict)
    result = json.dumps(items_dict, indent=2)

    assert ''.join(result.split()) == ''.join(json_string.split())


def test_parse_json():
    items_list = []
    json_dict = json.loads(json_string)
    result = parse_json(json_dict)

    assert ''.join(result.split()) == ''.join(xml_string.split())
