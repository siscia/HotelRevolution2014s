#
# DATABASE FUNCTIONS by Gio & Sara 
import sqlite3
import datetime
from config import DATABASE_PATH

## Dictionary
## pr_id, string, the prenotation id
## field, string, the name of the column to search
## value, string, the value to match

def free_rooms(checkin, checkout):
    "Return a list of the rooms which are free in the given period"
    conn = sqlite3.connect(DATABASE_PATH)
    fullrooms = set(conn.execute("SELECT id_room FROM reservations WHERE checkIN < ? OR checkOUT > ?", (checkin, checkout)))
    rooms = set(conn.execute("SELECT id_room FROM rooms"))
    freerooms = list(rooms.difference(fullrooms))
    frooms = []
    for room in freerooms:
        frooms.append(list(conn.execute("SELECT * FROM rooms WHERE id_room = ?", room))[0])
    return frooms

def Extract(cursor):
    "Just to make the syntax a bit more clear: cleans the count obtained by SELECT COUNT"
    return list(cursor)[0][0]

def n_checkin(date):
    "Calculate the number of checkins in a given date"
    conn = sqlite3.connect(DATABASE_PATH)
    n_checkin= conn.execute("SELECT COUNT(*) FROM reservations WHERE checkIN = ?", [date])
    return Extract(n_checkin)

def n_checkout(date):
    "Calculate the number of checkouts in a given date"
    conn = sqlite3.connect(DATABASE_PATH)
    n_checkout = conn.execute("SELECT COUNT(*) FROM reservations WHERE checkOUT = ?", [date])
    return list(n_checkout)[0][0]

def n_fullrooms(date):
    "Calculate how many rooms are full in a given date"
    conn = sqlite3.connect(DATABASE_PATH)
    return Extract(conn.execute("SELECT COUNT(*) FROM reservations WHERE checkIN < ? OR checkOUT > ?", [(checkin), (checkout)]))

def n_freerooms(date):
    "Calculate how many rooms are full in a given date"
    conn = sqlite3.connect(DATABASE_PATH)
    n_tot = Extract(conn.execute("SELECT COUNT(*) FROM rooms"))
    print 1
    n_full = Extract(n_FullRooms(checkin, checkout))
    return n_tot - n_full

def get_prenotation(pr_id):
    "Return a prenotation given the id"
    conn = sqlite3.connect(DATABASE_PATH)
    return list(conn.execute("SELECT * FROM reservations WHERE rowid = ?", [pr_id]))

def get_guests(field, value):
    "Return the list of guests that match the given parameter"
    conn = sqlite3.connect(DATABASE_PATH)
    return list(conn.execute("SELECT * FROM guests WHERE  " + field + "  = ?", [value]))

def checkout_date(date):
    """return all the checkOut in a given day"""
    conn = sqlite3.connect(DATABASE_PATH)
    return list(cursor.execute("SELECT * FROM reservations WHERE checkOUT=?",[date]))

def checkin_date(date):
    "Return a list of the checkin made in the given date"
    conn = sqlite3.connect(DATABASE_PATH)
    return list(cursor.execute("SELECT * FROM reservations WHERE checkIN=?",[date]))

def dataINTtodataTime(dataInt):
    """ given a date in INT format (i.e. year+month+day) it return the date in DATATIME format"""
    year = dataInt/10000
    month = (dataInt-(year*10000))/100
    day = dataInt -(year*10000+month*100)
    return datetime.datetime(year,month,day)

def price_from_room_id(id_room):
    """ return the priceiPerNight given the id of the room"""
    conn = sqlite3.connect(DATABASE_PATH)
    return list(cursor.execute("SELECT price_night FROM rooms WHERE id_room=?",[id_room]))[0]

def checkout_price(rooms):
    "Given a list of rooms return a map with the id of the room, the id of the guest and the total price for the particular staying."
    roomsInfo = []
    print rooms
    for r in rooms:
        checkIN = dataINTtodataTime(r[2])
        checkOUT = dataINTtodataTime(r[3])
        days = checkOUT - checkIN
        price = priceFromRoomId(r[0]) * days.days
        roomsInfo.append({"id_room" : r[0],
                         "id_guest" : r[1],
                         "price" : price})
    return roomsInfo

