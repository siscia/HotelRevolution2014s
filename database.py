
#***** DATABASE FUNCTIONS by Gio *****************************************

## Dictionary
## pr_id, string, the prenotation id
## field, string, the name of the column to search
## value, string, the value to match

import sqlite3
import datetime

from config import DATABASE_PATH



def get_prenotation(pr_id):
    "Return a prenotation given the id"
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM reservations WHERE rowid = ?", [pr_id])
    return cursor.fetchall()

def get_guests(field, value):
    "Return the list of guests that match the given parameter"
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM guests WHERE  " + field + "  = ?", [value])
    return cursor.fetchall()

def checkOut_date(data):
    "Return a list of today's checkouts"
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM reservations WHERE checkOUT=?",[data])
    return cursor.fetchall()

def dataINTtodataTime(dataInt):
    "Transform a date given as INT in a common date format"
    year = dataInt/10000
    month = (dataInt-(year*10000))/100
    day = dataInt -(year*10000+month*100)
    return datetime.datetime(year,month,day)

def priceFromRoomId(id_room):
    "Return the price of a room given the room ID"
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT price_night FROM rooms WHERE id_room=?",[id_room])
    return cursor.fetchone()[0]

def checkOut_price(rooms):
    "Calculate the price of a stay, given the reservation ID ?????? ###############################"
    roomsInfo = []
    for r in rooms:
        print r
        checkIN = dataINTtodataTime(r[2])
        checkOUT = dataINTtodataTime(r[3])
        days = checkOUT - checkIN
        price = priceFromRoomId(r[1])* days
        roomInfo.append({"id_room" : r[1],
                         "id_guest" : r[2],
                         "price" : price})
    return roomsInfo
