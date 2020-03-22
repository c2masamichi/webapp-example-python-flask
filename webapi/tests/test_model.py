from webapi.db import get_db
from webapi.model import Product


def test_fetch_all(app):
    with app.app_context():
        result = Product().fetch_all()
        assert result.code == 200

        products = result.value['result']
        assert len(products) == 2


def test_fetch(app):
    with app.app_context():
        product_id = 1
        result = Product().fetch(product_id)
        assert result.code == 200

        product = result.value['result']
        assert product['id'] == 1
        assert product['name'] == 'book'
        assert product['price'] == 600


def test_fetch_not_exists(app):
    with app.app_context():
        product_id = 10
        result = Product().fetch(product_id)
        assert result.value == {}


def test_create(app):
    with app.app_context():
        name = 'meat'
        price = 1000
        result = Product().create(name, price)
        assert result.code == 200

        db = get_db()
        with db.cursor() as cursor:
            cursor.execute('SELECT * FROM product WHERE id = 3')
            product = cursor.fetchone()
        assert product['name'] == name
        assert product['price'] == price


def test_update(app):
    with app.app_context():
        product_id = 2
        name = 'rice'
        price = 900
        result = Product().update(product_id, name, price)
        assert result.code == 200

        db = get_db()
        with db.cursor() as cursor:
            cursor.execute('SELECT * FROM product WHERE id = 2')
            product = cursor.fetchone()
        assert product['name'] == name
        assert product['price'] == price


def test_delete(app):
    with app.app_context():
        product_id = 1
        result = Product().delete(product_id)
        assert result.code == 200

        db = get_db()
        with db.cursor() as cursor:
            cursor.execute('SELECT * FROM product WHERE id = 1')
            product = cursor.fetchone()
        assert product is None
