import pytest
from fastapi.testclient import TestClient
from request_via_request_server.server import app

client = TestClient(app)


def test_ping():
    response = client.get('/ping')
    assert response.status_code == 200
    assert 'pong' in str(response.content)


def test_get_without_proxy_server_settings():
    response = client.post('/curl/get', json={"url": "http://info.cern.ch", "answer_type": "status_code"})
    assert response.status_code == 200
    assert '200' in str(response.content)


def test_get_with_proxy_server_settings_none():
    response = client.post('/curl/get', json={"url": "http://info.cern.ch", "answer_type": "status_code", "proxy_server": None})
    assert response.status_code == 200
    assert '200' in str(response.content)


def test_get_answer_type_content():
    response = client.post('/curl/get', json={"url": "http://info.cern.ch", "answer_type": "content"})
    assert response.status_code == 200
    assert 'CERN' in str(response.content)


def test_get_answer_type_json_null():
    response = client.post('/curl/get', json={"url": "http://info.cern.ch", "answer_type": "json"})
    assert response.status_code == 200
    assert 'null' in str(response.content)


def test_get_answer_type_json():
    response = client.post('/curl/get', json={"url": "https://httpbin.org/json", "answer_type": "json"})
    assert response.json() is not None
    assert response.status_code == 200


def test_get_headers():
    response = client.post('/curl/get', json={"url": "https://httpbin.org/response-headers", "answer_type": "headers"})
    assert response.content is not None
    assert 'application/json' in str(response.content)
    assert response.status_code == 200


def test_post_without_data():
    response = client.post('/curl/post', json={"url": "http:/info.cern.ch", "answer_type": "status_code"})
    assert response.status_code == 422


def test_post_with_wrong_type_data():
    response = client.post('/curl/post', json={"data": "{'qwe':'qwe'}", "url": "http:/info.cern.ch", "answer_type": "status_code"})
    assert response.status_code == 422


def test_post_with_data():
    response = client.post('/curl/post', json={"data": {'key': 'value'}, "url": "https://httpbin.org/post ", "answer_type": "status_code"})
    assert response.status_code == 200


def test_post_with_data_and_empty_proxy():
    response = client.post(
        '/curl/post', json={"data": {'key': 'value'}, "url": "https://httpbin.org/post ", "answer_type": "status_code", "proxy_server": None}
    )
    assert response.status_code == 200


def test_post_with_data_content():
    response = client.post('/curl/post', json={"data": {'key': 'value'}, "url": "https://httpbin.org/post ", "answer_type": "content"})
    assert response.status_code == 200
    assert 'W3C' in str(response.content)


def test_post_with_data_json():
    response = client.post('/curl/post', json={"data": {'key': 'value'}, "url": "https://httpbin.org/post ", "answer_type": "json"})
    assert response.status_code == 200


def test_post_with_data_headers():
    response = client.post('/curl/post', json={"data": {'key': 'value'}, "url": "https://httpbin.org/post ", "answer_type": "headers"})
    assert response.status_code == 200
    assert 'text/html' in str(response.content)


def test_get_with_proxy_without_proxy():
    with pytest.raises(ValueError):
        client.post('/curl/get?proxy=true', json={"url": "http://info.cern.ch ", "answer_type": "status_code"})


def test_post_with_proxy_without_proxy():
    with pytest.raises(ValueError):
        client.post('/curl/post?proxy=true', json={"data": {"key": "value"}, "url": "http://info.cern.ch ", "answer_type": "status_code"})


def test_get_with_proxy_without_proxy2():
    with pytest.raises(ValueError):
        client.post('/curl/get?proxy=true', json={"url": "http://info.cern.ch ", "answer_type": "status_code", "proxy_server": None})


def test_post_with_proxy_without_proxy2():
    with pytest.raises(ValueError):
        client.post('/curl/post?proxy=true', json={"data": {"key": "value"}, "url": "http://info.cern.ch ", "answer_type": "status_code", "proxy_server": None})