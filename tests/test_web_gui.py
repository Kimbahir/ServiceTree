import pytest
from app.flask_web import app
from flask import session
from app.flask_web.examples import example1
import json


@pytest.yield_fixture
def client():
    with app.test_client() as client:
        yield client


@pytest.yield_fixture
def loaded_client():
    with app.test_client() as client:
        with client.session_transaction() as session:
            session['datastructure'] = json.dumps(example1)
        yield client


def test_initial_load(client):
    rv = client.get("/")
    assert rv.status_code == 200

    rv = client.get("/load")
    assert rv.status_code == 200


def test_initial_redirects(client):
    urls = [
        '/patch',
        '/relate',
        '/detach',
        '/download'
    ]

    for url in urls:
        rv = client.get(url)
        assert rv.status_code == 302


def test_error_in_load(client):
    rv = client.get('/asdæaælsdkæakdsækasd')
    assert rv.status_code == 404


def test_no_redirect_loaded(loaded_client):

    urls = [
        '/',
        '/load',
        '/patch',
        '/relate',
        '/detach',
        '/download'
    ]

    for url in urls:
        rv = loaded_client.get(url)
        assert rv.status_code == 200
