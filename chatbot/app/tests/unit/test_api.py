import pytest
from fastapi.testclient import TestClient
from api.main import app

@pytest.fixture
def client():
    return TestClient(app)

def test_health_check(client):
    resp = client.get('/health')
    assert resp.status_code == 200
    assert resp.json()['status'] == 'ok'

def test_root_redirect(client):
    resp = client.get('/')
    assert resp.status_code in (200, 307, 302)

def test_new_session(client, monkeypatch):
    monkeypatch.setattr('api.main.redis_client', type('FakeRedis', (), {'sadd': lambda self, k, v: True})())
    resp = client.post('/v1/sessions/new')
    assert resp.status_code == 200
    assert 'thread_id' in resp.json()
