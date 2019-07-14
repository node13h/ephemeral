from urllib.parse import urljoin

from behave import when, then
import requests
from bs4 import BeautifulSoup


@when('a user submits a form with specific values and a CSRF token at the "{uri}" endpoint')
def _(context, uri):
    base_url = context.config.userdata.get('app_base_url')
    url = urljoin(base_url, uri)

    session = requests.session()
    response = session.get(url)

    soup = BeautifulSoup(response.text, 'html.parser')

    form = soup.find('form')
    fields = form.findAll('input')

    for field in fields:
        if field['name'] == '_csrf_token':
            csrf_token = field['value']
            break
    else:
        csrf_token = None

    data = {}

    data['_csrf_token'] = csrf_token

    row = dict([x for x in context.table[0].items()])

    data.update(row)

    context.response = session.post(url, data=data)


@when('a user submits a form with specific values at the "{uri}" endpoint')
def _(context, uri):
    base_url = context.config.userdata.get('app_base_url')
    url = urljoin(base_url, uri)

    session = requests.session()

    data = {}

    row = dict([x for x in context.table[0].items()])

    data.update(row)

    context.response = session.post(url, data=data)


@then('the response contains a link')
def _(context):
    soup = BeautifulSoup(context.response.text, 'html.parser')

    link = soup.find('a')

    assert link is not None


@then('the response does not contain a link')
def _(context):
    soup = BeautifulSoup(context.response.text, 'html.parser')

    link = soup.find('a')

    assert link is None
