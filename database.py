
#***** DATABASE FUNCTIONS by Gio & Sara *****************************************

## Dictionary
## pr_id, string, the prenotation id
## field, string, the name of the column to search
## value, string, the value to match

import sqlite3
import datetime
from config import DATABASE_PATH



def Free_Rooms(checkin, checkout):
    "Return a list of the rooms which are free in the given period"
    conn = sqlite3.connect(DATABASE_PATH)
    fullrooms = set(conn.execute("SELECT id_room FROM reservations WHERE checkIN <= ? AND checkOUT >= ?", (checkin, checkout)))
    rooms = set(conn.execute("SELECT * FROM rooms"))
    return list(rooms.difference(fullrooms))

def n_CheckIn(date):
    "Calculate the number of checkins in a given date"
    conn = sqlite3.connect(DATABASE_PATH)
    n_checkin=0
    for res in conn.execute("SELECT * FROM reservations WHERE checkIN = ?", [date]):
        n_checkin = n_checkin + 1
    return n_checkin

def n_CheckOut(date):
    conn = sqlite3.connect(DATABASE_PATH)
    "Calculate the number of checkouts in a given date"
    n_checkout=0
    for res in conn.execute("SELECT * FROM reservations WHERE checkOUT = ?", [date]):
        n_checkout = n_checkout + 1
    return n_checkout

def n_FullRooms(date):
    conn = sqlite3.connect(DATABASE_PATH)
    "Calculate how many rooms are full in a given date"
    n_full=0
    for res in conn.execute("SELECT * FROM reservations WHERE checkIN <= ? AND checkOUT >= ?", [date, date]):
        n_full = n_full + 1
    return n_full

def n_FreeRooms(date):
    conn = sqlite3.connect(DATABASE_PATH)
    "Calculate how many rooms are full in a given date"
    n_tot=0
    for res in conn.execute("SELECT * FROM rooms"):
        n_tot = n_tot + 1
    return n_tot - n_FullRooms(date)


def get_prenotation(pr_id):
    "Return a prenotation given the id"
    conn = sqlite3.connect(DATABASE_PATH)
    return list(conn.execute("SELECT * FROM reservations WHERE rowid = ?", [pr_id]))

def get_guests(field, value):
    "Return the list of guests that match the given parameter"
    conn = sqlite3.connect(DATABASE_PATH)
    return list(conn.execute("SELECT * FROM guests WHERE  " + field + "  = ?", [value]))

def checkOut_date(date):
    "Return a list of the checkout made in the given date"
    conn = sqlite3.connect(DATABASE_PATH)
    return list(cursor.execute("SELECT * FROM reservations WHERE checkOUT=?",[date]))

def checkIn_date(date):
    "Return a list of the checkin made in the given date"
    conn = sqlite3.connect(DATABASE_PATH)
    return list(cursor.execute("SELECT * FROM reservations WHERE checkIN=?",[date]))

def priceFromRoomId(id_room):
    "Return the price of a room given the room ID"
    conn = sqlite3.connect(DATABASE_PATH)
    return list(cursor.execute("SELECT price_night FROM rooms WHERE id_room=?",[id_room]))[0]
