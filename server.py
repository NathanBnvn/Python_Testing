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
    foundClub = [c for c in clubs if c['name'] == club]
    foundCompetition = [c for c in competitions if c['name'] == competition]
    if foundClub and foundCompetition:
        foundClub = foundClub[0]
        foundCompetition = foundCompetition[0]
        return render_template('booking.html',club=foundClub,competition=foundCompetition)
    else:
        flash("Something went wrong-please try again")
        return render_template('welcome.html', club=club, competitions=competitions)


@app.route('/purchasePlaces',methods=['POST'])
def purchasePlaces():
    competition = [c for c in competitions if c['name'] == request.form['competition']][0]
    club = [c for c in clubs if c['name'] == request.form['club']][0]
    present = datetime.now()
    if datetime.fromisoformat(str(competition['date'])) > present:
        placesRequired = int(request.form['places'])
        clubPoints = int(club['points']) - int(placesRequired * 3)
        if clubPoints > 0:
            club['points'] = clubPoints
            competition['numberOfPlaces'] = int(competition['numberOfPlaces'])-placesRequired
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