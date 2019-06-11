#!/usr/bin/env python
# coding: utf8
from database_connection_lib import *
from traitement_signal_lib import *
from sensor_lib import *
import RPi.GPIO as GPIO
import sys
import math
import time

# MongoDB connection part ####
import pymongo
from time import gmtime, strftime
Mongo_URI = "mongodb://Spicy_Telescope:ZmyWvqA7Bbfcol18@clusterinsaproject-shard-00-00-5sppd.mongodb.net:27017,clusterinsaproject-shard-00-01-5sppd.mongodb.net:27017,clusterinsaproject-shard-00-02-5sppd.mongodb.net:27017/test?ssl=true&replicaSet=ClusterINSAProject-shard-0&authSource=admin&retryWrites=true"

client = pymongo.MongoClient(Mongo_URI)
db = client.ClientsDB
scheme_db = db['ClientsCollection']
admin_db = db['Admin']
print('Connexion à la base de donnée effectuée !')
date = strftime("%Y-%m-%d %H:%M:%S", gmtime())

##############
# GPIO definitions ######

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

#TLC549
AD_Dat  = 24   
AD_Clk = 8
AD_CS = 7   
GPIO.setup(AD_CS,GPIO.OUT)
GPIO.setup(AD_Dat,GPIO.IN)
GPIO.setup(AD_Clk,GPIO.OUT)

# constantes pour le programme
user_array = []
N_MESURE = 50
compteur = 0
acquerir = False

# PYGAME PART #
import pygame
from pygame.locals import*
 
pygame.init()
  
LARGEUR = 1024
HAUTEUR = 648
fen = pygame.display.set_mode((LARGEUR, HAUTEUR))
pygame.display.set_caption("Acquisition de schema - forthouse")
fpsClock = pygame.time.Clock()

BACKGROUND = pygame.image.load('../interface_web/public/IMG/logo_fort_house.jpg')
BACKGROUND = pygame.transform.scale(BACKGROUND, (LARGEUR,HAUTEUR))

def temps():
    seconds = (pygame.time.get_ticks() - TpsZero) / 1000
    return seconds
TEXT_FONT = pygame.font.SysFont('monospace', 28)
NOIR = (0,0,0)
BLANC = (255,255,255)

# DETECTION PHASE #######
trigger = True
acquerir = False
continuer = 1
while continuer:

    
    if trigger:
        TpsZero = pygame.time.get_ticks() # DEPART CHRONO
        trigger = False

    fen.blit(BACKGROUND, (0,0))
    current_time = temps()

    	# ACQUISITION #
    
    value0=ADin(AD_Clk, AD_CS, AD_Dat) 
    
    MESSAGE = "Vous pouvez commencer l'acqusition dans :  " + str(3-current_time)             
    if current_time < 4:
        fen.blit(TEXT_FONT.render(MESSAGE, 1, BLANC), (20, HAUTEUR-50))
    if current_time > 4:
    	if value0 != 0:
	    acquerir = True 

    if acquerir:
        #conversion(value0)
        value=conversion(value0)
        user_array.append(value)
        compteur += 1
	print value
        print 'COMPTEUR : ',compteur
	if compteur == N_MESURE:
            continuer = 0
	    print user_array   
	    MESSAGE = "acquisition terminee !"
	    fen.blit(TEXT_FONT.render(MESSAGE, 1, BLANC), (20, HAUTEUR-50))


   
    pygame.display.flip()
    fpsClock.tick(60)

time.sleep(1.5)

##########################
import matplotlib.pyplot as pyplot
pyplot.plot(user_array)
pyplot.show()

print 'acces a la fin du programme'
pygame.display.quit()
pygame.quit()
### Sending to mongoDB
id = sys.argv[1]
from bson.objectid import ObjectId

if sys.argv[2] == 'client':
    send_scheme(scheme_db, user_array, ObjectId(id)) 
elif sys.argv[2] == 'admin':
    send_scheme(admin_db, user_array, ObjectId(id)) 
#sys.argv[1] => cf database.js and the arg on Python-shell
