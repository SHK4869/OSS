from flask import Flask, render_template, request, url_for, redirect,session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from functools import wraps
from sqlalchemy.sql import text

app = Flask(__name__)
app.config['SECRET_KEY'] = 'shhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh!!!'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:humaira@localhost/CricketTournament'
db = SQLAlchemy(app)
from sqlalchemy import Column, Integer, String
#print "fafsfasfssdsa"
"""
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

d['Points' ] = []
Points = db.engine.execute("SELECT * FROM \"PointsTable\";")
for i in Points:
	d['Points'].append(i)
	#print i.TeamName

Teams = db.engine.execute("SELECT \"Team\".\"TeamName\",\"MatchesPlayed\",\"Wins\",\"Lost\",\"Points\",\"Captain\",\"Coach\" FROM \"PointsTable\" NATURAL JOIN \"Team\" WHERE \"PointsTable\".\"TeamName\"=\"Team\".\"TeamName\";")

d['Teams'] = {}

for i in Teams:
	d['Teams'][i.TeamName] = i


Bowlers = db.engine.execute("SELECT \"PlayerId\",\"TeamName\",\"FirstName\",\"LastName\",\"Age\",\"Role\",\"Economy\",\"Wickets\",\"Matches\",\"BBI\",\"DoB\" FROM \"Team\" NATURAL JOIN (SELECT \"PlayerId\",\"FirstName\",\"LastName\",\"Age\",\"Role\",\"Economy\",\"Wickets\",\"Matches\",\"BBI\",\"DoB\",\"TeamID\" FROM \"Player\" NATURAL JOIN \"Bowler\" WHERE \"PlayerId\" = \"PlayerID\") AS \"INFO\" WHERE \"Team\".\"TeamID\"=\"INFO\".\"TeamID\";")

d['Bowlers'] = {}
for i in Bowlers:
	d['Bowlers'][i.PlayerId] = i
#print d['Bowlers']


Batsmen = db.engine.execute("SELECT \"PlayerId\",\"TeamName\",\"FirstName\",\"LastName\",\"Age\",\"Role\",\"HighScore\",\"StrikeRate\",\"TotalRuns\",\"DoB\" FROM \"Team\" NATURAL JOIN (SELECT \"PlayerId\",\"FirstName\",\"LastName\",\"Age\",\"Role\",\"HighScore\",\"TotalRuns\",\"Matches\",\"StrikeRate\",\"DoB\",\"TeamID\" FROM \"Player\" NATURAL JOIN \"Batting\" WHERE \"PlayerId\" = \"PlayerID\") AS \"INFO\" WHERE \"Team\".\"TeamID\"=\"INFO\".\"TeamID\";")

d['Batsmen'] = {}
for i in Batsmen:
	d['Batsmen'][i.PlayerId] = i
#print d['Batsmen']

d['login'] = {}

log = db.engine.execute("SELECT * FROM \"LogIn\";")
for i in log:
	d['login'][i.UserName] = i.Password
#print d['login']
"""


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'loggedin' not in session:
            return redirect(url_for('homepage'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/', methods=['GET','POST'])
def index():

    return redirect(url_for("homepage"))
    
@app.route('/homepage/')
def homepage():
	data = []
	Points = db.engine.execute("SELECT * FROM \"PointsTable\";")
	for i in Points:
		data.append(i)
#		print i.TeamName
	return render_template("main.html",data = data)


@app.route('/recent/')

def recent():

	data = []
	Matches = db.engine.execute("SELECT * FROM \"Match\"  WHERE \"Date\" < CURRENT_DATE ORDER BY \"Date\";")
	for i in Matches:
		data.append(i)
	#	print i.TeamA
	return render_template("recent.html", data=data)
	
@app.route('/upcoming/')
def upcoming():
	
	data = []
	Matches = db.engine.execute("SELECT * FROM \"Match\"  WHERE \"Date\" >= CURRENT_DATE ORDER BY \"Date\";")
	for i in Matches:
		data.append(i)
	#	print i.TeamA
	return render_template("upcoming.html", data = data)
	
@app.route('/matchresult', methods=['GET','POST'])

def matchresult():

    d = dict(request.form)
    matchid = d['matchid'][0]
    toss = d['toss'][0]
    result = d['result'][0]
    
    bname = d['bn'][0]
    strike = d['bs'][0]
    runs = d['brun'][0]
    biid =[]
    bid= db.engine.execute("SELECT \"PlayerId\" FROM \"Player\" WHERE \"FirstName\" = "+"\'"+bname+"\';")
    for x in bid:
    	biid.append(x)
    """
    print type(bname)
    print type(strike)
    print type(runs)
    print type(bid)
    print bid
    print biid[0].PlayerId
    print strike
    print runs
    """
    """
    temp  = "SELECT batting_insert(" +  str(biid[0].PlayerId) +  ","  +  str(strike)  + "," + str(runs)  +  ");"
    print temp
    print  db.engine.execute((temp))    
    """
    db.engine.execute("UPDATE \"Match\" SET \"Toss\" = \'" + toss + "\', \"Winner\" = \'" +result + "\' WHERE \"MatchID\" = " + matchid + ";")
    #if(username=="vineet" and password=="1234"):
    #	return redirect(url_for('upcoming'))

    # x=Point(1,"INDIA",2,1,4)
    # y=Point(2,"Aus",1,2,2)
    # data=[x,y]
    # return render_template("main.html", data=data)
    """
    with db.engine.connect() as con:
    	statement = text(SELECT batting_insert(%s,%s,%s);,(biid[0].PlayerId,strike,runs))
    	con.execute(statement)
    """
   # UPDATE "Batting" SET "TotalRuns" = "TotalRuns" + runs_scored,"StrikeRate" = strike, "Matches" = "Matches" +1   WHERE "PlayerID" = id;
#IF (SELECT "Batting"."HighScore" FROM "Batting" WHERE "PlayerID" = id) < runs_scored THEN
	#UPDATE "Batting" SET "HighScore" = runs_scored WHERE "PlayerID" = id;
   # data = db.session.query(func.public.batting_insert(int(biid[0].PlayerId), float(strike), int(runs)))
   # db.session.commit()
    db.engine.execute("UPDATE \"Batting\" SET \"TotalRuns\" = \"TotalRuns\" + "+str(runs)+" ,\"StrikeRate\" = "+str(strike)+" , \"Matches\" = \"Matches\" +1   WHERE \"PlayerID\" = " +str(biid[0].PlayerId)+";")
    temp = db.engine.execute("SELECT \"Batting\".\"HighScore\" FROM \"Batting\" WHERE \"PlayerID\" = "+str(biid[0].PlayerId))
    data = []
    for x in temp:
    	data.append(x)
    if data[0].HighScore < runs:
    	db.engine.execute("UPDATE \"Batting\" SET \"HighScore\" = "+str(runs)+" WHERE \"PlayerID\" = "+str(biid[0].PlayerId)+";")
   
    boname = d['boname'][0]

    economy = d['boe'][0]

    wickets = d['bow'][0]

    biid =[]

    bid= db.engine.execute("SELECT \"PlayerId\" FROM \"Player\" WHERE \"FirstName\" = "+"\'"+boname+"\';")

    for x in bid:

    	biid.append(x)
    	
    db.engine.execute("UPDATE \"Bowler\" SET \"Wickets\" = \"Wickets\" + "+wickets+",\"Economy\" = "+economy+", \"Matches\" = \"Matches\" +1   WHERE \"PlayerID\" = "+str(biid[0].PlayerId)+";")


    return redirect(url_for('manager'))
    
@app.route('/predict', methods=['GET','POST'])
#authentication
def predict():

    d = dict(request.form)
    username = d['username'][0]
    password = d['psw'][0]
    data = db.engine.execute("SELECT * FROM \"LogIn\";")
    #passs = db.engine.execute("SELECT \"Password\" FROM \"LogIn\";")
    
 #   print user[0].UserName
   # print passs[0].Password
    for x in data:
	    if((username == x.UserName) and (password == x.Password) ):
	    	session['loggedin'] = True;
	    	return redirect(url_for('manager'))

    # x=Point(1,"INDIA",2,1,4)
    # y=Point(2,"Aus",1,2,2)
    # data=[x,y]
    # return render_template("main.html", data=data)
    return redirect(url_for('homepage'))
    
@app.route('/manager/')
@login_required
def manager():
	
	return render_template("manager.html")
	
@app.route('/bestbat/')
	
def batsman():
	bestBat = db.engine.execute("SELECT * FROM \"Player\" NATURAL JOIN \"Batting\" WHERE \"Player\".\"PlayerId\"=\"Batting\".\"PlayerID\" ORDER BY \"TotalRuns\"DESC ; ")
	data = []
	for i in bestBat:
		data.append(i)
	return render_template("batsman.html", data=data)
	
@app.route('/bestbowl/')
def bowler():
	bestBowl = db.engine.execute("SELECT * FROM \"Player\" NATURAL JOIN \"Bowler\" WHERE \"Player\".\"PlayerId\"=\"Bowler\".\"PlayerID\" ORDER BY \"Wickets\" DESC ;")
	data = []
	for i in bestBowl:
		data.append(i)
	return render_template("bowlers.html", data=data)
	
@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    #flash('You were logged out')
    return redirect(url_for('homepage'))

if __name__ == "__main__":
	app.debug = True
	app.run(port=5000)
