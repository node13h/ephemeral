from urllib.parse import urljoin

import requests
from behave import given, then, when
from bs4 import BeautifulSoup


@given('a user has submitted a message "{body}" with pin "{pin}"')
def _(context, body, pin):
    base_url = context.config.userdata.get("app_base_url")
    url = urljoin(base_url, "/add")

    session = requests.session()
    response = session.get(url)

    soup = BeautifulSoup(response.text, "html.parser")

    form = soup.find("form")
    fields = form.findAll("input")

    for field in fields:
        if field["name"] == "_csrf_token":
            csrf_token = field["value"]
            break
    else:
        csrf_token = None

    data = {}

    data["_csrf_token"] = csrf_token

    data["body"] = body
    data["pin"] = pin

    context.response = session.post(url, data=data)

    soup = BeautifulSoup(context.response.text, "html.parser")

    a = soup.find("a")

    context.returned_url = a["href"]


@then("the response contains a form")
def _(context):
    soup = BeautifulSoup(context.response.text, "html.parser")

    form = soup.find("form")

    assert form is not None


@when("a user opens a URL returned by the message submit step")
def _(context):
    context.response = requests.get(context.returned_url)


@when("a user submits a form with specific values and a CSRF token at the returned URL")
def _(context):
    url = context.returned_url

    session = requests.session()
    response = session.get(url)

    soup = BeautifulSoup(response.text, "html.parser")

    form = soup.find("form")
    fields = form.findAll("input")

    for field in fields:
        if field["name"] == "_csrf_token":
            csrf_token = field["value"]
            break
    else:
        csrf_token = None

    data = {}

    data["_csrf_token"] = csrf_token

    row = dict([x for x in context.table[0].items()])

    data.update(row)

    context.response = session.post(url, data=data)


@when("a user submits a form with specific values at the returned URL")
def _(context):
    url = context.returned_url

    session = requests.session()

    data = {}

    row = dict([x for x in context.table[0].items()])

    data.update(row)

    context.response = session.post(url, data=data)
