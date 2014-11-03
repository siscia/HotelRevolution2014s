from flask import session, flash
import sqlite3, time


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


def logout():
    session.pop("logged_in", None)
    flash("Logout successfully :)")
    return 0