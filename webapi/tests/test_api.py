import json

import pytest

from webapi.db import get_db


def test_index(client):
    response = client.get('/')
    assert b'top' in response.data


def test_get_products(client):
    response = client.get('/products')
    data = json.loads(response.data)
    assert 'result' in data
    result = data['result']
    assert len(result) == 2


def test_get_product(client):
    response = client.get('/products/1')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'result' in data
    result = data['result']
    assert result['id'] == 1
    assert result['name'] == 'book'
    assert result['price'] == 600

    response = client.get('/products/3')
    assert response.status_code == 404
