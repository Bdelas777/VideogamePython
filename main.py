import pygame, random


# Definicion de  variables de la ventana
ANCHO = 800
LARGO= 600
NEGRO=(0,0,0)
BLANCO = (255,255,255)


# Creacion del menu principal
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((ANCHO,LARGO))
pygame.display.set_caption("Space invaders remaster")
reloj = pygame.time.Clock()
running = True

class Jugador (pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("assets/player.png")
        self.image.set_colorkey("NEGRO")
        self.rect = self.rect.image.get_rect()
        self.rect.centerx = ANCHO // 2
        self.rect.bottom = LARGO - 10
        self.speed_x = 0
        
    def update(self):
        pass

all_sprites = pygame.sprite.Group()

jugador = Jugador()

all_sprites.add(jugador)


while running:
    reloj.tick(60)