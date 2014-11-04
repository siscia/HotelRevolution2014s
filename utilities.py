
#**** UTILITIES by Gio & Sara **************************************************

from database import priceFromRoomId, get_guests
import datetime




def MapFromLists(keys, values):
    """ 
    Create a map merging two lists.
    The output has this layout: {..., keys[n] : values[n], ...}
    If the two lists have different lenght returns {"error":"lists of different lenght!"}
    """
    if len(keys)!=len(values):
        return {"error":"lists of different lenght!"}
    mappa = {}
    n = 0
    for n in xrange(len(keys)):
        mappa[keys[n]] = values[n]
    return mappa

def MatchingGuest(keys, values):
    """
    This function tries to find a guest in the database, given some parameters different from the ID.
    Returns a list of guests that match in the values given in "keys".
    The two lists MUST have the same lenght.
    """
#    match = set([])
    n = 0
    match=[]
    for n in xrange(len(keys)-1):
        dblista = get_guests(keys[n], values[n])
        if n == 0:
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

def revenue(reservations):
    "Calculate the total revenue in a certain period, given the list of reservation done in that period."
    revenue = []
    for r in reservations:
        print r
        checkIN = dataINTtodataTime(r[2])
        checkOUT = dataINTtodataTime(r[3])
        days = checkOUT - checkIN
        price = priceFromRoomId(r[1])* days
        roomInfo.append({"id_room" : r[1],
                         "id_guest" : r[2],
                         "price" : price})
    return revenue