import pytest
from app import app as flask_app


@pytest.fixture
def client():
    flask_app.config.update(TESTING=True)
    with flask_app.test_client() as client:
        yield client


def test_health(client):
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.get_json() == {"status": "ok"}


def test_list_devices(client):
    resp = client.get("/devices")
    assert resp.status_code == 200
    assert len(resp.get_json()) == 2


def test_get_device_found(client):
    resp = client.get("/devices/1")
    assert resp.status_code == 200
    assert resp.get_json()["name"] == "Living Room Dimmer"


def test_get_device_not_found(client):
    resp = client.get("/devices/999")
    assert resp.status_code == 404


def test_set_brightness_valid(client):
    resp = client.patch("/devices/2/brightness", json={"brightness": 55})
    assert resp.status_code == 200
    body = resp.get_json()
    assert body["brightness"] == 55
    assert body["on"] is True


def test_set_brightness_turns_off_at_zero(client):
    resp = client.patch("/devices/1/brightness", json={"brightness": 0})
    assert resp.status_code == 200
    assert resp.get_json()["on"] is False


def test_set_brightness_rejects_out_of_range(client):
    resp = client.patch("/devices/1/brightness", json={"brightness": 150})
    assert resp.status_code == 400


def test_set_brightness_rejects_non_integer(client):
    resp = client.patch("/devices/1/brightness", json={"brightness": "bright"})
    assert resp.status_code == 400