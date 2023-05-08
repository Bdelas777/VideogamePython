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

class Enemigo(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("assets/meteorGrey_med1.png").convert()
        self.image.set_colorkey(NEGRO)
        self.rect = self.image.get_rect()
        self.rect.y = random.randrange(-100, -40)
        self.speedy = random.randrange(1, 10)
        self.speedx = random.randrange(-5, 5)
        
    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.top > LARGO+ 10 or self.rect.left < -25 or self.rect.right > ANCHO + 22 :
            self.rect.x = random.randrange(ANCHO - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 8)
 
 # Cargar fondo.
background = pygame.image.load("assets/background.png").convert()
           
all_sprites = pygame.sprite.Group()
enemigoLista = pygame.sprite.Group()

jugador = Jugador()

all_sprites.add(jugador)

# Correr todo el juego
for i in range(8):
	enemigo = Enemigo()
	all_sprites.add(enemigo)
	enemigoLista.add(enemigo)

# Game Loop
running = True
while running:
	# Keep loop running at the right speed
	reloj.tick(60)
	# Process input (events)
	for event in pygame.event.get():
		# check for closing window
		if event.type == pygame.QUIT:
			running = False
		
	# Update
	all_sprites.update()

	#Draw / Render
	screen.blit(background, [0, 0])
	all_sprites.draw(screen)
	# *after* drawing everything, flip the display.
	pygame.display.flip()

pygame.quit()