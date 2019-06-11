#coding:utf8
import smtplib
from socket import gaierror

def windows_notification():

    message = "Une personne s'est infiltrée par la fenêtre !"
    #envoyer_mail(message)
    return message

def door_notification_authentified(user):

    message = user + " a toque a la porte !" + " Ouverture de la porte !"

    return message

def door_notification_unknown():

    message = "Une personne non authentifiée a toqué à votre porte"

    return message

def admin_notif():

    message = 'Bienvenue monsieur ! Votre café a été préparé en votre absence !'
    return message


def envoyer_mail(message):

    src_mail = 'forthouse.insa@gmail.com'
    dest_mail = 'jbeziaud@gmail.com'
    login = 'forthouse.insa'
    password = 'forthouse'

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.ehlo()
    server.starttls() # start secured transaction
    server.sendmail(src_mail, dest_mail, message)
