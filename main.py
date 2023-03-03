import pygame

size = (400,650)

window = pygame.display.set_mode(size)
bg = pygame.image.load('assets/back.jpg')
bg = pygame.transform.scale(bg, size)

clock = pygame.time.Clock()

class GameSprite(pygame.sprite.Sprite):
	def __init__(self, player_image, x, y, width, height, speed):
			pygame.sprite.Sprite.__init__(self)
			self.player_image =  pygame.transform.scale(pygame.image.load(player_image), (width, height))
			self.rect = self.player_image.get_rect()
			self.rect.x = x
			self.rect.y = y
			self.speed = speed

	def show(self):
		window.blit(self.player_image, (self.rect.x,self.rect.y))

class Hero(GameSprite):
	def move(self):
		keys = pygame.key.get_pressed()
		# print('x:',self.rect.x,'y:',self.rect.y)
		if keys[pygame.K_LEFT] and self.rect.x > -70:
			self.rect.x -= self.speed
		if keys[pygame.K_RIGHT] and self.rect.x < 265:
			self.rect.x += self.speed
		if keys[pygame.K_DOWN] and self.rect.y < 500:
			self.rect.y += self.speed
		if keys[pygame.K_UP] and self.rect.y > -50:
			self.rect.y -= self.speed

# player = GameSprite('assets/ship1.png', 100, 100, 100, 100, 5)
hero = Hero('assets/ship1.png', 0, 0, 200, 200, 5)

game = True
while game:
	window.blit(bg,(0,0))

	hero.show()
	hero.move()

	events = pygame.event.get()
	for event in events:
		if event.type == pygame.QUIT:
			game = False

	clock.tick(60)
	pygame.display.update()
