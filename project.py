from flask import Flask, request, send_from_directory, session, redirect, url_for, abort
from jinja2 import Environment, PackageLoader
from functions import login, logout
from database import get_guests
import sqlite3, time, sets

app = Flask(__name__, static_folder="/templates")

env = Environment(loader=PackageLoader('hello', 'templates'))


@app.route("/<path:filename>")
def staticfiles(filename):
    return send_from_directory(app.static_folder, filename)


@app.route("/login", methods=["GET", "POST"])
def loginpage():
    """
    loginpage()
    This function is called twice:
    - firstly in GET when the system loads, giving in output the mere template.
    - secondly in POST when the user logs in: the page calls login() (imported from functions) to verify the credential, then:
        - if login was successful, redirect the user on "main".
        - else renders the login page again showing the failure message to the user.
    """
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
    """
    main()
    This function retrieves only the data shown in the upper div of the mainpage and renders it.
    To do so, it implements various SQL queries, one for each value to retrieve.
    This rendered page allows the user to call 3 pages: free_rooms() (to begin the reservation process), reservations() (to search for present reservations), guests() (to search for registered guests).
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
        mappa = {"msg" : "Error: the number of today's reservations exceed the total number of rooms. Check the database!"}     #Keep this IF...
    oggi = {"day": "04", "month": "10", "year": "2014" }    
#    oggi = {"day": time.localtime().tm_mday, "month": time.localtime().tm_mon, "year": time.localtime().tm_year }
    mappa = { "oggi" : oggi, "msg" : msg, "n_checkin" : n_checkin, "n_checkout" : n_checkout, "n_occupate" : n_full, "n_libere" : n_free, "n_tot" : n_tot }
    template = env.get_template("main.html")
    return template.render(mappa)


@app.route("/free_rooms", methods=["GET"])
def free_rooms():
    """
    free_rooms()
    Here the system check how many rooms are available in the period of time given in input from the mainpage, create a list of them and renders the informations in the template. From that interface the user can choose which room to book and select it. He can also insert the rough information about the client, that will be used by the next functions (namely booking() ) before performing the actual booking process.
    """
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
   

@app.route("/confirm", methods=["POST"])
def confirm():
    """
    confirm()
    Here the system tries to find out if the guest's data inserted correspond to an already registered guest. If it finds a good match, it WILL NOT ASK FOR CONFIRMATION and will go straight on to confirm(), where the user will be at last allowed to confirm all the data entered before writing into the database. If it finds completely no match, he will prepare to write into the database the guest's info before performing the reservation process. In case of ambiguity, the system will suppose a new guest, while informing the user that there is a partial match.
    Priority of fields:
    - ID (usually not entered by the user, however)
    - Passport No.
    - Name & Surname
    - email address
    - any other data.
    """
    if not session.get('logged_in'):
        abort(401)
    template = env.get_template("confirm.html")
    
    names = set(get_guests("name", request.form["name"]))
    surnames = set(get_guests("surname", request.form["surname"]))
    identities = list(names.intersect(surnames))
    if identities:
        same = list(identities.intersect(set(get_guests("email", request.form["email"]))))
        if same:
            mappa= {"guest" : same, "msg" : "Exact match found." }
            return template.render(mappa)
        else:
            mappa = {"msg" : "Maybe you meant " + [for id in identitites: id[1] + " " + id[2] + "? "]}
    guest = [request.form["name"], request.form["surname"], request.form["email"]]
    mappa["guest"] = guest
    return template.render(mappa)




    
@app.route("/guests")
def guests():
    if not session.get('logged_in'):
        abort(401)
    template = env.get_template("guests.html")
    return template.render(mappa)



@app.route("/logout")
def logoutpage():
    """
    logoutpage()
    Calls the logout() function in functions.py and then redirects to the login page. In case of failure it must redirect the user on the mainpage with an error message (not implemented yet)
    """
    if logout() == 0:
        mappa = {"msg" : "Logout successfully"}
        template = env.get_template("login.html")
        return template.render(mappa)
    else:
        return "Logout failed!" #Fix this point
        


app.secret_key = "guhurehh4gh485gh85sqacszsedwph"

if __name__ == "__main__":
    app.run(debug=True)
