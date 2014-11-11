
#**** UTILITIES by Gio & Sara **************************************************

from database import price_from_room_id, get_item
import datetime



def matching_guest(keys, values):
    """
    This function tries to find a guest in the database, given some parameters different from the ID.
    Returns a list of guests that match in the values given in "keys".
    The two lists MUST have the same lenght.
    """
    n = 0
    match=[]
    for n in xrange(len(keys)):
        dblista = get_item("guests", keys[n], values[n])
#        print "    dblista " + keys[n] + ": " + values[n]
        if n == 0:
            match = set(dblista)
        match = match.intersection(set(dblista))
    return list(match)

def dataINT():
    "Return an integer number representing the current date"
    return 20141004
#    return time.localtime().tm_year * 10000 + time.localtime().tm_mon * 100 + time.localtime().tm_day


def dataINT_to_datatime(dataInt):
    "Transform a date given as INT in DATATIME format"
    year = dataInt/10000
    month = (dataInt-(year*10000))/100
    day = dataInt -(year*10000+month*100)
    return datetime.datetime(year,month,day)

def datepick_to_dataINT(data):
    "Convert the date format given by datepickr (string) into the dataINT format"
    if str(data).count("/") != 2:
        return int(data)
    d = data.split("/")
    date = int(d[0])*10000 + int(d[1])*100 + int(d[2])
    return date

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
