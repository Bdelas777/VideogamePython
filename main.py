'''
Este videojuego se ejecuta desde el main
'''


import pygame, random

# Proporcion de la ventana
ANCHO = 800
ALTO = 600


# Guia de colores a utilizar
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
VERDE = (0, 255, 0)

#Inicializacion del juego
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Space Invaders Remaster")
clock = pygame.time.Clock()

# Funcion para dibujar el texto
def dibujaTexto(surface, text, size, x, y):
	font = pygame.font.SysFont("serif", size)
	text_surface = font.render(text, True, (255, 255, 255))
	text_rect = text_surface.get_rect()
	text_rect.midtop = (x, y)
	surface.blit(text_surface, text_rect)


# Funcion para dibujar el escudo
def dibujaEscudo(surface, x, y, percentage):
	BARRA_LARGO= 100
	BARRA_ALTO = 10
	fill = (percentage / 100) * BARRA_LARGO
	border = pygame.Rect(x, y, BARRA_LARGO, BARRA_ALTO)
	fill = pygame.Rect(x, y, fill, BARRA_ALTO)
	pygame.draw.rect(surface, VERDE, fill)
	pygame.draw.rect(surface, BLANCO, border, 2)


# Clase de diseño de jugador
class Jugador(pygame.sprite.Sprite):
	def __init__(self):
		super().__init__()
		self.image = pygame.image.load("assets/player.png").convert()
		self.image.set_colorkey(NEGRO)
		self.rect = self.image.get_rect()
		self.rect.centerx = ANCHO // 2
		self.rect.bottom = ALTO - 10
		self.speed_x = 0
		self.escudo = 100

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

		#Agregamos sonido
		sonidoLaser.play()

# Clase de creacion de enemigo
class Enemigo(pygame.sprite.Sprite):
	def __init__(self):
		super().__init__()
		self.image = random.choice(enemigoImagenes)
		self.image.set_colorkey(NEGRO)
		self.rect = self.image.get_rect()
		self.rect.x = random.randrange(ANCHO - self.rect.width)
		self.rect.y = random.randrange(-100, -40)
		self.speedy = random.randrange(1, 10)
		self.speedx = random.randrange(-5, 5)

	def update(self):
		self.rect.x += self.speedx
		self.rect.y += self.speedy
		if self.rect.top > ALTO + 10 or self.rect.left < -25 or self.rect.right > ANCHO + 22 :
			self.rect.x = random.randrange(ANCHO - self.rect.width)

			#Cambio de variables
			self.rect.y = random.randrange(-150, -100)
			self.speedy = random.randrange(1, 8)

# Clase para crear el laser
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

# Clase que crea las explosiones
class Explosion(pygame.sprite.Sprite):
	def __init__(self, center):
		super().__init__()
		self.image = explosion_anim[0]
		self.rect = self.image.get_rect()
		self.rect.center = center
		self.frame = 0
		self.last_update = pygame.time.get_ticks()
		self.frame_rate = 50 # Cuanto esperar para la siguiente explosion

	def update(self):
		now = pygame.time.get_ticks()
		if now - self.last_update > self.frame_rate:
			self.last_update = now
			self.frame += 1
			if self.frame == len(explosion_anim):
				self.kill() 
			else:
				center = self.rect.center
				self.image = explosion_anim[self.frame]
				self.rect = self.image.get_rect()
				self.rect.center = center


def MuestraMenu():
	screen.blit(background, [0, 0])
	dibujaTexto(screen, "Space Invaders Remaster", 65, ANCHO // 2, ALTO / 4)
	dibujaTexto(screen, "Para moverse pulse la teclas y el espaciador para disparar", 27, ANCHO // 2, ALTO // 2)
	dibujaTexto(screen, "Presiona una tecla para comenzar", 17, ANCHO // 2, ALTO * 3/4)
	pygame.display.flip()
	waiting = True
	while waiting:
		clock.tick(60)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
			if event.type == pygame.KEYUP:
				waiting = False


# Listas de imagenes
enemigoImagenes = []
enemigoLista = ["assets/meteorGrey_big1.png", "assets/meteorGrey_big2.png", "assets/meteorGrey_big3.png", "assets/meteorGrey_big4.png",
				"assets/meteorGrey_med1.png", "assets/meteorGrey_med2.png", "assets/meteorGrey_small1.png", "assets/meteorGrey_small2.png",
				"assets/meteorGrey_tiny1.png", "assets/meteorGrey_tiny2.png"]
for img in enemigoLista:
	enemigoImagenes.append(pygame.image.load(img).convert())

## --------------- CARGAR IMAGENES EXPLOSIÓN -------------------------- ##
explosion_anim = []
for i in range(9):
	file = "assets/regularExplosion0{}.png".format(i)
	img = pygame.image.load(file).convert()
	img.set_colorkey(NEGRO)
	img_scale = pygame.transform.scale(img, (70, 70))
	explosion_anim.append(img_scale)


# Cargar fondo.
background = pygame.image.load("assets/background.png").convert()

# Cargar sonidos
sonidoLaser = pygame.mixer.Sound("assets/laser5.ogg")
explosion_sound = pygame.mixer.Sound("assets/explosion.wav")
pygame.mixer.music.load("assets/music.ogg")
pygame.mixer.music.set_volume(0.1)


#pygame.mixer.music.play(loops=-1)

# Game Loop
game_over = True
corriendo = True
while corriendo:
	if game_over:
		MuestraMenu()
		game_over = False
		all_sprites = pygame.sprite.Group()
		enemigoLista = pygame.sprite.Group()
		bullets = pygame.sprite.Group()

		jugador = Jugador()
		all_sprites.add(jugador)

		for i in range(8):
			enemigo = Enemigo()
			all_sprites.add(enemigo)
			enemigoLista.add(enemigo)

		#Marcador / narcador
		narcador = 0
	# Keep loop corriendo at the right speed
	clock.tick(60)
	# Process input (events)
	for event in pygame.event.get():
		# check for closing window
		if event.type == pygame.QUIT:
			corriendo = False
		
		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_SPACE:
				jugador.disparo()
		

	# Update
	all_sprites.update()

	# Colisiones enemigo - laser
	hits = pygame.sprite.groupcollide(enemigoLista, bullets, True, True)
	for hit in hits:
		narcador += 1
		#explosion_sound.play()
		explosion = Explosion(hit.rect.center)
		all_sprites.add(explosion)

		enemigo = Enemigo()
		all_sprites.add(enemigo)
		enemigoLista.add(enemigo)

		
	# Colisiones jugador - enemigoo


	################## CHANGES HERE ################################
	hits = pygame.sprite.spritecollide(jugador, enemigoLista, True) # Change here
	for hit in hits:
		jugador.escudo -= 25
		enemigo = Enemigo()
		all_sprites.add(enemigo)
		enemigoLista.add(enemigo)
		if jugador.escudo <= 0 :
			#corriendo = False
			game_over = True

	#Draw / Render
	screen.blit(background, [0, 0])
	all_sprites.draw(screen)

	# Marcador
	dibujaTexto(screen, str(narcador), 25, ANCHO // 2, 10)

	# ESCUDO.
	dibujaEscudo(screen, 5, 5, jugador.escudo)


	pygame.display.flip()

pygame.quit()