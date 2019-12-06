import pygame
from pygame.locals import *

#constantes
ANCHO_PANTALLA = 600
ALTO_PANTALLA = 800

pygame.display.init()
pygame.display.set_mode((ANCHO_PANTALLA, ALTO_PANTALLA))
pygame.display.set_caption("Arkanoid")

def pantalla():
    print("Hola")

while True:
    pantalla()

pygame.quit()