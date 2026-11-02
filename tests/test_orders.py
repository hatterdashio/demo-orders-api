import pytest

from api.app import create_app


@pytest.fixture
def client():
    return create_app().test_client()


def test_create_and_show_order(client):
    created = client.post("/orders", json={"customer": "Ada"})
    assert created.status_code == 201
    order = client.get(f"/orders/{created.get_json()['id']}").get_json()
    assert order == {"id": 1, "customer": "Ada", "status": "new"}


def test_unknown_order_is_404(client):
    assert client.get("/orders/99").status_code == 404


def test_search_finds_orders_by_customer(client):
    client.post("/orders", json={"customer": "Ada Lovelace"})
    client.post("/orders", json={"customer": "Grace Hopper"})
    found = client.get("/orders/search?customer=Ada").get_json()
    assert [order["customer"] for order in found] == ["Ada Lovelace"]
