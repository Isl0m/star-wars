import pygame
from random import randint

size = (400,650)
height = size[1]
hp_images_list = ['assets/hp/hp1.png','assets/hp/hp2.png','assets/hp/hp3.png','assets/hp/hp4.png','assets/hp/hp5.png','assets/hp/hp6.png','assets/hp/hp7.png','assets/hp/hp8.png','assets/hp/hp9.png','assets/hp/hp10.png','assets/hp/hp11.png']

window = pygame.display.set_mode(size)


def load_image(image, size):
		return pygame.transform.scale(pygame.image.load(image), size)

# Background Image
bg = load_image('assets/bg.jpg',size)

# HP Image
hp_image = load_image('assets/hp/hp1.png',(100,30))


# Music
pygame.mixer.init()
pygame.mixer.music.load('assets/music.mp3')
pygame.mixer.music.play()
sound = pygame.mixer.Sound('assets/sound.mp3')
blaster_sound = pygame.mixer.Sound('assets/blaster.mp3')

clock = pygame.time.Clock()


class GameSprite(pygame.sprite.Sprite):
	def __init__(self, no_move_image, x, y, width, height, speed):
			pygame.sprite.Sprite.__init__(self)

			self.size = (width,height)

			self.no_move_image = load_image(no_move_image, self.size)
			self.image = self.no_move_image

			self.rect = self.image.get_rect()
			self.rect.x = x
			self.rect.y = y

			self.speed = speed

	def show(self):
		window.blit(self.image, (self.rect.x,self.rect.y))

class Enemy(GameSprite):
	def update(self):
		self.rect.y += self.speed

		if self.rect.y > height:
			self.kill()

class Bullet(GameSprite):
	def update(self):
		self.rect.y -= self.speed

		if self.rect.y < 0:
			self.kill()

class Hero(GameSprite):
	def __init__(self, no_move_image, move_image, x, y, width, height, speed):
		super().__init__(no_move_image, x, y, width, height, speed)

		self.move_image = load_image(move_image, self.size)
		self.hp = 10

	def move(self):
		keys = pygame.key.get_pressed()
		
		if keys[pygame.K_LEFT] and self.rect.x > -10:
			self.rect.x -= self.speed

		elif keys[pygame.K_RIGHT] and self.rect.x < 350:
			self.rect.x += self.speed

		elif keys[pygame.K_DOWN] and self.rect.y < 500:
			self.rect.y += self.speed

		elif keys[pygame.K_UP] and self.rect.y > -10:
			sound.play()
			self.image = self.move_image
			self.rect.y -= self.speed

		else:
			sound.stop()
			self.image = self.no_move_image
		
	def fire(self):
		blaster_sound.play()
		
		bullet = Bullet('assets/laser.png',hero.rect.centerx - 15,hero.rect.y - 70, 25, 100, 15)
		bullet_left = Bullet('assets/laser1.png',hero.rect.centerx - 45,hero.rect.y - 5, 25, 70, 15)
		bullet_right = Bullet('assets/laser1.png',hero.rect.centerx + 15,hero.rect.y - 5, 25, 70, 15)
		
		bullets.add(bullet)
		bullets.add(bullet_left)
		bullets.add(bullet_right)


hero = Hero('assets/ship1.png','assets/ship2.png', 125, 500, 150, 150, 5)
enemies = pygame.sprite.Group()
bullets = pygame.sprite.Group()

y1 = 0
y2 = -height
i = 0

game = True

while game:
	y1 += 2
	y2 += 2
	
	window.blit(bg,(0,y1))
	window.blit(bg,(0,y2))

	if y1 > height:
		y1 = -height
	if y2 > height:
		y2 = -height

	hero.show()
	hero.move()

	bullets.draw(window)
	bullets.update()

	enemies.draw(window)
	enemies.update()

	window.blit(hp_image,(5,10))


	if i == 0:
		i = 18
		enemy = Enemy('assets/enemy.png', randint(0,7) * 100, -50, 100, 100, randint(2,3))
		enemies.add(enemy)
	else:
		i -= 1

	events = pygame.event.get()
	for event in events:
		if event.type == pygame.QUIT:
			game = False
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_SPACE:
				hero.fire()
			if event.key == pygame.K_ESCAPE:
				exit()
		if event.type == pygame.MOUSEBUTTONDOWN and event.button == pygame.BUTTON_LEFT:
			hero.fire()

	collides = pygame.sprite.groupcollide(bullets,enemies, True, True)
	if pygame.sprite.spritecollide(hero, enemies, True):
		if hero.hp == 0:
			hero.hp = 10
		else:
			hero.hp -= 1 

		hp_image = load_image(hp_images_list[10 - hero.hp],(100,30))

	clock.tick(60)
	pygame.display.update()
