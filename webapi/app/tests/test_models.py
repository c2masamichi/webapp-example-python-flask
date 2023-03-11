import pytest

from webapi.database import db
from webapi.models import Product


@pytest.mark.parametrize(
    ('name', 'price'),
    (
        ('aa', 1000),
        ('a' * 21, 100),
        ('A 01 %', 100),
        ('house', 1000000001),
        ('minus', -1),
    ),
)
def test_create_validate(app, name, price):
    with app.app_context():
        with pytest.raises(AssertionError):
            Product(name=name, price=price)


@pytest.mark.parametrize(
    ('name', 'price'),
    (
        ('aa', 1000),
        ('a' * 21, 100),
        ('A 01 %', 100),
        ('house', 1000000001),
        ('minus', -1),
    ),
)
def test_update_validate(app, name, price):
    product_id = 2
    with app.app_context():
        product = db.session.get(Product, product_id)
        with pytest.raises(AssertionError):
            product.name = name
            product.price = price
