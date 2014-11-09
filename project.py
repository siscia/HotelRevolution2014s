
#***** ROUTING FUNCTIONS by Sara & Simo ***************************************************

from flask import Flask, request, send_from_directory, redirect, url_for, abort, session, render_template
from jinja2 import Environment, PackageLoader
from session import login, logout, sudo
from database import get_item, n_checkin, n_checkout, n_fullrooms, n_freerooms, free_rooms, guest_leaving, price_from_room_id
from utilities import dataINT_to_datatime, datepick_to_dataINT, dataINT, matching_guest
import sqlite3, time, sets, datetime

app = Flask(__name__, static_folder="templates")

app.secret_key = ".ASF\x89m\x14\xc9s\x94\xfaq\xca}\xe1/\x1f3\x1dFx\xdc\xf0\xf9"

env = Environment(loader=PackageLoader('project', '/templates'))



# FIX WHEN POSSIBLE!!

#*************

@app.route('/<path:filename>')
def static_for_hr(filename):
    """Serve the static file from the directory app.static_folder"""
    return app.send_static_file(filename)

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
        template = env.get_template("login.html")
        return template.render()
    
    if request.method == "POST":
        log = login(request.form["name"], request.form["pass"])
        if not log:
            return redirect(url_for("main"))
        else:
            mappa = {"msg" : log , "error" : "TRUE" }
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
    mappa = { "today" : dataINT_to_datatime(today), "n_checkin" : n_checkin(today), "n_checkout" : n_checkout(today), "n_occupate" : n_fullrooms(today, today), "n_libere" : n_freerooms(today, today)}
    if n_freerooms(today, today) < 0:
        mappa["msg"]= "Error: the number of today's reservations exceed the total number of rooms. Check the database!"     #Keep this IF...
        mappa["error"] = "TRUE"
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
    mappa = {"rooms" : free_rooms(datepick_to_dataINT(request.args["checkin"]), datepick_to_dataINT(request.args["checkout"])), "checkin" : datepick_to_dataINT(request.args["checkin"]), "checkout" : datepick_to_dataINT(request.args["checkout"])}
    template = env.get_template("booking.html")
    return template.render(mappa)
   

@app.route("/confirm-<checkin>-<checkout>", methods=["GET"])
def confirm(checkin, checkout):
    """
    confirm()
    This page shows a sum-up of all the information inserted by the receptionist.
    Guest's data goes through some preprocessing before being shown: it's processed by matching_guest() in order to find if the guest has already been registered in the database. Four cases can be distinguished:
    - matching_guest() found only one perfectly matching row in the database. 
        In this case the infos shown are the ones found in the database.
    - matching_guest() found no perfectly matching rows in the database.
        - matching_guest() found one partial match.
            in this case the receptionist is asked to modify the database in order to update guest's data, instead than inserting a new entry.
        - matching_guest() found more than one partial match.
            In this case The receptionist is asked to choose the guest between the partial matching ones and modify it, or to insert a completely new entry.
        - matching_guest() found no matching rows.
            In this case the data shown are the one the receptionist entered before.

    matching_guest() permits to distinguish between "completely matching" and "partially matching".
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
    mappa["rooms"] = sel_rooms
    price = 0
    for room in sel_rooms:
        price = price + price_from_room_id(room[0])*(int(checkout)-int(checkin))
    mappa["price"] = price

    guest = []
    keys = []
    match = []
    for item in ["name", "surname", "email", "passport", "phone", "address", "info"]:
        if request.args[item] != "":
            guest.append(request.args[item])
            keys.append(item)
    match = matching_guest(keys, guest)
    if not match:
        for item in ["name", "surname", "passport"]:
            if request.args[item] != "":
                guest.append(request.args[item])
                keys.append(item)
        match = matching_guest(keys, guest)
        if not match:
            g=[0]
            for item in ["name", "surname", "email", "passport", "phone", "address", "info"]:
                g.append(request.args[item])
                if not request.args[item]:
                    g.append("")
                print item
            if g[1] == "" or g[2] == "" or g[4] == "":
                mappa["msg"] = "You must insert name, surname, and passport No of the guest."
                mappa["error"] = "TRUE"
            match.append(g)
    if len(match)>1:
        mappa["msg"] = "Warning: more than one guest matches the data you entered. Please insert more data."
        mappa["error"] = "TRUE"
    mappa["guests"] = match
    if mappa["error"] == "TRUE":
        mappa["checkin"] = int(checkin)
        mappa["checkout"] = int(checkout)
    
    template = env.get_template("booking_confirm.html")
    return template.render(mappa)


@app.route("/res_id")
def new_reserv_page():
    return "Fatto"
    
    
@app.route("/guests", methods=["GET","POST"])
def guests_page():
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
    if request.method == "GET":
        for field in ["name", "surname", "id_guest", "passport", "email"]:
            if request.args.get(field):
                n = n + 1
                mappa[field] = request.args.get(field)
                matching = set(get_item("guests", field, request.args.get(field)))
                if n == 1:
                    guests = matching
                else:
                    guests = guests.intersection(matching)
    if request.method == "POST":
        lista = []
        for field in ["name", "surname", "id_guest", "passport", "email", "note"]:
            lista.append(request.form[field])
        #Passo la lista alla funzione di Gio e ottengo un feedback (???)
        mappa["msg"] = "Database aggiornato correttamente"
        #Regenerate guest's list
        for field in ["name", "surname", "id_guest", "passport", "email"]:
            if request.form[field]:
                n = n + 1
                mappa[field] = request.form[field]
                matching = set(get_item("guests", field, request.form[field]))
                if n == 1:
                    guests = matching
                else:
                    guests = guests.intersection(matching)
    mappa["guest"] = list(guests)
    if len(guests) == 0:
        mappa["msg"] = "Nessun ospite corrisponde ai criteri di ricerca."
        mappa["error"] = "TRUE"
    print mappa
    template = env.get_template("guest.html")
    return template.render(mappa)

@app.route("/reservations")
def reserv_page():
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
        reserv.append(get_item("reservations", "id_res", request.args.get("id_res")))
        if len(reserv) > 1:
            mappa["msg"] = "An error occured: more than one reservation has the selected ID. Check the database!"
            mappa["error"] = "TRUE"
    elif request.args.get("surname"):
        surnames = get_item("guests", "surname", request.args.get("surname"))
        if request.args["name"]:
            names = set(get_item("guests", "name", request.args.get("name")))
            guests = list(set(surnames).intersection(names))
        else:
            guests = surnames
        if len(guests) > 1:
            mappa["msg"] = "More than one guest matches your search. Be careful!"
            mappa["error"] = "TRUE"
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
    mappa= {"lista" : list(guest_leaving(today))}
    mappa["username"] = session["username"]
    mappa["date"] = dataINT_to_datetime(today)
    return template.render(mappa)


@app.route("/revenue")
def revenue():
    template.env.get_template("revenue.html")
    return template.render()


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
    template = env.get_template("login.html")
    mappa["msg"] = "There was a problem during the logout process. Try login and logout again (if necessary)."
    mappa["error"] = "TRUE"
    return template.render(mappa)


if __name__ == "__main__":
    app.run(debug=True)
