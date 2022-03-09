
from urllib import response
from datetime import datetime
from tests.conftest import client
from server import clubs, competitions


class TestServer:
    def setup_method(self, client):
        #clubs.clear()
        #competitions.clear()

        self.name = "Johnny Test Club"
        self.email = "jtest@club.com"
        self.point = "10"
        self.clubs = [{
            "name": self.name,
            "email": self.email,
            "password": self.point
        }]

        self.competitionName = "Spring Contest"
        self.date = "2022-03-22 10:00:00"
        self.numberOfPlaces = "14"

        self.secondCompetitionName = "Swinging Lifting"
        self.secondDate = "2022-07-12 19:00:00"
        self.secondNumberOfPlaces = "7"

        self.competitions = [{
            "name": self.competitionName,
            "date": self.date,
            "numberOfPlaces": self.numberOfPlaces,
        },]


    def test_index(self, client):
        response = client.get('/')
        assert response.status_code == 200

    def test_login(self, client):
        email = "john@simplylift.co"
        response = client.post(
            "/showSummary", 
            data=dict(email=email)
        )
        assert response.status_code == 200

    def test_login_unauthorized_email(self, client):
        response = client.post(
            "/showSummary", 
            data=dict(email=self.email),
        )
        assert response.status_code == 302

    def test_not_authorized(self, client):
        response = client.post(
            "/showSummary",
            follow_redirects=True
        )
        assert response.status_code == 400

    # def test_book(self, client):
    #     response = client.get(
    #         "/book/<competition>/<club>",
    #     )
    #     assert response.status_code == 200


    # def test_purchase_place(self, client):
    #     response = client.post(
    #         "/purchasePlaces",
    #         data={'club' : self.clubs, 'competitions' : self.competitions}
    #         )
    #     data = response.data.decode()
    #     if datetime.fromisoformat(str(self.date)) > datetime.now():
    #         assert response.status_code == 400
    #         assert data.find("Great-booking complete!") == -1
    #     else:
    #         assert response.status_code == 200
    #         assert data.find("This competition is over!") == -1

    def test_board_points_should_status_code_ok(self, client):
        response = client.get("/board")
        assert response.status_code == 200

    def test_board_points_should_display(self, client):
        response = client.get("/board")
        data = response.data.decode()
        assert "She Lifts" in data
        assert "12" in data

    def test_logout(self, client):
        response = client.get(
            "/logout",
            follow_redirects=True
        )
        assert response.status_code == 200
        
    # def teardown_method(self):
    #     pass