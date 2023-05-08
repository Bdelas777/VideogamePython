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
        self.image = pygame.image.load("assets/player.png").convert()
        self.image.set_colorkey(NEGRO)
        self.rect = self.image.get_rect()
        self.rect.centerx = ANCHO // 2
        self.rect.bottom = LARGO - 10
        self.speed_x = 0
        
    def update(self):
        self.speed_x = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speed_x = -5
        if keystate[pygame.K_RIGHT]:
            self.speed_x = 5
        self.rect.x += self.speed_x
        if self.rect.right > ANCHO:
            self.rect.right = ANCHO
        if self.rect.left < 0:
            self.rect.left = 0

all_sprites = pygame.sprite.Group()

jugador = Jugador()

all_sprites.add(jugador)

# Correr todo el juego
while running:
    reloj.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
    all_sprites.update()
    screen.fill(NEGRO)
    all_sprites.draw(screen)
    pygame.display.flip()

pygame.quit()