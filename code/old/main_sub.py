import pygame, sys, time
from settings import *
from random import choice, randint

class Game:
	def __init__(self):
		
		# setup
		pygame.init()
		self.display_surface = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
		pygame.display.set_caption('Space Runner')
		self.clock = pygame.time.Clock()
		self.active = True

		# sprite groups
		self.all_sprites = pygame.sprite.Group()
		self.collision_sprites = pygame.sprite.Group()

		# scale factor
		bg_height = pygame.image.load('C:/Users/OliwerUrbaniak/Documents/Visual Studio Code/Python/SpaceRunner/graphics/environment/background.png').get_height()
		self.scale_factor = WINDOW_HEIGHT / bg_height

		# sprite setup 
		BG(self.all_sprites,self.scale_factor)
		Ground([self.all_sprites,self.collision_sprites],self.scale_factor)
		self.ship = Ship(self.all_sprites,self.scale_factor / 1.7)

		# timer
		self.obstacle_timer = pygame.USEREVENT + 1
		pygame.time.set_timer(self.obstacle_timer,1400)

		# text
		self.font = pygame.font.Font('C:/Users/OliwerUrbaniak/Documents/Visual Studio Code/Python/SpaceRunner/graphics/font/BD_Cartoon_Shout.ttf',30)
		self.score = 0
		self.start_offset = 0

		# menu
		self.menu_surf = pygame.image.load('C:/Users/OliwerUrbaniak/Documents/Visual Studio Code/Python/SpaceRunner/graphics/ui/menu.png').convert_alpha()
		self.menu_rect = self.menu_surf.get_rect(center = (WINDOW_WIDTH / 2,WINDOW_HEIGHT / 2))

		# music 
		self.music = pygame.mixer.Sound('C:/Users/OliwerUrbaniak/Documents/Visual Studio Code/Python/SpaceRunner/sounds/music.mp3')
		self.music.play(loops = -1)
		self.music.set_volume(0.3)

	def collisions(self):
		if pygame.sprite.spritecollide(self.ship,self.collision_sprites,False,pygame.sprite.collide_mask)\
		or self.ship.rect.top <= 0:
			for sprite in self.collision_sprites.sprites():
				if sprite.sprite_type == 'obstacle':
					sprite.kill()
			self.active = False
			self.ship.kill()

	def display_score(self):
		if self.active:
			self.score = (pygame.time.get_ticks() - self.start_offset) // 1000
			y = WINDOW_HEIGHT / 10
		else:
			y = WINDOW_HEIGHT / 2 + (self.menu_rect.height / 1.5)

		score_surf = self.font.render(str(self.score),True,'white')
		score_rect = score_surf.get_rect(midtop = (WINDOW_WIDTH / 2,y))
		self.display_surface.blit(score_surf,score_rect)

	def run(self):
		last_time = time.time()
		while True:
			
			# delta time
			dt = time.time() - last_time
			last_time = time.time()

			# event loop
			for event in pygame.event.get():
				if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
					pygame.quit()
					sys.exit()
				if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE or event.type == pygame.MOUSEBUTTONDOWN:
						if self.active:
							self.ship.jump()
						else:
							self.ship = Ship(self.all_sprites, self.scale_factor / 1.7)
							self.active = True
							self.start_offset = pygame.time.get_ticks()

				if event.type == self.obstacle_timer and self.active:
					Obstacle([self.all_sprites,self.collision_sprites],self.scale_factor * 1.1)
			
			# game logic
			self.display_surface.fill('black')
			self.all_sprites.update(dt)
			self.all_sprites.draw(self.display_surface)
			self.display_score()

			if self.active: 
				self.collisions()
			else:
				self.display_surface.blit(self.menu_surf,self.menu_rect)

			pygame.display.update()
			# self.clock.tick(FRAMERATE)
class BG(pygame.sprite.Sprite):
	def __init__(self,groups,scale_factor):
		super().__init__(groups)
		bg_image = pygame.image.load('C:/Users/OliwerUrbaniak/Documents/Visual Studio Code/Python/SpaceRunner/graphics/environment/background.png').convert()

		full_height = bg_image.get_height() * scale_factor
		full_width = bg_image.get_width() * scale_factor
		full_sized_image = pygame.transform.scale(bg_image,(full_width,full_height))
		
		self.image = pygame.Surface((full_width * 2,full_height))
		self.image.blit(full_sized_image,(0,0))
		self.image.blit(full_sized_image,(full_width,0))

		self.rect = self.image.get_rect(topleft = (0,0))
		self.pos = pygame.math.Vector2(self.rect.topleft)

	def update(self,dt):
		self.pos.x -= 300 * dt
		if self.rect.centerx <= 0:
			self.pos.x = 0
		self.rect.x = round(self.pos.x)

