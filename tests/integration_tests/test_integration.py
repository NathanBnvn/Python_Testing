from datetime import datetime
from tests.conftest import client, clubs_test, competitions_test


"""
We are testing how an user experience the whole booking process 
from accessing the page to book a competition

"""
class TestServer:

    def test_login_and_logout(self, client, clubs_test):
        response = client.get("/")
        data = response.data.decode()

        assert response.status_code == 200
        assert "Welcome to the GUDLFT Registration Portal!" in data

        response = client.post(
            "/showSummary", 
            data=dict(email=clubs_test[1]['email'])
            )
        data = response.data.decode()

        assert response.status_code == 200
        assert "Welcome, tatest@club.com"

        response = client.get("/logout", follow_redirects=True)
        data = response.data.decode()

        assert response.status_code == 200
    
    def test_book_and_purchase(self, client, clubs_test, competitions_test):
        competition = competitions_test[1]
        club = clubs_test[1]
        response = client.get(
                "/book/<competition>/<club>",
            )
        
        data = response.data.decode()
        assert response.status_code == 200
        assert competition['name'] in data
        
        response = client.post(
            "/purchasePlaces", 
                data=dict(club=club['name'], 
                competition=competition['name'], 
                places="10")
            )
        
        data = response.data.decode()

        expected_points_count = 4

        assert response.status_code == 200
        assert expected_points_count == club['points']
        assert "Great-booking complete!" in data
    