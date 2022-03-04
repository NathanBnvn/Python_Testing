
from urllib import response
from tests.conftest import client


def test_index(client):
    response = client.get('/')
    assert response.status_code == 200

def test_login(client):
    email = "john@simplylift.co"
    response = client.post(
        "/showSummary", 
        data=dict(email=email)
    )
    assert response.status_code == 200

def test_not_authorized(client):
    response = client.post(
        "/showSummary",
        follow_redirects=True
    )
    assert response.status_code == 400

def test_book():
    pass

def test_purchase_place():
    pass

def test_board_points_should_status_code_ok(client):
    response = client.get("/board")
    assert response.status_code == 200

def test_board_points_should_display(client):
    response = client.get("/board")
    data = response.data.decode()
    assert "She Lifts" in data
    assert "12" in data

def test_logout(client):
    response = client.get(
        "/logout",
        follow_redirects=True
    )
    assert response.status_code == 200
