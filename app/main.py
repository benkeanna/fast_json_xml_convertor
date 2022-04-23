"""App module."""

import json
from fastapi import FastAPI
from xml.etree.ElementTree import fromstring

from app.parsers import parse_xml, parse_json

app = FastAPI()


@app.get("/")
def home():
    """Home page."""
    return {"Hello": "World"}


@app.post("/xml2json/")
def xml2json(xml_string: str):
    """Returns XML converted to JSON."""
    my_xml = fromstring(xml_string)
    items_dict = {}
    parse_xml(my_xml, items_dict)

    return json.dumps(items_dict, indent=2)


@app.post("/json2xml/")
def json2xml(json_string: str):
    """Returns JSON converted to XML."""
    items_list = []
    json_dict = json.loads(json_string)

    return parse_json(json_dict)
