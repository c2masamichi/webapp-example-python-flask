import json

import pytest

from simplewebapi.db import get_db


def test_index(client):
    response = client.get('/')
    assert b'top' in response.data


def test_get_products(client):
    response = client.get('/products')
    data = json.loads(response.data)
    assert 'result' in data
    result = data['result']
    assert len(result) == 2
