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
