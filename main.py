import os  # step 22
import random  # step 12

import pygame  # step 1

# screen related stuff
WIDTH = 500
HEIGHT = 600
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)  # step 6
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

# initialize pygame & display (step 2)
pygame.init()
pygame.mixer.init()  # step 28
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Game")  # step 6

# set delay (step 5)
clock = pygame.time.Clock()
fps = 60

# import images (step 22)
background_img = pygame.image.load(os.path.join("img", "background.png")).convert()
player_img = pygame.image.load(os.path.join("img", "player.png")).convert()
# rock_img = pygame.image.load(os.path.join("img", "rock.png")).convert()
bullet_img = pygame.image.load(os.path.join("img", "bullet.png")).convert()
# step 26
rock_imgs = []
for i in range(7):
	rock_imgs.append(pygame.image.load(os.path.join("img", f"rock{i}.png")).convert())
# step 27
font_name = pygame.font.match_font("arial")

# import sound (step 28)
shoot_sound = pygame.mixer.Sound(os.path.join("sound", "shoot.wav"))
expl_sounds = [
	pygame.mixer.Sound(os.path.join("sound", "expl0.wav")),
	pygame.mixer.Sound(os.path.join("sound", "expl1.wav"))
]
pygame.mixer.music.load(os.path.join("sound", "background.ogg"))
pygame.mixer.music.set_volume(0.4)


def draw_text(surf, text, size, x, y):
	font = pygame.font.Font(font_name, size)
	text_surface = font.render(text, True, WHITE)
	text_rect = text_surface.get_rect()
	text_rect.centerx = x
	text_rect.top = y
	surf.blit(text_surface, text_rect)


# sprite (step 7)
class Player(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		# self.image d= pygame.Surface((50, 40))  # a surface object with width, height
		# self.image.fill(GREEN)  # fill it with colour
		# self.image = player_img  # step 22
		self.image = pygame.transform.scale(player_img, (50, 38))  # step 22
		self.image.set_colorkey(BLACK)
		self.rect = self.image.get_rect()
		# step 23
		self.radius = 20
		# self.rect.center = (WIDTH/2, HEIGHT/2)  # step 10
		self.rect.centerx = WIDTH / 2
		self.rect.bottom = HEIGHT - 20
		self.speed = 8

	def update(self):  # step 9
		# check user input
		key_pressed = pygame.key.get_pressed()  # step 10
		if key_pressed[pygame.K_d]:
			self.rect.x += self.speed
		if key_pressed[pygame.K_a]:
			self.rect.x -= self.speed
		if key_pressed[pygame.K_w]:
			self.rect.y -= self.speed
		if key_pressed[pygame.K_s]:
			self.rect.y += self.speed

		# Border the screen (step 11)
		if self.rect.right > WIDTH:
			self.rect.right = WIDTH
		if self.rect.left < 0:
			self.rect.left = 0
		if self.rect.top < 0:
			self.rect.top = 0
		if self.rect.bottom > HEIGHT:
			self.rect.bottom = HEIGHT

	# self.rect.x += 2  # step 10
	# if self.rect.left > WIDTH:
	# 	self.rect.right = 0

	def shoot(self):  # step 18
		bullet = Bullet(self.rect.centerx, self.rect.top)
		all_sprite.add(bullet)
		bullets.add(bullet)  # 19
		shoot_sound.play()  # 28


class Rock(pygame.sprite.Sprite):  # step 12
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		# self.image = pygame.Surface((30, 40))  # a surface object with width, height
		# self.image.fill(RED)  # fill it with colour
		# step 22
		# self.image = rock_img
		# self.image.set_colorkey(BLACK)
		# step 26
		self.image_ori = random.choice(rock_imgs)
		# step 24
		# self.image_ori = rock_img
		self.image_ori.set_colorkey(BLACK)
		self.image = self.image_ori.copy()
		self.rect = self.image.get_rect()
		# step 23
		# self.radius = 25
		self.radius = self.rect.width * 0.85 / 2
		# step 15
		self.rect.x = random.randrange(0, WIDTH - self.rect.width)
		# self.rect.y = random.randrange(-100, 40)
		self.rect.y = random.randrange(-180, -100)  # step 26
		self.speedy = random.randrange(2, 10)
		self.speedx = random.randrange(-3, 3)
		# step 25
		self.rot_degree = random.randrange(-3, 3)
		# step 24
		# self.rot_degree = 5
		self.total_degree = 0

	# step 24
	def rotate(self):
		self.total_degree += self.rot_degree
		self.total_degree = self.total_degree % 360
		self.image = pygame.transform.rotate(self.image_ori, self.total_degree)
		# step 25
		center = self.rect.center
		self.rect = self.image.get_rect()
		self.rect.center = center

	def update(self):  # step 13
		self.rotate()  # step 24
		self.rect.y += self.speedy
		self.rect.x += self.speedx
		# check if the rock exit the border (step 15)
		if self.rect.top > HEIGHT or self.rect.left > WIDTH or self.rect.right < 0:
			self.rect.x = random.randrange(0, WIDTH - self.rect.width)
			self.rect.y = random.randrange(-100, 40)
			self.speedy = random.randrange(2, 10)
			self.speedx = random.randrange(-3, 3)


class Bullet(pygame.sprite.Sprite):  # step 16
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		# self.image = pygame.Surface((10, 20))  # a surface object with width, height
		# self.image.fill(YELLOW)  # fill it with colour
		self.image = bullet_img  # step 22
		self.image.set_colorkey(BLACK)
		self.rect = self.image.get_rect()
		self.rect.centerx = x
		self.rect.bottom = y
		self.speedy = -10

	def update(self):
		self.rect.y += self.speedy
		if self.rect.bottom < 0:
			self.kill()


# sprite group (step 8)
all_sprite = pygame.sprite.Group()
player = Player()
all_sprite.add(player)
# step 19
rocks = pygame.sprite.Group()
bullets = pygame.sprite.Group()
# rock = Rock()  # step 13
# all_sprite.add(rock)
for i in range(8):  # step 14
	r = Rock()
	all_sprite.add(r)
	rocks.add(r)  # 19
score = 0  # step 27
pygame.mixer.music.play(-1)  # 28

running = True

# game loop (step 3)
while running:
	# delay (step 5)
	clock.tick(fps)

	# process input (step 4)
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
		elif event.type == pygame.KEYDOWN:  # step 17
			if event.key == pygame.K_SPACE:
				player.shoot()

	# update game
	all_sprite.update()  # step 9
	# pygame.sprite.groupcollide(rocks, bullets, True, True)  # step 19
	hits = pygame.sprite.groupcollide(rocks, bullets, True, True)  # step 20
	for hit in hits:
		random.choice(expl_sounds).play()  # 28
		score += hit.radius  # step 27
		r = Rock()
		all_sprite.add(r)
		rocks.add(r)

	# step 21
	# hits = pygame.sprite.spritecollide(player, rocks, False)
	hits = pygame.sprite.spritecollide(player, rocks, False, pygame.sprite.collide_circle)  # step 23
	if hits:
		running = False

	# display output (render) (step 6)
	# screen.fill(WHITE)
	# step 18
	screen.fill(BLACK)
	screen.blit(background_img, (0, 0))
	all_sprite.draw(screen)
	# step 27
	# draw_text(screen, str(score), 18, WIDTH/2, 10)
	draw_text(screen, str(int(score)), 18, WIDTH / 2, 10)

	pygame.display.update()

pygame.quit()
