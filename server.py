from datetime import datetime
import json
from flask import Flask,render_template,request,redirect,flash,url_for, redirect


def loadClubs():
    with open('clubs.json') as c:
        listOfClubs = json.load(c)['clubs']
        return listOfClubs


def loadCompetitions():
    with open('competitions.json') as comps:
         listOfCompetitions = json.load(comps)['competitions']
         return listOfCompetitions


app = Flask(__name__)
app.secret_key = 'something_special'

competitions = loadCompetitions()
clubs = loadClubs()

@app.route('/')
def index():
    return render_template('index.html', clubs=clubs)


@app.route('/showSummary',methods=['POST'])
def showSummary():
    club = [club for club in clubs if club['email'] == request.form['email']]
    if club:
        club = club[0]
        return render_template('welcome.html',club=club,competitions=competitions)
    else:
        return redirect(f'unauthorized')


@app.route('/unauthorized')
def not_allowed():
    return render_template('forbidden.html')


@app.route('/book/<competition>/<club>')
def book(competition,club):
    found_club = [c for c in clubs if c['name'] == club]
    found_competition = [c for c in competitions if c['name'] == competition]
    if found_club and found_competition:
        found_club = found_club[0]
        found_competition = found_competition[0]
        return render_template('booking.html',club=found_club,competition=found_competition)
    else:
        flash("Something went wrong-please try again")
        return render_template('welcome.html', club=club, competitions=competitions)


@app.route('/purchasePlaces',methods=['POST'])
def purchasePlaces():
    competition = [c for c in competitions if c['name'] == request.form['competition']][0]
    club = [c for c in clubs if c['name'] == request.form['club']][0]
    present = datetime.now()
    if datetime.fromisoformat(str(competition['date'])) > present:
        places_required = int(request.form['places'])
        club_points = int(club['points']) - int(places_required * 3)
        if club_points > 0:
            club['points'] = club_points
            competition['numberOfPlaces'] = int(competition['numberOfPlaces'])-places_required
            flash('Great-booking complete!')
            return render_template('welcome.html', club=club, competitions=competitions)
        else:
            flash('You dont have enough points')
            return render_template('welcome.html', club=club, competitions=competitions)
    else:
        flash('This competition is over!')
        return render_template('welcome.html', club=club, competitions=competitions)


@app.route('/logout')
def logout():
    return redirect(url_for('index'))