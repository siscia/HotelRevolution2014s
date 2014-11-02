from flask import Flask, request, send_from_directory, session, redirect, url_for, abort
from jinja2 import Environment, PackageLoader
import sqlite3, time, sets

app = Flask(__name__, static_folder="/templates")

env = Environment(loader=PackageLoader('hello', 'templates'))

@app.route("/<path:filename>")
def home(filename):
    return send_from_directory(app.static_folder, filename)

def login(name, passw):
        conn = sqlite3.connect("hotel.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE user = ?", ([name]))  
        user = cursor.fetchone()
        if user:
            if user[1] != passw:
                return "Invalid password"
            session["logged_in"] = True
            return
        return "Invalid username"
 

@app.route("/login", methods=["GET", "POST"])
def loginpage():
    if request.method == "GET":
        mappa = {}
        template = env.get_template("login.html")
        return template.render(mappa)
    
    if request.method == "POST":
        log = login(request.form["name"], request.form["pass"])
        if not log:
            return redirect(url_for("main"))
        else:
            mappa = {"msg" : log }
            template = env.get_template("login.html")
            return template.render(mappa)
    return "How could I end up here? :/"


@app.route("/main", methods=["GET"])
def main():
    """documentazione
    sdbseg
    """
    if not session.get('logged_in'):
        abort(401)
    today=20141004
#    today = time.localtime().tm_year * 10000 + time.localtime().tm_mon * 100 + time.localtime().tm_day
    conn = sqlite3.connect("hotel.db")
    cursor = conn.cursor() 
    n_checkin=0
    for res in cursor.execute("SELECT * FROM reservations WHERE checkIN = ?", [today]):
        n_checkin = n_checkin + 1
    n_checkout=0
    for res in cursor.execute("SELECT * FROM reservations WHERE checkOUT = ?", [today]):
        n_checkout = n_checkout + 1
    n_full=0
    for res in cursor.execute("SELECT * FROM reservations WHERE checkIN <= ? AND checkOUT >= ?", [today, today]):
        n_full = n_full + 1
    n_tot=0
    for res in cursor.execute("SELECT * FROM rooms"):
        n_tot = n_tot + 1
    if n_tot == 0:
        msg = "No rooms in this hotel?"   #Debug
    else:
        msg  = "Tutto ok!"
    n_free = n_tot - n_full
    if n_free < 0:
        mappa = {"msg" : "Error: the number of today's reservations exceed the total number of rooms. Check the database!"}     #Tenere questo controllo
    oggi = {"day": "04", "month": "10", "year": "2014" }    
#    oggi = {"day": time.localtime().tm_mday, "month": time.localtime().tm_mon, "year": time.localtime().tm_year }
    mappa = { "oggi" : oggi, "msg" : msg, "n_checkin" : n_checkin, "n_checkout" : n_checkout, "n_occupate" : n_full, "n_libere" : n_free, "n_tot" : n_tot }
    template = env.get_template("main.html")
    return template.render(mappa)


@app.route("/booking", methods=["GET"])
def booking():
    if not session.get('logged_in'):
        abort(401)
    today=20141004
#    today = time.localtime().tm_year * 10000 + time.localtime().tm_mon * 100 + time.localtime().tm_mday
    oggi = {"day": "04", "month": "10", "year": "2014" }    
#    oggi = {"day": time.localtime().tm_mday, "month": time.localtime().tm_mon, "year": time.localtime().tm_year }
    conn = sqlite3.connect("hotel.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id_room FROM reservations WHERE checkIN <= ? AND checkOUT >= ?", [request.args["checkin"], request.args["checkout"]])
    dbfullrooms = cursor.fetchall()
    cursor.execute("SELECT * FROM rooms")
    dbrooms = cursor.fetchall()
    rooms = set(dbrooms)
    fullrooms = set(dbfullrooms)
    freerooms = list(rooms.difference(fullrooms))
    mappa = {"rooms" : freerooms}
    template = env.get_template("booking.html")
    return template.render(mappa)
   
@app.route("/booking2", methods=["GET"])
def booking2():
    if not session.get('logged_in'):
        abort(401)       
        
    template = env.get_template("booking.html")
    return template.render(mappa)
        
    

@app.route("/booking_2")
def booking2():
    if not session.get('logged_in'):
        abort(401)
    today=20141004
#    today = time.localtime().tm_year * 10000 + time.localtime().tm_mon * 100 + time.localtime().tm_mday
    oggi = {"day": "04", "month": "10", "year": "2014" }    
#    oggi = {"day": time.localtime().tm_mday, "month": time.localtime().tm_mon, "year": time.localtime().tm_year }
    if request.method == "GET":
        conn = sqlite3.connect("hotel.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM rooms WHERE id_room = ?", [(request.args["room"])])
        room = cursor.fetchone()
        mappa = {"oggi" : oggi, "room": room}   #Quando chiamo in GET uso questa funzione, invece di request.form[]
        template = env.get_template("booking2.html")
        return template.render(mappa)
    
    conn = sqlite3.connect("hotel.db")
    cursor = conn.cursor()
    
    print request.args["x"]
    
    return #redirect(url_for("main"))
    
    
@app.route("/guests")
def guests():
    if not session.get('logged_in'):
        abort(401)
    
    
    
    template = env.get_template("guests.html")
    return template.render(mappa)



@app.route("/logout")
def logout():
    
    return redirect(url_for("login"))


app.secret_key = "guhurehh4gh485gh85sqacszsedwph"

if __name__ == "__main__":
    app.run(debug=True)