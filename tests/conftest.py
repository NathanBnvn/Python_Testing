import pytest
from server import app, clubs, competitions

@pytest.fixture
def client():
    app.config['TESTING'] = True  
    with app.test_client() as client:
        yield client

@pytest.fixture
def clubs_test():
    clubs.clear()
    club = {
        "name" : "Johnny Test Club",
        "email" : "jtest@club.com", 
        "points" : "10"
    }
    secondClub = {
        "name" : "Tania Test Club",
        "email" : "tatest@club.com", 
        "points" : "34"
    }

    clubs.append(club) 
    clubs.append(secondClub)
    return clubs


@pytest.fixture
def competitions_test():
    competitions.clear()
    competition = {
            "name" : "Spring Contest",
            "date" : "2022-02-22 10:00:00",
            "numberOfPlaces" : "14"
        }
    secondCompetition = {
            "name" : "Xtrm Winter Weight",
            "date" : "2222-12-01 20:00:00",
            "numberOfPlaces" : "54"
        }

    competitions.append(competition)
    competitions.append(secondCompetition)
    return competitions
