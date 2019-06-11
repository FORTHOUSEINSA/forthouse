#coding=utf-8
import pygame
from pygame.locals import*
 
pygame.init()
  
#affichage de la fenêtre
fen = pygame.display.set_mode((640, 480))
pygame.display.set_caption("Chrono")
fpsClock = pygame.time.Clock()

BACKGROUND = pygame.image.load('../interface_web/public/IMG/logo_fort_house.jpg')
BACKGROUND = pygame.transform.scale(BACKGROUND, (640,480))

def temps():
    seconds = (pygame.time.get_ticks() - TpsZero) / 1000
    return seconds
TEXT_FONT = pygame.font.SysFont('monospace', 26)
NOIR = (0,0,0)
BLANC = (255,255,255)
     
continuer = True
trigger = True
while continuer:
    if trigger:
	TpsZero = pygame.time.get_ticks() # DEPART
	trigger = False
    for evenement in pygame.event.get():
        if evenement.type == QUIT:
            continuer = False
        if evenement.type == KEYDOWN:
            if evenement.key == K_ESCAPE:
                continuer = False
   
    fen.blit(BACKGROUND, (0,0))
    current_time = temps()
    MESSAGE = "demarrage de l'acquisition dans : " + str(3-current_time)             
    if current_time < 4:
	fen.blit(TEXT_FONT.render(MESSAGE, 1, BLANC), (20, 480-50))

    if current_time<11 and current_time > 3:
	MESSAGE = "fin de l'acquisition dans : " + str(10-current_time)	
     	fen.blit(TEXT_FONT.render(MESSAGE, 1 , BLANC), (20, 480-50))

    pygame.display.flip()
    fpsClock.tick(60)
 
pygame.quit()
