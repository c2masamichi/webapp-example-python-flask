import pytest

from webapi.models import Product


@pytest.mark.parametrize(
    ('name', 'price'),
    (
        ('aa', 1000),
        ('a' * 21, 1000),
        ('house', 1000000001),
        ('minus', -1),
        ('A 01 %', 100),
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
        ('a' * 21, 1000),
        ('house', 1000000001),
        ('minus', -1),
        ('A 01 %', 100),
    ),
)
def test_update_validate(app, name, price):
    with app.app_context():
        with pytest.raises(AssertionError):
            product_id = 2
            product = Product.query.get(product_id)
            product.name = name
            product.price = price