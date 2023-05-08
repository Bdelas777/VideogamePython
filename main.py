import pygame, random


# Definicion de  variables de la ventana
ANCHO = 800
LARGO= 600
NEGRO=(0,0,0)
marcador = 0
running = True


# Creacion del menu principal
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((ANCHO,LARGO))
pygame.display.set_caption("Space invaders remaster")
reloj = pygame.time.Clock()


def dibujaTexto(surface, text, size, x, y):
	font = pygame.font.SysFont("serif", size)
	text_surface = font.render(text, True, (255, 255, 255))
	text_rect = text_surface.get_rect()
	text_rect.midtop = (x, y)
	surface.blit(text_surface, text_rect)


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
    
    def disparo(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)

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
            
class Bullet(pygame.sprite.Sprite):
	def __init__(self, x, y):
		super().__init__()
		self.image = pygame.image.load("assets/laser1.png")
		self.image.set_colorkey(NEGRO)
		self.rect = self.image.get_rect()
		self.rect.y = y
		self.rect.centerx = x
		self.speedy = -10

	def update(self):
		self.rect.y += self.speedy
		if self.rect.bottom < 0:
			self.kill()


enemigoImagenes = []
enemigoLista = ["assets/meteorGrey_big1.png", "assets/meteorGrey_big2.png", "assets/meteorGrey_big3.png", "assets/meteorGrey_big4.png",
				"assets/meteorGrey_med1.png", "assets/meteorGrey_med2.png", "assets/meteorGrey_small1.png", "assets/meteorGrey_small2.png",
				"assets/meteorGrey_tiny1.png", "assets/meteorGrey_tiny2.png"]
for img in enemigoLista:
	enemigoImagenes.append(pygame.image.load(img).convert())
 
 # Cargar fondo.
background = pygame.image.load("assets/background.png").convert()
           
all_sprites = pygame.sprite.Group()
enemigoLista = pygame.sprite.Group()
bullets = pygame.sprite.Group()

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
		
		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_SPACE:
				jugador.disparo()
		

	# Update
	all_sprites.update()

	# Colisiones meteoro - laser
	hits = pygame.sprite.groupcollide(enemigoLista, bullets, True, True)
	for hit in hits:
		marcador += 1
		enemigo = Enemigo()
		all_sprites.add(enemigo)
		enemigoLista.add(enemigo)

		
	# Colisiones jugador - meteoro
	hits = pygame.sprite.spritecollide(jugador, enemigoLista, False)
	if hits:
		running = False

	#Draw / Render
	screen.blit(background, [0, 0])
	all_sprites.draw(screen)

	# Marcador
	dibujaTexto(screen, str(marcador), 25,ANCHO    // 2, 10)


	pygame.display.flip()

pygame.quit() 