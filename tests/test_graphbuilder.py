import pytest
from app.GraphBuilder import graphBuilder
from app.flask_web.examples import empty, example1, example2


def test_load():
    g = graphBuilder()
    g.loadServiceTreeFromJSON(empty)

    assert True
