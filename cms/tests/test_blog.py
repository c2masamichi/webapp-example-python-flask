import pytest


def test_index(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'Test Title 1' in response.data
    assert b'2019-01-01' in response.data
    assert b'This body is test.' in response.data


def test_get_entry(client):
    response = client.get('/entry/1')
    assert response.status_code == 200
    assert b'Test Title 1' in response.data
    assert b'2019-01-01' in response.data
    assert b'This body is test.' in response.data


def test_get_entry_error(client):
    response = client.get('/entry/5')
    assert response.status_code == 404
