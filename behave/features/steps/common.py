from urllib.parse import urljoin

import requests
from behave import then, when


@when('a user makes a request to get the "{uri}" endpoint')
def _(context, uri):
    base_url = context.config.userdata.get("app_base_url")
    url = urljoin(base_url, uri)

    context.response = requests.get(url)


@then("the response status code is {status_code:d}")
def _(context, status_code):
    print(context.response.status_code)
    assert context.response.status_code == status_code


@then('the response contains "{s}"')
def _(context, s):
    assert s in context.response.text


@then('the response does not contain "{s}"')
def _(context, s):
    assert s not in context.response.text
