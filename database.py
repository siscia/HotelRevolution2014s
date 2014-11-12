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
        item = list(conn.execute("SELECT * FROM rooms WHERE id_room = ?", room).fetchall())
        if item: 
            frooms.append(list(conn.execute("SELECT * FROM rooms WHERE id_room = ?", room).fetchall())[0])
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
                         "id_guest" : r[2],
                         "name" : name,
                         "surname" : surname,
                         "price" : price})
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


def get_revenue(start_date, end_date):
    def clean_data(reservation):
        checkIN = dataINT_to_datatime(r[0])
        checkOUT = dataINT_to_datatime(r[1])
        price_night = float(r[2])
        return [(checkOUT - checkIN).days * price_night,
                checkOUT]
    conn = sqlite3.connect(DATABASE_PATH)
    aggregate = []
    rev = conn.execute("""
    SELECT 
        checkIN, checkOUT, price_night 
    FROM reservations 
    INNER JOIN rooms 
        ON reservations.id_room = rooms.id_room
    WHERE checkOUT > ? AND checkOUT < ?
    ORDER BY checkOUT asc
    """, [start_date, end_date])
    res_out = [clean_data(r) for r in rev.fetchall()]
    # for r in res_out:
    #     if r[1] in aggregate:
    #         aggregate[r[1]] += r[0]
    #     else: aggregate[r[1]] = r[0]
    aggregate.append(res_out[0])
    for r in res_out[1:]:
        if r[1] == aggregate[-1:][0][1]:
            aggregate[-1:][0][0] += r[0]
        else: aggregate.append(r)
    return aggregate


def revenue(start_date, end_date):
    data = get_revenue(start_date, end_date)
    rev = 0
    for field in data:
        rev = rev + field[0]
    return rev


def add_generic(table):
    "add rows in the specified table"
    def add_specific(values):
        conn = sqlite3.connect(DATABASE_PATH)
        with conn:
            cur =  conn.cursor()
            s = "?, " * (len(values)-1) + "?"
            #print "INSERT INTO " + table + " VALUES ( null, " + s + ")", values 
            cur.execute("INSERT INTO " + table + " VALUES ( null, " + s + ")", values )
            conn.commit()
        return cur.lastrowid
    return add_specific      

def modify(table):
    "Modifies the row identified by oldvalue and oldfield. if newfield is empty rewrites the whole line."
    def modify_specific(newfield, newvalue, oldfield, oldvalue):
        conn = sqlite3.connect(DATABASE_PATH)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        with conn:
            if newfield == "":
                cur.execute("SELECT * FROM " + table)
                row = cur.fetchone()
                newfield = row.keys()[1:]
                print newfield
            #print "UPDATE " + table + " SET " + str(tuple(newfield)) + " = " + str(tuple(newvalue)) + " WHERE " + oldfield + " = " + oldvalue
            for n in xrange(len(newfield)):
                print "UPDATE " + table + " SET " + str(newfield[n]) + " = " + str(newvalue[n]) + " WHERE " + oldfield + " = " + oldvalue
                cur.execute("UPDATE " + table + " SET " + str(newfield[n]) + " = " + str(newvalue[n]) + " WHERE " + oldfield + " = " + oldvalue)
            conn.commit()
        return cur.lastrowid
    return modify_specific

