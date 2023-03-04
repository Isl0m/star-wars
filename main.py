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

IS_FINISH = False
IS_STOP = True


# Image source lists
hp_images_list = [f'assets/hp/hp{n}.png' for n in range(1,12)]
exp_image_list = [f'assets/exp/exp0{n}.png' for n in range(9)]

# Init Functions
pygame.display.set_caption('Star Wars')
window = pygame.display.set_mode(SCREEN_SIZE)
clock = pygame.time.Clock()

# Font
pygame.font.init()
h1 = pygame.font.Font('assets/Heavy Data Nerd Font Complete.ttf', 24)
h2 = pygame.font.Font('assets/Heavy Data Nerd Font Complete.ttf', 18)

health = h1.render("Health:", True, (255, 255, 255))
score = h1.render(f"Score: {SCORE}",True, (255, 255, 255))
reload_text = h1.render("Reloading...",True, (255, 255, 255))
you_win_text = h1.render("You Win!!!",True, (255, 255, 0))
you_lose_text = h1.render("You Lose",True, (255, 0, 0))
range_mode_text = h1.render("Range Mode!!!", True, (255, 0, 0))
play_again_text = h2.render("Press r to play again", True, (255, 255, 255))
press_to_continue_text = h2.render("Press Esc to play", True, (255, 255, 255))


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
	score = h1.render(f"Score: {SCORE}",False, (255, 255, 255))
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
def show_key_hint():
	window.blit(play_again_text, calc_text_pos(play_again_text.get_size(), 60))
def create_end_game_state(text):
	text_size = text.get_size()
	score_size = score.get_size()
	def end_state():
		window.fill('black')
		window.blit(text, calc_text_pos(text_size))
		window.blit(score, calc_text_pos(score_size, 30))
		show_key_hint()
	return end_state

you_win = create_end_game_state(you_win_text)
you_lose = create_end_game_state(you_lose_text)


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
all_sounds = [sound,blaster_sound,exp_sound]

def stop_sounds():
	for sound in all_sounds:
		sound.stop()
	pygame.mixer.music.stop()

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
		bullet = DownBullet('assets/enemy_laser.png', self.rect.centerx - 10, self.rect.y + 50, 20, 20, 18,  player.rect.centerx + 20, player.rect.centery)
		enemy_bullets.add(bullet)

		# angle = bullet.calc_angle(bullet.rect.x, bullet.rect.y, player.rect.centerx + 20, player.rect.centery)
		# bullet.image = pygame.transform.rotate(bullet.image, -angle)


player = Player('assets/ship1.png','assets/ship2.png', 125, 500, 150, 150, 10)
enemies = pygame.sprite.Group()
reflection_bullets = pygame.sprite.Group()
bullets = pygame.sprite.Group()
enemy_bullets = pygame.sprite.Group()

secondary_sprites = [enemies, enemy_bullets, bullets, reflection_bullets]

y1 = 0
y2 = -SCREEN_HEIGHT
i,j = 0,0

game = True

while game:
	events = pygame.event.get()

	if not IS_FINISH and not IS_STOP:
		y1 += 2
		y2 += 2
		
		window.blit(bg,(0,y1))
		window.blit(bg,(0,y2))

		if y1 > SCREEN_HEIGHT:
			y1 = -SCREEN_HEIGHT
		if y2 > SCREEN_HEIGHT:
			y2 = -SCREEN_HEIGHT

		player.show()
		player.move()

		for bullet in reflection_bullets:
			if bullet.rect.x >= SCREEN_WIDTH - 70:
				bullet.sign = -1
				bullet.image = pygame.transform.rotate(bullet.image, 90)


			if bullet.rect.x <= 0:
				bullet.sign = 1
				bullet.image = pygame.transform.rotate(bullet.image, -90)


		for sprite in secondary_sprites:
			sprite.draw(window)
			sprite.update()

		window.blit(hp_image,(5,15))
		window.blit(health, (10, 0))
		window.blit(score, (SCREEN_WIDTH - 120, 0))

		# Generate Enemies
		if i == 0:
			i = 15
			enemy = Enemy('assets/enemy.png', randint(0,3) * 100, -50, 100, 100, randint(5,6))
			enemy.fire()
			enemies.add(enemy)
		else:
			i -= 1

		# Make enemies fire
		if j == 0:
			for e in enemies:
				j = 60
				e.fire()
		else:
			j -= 1

		
		for event in events:
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE:
					if player.fire_number < 10 and not player.is_reload_fire:
						player.fire()
					if player.fire_number >= 10:
						start_time = time()
						player.is_reload_fire = True
			if event.type == pygame.MOUSEBUTTONDOWN:
				player.fire()

		if player.is_reload_fire:
			period = time() - start_time
			is_was_range_mode = False
			if period >= 3:
				player.is_reload_fire = False
				player.fire_number = 0
				if is_was_range_mode:
					player.is_range_mode = True
			else:
				if player.is_range_mode:
					player.is_range_mode = False
					is_was_range_mode = True
				window.blit(reload_text, calc_text_pos(reload_text.get_size()))
	
		if player.is_range_mode and not player.is_reload_fire:
			window.blit(range_mode_text, calc_text_pos(range_mode_text.get_size()))

		# When player's bullets and enemies collide show explosion
		r_collides = pygame.sprite.groupcollide(reflection_bullets,enemies, True, True)
		for c in r_collides:
			inc_score()
			show_explosion(c)

		collides = pygame.sprite.groupcollide(bullets,enemies, True, True)
		for c in collides:
			inc_score()
			show_explosion(c)

		# When player's and enemies bullets collide remove both
		pygame.sprite.groupcollide(reflection_bullets, enemy_bullets, True, True)
		pygame.sprite.groupcollide(bullets, enemy_bullets, True, True)

		# When player gets damage
		if pygame.sprite.spritecollide(player, enemies, True) or pygame.sprite.spritecollide(player, enemy_bullets, True):
			exp_sound.play()
			e = 0
			for i in range(9):
				if e == 0:
					e = 50
					enemy_bullets.image = load_image(exp_image_list[i],(100,100))
					window.blit(enemy_bullets.image, (player.rect.x + 30, player.rect.y))
				else:
					e -= 1

			player.hp -= 1 
			hp_image = load_image(hp_images_list[10 - player.hp],(100,30))
			
	if SCORE == 25:
		IS_FINISH = True
		you_win()
		stop_sounds()
	elif SCORE == 15:
		player.is_range_mode = True

	if player.hp == 0:
		IS_FINISH = True
		you_lose()
		stop_sounds()

	if IS_STOP:
		window.blit(press_to_continue_text, calc_text_pos(press_to_continue_text.get_size()))

	for event in events:
		if event.type == pygame.QUIT:
			game = False
			pygame.quit()
			quit()
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_q:
				exit()
			if event.key == pygame.K_ESCAPE:
				if not player.is_reload_fire:
					IS_STOP = not IS_STOP
			if event.key == pygame.K_r and IS_FINISH:
				for sprite in secondary_sprites:
					sprite.empty()
				player = Player('assets/ship1.png','assets/ship2.png', 125, 500, 150, 150, 10)
				
				y1 = 0
				y2 = -SCREEN_HEIGHT
				i,j = 0,0
				SCORE = 0
				player.hp = 10

				score = h1.render(f"Score: {SCORE}",False, (255, 255, 255))
				hp_image = load_image(hp_images_list[10 - player.hp],(100,30))

				
				IS_FINISH = False

	clock.tick(FPS)
	pygame.display.update()
