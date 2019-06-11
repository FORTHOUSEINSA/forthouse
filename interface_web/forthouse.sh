#!/bin/bash

start="start"
stop="stop"
if [ "$1" == "$start" ]
then
        nodejs /home/pi/FORTHOUSE/v1.0/interface_web/menu.js &
	nodejs /home/pi/FORTHOUSE/v1.0/interface_web/database.js &
	nodejs /home/pi/FORTHOUSE/v1.0/interface_web/notification.js &
	nodejs /home/pi/FORTHOUSE/v1.0/interface_web/mon_compte.js &
	nodejs /home/pi/FORTHOUSE/v1.0/interface_web/about_us.js &

elif [ "$1" == "$stop" ] 
then
	echo '### ARRET DE TOUT LES SERVEURS ###'
        sudo killall nodejs
fi
