
from datetime import datetime
from urllib import response
from tests.conftest import client, clubs_test, competitions_test

class TestServer:

    def test_index(self, client):
        response = client.get('/')
        assert response.status_code == 200

    def test_board_points_should_display(self, client, clubs_test):
        response = client.get("/")
        data = response.data.decode()
        assert "Johnny Test Club" in data
        assert "10" in data
    
    def test_login(self, client, clubs_test):
        response = client.post(
            "/showSummary", 
            data=dict(email="jtest@club.com")
            )
        assert response.status_code == 200


    def test_login_unauthorized_email(self, client, clubs_test):
        invalid_email = "joker@laugh.io"
        response = client.post(
            "/showSummary", 
            data=dict(email=invalid_email),
        )
        assert response.status_code == 302


    def test_not_authorized(self, client):
        response = client.post(
            "/showSummary",
            follow_redirects=True
        )
        assert response.status_code == 400

    def test_redirect_to_unauthorized(self, client):
        response = client.get(
            "/unauthorized"
        )
        data = response.data.decode()
        assert "Your secretary email is not valid" in data


    def test_book(self, client, clubs_test, competitions_test):
        response = client.get(
            "/book/<competition>/<club>",
        )
        assert response.status_code == 200


    def test_purchase_place_futur_event(self, client, clubs_test, competitions_test):
        competition = competitions_test[1]
        club = clubs_test[0]
        response = client.post(
            "/purchasePlaces", 
                data=dict(club=club['name'], competition=competition['name'], places="1")
            )
            
        data = response.data.decode()
        assert response.status_code == 200
        assert "Great-booking complete!" in data


    def test_cannot_purchase_place_past_event(self, client, clubs_test, competitions_test):
        competition = competitions_test[0]
        club = clubs_test[0]
        response = client.post(
            "/purchasePlaces", 
                data=dict(club=club['name'], competition=competition['name'], places="6")
            )
        data = response.data.decode()
        assert response.status_code == 200
        assert "This competition is over!" in data


    def test_club_points_balance(self, client, clubs_test, competitions_test):
        club = clubs_test[1]
        competition = competitions_test[1]
        response = client.post(
            "/purchasePlaces", 
                data=dict(club=club['name'], competition=competition['name'], places="2")
            )
        expected_points = 28

        assert response.status_code == 200
        assert club['points'] == expected_points


    def test_club_points_wrong_balance(self, client, clubs_test, competitions_test):
        club = clubs_test[0]
        competition = competitions_test[1]
        response = client.post(
            "/purchasePlaces", 
                data=dict(club=club['name'], competition=competition['name'], places="5")
            )
        data = response.data.decode()
        assert "You dont have enough points" in data


    def test_logout(self, client):
        response = client.get(
            "/logout",
            follow_redirects=True
        )
        assert response.status_code == 200
