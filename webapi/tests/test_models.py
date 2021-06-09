import pytest

from webapi.models import Product


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
