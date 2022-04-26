"""App module."""
# pylint: disable=no-name-in-module

import json
from xml.etree.ElementTree import fromstring

from pathlib import Path
from pydantic import BaseModel
from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.templating import Jinja2Templates

from app import queries
from app.errors import QueryError
from app.parsers import parse_xml, parse_json


BASE_DIR = Path(__file__).resolve().parent

templates = Jinja2Templates(directory=str(Path(BASE_DIR, 'templates')))


class UserText(BaseModel):
    """User text model."""
    # pylint: disable=too-few-public-methods
    # FastAPI docs says class is fine
    text: str


app = FastAPI()


@app.get("/")
def home(request: Request):
    """Home page."""
    return templates.TemplateResponse("forms.html", {
        "request": request, 'converted_to_json': '', 'converted_to_xml': ''})


@app.post("/xml2json")
def xml2json(request: Request, xml_string: str = Form(...)):
    """Returns XML converted to JSON."""
    my_xml = fromstring(xml_string)
    items_dict = {}
    parse_xml(my_xml, items_dict)

    converted_to_json = json.dumps(items_dict, indent=2)
    return templates.TemplateResponse("forms.html", {
        "request": request, 'converted_to_json': converted_to_json, 'converted_to_xml': ''})


@app.post("/json2xml/")
def json2xml(request: Request, json_string: str = Form(...)):
    """Returns JSON converted to XML."""
    json_dict = json.loads(json_string)

    converted_to_xml = parse_json(json_dict)
    return templates.TemplateResponse("forms.html", {
        "request": request, 'converted_to_json': '', 'converted_to_xml': converted_to_xml})


@app.get("/user")
def get_user(email: str):
    """Returns user with given email."""
    try:
        return queries.get_user(email)
    except QueryError as error:
        raise HTTPException(status_code=404, detail="User not found") from error


@app.post("/user")
def create_user(email: str, user: UserText):
    """Returns created user."""
    try:
        usr = queries.create_user(email, user.text)
    except QueryError as error:
        raise HTTPException(status_code=400, detail="Duplicate entry") from error
    return usr


@app.delete("/user")
def delete_user(email: str):
    """Deletes user."""
    try:
        email = queries.delete_user(email)
        return email
    except QueryError as error:
        raise HTTPException(status_code=404, detail="User not found") from error


@app.get("/users")
def get_all_users(limit: int = 10, offset: int = 0):
    """Returns all existing users."""

    return queries.get_all_users(limit, offset)
