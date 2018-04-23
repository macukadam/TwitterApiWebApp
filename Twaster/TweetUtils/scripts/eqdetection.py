from django.test import TestCase
import timeit
import math
import sqlite3
from threading import Timer
import time
from datetime import datetime
from django.contrib.auth.models import User
from ..models import User_Location
from . import emailservice as es

loccount = 0
locations = [[]]
locations.clear()
lim = 10
erqcheck = True
flag = True
tm = timeit.default_timer()
start = tm
threadstart = tm

def refresh():
    global loccount
    global lim
    global erqcheck
    global flag
    global start
    global threadstart
    tm = timeit.default_timer()
    start = tm
    threadstart = tm
    loccount = 0
    lim = 10
    erqcheck = True
    flag = True

def refresheq():
    global start
    global threadstart
    global lim
    tm = timeit.default_timer()
    start = tm
    threadstart = tm
    locations.clear()
    lim = 10

def refreshit():
    t = Timer(30.0, refreshit)
    refresheq()
    t.start()

refreshit()

def disatstercounter(locations):
    newlist, dicpos, countlist = [],{}, []
    for city,country,time in locations:
        if city in dicpos:
            newlist[dicpos[city]].append(city)
        else:
            newlist.append([city])
            dicpos[city] = len(dicpos)

    for lst in newlist:
        countlist.append([len(lst), lst[0]])

    countlist.sort(reverse=True)

    return countlist

def _sign(lat, long, latgiven, longgiven):
    return math.sqrt((abs(lat - latgiven))**2 + abs((long - longgiven))**2)

def location_predicter(latitude, longitude,created_at):
    global lim
    global loccount
    global erqcheck
    global locations
    global start
    global threadstart
    with sqlite3.connect('/home/macukadam/Twaster/db.sqlite3') as conn:
        c = conn.cursor()
        conn.create_function("sign", 4, _sign)
        sqlcomand = "select City,Country,id from TweetUtils_location Where sign(Latitude,Longitude,{0},{1}) = (select MIN(sign(Latitude,Longitude,{0},{1})) from TweetUtils_location)".format(latitude,longitude)
        c.execute(sqlcomand)
        rows = c.fetchall()
        loccount += 1
        for row in rows:
            locations.append([row[0],row[1],created_at])
        stop = timeit.default_timer()
        #print("stop:{0} - start:{1} stop - start:{2}".format(stop,start,stop-start))
        if (stop - start) > 600 and erqcheck:
            tm = timeit.default_timer()
            start = tm
            stop = tm
            lim = 10
            locations.clear()
        if (stop - start) > lim / 10:
            countlist = disatstercounter(locations)
            #print("recordcount:{0} - limit:{1}".format(countlist[0][0],lim))
            if countlist[0][0] > 2 * lim / 10 - 1 and erqcheck:
                #print("recordcount:{0} - limit:{1}".format(countlist[0][0],lim))
                print("Eartquake detected in {0} at {1}".format(countlist[0][1], created_at))
                locations.clear()
                erqcheck = False
                created_time = datetime.strptime(created_at,'%a %b %d %H:%M:%S %z %Y')
                date = created_time.strftime('%Y-%m-%d')
                hour = created_time.strftime('%H:%M:%S')
                for row in rows:
                    c.execute("insert into TweetUtils_disaster_record values (NULL, ?, ?, ?, ?);", (date,hour,1,row[2]))
                    conn.commit()
                    user_locs = User_Location.objects.filter(Location_id=row[2]).values('User_id')
                    users = User.objects.filter(id__in=user_locs)
                    for usr in users:
                        es.sendmail(usr.email,countlist[0][1])

                    t = Timer(600.0, refresh)
                    t.start()
            lim = lim + (stop - threadstart) / 3
            #print("newlim:{0}".format(lim))
            threadstart = timeit.default_timer()