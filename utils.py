import pygame
from random import randint
from math import sin, cos, atan2, degrees, pi
from time import time

# Constants
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 650
SCREEN_SIZE = (400,650)

SCORE = 0
FPS = 30

# Image source lists
hp_images_list = [f'assets/hp/hp{n}.png' for n in range(1,12)]
exp_image_list = [f'assets/exp/exp0{n}.png' for n in range(9)]

# Init Functions
pygame.display.set_caption('Star Wars')
window = pygame.display.set_mode(SCREEN_SIZE)
clock = pygame.time.Clock()

# Font
pygame.font.init()
font = pygame.font.Font('assets/Heavy Data Nerd Font Complete.ttf', 24)
health = font.render("Health:", True, (255, 255, 255))
score = font.render(f"Score: {SCORE}",False, (255, 255, 255))
reload_text = font.render("Reloading...",False, (255, 255, 255))
you_win_text = font.render("You Win!!!",False, (255, 255, 255))
you_lose_text = font.render("You Lose",False, (255, 255, 255))
range_mode_text = font.render("Range Mode!!!", False, (255, 0, 0))

# Functions
def load_image(image, size):
		return pygame.transform.scale(pygame.image.load(image), size)
def calc_text_pos(size, offset_y = 0) :
	x = (SCREEN_WIDTH / 2) - (size[0] / 2)
	y = SCREEN_HEIGHT / 2 + offset_y
	return (x, y)
def inc_score():
	global score, SCORE
	SCORE += 1
	score = font.render(f"Score: {SCORE}",False, (255, 255, 255))
def show_explosion(c):
	exp_sound.play()
	e = 0
	for i in range(9):
		if e == 0:
			e = 50
			c.image = load_image(exp_image_list[i],(100,100))
			window.blit(c.image, (c.rect.x , c.rect.y))
		else:
			e -= 1
def you_win():
	window.fill('black')
	window.blit(you_win_text, calc_text_pos(you_win_text.get_size()))
	window.blit(score, calc_text_pos(score.get_size(), 30))
def you_lose():
	window.fill('black')
	window.blit(you_lose_text, calc_text_pos(you_lose_text.get_size()))
	window.blit(score, calc_text_pos(score.get_size(), 30))


# Loading Base Images
bg = load_image('assets/bg.jpg',SCREEN_SIZE)
hp_image = load_image('assets/hp/hp1.png',(100,30))


# Music
pygame.mixer.init()
pygame.mixer.music.load('assets/music.mp3')
pygame.mixer.music.play()

sound = pygame.mixer.Sound('assets/sound.mp3')
blaster_sound = pygame.mixer.Sound('assets/blaster.mp3')
exp_sound = pygame.mixer.Sound('assets/explosion.mp3')


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

class Bullet(GameSprite):
	def update(self):
		self.rect.y -= self.speed

		if self.rect.y < 0:
			self.kill()

class ReflectionBullet(GameSprite):
	def __init__(self, sign, *args):
		super().__init__(*args)
		self.sign = sign
		self.angle = 120
	def update(self):
		self.rect.y -= self.speed * sin(self.angle)
		self.rect.x += (self.speed * cos(self.angle)) * self.sign

		if self.rect.y <= 0:
			self.kill()

class DownBullet(GameSprite):
	def __init__(self, no_move_image, x, y, width, height, speed, target_x, target_y):
		super().__init__(no_move_image, x, y, width, height, speed)
		angle = atan2(target_y - y, target_x - x)
		self.target_x = cos(angle) * self.speed
		self.target_y = sin(angle) * self.speed

	def update(self):
		self.rect.y += self.target_y
		self.rect.x += self.target_x

		if self.rect.y > SCREEN_HEIGHT:
			self.kill()

	def calc_angle(self, x, y, target_x, target_y):
		dy = target_y - y
		dx = target_x - x

		rad = atan2(-dy, dx)
		rad = rad % (2*pi)

		angle = degrees(rad)

		return angle 
	
