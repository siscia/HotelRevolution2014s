
#***** SESSION MANAGMENT by Sara *****************************************

from flask import session, flash
import sqlite3, datetime, time


def login(name, passw):
    """ Perform the login for every user recoreded in the table "users" of the database """
    conn = sqlite3.connect("hotel.db")
    with conn:
        user = list(conn.execute("SELECT * FROM users WHERE user = ?", ([name])))[0]    #Suppose that I will get only one user with this username
        if user:
            if user[1] != passw:
                return "Invalid password"
            session["logged_in"] = True
            return
        return "Invalid username"

def logout():
    """ Perform the logout """
    session.pop("logged_in", None)
    flash("Logout successfully :)")
    return 0

