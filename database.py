import sqlite3
import datetime
from config import DATABASE_PATH

## Dictionary
## pr_id, string, the prenotation id
## field, string, the name of the column to search
## value, string, the value to match
## price = total price of a room
def get_prenotation(pr_id):
    "Return a prenotation given the id"
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM reservations WHERE rowid = ?", [pr_id])
    return cursor.fetchall()

def get_guests(field, value):
    """return the all information of a guest given a field (a name of the column in the database: in which colomn the function has to look for the VALUE) and a VALUE : a string (the input data)"""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM guests WHERE  " + field + "  = ?", [value])
    return cursor.fetchall()

def checkOut_date(date):
    """given a checOUT date it returns all the data of the rooms who have the checkOUT in that particular date"""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM reservations WHERE checkOUT=?",[date])
    return cursor.fetchall()

def dataINTtodataTime(dataInt):
    """ given a date in INT format (i.e. year+month+day) it return the date in DATATIME format"""
    year = dataInt/10000
    month = (dataInt-(year*10000))/100
    day = dataInt -(year*10000+month*100)
    return datetime.datetime(year,month,day)

def priceFromRoomId(id_room):
    """ return the priceiPerNight given the id of the room"""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT price_night FROM rooms WHERE id_room=?",[id_room])
    return cursor.fetchone()[0]

def checkOut_price(rooms):
    """ return the total bill(i.e. pricePerNight * days booked), the id_room and the id_guest for all the given rooms"""
    roomsInfo = []
    for r in rooms:
        checkIN = dataINTtodataTime(r[2])
        checkOUT = dataINTtodataTime(r[3])
        days = checkOUT - checkIN
        price = priceFromRoomId(r[0]) * days.days
        roomsInfo.append({"id_room" : r[0],
                         "id_guest" : r[1],
                         "price" : price})
    return roomsInfo

