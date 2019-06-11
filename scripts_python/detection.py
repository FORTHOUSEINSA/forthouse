#!/usr/bin/env python
# coding=utf-8

from notification_lib import *
from database_connection_lib import *
from sensor_lib import *
from traitement_signal_lib_v3 import *

import time
import RPi.GPIO as GPIO
from picamera import PiCamera
import math
import matplotlib.pyplot as plt
import pygame
from pygame.locals import *

pygame.init()

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

# servo moteur

GPIO.setup(18,GPIO.OUT)

pwm=GPIO.PWM(18,50)
pwm.start(10) #full left position
reset_chrono_locket = True
time.sleep(3)
pwm.ChangeDutyCycle(0)

# Camera

camera = PiCamera()

# PIR setup

GPIO.setup(26, GPIO.IN)

#########

# MongoDB connection part ####
import pymongo
from time import strftime, localtime
Mongo_URI = "mongodb://Spicy_Telescope:ZmyWvqA7Bbfcol18@clusterinsaproject-shard-00-00-5sppd.mongodb.net:27017,clusterinsaproject-shard-00-01-5sppd.mongodb.net:27017,clusterinsaproject-shard-00-02-5sppd.mongodb.net:27017/test?ssl=true&replicaSet=ClusterINSAProject-shard-0&authSource=admin&retryWrites=true"

client = pymongo.MongoClient(Mongo_URI)
db = client.ClientsDB
Clients_DB_raw = db['ClientsCollection'] # base de donnee contenant les utilisateurs
Clients_DB = []
for user in Clients_DB_raw.find({}):
	Clients_DB.append(user) # On convertit l'objet mongoDB en objet list python 
                            # pour effectuer des operations dessus

notification_db = db['ClientsNotif'] # base de donnee contenant les notifications
admin_db_raw = db['Admin']
for admins in admin_db_raw.find({}):
    admin = admins

print('Connexion à la base de donnée effectuée !')
date = strftime("%Y-%m-%d %H:%M:%S", localtime())

#########

# Acquisition settings (door)

N_MESURE = 50
INCERTITUDE = 0.15

create_chrono_locket = False
REF_CHRONO_LOCKET = 0
REF_CHRONO = 0
create_chrono_reset_locket = False


# Constant for windows

reset_chrono = False
TIMEOUT_FENETRE = 50 #secondes
create_chrono_fenetre = False
REF_CHRONO_FENETRE = 0

# DETECTION PHASE #######

def reset_detection():
    compteur_mesure = 0 # donne un suivi du nombre de mesure stockées dans un schema
    acquerir = True # variable permettant de commencer l'acquisition d'un schema si valeur de voltage > 0
    creer_schema = False # variable indiquant si on peut stocker la valeur de voltage dans un tableau
    scheme_array = [] # creation du tableau qui va acceuillir le schema detecte
    utilisateur_identifie = "Unknown" # Par defaut, la personne est inconnue
    return compteur_mesure, acquerir, creer_schema, scheme_array, utilisateur_identifie

compteur_mesure, acquerir, creer_schema, scheme_array, utilisateur_identifie = reset_detection()
continuer = 1
print "demarrage de l'acqusition"
while continuer:

    ######################### PARTIE PORTE ##########################

   
    time.sleep(0.04)
    value0=ADin(AD_Clk, AD_CS, AD_Dat)
    value=conversion(value0)
    print 'voltage value : ',value 
    if value0 > 0 and acquerir: # active l'acquisition du schema
        creer_schema = True
        acquerir = False # on empeche d'en commencer un autre si l'ancien n'est pas cree
	# On prend une photo pour l'identification
	
    if creer_schema:
        scheme_array.append(value)
        compteur_mesure += 1

    if compteur_mesure == N_MESURE:  

	date = strftime("%Y-%m-%d %H:%M:%S", localtime())
	camera.capture('/home/pi/FORTHOUSE/v1.0/interface_web/public/CAM_PHOTO/PORTE_{0}.jpg'.format(date))
	# On arrete la creation du schema, on passe à la partie traitement de signal
	#pyplot.plot(scheme_array)
	#pyplot.show()
        ###### PARTIE TRAITEMENT DE SIGNAL #######
        
	for utilisateurs in Clients_DB:
            degre_similarite = comparer(utilisateurs['schema'], scheme_array, N_MESURE)
	    print 'degre de similitude lie a {0} : {1} '.format(utilisateurs['firstname'], degre_similarite) 
	    if degre_similarite > (1-INCERTITUDE): # si le degre de similarite est dans la fourchette estimee
                utilisateur_identifie = utilisateurs['firstname']
            degre_similarite_admin = comparer(admin['schema'], scheme_array, N_MESURE, 'admin')
            if degre_similarite_admin > (1-INCERTITUDE):
                utilisateur_identifie = admin['nom']

        ###### PARTIE NOTIFICATION ######
        
        if utilisateur_identifie == "Unknown": #Utilisateur inconnu => on envoie une notif dans la base de donnee
            
	    send_notif(notification_db, door_notification_unknown(), date)
        
	elif utilisateur_identifie == admin['nom']: #Admin detecte ! 
            
	    send_notif(notification_db, admin_notif, date)
            pwm.ChangeDutyCycle(5) # ouverture du moteur
	    create_chrono_locket = True #on demarre le chrono => reset du locket au bout de 30sec     
	    create_chrono_reset_locket = True # elimine le comportement parkinson en 2 sec
       
	else: # Utilisateur authentifie ! On ouvre le loquet !
            
	    send_notif(notification_db, door_notification_authentified(utilisateur_identifie), date)
            pwm.ChangeDutyCycle(5) # ouverture du moteur
	    create_chrono_locket = True #on demarre le chrono => reset du locket au bout de 30sec     
	    create_chrono_reset_locket = True # elimine le comportement parkinson en 2 sec

        # Reste a reset pour la dectetion du schema suivant 
        compteur_mesure, acquerir, creer_schema, scheme_array, utilisateur_identifie = reset_detection()


    ######################### FIN PARTIE PORTE ##########################
 
    ######################### PARTIE FENETRE ############################

    if GPIO.input(26):
	if create_chrono_fenetre:
		REF_CHRONO_FENETRE = pygame.time.get_ticks()
		send_notif(notification_db, windows_notification(), date)
      		print 'DETECTION AU NIVEAU DE LA FENETRE'
		create_chrono_fenetre = False    
    # on met la condition de detection independament de la detection sur le pin 26
    if (pygame.time.get_ticks()-REF_CHRONO_FENETRE)/1000 >= TIMEOUT_FENETRE:
    	create_chrono_fenetre = True
    
    ########################## FIN PARTIE FENETRE #######################


    ########################## GESTION DU LOCKET ########################

	
    if create_chrono_locket:
	REF_CHRONO_LOCKET = pygame.time.get_ticks()
	create_chrono_locket = False
		
    if (pygame.time.get_ticks()-REF_CHRONO_LOCKET)/1000 >= 30: #relock du locket au bout de 30 sec
	pwm.ChangeDutyCycle(10) #fermeture du locket		
        REF_CHRONO_LOCKET = pygame.time.get_ticks() # comme ca la duree n'existe pas
	create_chrono_reset_locket = True # au bout de 2 sec dutycycle a 0

    if create_chrono_reset_locket:	
	REF_CHRONO = pygame.time.get_ticks()
	create_chrono_reset_locket = False
    if (pygame.time.get_ticks()-REF_CHRONO)/1000 == 3:
	pwm.ChangeDutyCycle(0) #eviter parkinson sur le loquet
'

GPIO.Cleanup()


