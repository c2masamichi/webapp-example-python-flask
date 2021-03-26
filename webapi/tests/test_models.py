import pytest

from webapi.db import get_db
from webapi.model import Product


def test_fetch_all(app):
    with app.app_context():
        result = Product().fetch_all()
        assert result.code == 200

        products = result.value
        assert len(products) == 2


def test_fetch(app):
    with app.app_context():
        product_id = 1
        name = 'book'
        price = 600
        result = Product().fetch(product_id)
        assert result.code == 200

        product = result.value
        assert product['id'] == product_id
        assert product['name'] == name
        assert product['price'] == price


def test_fetch_not_exists(app):
    with app.app_context():
        product_id = 10
        result = Product().fetch(product_id)
        assert result.value == {}


def test_create(app):
    with app.app_context():
        name = 'Mineral water 500ml'
        price = 100
        result = Product().create(name, price)
        assert result.code == 200

        db = get_db()
        with db.cursor() as cursor:
            cursor.execute(
                'SELECT * FROM product WHERE name = %s',
                (name,)
            )
            product = cursor.fetchone()
        assert product['price'] == price


@pytest.mark.parametrize(
    ('name', 'price', 'message'),
    (
        ('aa', 1000, 'Bad data'),
        ('a' * 21, 1000, 'Bad data'),
        ('house', 1000000001, 'Bad data'),
        ('minus', -1, 'Bad data'),
        ('A 01 %', 100, 'Bad data'),
    ),
)
def test_create_validate(app, name, price, message):
    with app.app_context():
        result = Product().create(name, price)
        assert result.code == 400
        assert message in result.description


def test_update(app):
    with app.app_context():
        product_id = 2
        name = 'rice'
        price = 900
        result = Product().update(product_id, name, price)
        assert result.code == 200

        db = get_db()
        with db.cursor() as cursor:
            cursor.execute(
                'SELECT * FROM product WHERE id = %s',
                (product_id,)
            )
            product = cursor.fetchone()
        assert product['name'] == name
        assert product['price'] == price


@pytest.mark.parametrize(
    ('name', 'price', 'message'),
    (
        ('aa', 1000, 'Bad data'),
        ('a' * 21, 1000, 'Bad data'),
        ('house', 1000000001, 'Bad data'),
        ('minus', -1, 'Bad data'),
        ('A 01 %', 100, 'Bad data'),
    ),
)
def test_update_validate(app, name, price, message):
    with app.app_context():
        product_id = 2
        result = Product().update(product_id, name, price)
        assert result.code == 400
        assert message in result.description


def test_delete(app):
    with app.app_context():
        product_id = 2
        result = Product().delete(product_id)
        assert result.code == 200

        db = get_db()
        with db.cursor() as cursor:
            cursor.execute(
                'SELECT * FROM product WHERE id = %s',
                (product_id,)
            )
            product = cursor.fetchone()
        assert product is None