class Player(GameSprite):
	def __init__(self, no_move_image, move_image, x, y, width, height, speed):
		super().__init__(no_move_image, x, y, width, height, speed)

		self.move_image = load_image(move_image, self.size)
		self.hp = 10
		self.fire_number = 0
		self.is_reload_fire = False
		self.is_range_mode = False

	def move(self):
		keys = pygame.key.get_pressed()
		
		is_left = keys[pygame.K_LEFT] or keys[pygame.K_a]
		is_right = keys[pygame.K_RIGHT] or keys[pygame.K_d]
		is_up = keys[pygame.K_UP] or keys[pygame.K_w]
		is_down = keys[pygame.K_DOWN] or keys[pygame.K_s]

		if is_left and self.rect.x > -10:
			self.rect.x -= self.speed

		elif is_right and self.rect.x < 350:
			self.rect.x += self.speed

		elif is_down and self.rect.y < 500:
			self.rect.y += self.speed

		elif is_up and self.rect.y > -10:
			sound.play()
			self.image = self.move_image
			self.rect.y -= self.speed

		else:
			sound.stop()
			self.image = self.no_move_image
		
	def fire(self):
		self.fire_number += 1
		blaster_sound.play()
		
		bullet = Bullet('assets/laser.png',player.rect.centerx - 15,player.rect.y - 70, 25, 100, 15)
		bullet_left = ReflectionBullet(-1,'assets/laser1.png',player.rect.centerx - 75,player.rect.y - 5, 25, 70, 15)
		bullet_right = ReflectionBullet(1,'assets/laser1.png',player.rect.centerx + 15,player.rect.y - 5, 25, 70, 15)
		

		bullets.add(bullet)
		reflection_bullets.add(bullet_left,bullet_right)

		bullet_left.image = pygame.transform.rotate(bullet_left.image, 30)
		bullet_right.image = pygame.transform.rotate(bullet_right.image, -30)

		if self.is_range_mode:
			self.range_mode()

	def range_mode(self):
		self.is_reload_fire = False
		range_bullet1 = Bullet('assets/laser.png',player.rect.centerx,player.rect.y - 70, 25, 100, 15)
		range_bullet2 = Bullet('assets/laser.png',player.rect.centerx - 30,player.rect.y - 70, 25, 100, 15)
		range_bullet_left = ReflectionBullet(-1,'assets/laser1.png',player.rect.centerx - 90,player.rect.y - 5, 25, 70, 15)
		range_bullet_right = ReflectionBullet(1,'assets/laser1.png',player.rect.centerx,player.rect.y - 5, 25, 70, 15)

		bullets.add(range_bullet1,range_bullet2)
		reflection_bullets.add(range_bullet_left, range_bullet_right)

		range_bullet_left.image = pygame.transform.rotate(range_bullet_left.image, 30)
		range_bullet_right.image = pygame.transform.rotate(range_bullet_right.image, -30)
		

class Enemy(GameSprite):
	def update(self):
		self.rect.y += self.speed

		if self.rect.y > SCREEN_HEIGHT:
			self.kill()
	def fire(self):
		bullet = DownBullet('assets/enemy_laser.png', self.rect.centerx - 10, self.rect.y + 50, 20, 20, 18,  Game.player.rect.centerx + 20, Game.player.rect.centery)
		Game.enemy_bullets.add(bullet)

		# angle = bullet.calc_angle(bullet.rect.x, bullet.rect.y, player.rect.centerx + 20, player.rect.centery)
		# bullet.image = pygame.transform.rotate(bullet.image, -angle)


