import json

import pytest

from webapi.db import get_db

PATH_PREFIX = '/api/v1'


def test_get_products(client):
    path = '{0}/products'.format(PATH_PREFIX)
    response = client.get(path)
    data = response.get_json()
    assert 'result' in data
    products = data['result']
    assert len(products) == 2


def test_get_product(client):
    product_id = 1
    name = 'book'
    price = 600
    path = '{0}/products/{1}'.format(PATH_PREFIX, product_id)
    response = client.get(path)
    assert response.status_code == 200

    data = response.get_json()
    assert 'result' in data
    product = data['result']
    assert product['id'] == product_id
    assert product['name'] == name
    assert product['price'] == price


def test_get_product_exists_required(client):
    path = '{0}/products/10'.format(PATH_PREFIX)
    response = client.get(path)
    assert response.status_code == 404


def test_create_product(client, app):
    name = 'meat'
    price = 1000
    new_product = json.dumps({
        'name': name,
        'price': price,
    })
    path = '{0}/products'.format(PATH_PREFIX)
    response = client.post(
        path, data=new_product,
        content_type='application/json'
    )
    assert response.status_code == 200

    with app.app_context():
        db = get_db()
        with db.cursor() as cursor:
            cursor.execute('SELECT * FROM product WHERE id = 3')
            product = cursor.fetchone()
        assert product['name'] == name
        assert product['price'] == price


def test_create_product_validate01(client):
    path = '{0}/products'.format(PATH_PREFIX)
    response = client.post(path, data='wrong data')
    assert response.status_code == 400
    data = response.get_json()
    assert 'Content-Type must be application/json.' in data['error']


@pytest.mark.parametrize(
    'data',
    (
        {'name': 'meat'},
        {'price': 1000},
    )
)
def test_create_product_validate02(client, data):
    path = '{0}/products'.format(PATH_PREFIX)
    response = client.post(
        path, data=json.dumps(data),
        content_type='application/json'
    )
    assert response.status_code == 400
    data = response.get_json()
    assert 'The key "name" and "price" are required.' in data['error']


def test_create_product_validate03(client):
    name = 'minus'
    price = -1
    new_product = json.dumps({
        'name': name,
        'price': price,
    })
    path = '{0}/products'.format(PATH_PREFIX)
    response = client.post(
        path, data=new_product,
        content_type='application/json'
    )
    assert response.status_code == 400
    data = response.get_json()
    assert 'Bad data' in data['error']


def test_update_product(client, app):
    product_id = 2
    name = 'rice'
    price = 900
    updated_data = json.dumps({
        'name': name,
        'price': price,
    })
    path = '{0}/products/{1}'.format(PATH_PREFIX, product_id)
    response = client.put(
        path, data=updated_data,
        content_type='application/json'
    )
    assert response.status_code == 200

    with app.app_context():
        db = get_db()
        with db.cursor() as cursor:
            cursor.execute(
                'SELECT * FROM product WHERE id = %s',
                (product_id,)
            )
            product = cursor.fetchone()
        assert product['name'] == name
        assert product['price'] == price


def test_update_product_exists_required(client):
    updated_data = json.dumps({
        'name': 'rice',
        'price': 900,
    })
    path = '{0}/products/10'.format(PATH_PREFIX)
    response = client.put(
        path, data=updated_data,
        content_type='application/json'
    )
    assert response.status_code == 404


def test_update_product_validate01(client):
    product_id = 2
    path = '{0}/products/{1}'.format(PATH_PREFIX, product_id)
    response = client.put(path, data='wrong data')
    assert response.status_code == 400
    data = response.get_json()
    assert 'Content-Type must be application/json.' in data['error']


@pytest.mark.parametrize(
    'data',
    (
        {'name': 'meat'},
        {'price': 1000},
    )
)
def test_update_product_validate02(client, data):
    product_id = 2
    path = '{0}/products/{1}'.format(PATH_PREFIX, product_id)
    response = client.put(
        path, data=json.dumps(data),
        content_type='application/json'
    )
    assert response.status_code == 400
    data = response.get_json()
    assert 'The key "name" and "price" are required.' in data['error']


def test_update_product_validate03(client):
    product_id = 2
    name = 'minus'
    price = -1
    updated_data = json.dumps({
        'name': name,
        'price': price,
    })
    path = '{0}/products/{1}'.format(PATH_PREFIX, product_id)
    response = client.put(
        path, data=updated_data,
        content_type='application/json'
    )
    assert response.status_code == 400
    data = response.get_json()
    assert 'Bad data' in data['error']


def test_delete_product(client, app):
    product_id = 2
    path = '{0}/products/{1}'.format(PATH_PREFIX, product_id)
    response = client.delete(path)
    assert response.status_code == 200

    with app.app_context():
        db = get_db()
        with db.cursor() as cursor:
            cursor.execute(
                'SELECT * FROM product WHERE id = %s',
                (product_id,)
            )
            product = cursor.fetchone()
        assert product is None


def test_delete_product_exists_required(client):
    path = '{0}/products/10'.format(PATH_PREFIX)
    response = client.delete(path)
    assert response.status_code == 404
