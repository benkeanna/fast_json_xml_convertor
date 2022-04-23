"""Tests for parsers."""

import json

from xml.etree.ElementTree import fromstring

from app.parsers import parse_xml, parse_json
from tests.test_data import XML_STRING, JSON_STRING


def test_parse_xml():
    """Test for parse_xml."""
    my_xml = fromstring(XML_STRING)
    items_dict = {}
    parse_xml(my_xml, items_dict)
    result = json.dumps(items_dict, indent=2)

    assert ''.join(result.split()) == ''.join(JSON_STRING.split())


def test_parse_json():
    """Test for parse_json."""
    json_dict = json.loads(JSON_STRING)
    result = parse_json(json_dict)

    assert ''.join(result.split()) == ''.join(XML_STRING.split())
