#!/usr/bin/env python
# coding: utf8
from database_connection_lib import *
from traitement_signal_lib import *
from sensor_lib import *
import sys
import math

# MongoDB connection part ####
import pymongo
from time import gmtime, strftime
Mongo_URI = "mongodb://Spicy_Telescope:ZmyWvqA7Bbfcol18@clusterinsaproject-shard-00-00-5sppd.mongodb.net:27017,clusterinsaproject-shard-00-01-5sppd.mongodb.net:27017,clusterinsaproject-shard-00-02-5sppd.mongodb.net:27017/test?ssl=true&replicaSet=ClusterINSAProject-shard-0&authSource=admin&retryWrites=true"

client = pymongo.MongoClient(Mongo_URI)
db = client.ClientsDB
notif_db_raw = db['ClientsNotifs']
notif_db = []
print('Connexion à la base de donnée effectuée !')
date = strftime("%Y-%m-%d %H:%M:%S", gmtime())

#############

import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
#TLC549
AD_Dat  = 24   
AD_Clk = 8
AD_CS = 7   
GPIO.setup(AD_CS,GPIO.OUT)
GPIO.setup(AD_Dat,GPIO.IN)
GPIO.setup(AD_Clk,GPIO.OUT)

while 1:

    value0=ADin(AD_Clk, AD_CS, AD_Dat)
    value=conversion(value0) 	
    print 'voltage value RAW : ',value0 
    print 'voltage value : ',value
    time.sleep(0.3)

GPIO.cleanup()
