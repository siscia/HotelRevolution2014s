import sqlite3
import datetime

from config import DATABASE_PATH

## Dictionary
## pr_id, string, the prenotation id
## field, string, the name of the column to search
## value, string, the value to match

def get_prenotation(pr_id):
    "Return a prenotation given the id"
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM reservations WHERE rowid = ?", [pr_id])
    return cursor.fetchall()

def get_guests(field, value):
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM guests WHERE  " + field + "  = ?", [value])
    return cursor.fetchall()

def checkOut_date(data):
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM reservations WHERE checkOUT=?",[data])
    return cursor.fetchall()

def dataINTtodataTime(dataInt):
    year = dataInt/10000
    month = (dataInt-(year*10000))/100
    day = dataInt -(year*10000+month*100)
    return datetime.datetime(year,month,day)

def priceFromRoomId(id_room):
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT price_night FROM rooms WHERE id_room=?",[id_room])
    return cursor.fetchone()[0]

def checkOut_price(rooms):
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
