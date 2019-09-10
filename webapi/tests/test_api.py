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


def test_get_product_error(client):
    response = client.get('/products/3')
    assert response.status_code == 404


def test_post_product(client, app):
    new_product = json.dumps({
        'name': 'meat',
        'price': 1000,
    })
    response = client.post(
        '/products', data=new_product,
        content_type='application/json'
    )
    assert response.status_code == 201
    data = json.loads(response.data)
    assert data.get('result') == 'Successfully Created.'

    with app.app_context():
        db = get_db()
        count = db.execute('SELECT COUNT(id) FROM product').fetchone()[0]
        assert count == 3


def test_post_product_error(client):
    response = client.post('/products', data='wrong data')
    assert response.status_code == 400


def test_delete_product(client, app):
    response = client.delete('/products/1')
    assert response.status_code == 200


def test_delete_product(client, app):
    response = client.delete('/products/3')
    assert response.status_code == 404
