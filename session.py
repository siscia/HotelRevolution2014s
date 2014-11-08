
#***** SESSION MANAGMENT by Sara *****************************************

from flask import session, flash
from database import get_item
import sqlite3, datetime, time


def login(name, passw):
    """ Perform the login for every user recoreded in the table "users" of the database """
    conn = sqlite3.connect("hotel.db")
    with conn:
        user = list(conn.execute("SELECT * FROM users WHERE user = ?", ([name])))
        if user:
            if user[0][1] != passw:         #Suppose that I will get only one user with this username
                return "Invalid password"
            session["logged_in"] = True
            session["username"] = user[0][0]
            return
        return "Invalid username"

def logout():
    """ Perform the logout """
    session.pop("logged_in", None)
    return 0

def sudo():
    if 'username' in session:
        sudo = get_item("users", "user", session["username"])[0][2]
        return sudo
    return False