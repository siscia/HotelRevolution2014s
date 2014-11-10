#
# DATABASE FUNCTIONS by Gio & Sara 
import sqlite3
import datetime
from config import DATABASE_PATH

## Dictionary
## pr_id, string, the prenotation id
## field, string, the name of the column to search
## value, string, the value to match

def full_rooms(checkin, checkout):
    "Return a list of the rooms which are full in the given period"
    conn = sqlite3.connect(DATABASE_PATH)
    rooms = set(conn.execute("SELECT id_room FROM rooms").fetchall())
    free = id_free_rooms(checkin, checkout)
    full = list(rooms.difference(free))
    frooms = []
    for room in full:
        frooms.append(list(conn.execute("SELECT * FROM rooms WHERE id_room = ?", room).fetchall())[0])
    print "fullrooms:"
    print frooms
    return frooms

def free_rooms(checkin, checkout):
    "Return a list of rooms which are free in the given period"
    conn = sqlite3.connect(DATABASE_PATH)
    free = id_free_rooms(checkin, checkout)
    frooms = []
    for room in free:
        frooms.append(list(conn.execute("SELECT * FROM rooms WHERE id_room = ?", room).fetchall())[0])
    print "freerooms:"
    print frooms
    return frooms

def id_rooms():
    "Return the number of all the rooms of the hotel."
    conn = sqlite3.connect(DATABASE_PATH)
    return list(conn.execute("SELECT id_room FROM rooms").fetchall())

def id_free_rooms(checkin, checkout):
    "Return a set of id of the rooms which are free in the given period"
    conn = sqlite3.connect(DATABASE_PATH)
    rooms = set(conn.execute("SELECT id_room FROM rooms").fetchall())
    reserv = set(conn.execute("SELECT id_room FROM reservations").fetchall())
    surefree= rooms.difference(reserv)
    free = set(conn.execute("SELECT id_room FROM reservations WHERE checkIN > ? OR checkOUT < ?", [checkout, checkin]).fetchall())
    free = free.union(surefree)
    return free

def n_checkin(date):
    "Calculate the number of checkins in a given date"
    conn = sqlite3.connect(DATABASE_PATH)
    n_checkin= conn.execute("SELECT COUNT(*) FROM reservations WHERE checkIN = ?", [date])
    return n_checkin.fetchall()[0][0]

def n_checkout(date):
    "Calculate the number of checkouts in a given date"
    conn = sqlite3.connect(DATABASE_PATH)
    n_checkout = conn.execute("SELECT COUNT(*) FROM reservations WHERE checkOUT = ?", [date])
    return n_checkout.fetchall()[0][0]

def n_freerooms(checkin, checkout):
    "Calculate how many rooms are free in a given date"
    n_free = 0
    for r in free_rooms(checkin, checkout):
        n_free = n_free + 1
    return n_free

def n_fullrooms(checkin, checkout):
    "Calculate how many rooms are full in a given date"
    n_full = 0
    for r in full_rooms(checkin, checkout):
        n_full = n_full + 1
    return n_full

def n_items(table, field, value):
    "Counts how many items in the database match the given parameter. if field is empty, return a list of all the items in the selected table."
    conn = sqlite3.connect(DATABASE_PATH)
    if field == "":
        n_guest= conn.execute("SELECT COUNT(*) FROM " + table)
        return n_guest.fetchall()[0][0]
    n_guest= conn.execute("SELECT COUNT(*) FROM " + table + " WHERE " + field + " = ?", [value])
    return n_guest.fetchall()[0][0]

def get_item(table, field, value):
    "Return a list of items given the field of the value to match"
    conn = sqlite3.connect(DATABASE_PATH)
    return conn.execute("SELECT * FROM " + table + " WHERE " + field + "  = ?", [value]).fetchall()

def checkout_date(date):
    "Return all the checkOut in a given day"
    conn = sqlite3.connect(DATABASE_PATH)
    return cursor.execute("SELECT * FROM reservations WHERE checkOUT=?",[date]).fetchall()

def checkin_date(date):
    "Return a list of the checkin made in the given date"
    conn = sqlite3.connect(DATABASE_PATH)
    return cursor.execute("SELECT * FROM reservations WHERE checkIN=?",[date]).fetchall()

def dataINT_to_datatime(dataInt):
    """ given a date in INT format (i.e. year+month+day) it return the date in DATATIME format"""
    year = dataInt/10000
    month = (dataInt-(year*10000))/100
    day = dataInt -(year*10000+month*100)
    return datetime.datetime(year,month,day)

