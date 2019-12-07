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


class Bola(pygame.sprite.Sprite):
    def __init__(self, x, y, ancho, alto):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((ancho, alto))
        self.rect = self.image.get_rect()
        self.rect.left = x
        self.rect.top = y
        self.image.fill(White)
        self.movimiento = [3, -3]  # movimiento bola (x, y)
        self.name = 'ball'

    def crea(self):
        pantalla.blit(self.image, self.rect)

    def actualiza(self, cursor, ladrillos):
        self.rect = self.rect.move(self.movimiento)
        self.detecta(cursor, ladrillos)
        self.limites()

    def limites(self):
        if self.rect.left < 0 or self.rect.right > ANCHO_PANTALLA:  # paredes
            self.movimiento[0] *= -1

        if self.rect.top < 0:  # techo
            self.movimiento[1] *= -1

    def detecta(self, cursor, ladrillos):
        golpe = pygame.sprite.Group(cursor, ladrillos)
        lista = pygame.sprite.spritecollide(self, golpe, False)
        if len(lista) > 0:
            for sprite in lista:
                print(sprite)
                posicion = self.rect[0] - sprite.rect[0]
                """ni idea de como conseguir donde colisiona asi que calcula la x de la posicion del cursor 
                y la x de la posicion de la bola y las resto"""
                if sprite.name == 'paddle':
                    if posicion <= 80 / 5:
                        self.movimiento[0] = -4.5  # divido el cursor en 5 segmentos para rebote
                    elif posicion <= 80 / 5 * 2:
                        self.movimiento[0] = -3
                    elif posicion <= 80 / 5 * 3:
                        self.movimiento[0] = 0
                    elif posicion <= 80 / 5 * 4:
                        self.movimiento[0] = 3
                    else:
                        self.movimiento[0] = 4.5

            self.movimiento[1] *= -1


class Cursor(pygame.sprite.Sprite):
    def __init__(self, x, y, ancho, alto):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((ancho, alto))
        self.rect = self.image.get_rect()  # consigo las coordenadas del cursor
        self.rect.left = x
        self.rect.top = y
        self.image.fill(White)
        self.movimiento = [0, 0]  # movimiento cursor (x, y)
        self.name = 'paddle'

    def crea(self):
        pantalla.blit(self.image, self.rect)

    def actualiza(self, mousex):
        self.rect = self.rect.move(self.movimiento)
        if self.rect.x >= 0 and self.rect.right <= ANCHO_PANTALLA:
            self.rect.centerx = mousex
        self.limites()  # para evitar que el cursor se salga de la pantalla

    def limites(self):
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > ANCHO_PANTALLA:
            self.rect.right = ANCHO_PANTALLA


class Ladrillos(pygame.sprite.Sprite):
    def __init__(self, ancho, alto):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((ancho, alto))
        self.image.fill(White)
        self.rect = self.image.get_rect()
        self.name = 'bloque'

    def creaBloques(self):
        blocks = pygame.sprite.Group
        for fila in range(10):
            for columna in range(9):
                self.rect.x = 1 + columna * (60 + 7)  # ancho ladrillo + espacio
                self.rect.y = 1 + fila * (20 + 7)  # alto ladrillo + espacio
                if columna == 0 or columna % 2 == 0:
                    self.image.fill(Grey)
                else:
                    self.image.fill(Red)

                pantalla.blit(self.image, self.rect)


class Juego:
    def __init__(self):
        pygame.init()
        self.pantalla, self.rect = self.screen()
        self.mousex = 0

    def screen(self):
        pygame.display.set_caption('Arkanoid')
        rect = pantalla.get_rect()
        pantalla.convert()

        return pantalla, rect

    def bucle(self):
        game_over = False
        cursor = Cursor(ANCHO_PANTALLA / 2, ALTO_PANTALLA - ALTO_PANTALLA / 10, 80, 10)  # constructor del cursor
        bola = Bola(500, 500, 10, 10)  # constructor de la bola
        ladrillos = Ladrillos(60, 20)  # constructor de ladrillos
        while not game_over:
            for event in pygame.event.get():  # detecta clicks y teclas
                if event.type == pygame.QUIT:  # detecta solo cuando haces click en cerrar la ventana
                    game_over = True

                if event.type == MOUSEMOTION:  # movimiento del cursor por raton
                    self.mousex = event.pos[0]

            pantalla.fill(Black)

            ladrillos.creaBloques()

            bola.actualiza(cursor, ladrillos)
            bola.crea()

            cursor.actualiza(self.mousex)
            cursor.crea()

            pygame.display.update()

            clock.tick(60)  # para que vaya a 60 fps (PCMR)

        pygame.quit()
        quit()


if __name__ == '__main__':
    game = Juego()
    game.bucle()
