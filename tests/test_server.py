
from urllib import response
from tests.conftest import client

def test_board_points_should_status_code_ok(client):
    response = client.get('/board')
    assert response.status_code == 200

def test_board_points_should_display(client):
    response = client.get('/board')
    data = response.data.decode()
    assert "She Lifts" in data
    assert "12" in data