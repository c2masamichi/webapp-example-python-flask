from webapi import create_app


def test_healthcheck(client):
    response = client.get('/healthcheck')
    assert response.data == b'app running'
