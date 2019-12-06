from time import clock
import pygame
from pygame.locals import *
import time

clock = pygame.time.Clock()

# constantes
ANCHO_PANTALLA = 600
ALTO_PANTALLA = 800

# dimensiones de la pantalla
pantalla = pygame.display.set_mode((ANCHO_PANTALLA, ALTO_PANTALLA))

# colores
White = (255, 255, 255)
Red = (169, 19, 38)
Black = (0, 0, 0)
Green = (8, 101, 55)
Silver = (192, 192, 192)
Gold = (255, 188, 0)
Grey = (100, 100, 100)
Yellow = (255, 255, 0)


class Cursor:
    def __init__(self, x, y, ancho, alto):
        self.image = pygame.Surface((ancho, alto), SRCALPHA, 32)
        self.rect = self.image.get_rect()  # consigo las coordenadas del cursor
        self.rect.left = x
        self.rect.top = y
        self.image.fill(White)
        self.movimiento = [0, 0]  # movimiento cursor (x, y)
        self.velocidad = 8

    def crea(self):
        pantalla.blit(self.image, self.rect)

    def actualiza(self):
        self.rect = self.rect.move(self.movimiento)
        self.limites()  # para evitar que el cursor se salga de la pantalla

    def limites(self):
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > ANCHO_PANTALLA:
            self.rect.right = ANCHO_PANTALLA


class Juego:
    def __init__(self):
        pygame.init()
        self.pantalla, self.rect = self.screen()

    def screen(self):
        pygame.display.set_caption('Arkanoid')
        rect = pantalla.get_rect()
        pantalla.convert()

        return pantalla, rect

    def bucle(self):
        game_over = False
        cursor = Cursor(ANCHO_PANTALLA / 2, ALTO_PANTALLA - ALTO_PANTALLA / 10, 80, 10)  # constructor del cursor
        while not game_over:
            for event in pygame.event.get():  # detecta clicks y teclas
                if event.type == pygame.QUIT:  # detecta solo cuando haces click en cerrar la ventana
                    game_over = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:  # detecta flechas para movimiento (<- && ->)
                        cursor.movimiento[0] = cursor.velocidad * -1
                    if event.key == pygame.K_RIGHT:
                        cursor.movimiento[0] = cursor.velocidad
                if event.type == pygame.KEYUP:  # deja de moverse cuando retiras el dedo del cursor
                    if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                        cursor.movimiento[0] = 0

            pantalla.fill(Black)

            cursor.actualiza()
            cursor.crea()

            pygame.display.update()
            clock.tick(60)  # para que vaya a 60 fps (PCMR)

        pygame.quit()
        quit()


if __name__ == '__main__':
    game = Juego()
    game.bucle()
