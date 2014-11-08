
#***** ROUTING FUNCTIONS by Sara & Simo ***************************************************

from flask import Flask, request, send_from_directory, redirect, url_for, abort, session, render_template
from jinja2 import Environment, PackageLoader
from session import login, logout, sudo
from database import get_item, n_checkin, n_checkout, n_fullrooms, n_freerooms, free_rooms, guest_leaving
from utilities import dataINT_to_datatime, dataINT, matching_guest
import sqlite3, time, sets, datetime

app = Flask(__name__, static_folder="/templates")
app = Flask(__name__, static_url_path='/static')

env = Environment(loader=PackageLoader('project', 'templates'))





# FIX WHEN POSSIBLE!!
@app.route('/stylesheet.css')
def stylesheet():
    template = env.get_template("stylesheet.css")
    return template.render()
@app.route('/bootstrap-3.2.0-dist/css/bootstrap.css')
def bootstrap():
    template = env.get_template("bootstrap-3.2.0-dist/css/bootstrap.css")
    return template.render()
@app.route('/bootstrap-3.2.0-dist/fonts/glyphicons-halflings-regular.woff')
def bootstrap_1():
    template = env.get_template("/bootstrap-3.2.0-dist/fonts/glyphicons-halflings-regular.woff")
    return template.render()
@app.route('/bootstrap-3.2.0-dist/fonts/glyphicons-halflings-regular.ttf')
def bootstrap_2():
    template = env.get_template("/bootstrap-3.2.0-dist/fonts/glyphicons-halflings-regular.ttf")
    return template.render()
@app.route('/business_man.png')
def img_1():
    template = env.get_template("business_man.png")
    return template.render()
@app.route('/HR.png')
def img_2():
    template = env.get_template("HR.png")
    return template.render()
