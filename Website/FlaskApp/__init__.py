from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:humaira@localhost/CricketTournament'
db = SQLAlchemy(app)
from sqlalchemy import Column, Integer, String
"""
class User(db.Model):
	
     __tablename__ = 'users'

     id = db.Column(Integer, primary_key=True)
     name = db.Column(String)
     fullname = db.Column(String)
     password = db.Column(String)

     def __repr__(self):
        return "<User(name='%s', fullname='%s', password='%s')>" % (
                             self.name, self.fullname, self.password)
     
"""

#res = db.engine.execute("SELECT * FROM Player NATURAL JOIN Team;")
bestBat = db.engine.execute("SELECT \"FirstName\", \"TotalRuns\" FROM \"Player\" NATURAL JOIN \"Batting\" WHERE \"Batting\".\"PlayerID\" = \"Player\".\"PlayerId\" AND \"TotalRuns\" = (SELECT max(\"TotalRuns\") FROM \"Player\" NATURAL JOIN \"Batting\" WHERE \"Batting\".\"PlayerID\" = \"Player\".\"PlayerId\");") 

bestBowl = db.engine.execute("SELECT \"FirstName\", \"Wickets\" FROM \"Player\" NATURAL JOIN \"Bowler\" WHERE \"Bowler\".\"PlayerID\" = \"Player\".\"PlayerId\" AND \"Wickets\" = (SELECT max(\"Wickets\") FROM \"Player\" NATURAL JOIN \"Bowler\" WHERE \"Bowler\".\"PlayerID\" = \"Player\".\"PlayerId\");")
d={}


for i in bestBat:
	d['BestBat'] = i
for i in bestBowl:
	d['BestBowl'] = i
bestBat = db.engine.execute("SELECT * FROM \"Player\" NATURAL JOIN \"Batting\" WHERE \"Batting\".\"PlayerID\" = \"Player\".\"PlayerId\" AND \"TotalRuns\" = (SELECT max(\"TotalRuns\") FROM \"Player\" NATURAL JOIN \"Batting\" WHERE \"Batting\".\"PlayerID\" = \"Player\".\"PlayerId\");")
bestBowl = db.engine.execute("SELECT * FROM \"Player\" NATURAL JOIN \"Bowler\" WHERE \"Bowler\".\"PlayerID\" = \"Player\".\"PlayerId\" AND \"Wickets\" = (SELECT max(\"Wickets\") FROM \"Player\" NATURAL JOIN \"Bowler\" WHERE \"Bowler\".\"PlayerID\" = \"Player\".\"PlayerId\");")
for i in bestBat:
	d['BestBatFull'] = i
for i in bestBowl:
	d['BestBowlFull'] = i

bestBat = db.engine.execute("SELECT * FROM \"Player\" NATURAL JOIN \"Batting\" WHERE \"Player\".\"PlayerId\"=\"Batting\".\"PlayerID\" ORDER BY \"TotalRuns\" DESC LIMIT 3;")
bestBowl = db.engine.execute("SELECT * FROM \"Player\" NATURAL JOIN \"Bowler\" WHERE \"Player\".\"PlayerId\"=\"Bowler\".\"PlayerID\" ORDER BY \"Wickets\" DESC LIMIT 3;")


for i in bestBat:
	d['BestBatTop'] = i
for i in bestBowl:
	d['BestBowlTop'] = i

d['Points' ] = []
Points = db.engine.execute("SELECT * FROM \"PointsTable\";")
for i in Points:
	d['Points'].append(i)
	
print d['Points']

Teams = db.engine.execute("SELECT \"Team\".\"TeamName\",\"MatchesPlayed\",\"Wins\",\"Lost\",\"Points\",\"Captain\",\"Coach\" FROM \"PointsTable\" NATURAL JOIN \"Team\" WHERE \"PointsTable\".\"TeamName\"=\"Team\".\"TeamName\";")

d['Teams'] = {}

for i in Teams:
	d['Teams'][i.TeamName] = i


Bowlers = db.engine.execute("SELECT \"PlayerId\",\"TeamName\",\"FirstName\",\"LastName\",\"Age\",\"Role\",\"Economy\",\"Wickets\",\"Matches\",\"BBI\",\"DoB\" FROM \"Team\" NATURAL JOIN (SELECT \"PlayerId\",\"FirstName\",\"LastName\",\"Age\",\"Role\",\"Economy\",\"Wickets\",\"Matches\",\"BBI\",\"DoB\",\"TeamID\" FROM \"Player\" NATURAL JOIN \"Bowler\" WHERE \"PlayerId\" = \"PlayerID\") AS \"INFO\" WHERE \"Team\".\"TeamID\"=\"INFO\".\"TeamID\";")

d['Bowlers'] = {}
for i in Bowlers:
	d['Bowlers'][i.PlayerId] = i
print d['Bowlers']


Batsmen = db.engine.execute("SELECT \"PlayerId\",\"TeamName\",\"FirstName\",\"LastName\",\"Age\",\"Role\",\"HighScore\",\"StrikeRate\",\"TotalRuns\",\"DoB\" FROM \"Team\" NATURAL JOIN (SELECT \"PlayerId\",\"FirstName\",\"LastName\",\"Age\",\"Role\",\"HighScore\",\"TotalRuns\",\"Matches\",\"StrikeRate\",\"DoB\",\"TeamID\" FROM \"Player\" NATURAL JOIN \"Batting\" WHERE \"PlayerId\" = \"PlayerID\") AS \"INFO\" WHERE \"Team\".\"TeamID\"=\"INFO\".\"TeamID\";")

d['Batsmen'] = {}
for i in Batsmen:
	d['Batsmen'][i.PlayerId] = i
print d['Batsmen']

d['login'] = {}

log = db.engine.execute("SELECT * FROM \"LogIn\";")
for i in log:
	d['login'][i.UserName] = i.Password
print d['login']

@app.route('/', methods=['GET','POST'])
def homepage():
    return render_template("main.html", d = d)
    
@app.route('/batsman', methods = ['GET', 'POST'])
def batsman():
	return render_template("batsman.html", d=d)


if __name__ == "__main__":
	app.debug = True
	app.run(port=5000)