class Ground(pygame.sprite.Sprite):
	def __init__(self,groups,scale_factor):
		super().__init__(groups)
		self.sprite_type = 'ground'
		
		# image
		ground_surf = pygame.image.load('C:/Users/OliwerUrbaniak/Documents/Visual Studio Code/Python/SpaceRunner/graphics/environment/ground.png').convert_alpha()
		self.image = pygame.transform.scale(ground_surf,pygame.math.Vector2(ground_surf.get_size()) * scale_factor)
		
		# position
		self.rect = self.image.get_rect(bottomleft = (0,WINDOW_HEIGHT))
		self.pos = pygame.math.Vector2(self.rect.topleft)

		# mask
		self.mask = pygame.mask.from_surface(self.image)

	def update(self,dt):
		self.pos.x -= 360 * dt
		if self.rect.centerx <= 0:
			self.pos.x = 0

		self.rect.x = round(self.pos.x)

class Ship(pygame.sprite.Sprite):
	def __init__(self,groups,scale_factor):
		super().__init__(groups)

		# image 
		self.import_frames(scale_factor)
		self.frame_index = 0
		self.image = self.frames[self.frame_index]

		# rect
		self.rect = self.image.get_rect(midleft = (WINDOW_WIDTH / 20,WINDOW_HEIGHT / 2))
		self.pos = pygame.math.Vector2(self.rect.topleft)

		# movement
		self.gravity = 600
		self.direction = 0

		# mask
		self.mask = pygame.mask.from_surface(self.image)

		# sound
		self.jump_sound = pygame.mixer.Sound('C:/Users/OliwerUrbaniak/Documents/Visual Studio Code/Python/SpaceRunner/sounds/jump.wav')
		self.jump_sound.set_volume(0.5)

	def import_frames(self,scale_factor):
		self.frames = []
		for i in range(3):
			surf = pygame.image.load(f'C:/Users/OliwerUrbaniak/Documents/Visual Studio Code/Python/SpaceRunner/graphics/ship/smil{i}.png').convert_alpha()
			scaled_surface = pygame.transform.scale(surf,pygame.math.Vector2(surf.get_size())* scale_factor)
			self.frames.append(scaled_surface)

	def apply_gravity(self,dt):
		self.direction += self.gravity * dt
		self.pos.y += self.direction * dt
		self.rect.y = round(self.pos.y)

	def jump(self):
		self.jump_sound.play()
		self.direction = -400

	def animate(self,dt):
		self.frame_index += 10 * dt
		if self.frame_index >= len(self.frames):
			self.frame_index = 0
		self.image = self.frames[int(self.frame_index)]

	def rotate(self):
		rotated_ship = pygame.transform.rotozoom(self.image,-self.direction * 0.06,1)
		self.image = rotated_ship
		self.mask = pygame.mask.from_surface(self.image)

	def update(self,dt):
		self.apply_gravity(dt)
		self.animate(dt)
		self.rotate()

class Obstacle(pygame.sprite.Sprite):
	def __init__(self,groups,scale_factor):
		super().__init__(groups)
		self.sprite_type = 'obstacle'

		orientation = choice(('up','down'))
		surf = pygame.image.load(f'C:/Users/OliwerUrbaniak/Documents/Visual Studio Code/Python/SpaceRunner/graphics/obstacles/{choice((1,2))}.png').convert_alpha()
		self.image = pygame.transform.scale(surf,pygame.math.Vector2(surf.get_size()) * scale_factor)
		
		x = WINDOW_WIDTH + randint(40,100)

		if orientation == 'up':
			y = WINDOW_HEIGHT + randint(10,50)
			self.rect = self.image.get_rect(midbottom = (x,y))
		else:
			y = randint(-50,-10)
			self.image = pygame.transform.flip(self.image,False,True)
			self.rect = self.image.get_rect(midtop = (x,y))

		self.pos = pygame.math.Vector2(self.rect.topleft)

		# mask
		self.mask = pygame.mask.from_surface(self.image)

	def update(self,dt):
		self.pos.x -= 400 * dt
		self.rect.x = round(self.pos.x)
		if self.rect.right <= -100:
			self.kill()

if __name__ == '__main__':
	game = Game()
	game.run()