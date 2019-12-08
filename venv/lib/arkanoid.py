# TODO: vidas, menu, panel gameOver, hitbox de la pelota mejorable, texturas?

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

#audio
inicio = 'sound/inicio.wav'
sonCursor = 'sound/cursor.wav'
sonBloque = 'sound/block.wav'

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
        self.gameOver = False
        self.image = pygame.Surface((ancho, alto))
        self.rect = self.image.get_rect()
        self.rect.left = x
        self.rect.top = y
        self.image.fill(White)
        self.movimiento = [5, -5]  # movimiento bola (x, y)
        self.name = 'ball'
        self.start = False
        self.ladrillosRotos = 0

    def crea(self):
        pantalla.blit(self.image, self.rect)

    def actualiza(self, cursor, blocks, mousex):
        if self.start:
            self.rect = self.rect.move(self.movimiento)
            self.detecta(cursor, blocks)
            self.limites()
        else:
            self.rect.centerx = mousex

    def limites(self):
        if self.rect.left < 0 or self.rect.right > ANCHO_PANTALLA:  # paredes
            self.movimiento[0] *= -1

        if self.rect.top < 0:  # techo
            self.movimiento[1] *= -1

        if self.rect.top > ALTO_PANTALLA:  # suelo
            # self.gameOver = True
            self.movimiento[1] *= -1

    def detecta(self, cursor, blocks):
        golpea = pygame.sprite.Group(cursor, blocks)
        lista = pygame.sprite.spritecollide(self, golpea, False)
        if len(lista) > 0:
            for sprite in lista:
                posicion = self.rect.centerx - sprite.rect[0]
                """ni idea de como conseguir donde colisiona asi que calcula la x de la posicion del cursor 
                y la x de la posicion de la bola y las resto"""

                if sprite.name == 'paddle':
                    pygame.mixer.music.load(sonCursor)
                    pygame.mixer.music.play()

                    if posicion <= 80 / 4:
                        self.movimiento[0] = -4.5  # divido el cursor en 4 segmentos para rebote
                    elif posicion <= 80 / 4 * 2:
                        self.movimiento[0] = -3
                    elif posicion <= 80 / 4 * 3:
                        self.movimiento[0] = 3
                    else:
                        self.movimiento[0] = 4.5

                elif sprite.name == 'bloque':
                    pygame.mixer.music.load(sonBloque)
                    pygame.mixer.music.play()

                    sprite.kill()
                    # determino que ladrillo he golpeado
                    # print(int(sprite.rect.x / 60 - (0.11 * int(sprite.rect.x / 60)) + 1))

                    ladrilloGolpeado = int(sprite.rect.x / 60 - (0.11 * int(sprite.rect.x / 60)))

                    # determino el punto del ladrillo en el que ha golpeado la bola

                    inicioLadrillo = 2 + ladrilloGolpeado * 67
                    finalLadrillo = inicioLadrillo + 60
                    impacto = 60 - (finalLadrillo - self.rect.centerx)

                    if impacto <= 60 / 2:
                        self.movimiento[0] = -3  # divido los ladrillos en 2 segmentos
                    else:
                        self.movimiento[0] = 3

                    #print(60 - (finalLadrillo - self.rect.centerx))  # error de 5 maximo

                    self.ladrillosRotos += 1
                    if self.ladrillosRotos == 90:
                        self.gameOver = True

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
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((60, 20))
        self.image.fill(White)
        self.rect = self.image.get_rect()
        self.name = 'bloque'


class Puntuacion(object):
    def __init__(self):
        self.score = 0
        self.font = pygame.font.SysFont('Arial', 25)
        self.render = self.font.render('Score: ' + str(self.score), True, White, Black)
        self.rect = self.render.get_rect()
        self.rect.x = 0
        self.rect.bottom = ALTO_PANTALLA


class FPS(object):
    def __init__(self):
        self.fps = str(int(clock.get_fps()))
        self.font = pygame.font.SysFont('Arial', 25)
        self.render = self.font.render('FPS: ' + self.fps, True, White, Black)
        self.rect = self.render.get_rect()
        self.rect.x = 500
        self.rect.bottom = ALTO_PANTALLA


class Juego(object):
    def __init__(self):
        pygame.init()

        pygame.mixer.init()
        pygame.mixer.music.load(inicio)
        pygame.mixer.music.play()

        self.pantalla, self.rect = self.screen()
        self.mousex = 0
        self.blocks = self.creaBloques()
        self.bola = self.creaBola()
        self.cursor = self.creaCursor()
        self.puntuacion = Puntuacion()
        self.fps = FPS()
        self.todosLosSprites = pygame.sprite.Group(self.blocks, self.bola, self.cursor)

    def actualizaFPS(self):
        self.fps.fps = str(int(clock.get_fps()))
        self.fps.render = self.fps.font.render('FPS: ' + self.fps.fps, True, White, Black)
        self.fps.rect = self.fps.render.get_rect()
        self.fps.rect.x = 500
        self.fps.rect.bottom = ALTO_PANTALLA

    def actualizaPuntuacion(self):
        self.puntuacion.score = self.bola.ladrillosRotos
        self.puntuacion.render = self.puntuacion.font.render('Score: ' + str(self.puntuacion.score), True, White, Black)
        self.puntuacion.rect = self.puntuacion.render.get_rect()
        self.puntuacion.rect.x = 0
        self.puntuacion.rect.bottom = ALTO_PANTALLA

    def screen(self):
        pygame.display.set_caption('Arkanoid')
        rect = pantalla.get_rect()
        pantalla.convert()

        return pantalla, rect

    def creaBola(self):
        bola = Bola(ANCHO_PANTALLA / 2, 705, 10, 10)  # constructor de la bola
        return bola

    def creaCursor(self):
        cursor = Cursor(ANCHO_PANTALLA / 2, ALTO_PANTALLA - ALTO_PANTALLA / 10, 80, 10)  # constructor del cursor
        return cursor

    def creaBloques(self):
        blocks = pygame.sprite.Group()

        for fila in range(10):
            for columna in range(9):
                block = Ladrillos()
                block.rect.x = 2 + columna * (60 + 7)  # ancho ladrillo + espacio
                block.rect.y = 2 + fila * (20 + 7)  # alto ladrillo + espacio
                if columna == 0 or columna % 2 == 0:
                    block.image.fill(Grey)
                else:
                    block.image.fill(Red)
                blocks.add(block)
        return blocks

    def bucle(self):
        game_over = False
        while not game_over:
            for event in pygame.event.get():  # detecta clicks y teclas
                if event.type == pygame.QUIT:  # detecta solo cuando haces click en cerrar la ventana
                    game_over = True

                if event.type == MOUSEMOTION:  # movimiento del cursor por raton
                    self.mousex = event.pos[0]

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.bola.start = True

            pantalla.fill(Black)

            self.todosLosSprites.update(self.mousex, self.blocks, self.cursor)
            self.todosLosSprites.draw(self.pantalla)

            self.cursor.actualiza(self.mousex)

            self.bola.actualiza(self.cursor, self.blocks, self.mousex)

            pantalla.blit(self.puntuacion.render, self.puntuacion.rect)
            self.actualizaPuntuacion()

            pantalla.blit(self.fps.render, self.fps.rect)
            self.actualizaFPS()

            pygame.display.update()

            clock.tick(60)  # para que vaya a 60 fps (PCMR)

            if self.bola.gameOver:
                game_over = True

        pygame.quit()
        quit()


if __name__ == '__main__':
    game = Juego()
    game.bucle()

