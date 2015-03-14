#!/bin/env python
# encoding: utf-8

"""
Webservice prototype for exposing cell data via
HTTP and JSON/JSONP
"""

import json
import time
import math
#import redis
from threading import Thread
import signal
import sys
from flask import Flask
from flask import request
from flask import abort, jsonify
from flask import url_for
from flask import make_response
from flask import Response
from flask import stream_with_context
#from pymongo import Connection
#from bson import json_util
import random
import pandas as pd
import Geohash
import memcache
from service.hourly_in_a_week import play_back_a_week
#red = redis.StrictRedis()

import gevent
from gevent.pywsgi import WSGIServer
from gevent import monkey
monkey.patch_all()

client = memcache.Client([('127.0.0.1', 11211)])




def signal_handler(signal, frame):
    print 'You pressed Ctrl+C!'
    sys.exit(0)


def generate():
    while 1==1:
        time.sleep(3.000)
        #print(hourly_data)
        #print('wait\n')
        if client.get("pfx_data"):
            #print(client.get("pfx_hour_in_week") + '\n')
            #print("wait"+",".join(client.get("pfx_data")) + '\n' )
            #yield '{"result":'+",".join(client.get("pfx_data"))+',"ctime":' + client.get("pfx_hour_in_week") +'}'
            yield 'data:'+ client.get("pfx_hour_in_week") + "," + "|".join(client.get("pfx_data")) + "," + "|".join(client.get("pfx_eta")) + '\n\n'




app = Flask(__name__)


@app.route('/_add_numbers')
def add_numbers():
    millis = int(round(time.time()))
    files = ['in_hail', 'occupied','available']
    ifile = open('/Users/xianyun/Documents/program1/'+files[millis % 3], 'rb')
    rows = ifile.readlines()
    ifile.close()
    latlng_data = []
    for content in rows:
        cleaned_content = " ".join((content.rstrip('\n')).split(','))
        latlng_data.append(cleaned_content)
    return jsonify(result=latlng_data, filename=files[millis % 3])

@app.route('/_flip_tiles')
def flip_tiles():
    grid = 20
    latmin = 37.687309
    latmax = 37.815133
    lngmin = -122.523438
    lngmax = -122.350574
#    latlng_data = []
#    for i in range(0, grid):
#        for j in range(0, grid):
#            content = []
#            content.append(latmin + i*(latmax-latmin)/grid)
#            content.append(latmin + (i+1)*(latmax-latmin)/grid)
#            content.append(lngmin + j*(lngmax-lngmin)/grid)
#            content.append(lngmin + (j+1)*(lngmax-lngmin)/grid)
#            content.append(random.random())
#            cleaned_content = " ".join(list(str(x) for x in content))
#            latlng_data.append(cleaned_content)
    global latlng_data
    global c_timestamp
    return jsonify(result=latlng_data, ctime=c_timestamp, result_rides = latlng_data_rides, ctime_rides = c_timestamp_rides)


@app.route('/_hourly_in_a_week')
def get_hourly_in_a_week():
    #return Response(stream_with_context(generate()), headers={'Content-Type':'text/event-stream'})
    return Response(generate(), headers={'Content-Type':'text/event-stream'})



def generate_jetson():
    while 1==1:

        #print(hourly_data)
        #print('wait\n')
        if client.get("jetson_data"):
            #print(client.get("jetson_data") + '\n')
            #print("wait"+",".join(client.get("pfx_data")) + '\n' )
            #yield '{"result":'+",".join(client.get("pfx_data"))+',"ctime":' + client.get("pfx_hour_in_week") +'}'
            yield 'data:'+ client.get("jetson_last_ts") + "," + client.get("jetson_last_epoch") + "," + "|".join(client.get("jetson_data"))  + '\n\n'
        time.sleep(299.000)
@app.route('/_jetson_rt')
def get_jetson_rt():
    #return Response(stream_with_context(generate()), headers={'Content-Type':'text/event-stream'})
    return Response(generate_jetson(), headers={'Content-Type':'text/event-stream'})


def generate_lr_metrics():
    while 1==1:
        if client.get("lr_request"):
            yield 'data:'+ client.get("lr_last_ts") + "&" + "|".join(client.get("lr_app_open")) + "&" + "|".join(client.get("lr_request")) + "&" + "|".join(client.get("lr_eta")) + "&" + "|".join(client.get("lr_drivers")) + '\n\n'
        time.sleep(299.000)
@app.route('/_lr_metrics')
def get_lr_metrics():
    #return Response(stream_with_context(generate()), headers={'Content-Type':'text/event-stream'})
    return Response(generate_lr_metrics(), headers={'Content-Type':'text/event-stream'})

#@app.before_first_request
#def runThread():
    #st = Thread( target = tail_mongo_thread )
    #st = Thread( target = create_stream, args = (5, 5, 6)  )
    #st.start()
    #st1 = Thread( target = create_stream_rides, args = (730, 5, 6)  )
    #st1.start()
#    st2 = Thread( target = play_back_a_week, args = (5,)  )
#    st2.start()


latlng_data = []
c_timestamp = []

latlng_data_rides = []
c_timestamp_rides = []

latlng_data_rides_c = []
c_timestamp_rides_c = []




if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal_handler)
    #app.before_first_request(runThread)
    #app.run(debug=True, host='0.0.0.0')
    http = WSGIServer(('0.0.0.0', 5000), app)
    http.serve_forever()
