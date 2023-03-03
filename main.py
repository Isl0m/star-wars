import pygame
from random import randint

size = (400,650)
height = size[1]

# Background Image
window = pygame.display.set_mode(size)
bg = pygame.image.load('assets/bg.jpg')
bg = pygame.transform.scale(bg, size)

# Music
pygame.mixer.init()
pygame.mixer.music.load('assets/music.mp3')
pygame.mixer.music.play()
sound = pygame.mixer.Sound('assets/sound.mp3')

clock = pygame.time.Clock()

def load_image(image, size):
		return pygame.transform.scale(pygame.image.load(image), size)


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
			self.rect.y = 0

class Hero(GameSprite):
	def __init__(self, no_move_image, move_image, x, y, width, height, speed):
		super().__init__(no_move_image, x, y, width, height, speed)

		self.move_image = load_image(move_image, self.size)

	def move(self):
		keys = pygame.key.get_pressed()
		
		if keys[pygame.K_LEFT] and self.rect.x > -30:
			self.rect.x -= self.speed

		elif keys[pygame.K_RIGHT] and self.rect.x < 230:
			self.rect.x += self.speed

		elif keys[pygame.K_DOWN] and self.rect.y < 480:
			self.rect.y += self.speed

		elif keys[pygame.K_UP] and self.rect.y > -30:
			sound.play()
			self.image = self.move_image
			self.rect.y -= self.speed

		elif keys[pygame.K_ESCAPE]:
			exit()

		else:
			sound.stop()
			self.image = self.no_move_image

hero = Hero('assets/ship1.png','assets/ship2.png', 100, 450, 200, 200, 5)
enemies = pygame.sprite.Group()

for i in range(30):
	enemy = Enemy('assets/enemy.png', randint(0,7) * 50, -25, 50, 50, randint(2,3))
	enemies.add(enemy)

y1 = 0
y2 = -height

game = True
while game:
	y1 += 2
	y2 += 2
	i = 0
	
	window.blit(bg,(0,y1))
	window.blit(bg,(0,y2))

	if y1 > height:
		y1 = -height
	if y2 > height:
		y2 = -height

	hero.show()
	hero.move()

	enemies.draw(window)
	enemies.update()

	events = pygame.event.get()
	for event in events:
		if event.type == pygame.QUIT:
			game = False

	clock.tick(60)
	pygame.display.update()