class Game():
	def __init__(self):
		self.player = Player('assets/ship1.png','assets/ship2.png', 125, 500, 150, 150, 10)
		self.enemies = pygame.sprite.Group()
		self.reflection_bullets = pygame.sprite.Group()
		self.bullets = pygame.sprite.Group()
		self.enemy_bullets = pygame.sprite.Group()

		self.secondary_sprites = [self.enemies, self.enemy_bullets, self.bullets, self.reflection_bullets]

		self.y1 = 0
		self.y2 = -SCREEN_HEIGHT
		self.i,self.j = 0,0

		self.game = True
		self.is_finish = False
		self.events = pygame.event.get()
		
	def main(self):
		if not self.is_finish:
			self.run()

	def run(self):
		self.bg_init()

		self.player.show()
		self.player.move()

		if self.player.is_range_mode:
			window.blit(range_mode_text, calc_text_pos(range_mode_text.get_size()))
	
		self.secondary_sprite_init()

		window.blit(hp_image,(5,15))
		window.blit(health, (10, 0))
		window.blit(score, (SCREEN_WIDTH - 120, 0))

		self.enemies_init()

		for event in self.events:
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE:
					if self.player.fire_number < 10 and not self.player.is_reload_fire:
						self.player.fire()
					if self.player.fire_number >= 10:
						start_time = time()
						self.player.is_reload_fire = True
			if event.type == pygame.MOUSEBUTTONDOWN:
				self.player.fire()

		if self.player.is_reload_fire:
			period = time() - start_time
			if period >= 3:
				self.player.is_reload_fire = False
				self.player.fire_number = 0
			else:
				window.blit(reload_text, calc_text_pos(reload_text.get_size()))
		
		
		self.player_bullets_enemy_collide()
		
		self.bullets_collide()

		self.player_gets_damage()

	def bg_init(self): 
		self.y1 += 2
		self.y2 += 2
		
		window.blit(bg,(0,self.y1))
		window.blit(bg,(0,self.y2))

		if self.y1 > SCREEN_HEIGHT:
			self.y1 = -SCREEN_HEIGHT
		if self.y2 > SCREEN_HEIGHT:
			self.y2 = -SCREEN_HEIGHT

	def secondary_sprite_init(self):
		for bullet in self.reflection_bullets:
			if bullet.rect.x >= SCREEN_WIDTH - 70:
				bullet.sign = -1
				bullet.image = pygame.transform.rotate(bullet.image, 90)


			if bullet.rect.x <= 0:
				bullet.sign = 1
				bullet.image = pygame.transform.rotate(bullet.image, -90)


		for sprite in self.secondary_sprites:
			sprite.draw(window)
			sprite.update()

	def enemies_init(self):
		# Generate Enemies
		i = self.i
		j = self.j
		if i == 0:
			i = 15
			enemy = Enemy('assets/enemy.png', randint(0,3) * 100, -50, 100, 100, randint(5,6))
			enemy.fire()
			self.enemies.add(enemy)
		else:
			i -= 1

		# Make enemies fire
		if j == 0:
			for e in self.enemies:
				j = 60
				e.fire()
		else:
			j -= 1

	def player_bullets_enemy_collide(self):
		r_collides = pygame.sprite.groupcollide(self.reflection_bullets,self.enemies, True, True)
		for c in r_collides:
			inc_score()
			show_explosion(c)

		collides = pygame.sprite.groupcollide(self.bullets,self.enemies, True, True)
		for c in collides:
			inc_score()
			show_explosion(c)

	def bullets_collide(self):
		pygame.sprite.groupcollide(self.reflection_bullets, self.enemy_bullets, True, True)
		pygame.sprite.groupcollide(self.bullets, self.enemy_bullets, True, True)

	def player_gets_damage(self):
		player = self.player
		if pygame.sprite.spritecollide(player, self.enemies, True) or pygame.sprite.spritecollide(player, self.enemy_bullets, True):
			exp_sound.play()
			e = 0
			for i in range(9):
				if e == 0:
					e = 50
					self.enemy_bullets.image = load_image(exp_image_list[i],(100,100))
					window.blit(self.enemy_bullets.image, (player.rect.x + 30, player.rect.y))
				else:
					e -= 1

			player.hp -= 1 
			hp_image = load_image(hp_images_list[10 - player.hp],(100,30))
