import pytest
import io

def test_health_check(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'Matplotlib Graph Render API is live!' in response.data

def test_render_no_auth(client):
    response = client.post('/render-matplotlib', json={"code": "print('hello')"})
    assert response.status_code == 401

def test_render_invalid_auth(client):
    response = client.post('/render-matplotlib',
                           headers={'X-API-Key': 'wrong-key'},
                           json={"code": "print('hello')"})
    assert response.status_code == 401

def test_render_missing_code(client):
    response = client.post('/render-matplotlib',
                           headers={'X-API-Key': 'test-secret-key'},
                           json={})
    assert response.status_code == 400
    assert b"Missing or invalid 'code' field" in response.data

def test_render_success(client):
    code = """
import matplotlib.pyplot as plt
plt.plot([1, 2, 3], [1, 2, 3])
"""
    response = client.post('/render-matplotlib',
                           headers={'X-API-Key': 'test-secret-key'},
                           json={"code": code})
    assert response.status_code == 200
    assert response.mimetype == 'image/png'

def test_render_execution_error(client):
    code = "raise ValueError('Simulated error')"
    response = client.post('/render-matplotlib',
                           headers={'X-API-Key': 'test-secret-key'},
                           json={"code": code})
    assert response.status_code == 500
    assert b"Simulated error" in response.data

def test_render_invalid_json(client):
    response = client.post('/render-matplotlib',
                            headers={'X-API-Key': 'test-secret-key'},
                            data="not json")
    assert response.status_code == 400