def price_from_room_id(id_room):
    """ return the priceiPerNight given the id of the room"""
    conn = sqlite3.connect(DATABASE_PATH)
    return conn.execute("SELECT price_night FROM rooms WHERE id_room=?",[id_room]).fetchall()[0][0] #Suppose that it will find just one room with the selected ID

def reserv_info(reserv):
    "Given a list of reservations id return a map with the id of the room, the name and surname of the guest and the total price for the particular staying."
    roomsInfo = []
    
    for res in reserv:
        conn = sqlite3.connect(DATABASE_PATH)
        r = conn.execute("SELECT * FROM reservations WHERE id_res=?", [res[0]]).fetchone()     #Suppose that it will find just one reservation with the selected ID
        checkIN = dataINT_to_datatime(r[3])
        checkOUT = dataINT_to_datatime(r[4])
        days = checkOUT - checkIN
        price = price_from_room_id(r[1]) * days.days
        name = conn.execute("SELECT name FROM guests WHERE id_guest=?", [r[2]]).fetchone()[0]
        surname = conn.execute("SELECT surname FROM guests WHERE id_guest=?", [r[2]]).fetchone()[0]
        roomsInfo.append({"id_res" : r[0],
                         "room" : r[1],
                         "checkin" : dataINT_to_datatime(r[3]),
                         "checkout" : dataINT_to_datatime(r[4]),
                         "name" : name,
                         "surname" : surname,
                         "price" : price})
    print roomsInfo
    return roomsInfo

def guest_leaving(date):
    """Given a date (INT format) in input return a list of guest who are leaving."""
    conn = sqlite3.connect(DATABASE_PATH)
    guest = conn.execute("""select 
            guests.name, guests.surname, 
            reservations.checkIN, reservations.checkOUT, 
            rooms.price_night, rooms.id_room,
            reservations.rowid
        from reservations 
        inner join guests on reservations.id_guest = guests.id_guest 
        inner join rooms on reservations.id_room = rooms.id_room 
        where checkOUT = ?""", [(date)])
    guest = [{"name" : g[0], "surname" : g[1],
              "checkIN" : dataINT_to_datatime(g[2]),
              "checkOUT" : dataINT_to_datatime(g[3]),
              "days_stayed" : dataINT_to_datatime(g[3]) - dataINT_to_datatime(g[2]),
              "due" : (dataINT_to_datatime(g[3]) - dataINT_to_datatime(g[2])).days * g[4],
              "room_number" : g[5],
              "reservation_id" : g[6]
          } for g in guest.fetchall()]
    return guest


def columnNames(table):
    """given database (i.e. the name of a database) and table (i.e. the name of a table contained inside the databese) the function returns a list with the column's names of the table"""
    columnNames = list()
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM "+ table + " ")
    for i in cursor.description:
        columnNames.append(i[0])
    return columnNames

def add_to_dbb(table, info):
    """given a database, a table, and a information to add, the function add the information"""
    con = sqlite3.connect(DATABASE_PATH)
    data = list()
    num = columnNames(table)
    colName = '('
    for i in range(len(num)):
        if i != len(num)-1:
            colName = colName+"'"+num[i]+"'"+","
        else:
            colName = colName +"'"+num[i]+"'"
    colName = colName +')'
    quere = "("
    for i in range(len(num)):
        if i != len(num)-1:
            quere = quere +"?,"
        else:
            quere = quere +"?)"
    with con:
       cur = con.cursor()
       cur.execute("INSERT INTO "+ table +" "+ colName +" VALUES"+ quere+"",info)
       con.commit()
    return 1

def add_to_db(table, row):
    """given a database, a table, and a information to add, the function add the information"""
    con = sqlite3.connect(DATABASE_PATH)
    with con:
        keys = columnNames(table)
        cur= con.cursor()
        print keys
        #cur.execute("INSERT INTO " + table + str(tuple(row)) + " VALUES " + str(tuple(row)))
        #con.commit()
    return 1

def modify_db (table, oldfield, oldvalue, newfield, newvalue):
    con = sqlite3.connect(DATABASE_PATH)
    with con:
        cur= con.cursor()
        cur.execute("UPDATE " + table + " SET " + newfield + " = "+ newvalue + " WHERE " + oldfield + " = " + oldvalue)
        con.commit()
    return 1
