
#**** UTILITIES by Gio & Sara **************************************************

from database import priceFromRoomId, get_guests
import datetime


def MatchingGuest(keys, values):
    """
    This function tries to find a guest in the database, given some parameters different from the ID.
    Returns a list of guests that match in the values given in "keys".
    The two lists MUST have the same lenght.
    """
    match = set([])
    for field in keys:
        dblista = get_guests(field, lista[field])
        if dblista != []:
            if field == 0:
                match = set(dblista)
            match = match & set(dblista)
    return match
    

def dataINT():
    "Return an integer number representing the current date"
    return 20141004
#    return time.localtime().tm_year * 10000 + time.localtime().tm_mon * 100 + time.localtime().tm_day

def dataINTtodataTime(dataInt):
    "Transform a date given as INT in a common date format"
    year = dataInt/10000
    month = (dataInt-(year*10000))/100
    day = dataInt -(year*10000+month*100)
    return datetime.datetime(year,month,day)

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