from time import clock

import pygame
from pygame.locals import *
import time

clock = pygame.time.Clock()

# constantes
ANCHO_PANTALLA = 600
ALTO_PANTALLA = 800

# colores
White = (255, 255, 255)
Red = (169, 19, 38)
Black = (0, 0, 0)
Green = (8, 101, 55)
Silver = (192, 192, 192)
Gold = (255, 188, 0)
Grey = (100, 100, 100)
Yellow = (255, 255, 0)

x = ANCHO_PANTALLA / 2
y = 50
vX = 1
vY = 2


class Juego(object):
    def __init__(self):
        pygame.init()
        self.dimensiones, self.rect = self.pantalla()

    def pantalla(self):
        pygame.display.set_caption('Arkanoid')
        dimensiones = pygame.display.set_mode((ANCHO_PANTALLA, ALTO_PANTALLA))
        rect = dimensiones.get_rect()
        dimensiones.fill(Black)
        dimensiones.convert()

        return dimensiones, rect

    def bucle(self):
        game_over = False
        while not game_over:
            for event in pygame.event.get():  # detecta clicks y teclas
                if event.type == pygame.QUIT:  # detecta solo cuando haces click en cerrar la ventana
                    game_over = True

            pygame.display.update()
            clock.tick(60)

        pygame.quit()
        quit()


if __name__ == '__main__':
    game = Juego()
    game.bucle()
