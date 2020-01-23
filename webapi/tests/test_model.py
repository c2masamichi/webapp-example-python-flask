from webapi.db import get_db
from webapi.model import Product


def test_fetch_all(app):
    with app.app_context():
        response = Product().fetch_all()
        assert 'result' in response
        result = response['result']
        assert len(result) == 2


def test_fetch(app):
    with app.app_context():
        product_id = 1
        response = Product().fetch(product_id)
        assert 'result' in response
        result = response['result']
        assert result['id'] == 1
        assert result['name'] == 'book'
        assert result['price'] == 600


def test_fetch_not_exists(app):
    with app.app_context():
        product_id = 3
        response = Product().fetch(product_id)
        assert response is None


def test_create(app):
    with app.app_context():
        name = 'meat'
        price = 1000
        result = Product().create(name, price)
        assert result.code == 200

        db = get_db()
        with db.cursor() as cursor:
            cursor.execute('SELECT * FROM product WHERE id = 3')
            row = cursor.fetchone()
        assert row['name'] == name
        assert row['price'] == price


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
            row = cursor.fetchone()
        assert row['name'] == name
        assert row['price'] == price


def test_delete(app):
    with app.app_context():
        product_id = 1
        result = Product().delete(product_id)
        assert result.code == 200

        db = get_db()
        with db.cursor() as cursor:
            cursor.execute('SELECT * FROM product WHERE id = 1')
            row = cursor.fetchone()
        assert row is None