#*************



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
    From here the user can call 3 pages: free_rooms() (to begin the reservation process), reservations() (to search for present reservations), guests() (to search for registered guests).
    """
    if not session.get('logged_in'):
        abort(401)
    today = dataINT()
#    if n_freerooms(today, today) < 0:
#        msg = "Error: the number of today's reservations exceed the total number of rooms. Check the database!"     #Keep this IF...
#    else:
#        msg = ""
    msg = ""
    mappa = { "today" : dataINT_to_datatime(today), "msg" : msg, "n_checkin" : "##", "n_checkout" : "##", "n_occupate" : "##", "n_libere" : "##"}
#    mappa = { "today" : dataINT_to_dataTime(today), "msg" : msg, "n_checkin" : n_checkin(today), "n_checkout" : n_checkout(today), "n_occupate" : "##", "n_libere" : "##"}
    template = env.get_template("main.html")
    return template.render(mappa)


@app.route("/free_rooms", methods=["GET"])
def free_rooms_page():
    """
    free_rooms()
    In this page are shown a list of available rooms in a certain period of time and a form that the receptionist have to fill with the guest's data.
    From this interface the user can choose which room to book and select it. He can also insert the informations about the client, that will be used by the next functions before performing the actual booking process.
    """
    if not session.get('logged_in'):
        abort(401)
    today = dataINT()
    mappa = {"rooms" : free_rooms(request.args["checkin"], request.args["checkout"]), "checkin" : request.args["checkin"], "checkout" : request.args["checkout"]}
    template = env.get_template("booking.html")
    return template.render(mappa)
   

@app.route("/confirm-<checkin>-<checkout>", methods=["GET"])
def confirm(checkin, checkout):
    """
    confirm()
    This page shows a sum-up of all the information inserted by the receptionist.
    Guest's data goes through some preprocessing before being shown: it's processed by MatchingGuest() in order to find if the guest has already been registered in the database. Four cases can be distinguished:
    - MatchingGuest() found only one perfectly matching row in the database. 
        In this case the infos shown are the ones found in the database.
    - MatchingGuest() found no perfectly matching rows in the database.
        - MatchingGuest() found one partial match.
            in this case the receptionist is asked to modify the database in order to update guest's data, instead than inserting a new entry.
        - MatchingGuest() found more than one partial match.
            In this case The receptionist is asked to choose the guest between the partial matching ones and modify it, or to insert a completely new entry.
        - MatchinGuest() found no matching rows.
            In this case the data shown are the one the receptionist entered before.

    MatchingGuest() permits to distinguish between "completely matching" and "partially matching".
    - Perfectly matching: all the fields matches, notes excluded.
    - Partially matching: name, surname, passport matches.
    """
    if not session.get('logged_in'):
        abort(401)
    mappa = {"checkin": checkin, "checkout": checkout}
    sel_rooms=[]
    for room in free_rooms(checkin, checkout):
        if request.args.get(str(room[0])) == "on":
            sel_rooms.append(room)
    print sel_rooms
    mappa["rooms"] = sel_rooms
    print 2
    """
    
    guests = []
    keys = []
    for item in request.args:
        if request.args[item] != "":
            guest.append(request.args[item])
            keys.append(item)
    match = MatchingGuest(keys, guests)
    if match:
        mappa["guests"] = match
        return mappa
    for item in ["name", "surname", "passport"]:
        if request.args[item] != "":
            guest.append(request.args[item])
            keys.append(item)
    match = MatchingGuest(keys, guest)
    """
    template = env.get_template("booking_confirm.html")
    return template.render(mappa)

    
    
    
@app.route("/guests")
def guests():
    """
    guests()
    Shows a list of all the guests recorded in the hotel's database that match the parameter selected in the mainpage.
    Allows the receptionist to view and modify the informations about any guest: this is useful to update the database.
    Includes also the informations about all the reservations made by every guest. TO DO!!
    """
    if not session.get('logged_in'):
        abort(401)
    guests = set([])
    mappa = {}
    n = 0
    for field in ["name", "surname", "id_guest", "passport", "email"]:
        if request.args.get(field):
            n = n + 1
            mappa[field] = request.args.get(field)
            matching = set(get_item("guests", field, request.args.get(field)))
            if n == 1:
                guests = matching
            else:
                guests = guests.intersection(matching)
    mappa["guest"] = list(guests)
    print mappa
    template = env.get_template("guest.html")
    return template.render(mappa)


@app.route("/reservations")
def reserv():
    """
    reserv()
    Allow the receptionist to find a reservation given the ID or the name of the guest.
    In case of many guest with the same name and surname returns the reservations made by both of them: the receptionist can discriminate the users by ID.
    Anyway, a message will alert the user about that.
    """
    if not session.get('logged_in'):
        abort(401)
    reserv = []
    n_res = 0
    mappa = {}
    if request.args.get("id_res"):
        mappa["id_res"] = request.args.get("id_res")
        res = get_item("reservations", "id_res", request.args.get("id_res"))
        reserv.append(res)
        if len(reserv) > 1:
            mappa["msg"] = "An error occured: more than one reservation has the selected ID. Check the database!"
    elif request.args.get("surname"):
        mappa["name"]= request.args.get("name")
        mappa["surname"]= request.args.get("surname")
        surnames = get_item("guests", "surname", request.args.get("surname"))
        if request.args["name"]:
            names = set(get_item("guests", "name", request.args.get("name")))
            guests = list(set(surnames).intersection(names))
        else:
            guests = surnames
        if len(guests) > 1:
            mappa["msg"] = "More than one guest matches your search. Be careful!"
        for guest in guests:
            res = get_item("reservations", "id_guest", guest[0])
            reserv.append(get_item("reservations", "id_guest", guest[0])[0])
            n_res = n_res + len(res)
    mappa["n_res"] = n_res
    mappa["reservations"] = reserv
    template = env.get_template("reservations.html")
    return template.render(mappa)


@app.route("/checkout")
def checkout():
    if not session.get('logged_in') or sudo() == "FALSE":
        abort(401)
    today = dataINT()
    template = env.get_template("manager.html")
    mappa= {"c" : list(guest_leaving(today))}
    mappa["username"] = session["username"]
    return template.render(mappa)


@app.route("/revenue")
def revenue():
    return


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
        


app.secret_key = ".ASF\x89m\x14\xc9s\x94\xfaq\xca}\xe1/\x1f3\x1dFx\xdc\xf0\xf9"

if __name__ == "__main__":
    app.run(debug=True)
