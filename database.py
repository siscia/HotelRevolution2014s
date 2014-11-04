
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
    rooms = set(conn.execute("SELECT id_room FROM reservations WHERE checkIN <= ? AND checkOUT >= ?", (checkin, checkout)))
    fullrooms = set(conn.execute("SELECT * FROM rooms"))
    return list(rooms.difference(fullrooms))

def n_CheckIn(date):
    "Calculate the number of checkins in a given date"
    conn = sqlite3.connect(DATABASE_PATH)
    n_checkin=0
    for res in conn.execute("SELECT * FROM reservations WHERE checkIN = ?", [date]):
        n_checkin = n_checkin + 1
    return n_checkin

def n_CheckOut(date):
    "Calculate the number of checkouts in a given date"
    conn = sqlite3.connect(DATABASE_PATH)
    n_checkout=0
    for res in conn.execute("SELECT * FROM reservations WHERE checkOUT = ?", [date]):
        n_checkout = n_checkout + 1
    return n_checkout

def n_FullRooms(date):
    "Calculate how many rooms are full in a given date"
    conn = sqlite3.connect(DATABASE_PATH)
    n_full=0
    for res in conn.execute("SELECT * FROM reservations WHERE checkIN <= ? AND checkOUT >= ?", [date, date]):
        n_full = n_full + 1
    return n_full

def n_FreeRooms(date):
    "Calculate how many rooms are full in a given date"
    conn = sqlite3.connect(DATABASE_PATH)
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

def dataINTtodataTime(dataInt):
    "Transform a date given as INT in a common date format"
    year = dataInt/10000
    month = (dataInt-(year*10000))/100
    day = dataInt -(year*10000+month*100)
    return datetime.datetime(year,month,day)

def priceFromRoomId(id_room):
    "Return the price of a room given the room ID"
    conn = sqlite3.connect(DATABASE_PATH)
    return list(cursor.execute("SELECT price_night FROM rooms WHERE id_room=?",[id_room]))[0]

def checkOut_price(rooms):
    "Given a list of rooms return a map with the id of the room, the id of the guest and the total price for the particular staying."
    roomsInfo = []
    print rooms
    for r in rooms:
        checkIN = dataINTtodataTime(r[2])
        checkOUT = dataINTtodataTime(r[3])
        days = (checkOUT - checkIN).days
        price = priceFromRoomId(r[0]) * days
        roomsInfo.append({"id_room" : r[0],
                          "id_guest" : r[2],
                          "price" : price})
    return roomsInfo
