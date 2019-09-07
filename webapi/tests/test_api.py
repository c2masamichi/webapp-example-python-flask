import pytest

from simplewebapi.db import get_db


def test_index(client):
    response = client.get('/')
    assert b'top' in response.data
