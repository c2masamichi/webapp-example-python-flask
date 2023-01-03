import json

import pytest

from webapi.models import Product

PATH_PREFIX = '/api/v1'


def test_get_products(client):
    path = '{0}/products'.format(PATH_PREFIX)
    response = client.get(path)
    assert response.status_code == 200

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
    product_id = 10  # not exist
    path = '{0}/products/{1}'.format(PATH_PREFIX, product_id)
    response = client.get(path)
    assert response.status_code == 404


def test_create_product(client, app):
    product_id = 3
    name = 'meet'
    price = 1000
    post_data = {
        'name': name,
        'price': price,
    }
    path = '{0}/products'.format(PATH_PREFIX)
    response = client.post(
        path, data=json.dumps(post_data),
        content_type='application/json'
    )
    assert response.status_code == 200

    data = response.get_json()
    assert 'result' in data
    result = data['result']
    assert result['id'] == product_id
    assert result['name'] == name
    assert result['price'] == price

    with app.app_context():
        product = Product.query.get(3)
        assert product.name == name
        assert product.price == price


def test_create_product_validate_content_type(client):
    post_data = {
        'name': 'meet',
        'price': 1000,
    }
    path = '{0}/products'.format(PATH_PREFIX)
    response = client.post(
        path, data=json.dumps(post_data),
    )
    assert response.status_code == 400
    data = response.get_json()
    assert 'Content-Type must be application/json.' in data['error']


@pytest.mark.parametrize(
    'post_data',
    (
        {'name': 'meat'},
        {'price': 1000},
    )
)
def test_create_product_validate_required_key(client, post_data):
    path = '{0}/products'.format(PATH_PREFIX)
    response = client.post(
        path, data=json.dumps(post_data),
        content_type='application/json'
    )
    assert response.status_code == 400
    data = response.get_json()
    assert 'The key "name" and "price" are required.' in data['error']


@pytest.mark.parametrize(
    'post_data',
    (
        {
            'name': 'aa',
            'price': 1000,
        },
        {
            'name': 'minus',
            'price': -1,
        },
    )
)
def test_create_product_validate_assertion_error(client, post_data):
    path = '{0}/products'.format(PATH_PREFIX)
    response = client.post(
        path, data=json.dumps(post_data),
        content_type='application/json'
    )
    assert response.status_code == 400
    data = response.get_json()
    assert 'Bad data' in data['error']


def test_update_product(client, app):
    product_id = 2
    name = 'rice'
    price = 900
    post_data = {
        'name': name,
        'price': price,
    }
    path = '{0}/products/{1}'.format(PATH_PREFIX, product_id)
    response = client.put(
        path, data=json.dumps(post_data),
        content_type='application/json'
    )
    assert response.status_code == 200

    data = response.get_json()
    assert 'result' in data
    result = data['result']
    assert result['id'] == product_id
    assert result['name'] == name
    assert result['price'] == price

    with app.app_context():
        product = Product.query.get(product_id)
        assert product.name == name
        assert product.price == price


def test_update_product_exists_required(client):
    product_id = 10  # not exist
    post_data = {
        'name': 'rice',
        'price': 900,
    }
    path = '{0}/products/{1}'.format(PATH_PREFIX, product_id)
    response = client.put(
        path, data=json.dumps(post_data),
        content_type='application/json'
    )
    assert response.status_code == 404


def test_update_product_validate_content_type(client):
    product_id = 2
    post_data = {
        'name': 'rice',
        'price': 900,
    }
    path = '{0}/products/{1}'.format(PATH_PREFIX, product_id)
    response = client.put(
        path, data=json.dumps(post_data),
    )
    assert response.status_code == 400
    data = response.get_json()
    assert 'Content-Type must be application/json.' in data['error']


@pytest.mark.parametrize(
    'post_data',
    (
        {'name': 'meat'},
        {'price': 1000},
    )
)
def test_update_product_validate_required_key(client, post_data):
    product_id = 2
    path = '{0}/products/{1}'.format(PATH_PREFIX, product_id)
    response = client.put(
        path, data=json.dumps(post_data),
        content_type='application/json'
    )
    assert response.status_code == 400
    data = response.get_json()
    assert 'The key "name" and "price" are required.' in data['error']


@pytest.mark.parametrize(
    'post_data',
    (
        {
            'name': 'aa',
            'price': 1000,
        },
        {
            'name': 'minus',
            'price': -1,
        },
    )
)
def test_update_product_validate_assertion_error(client, post_data):
    product_id = 2
    path = '{0}/products/{1}'.format(PATH_PREFIX, product_id)
    response = client.put(
        path, data=json.dumps(post_data),
        content_type='application/json'
    )
    assert response.status_code == 400
    data = response.get_json()
    assert 'Bad data' in data['error']


def test_delete_product(client, app):
    product_id = 2
    name = 'fish'
    price = 200
    path = '{0}/products/{1}'.format(PATH_PREFIX, product_id)
    response = client.delete(path)
    assert response.status_code == 200

    data = response.get_json()
    assert 'result' in data
    result = data['result']
    assert result['id'] == product_id
    assert result['name'] == name
    assert result['price'] == price

    with app.app_context():
        product = Product.query.get(product_id)
        assert product is None


def test_delete_product_exists_required(client):
    product_id = 10  # not exist
    path = '{0}/products/{1}'.format(PATH_PREFIX, product_id)
    response = client.delete(path)
    assert response.status_code == 404
