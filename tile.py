import pygame
from settings import *
from support import import_folder

class Tile(pygame.sprite.Sprite):
	def __init__(self, pos, groups, surf = pygame.Surface((TILESIZE, TILESIZE))):
		super().__init__(groups)
		self.image = surf
		self.rect = self.image.get_rect(topleft = pos)

class SavePoint(pygame.sprite.Sprite):
	def __init__(self, pos, groups):
		super().__init__(groups)
		self.surf = pygame.display.get_surface()
		self.image = pygame.Surface((30,30))
		self.image = pygame.transform.scale(self.image, (self.image.get_width() * SCALE, self.image.get_height() * SCALE))
		self.rect = self.image.get_rect(topleft = pos)

class AnimatedTile(pygame.sprite.Sprite):
	def __init__(self, pos, groups, path):
		super().__init__(groups)

		#self.sprite_type = sprite_type
		self.frames = import_folder(path)
		self.frame_index = 0
		self.image = self.frames[self.frame_index]
		self.rect = self.image.get_rect(topleft = pos)

	def animate(self):
		self.frame_index += 0.2
		if self.frame_index >= len(self.frames):
			self.frame_index = 0
		self.image = self.frames[int(self.frame_index)]

	def update(self):
		self.animate()

class Door(pygame.sprite.Sprite):
	def __init__(self, pos, groups, number):
		super().__init__(groups)
		self.number = number
		self.surf = pygame.display.get_surface()
		self.image = pygame.image.load('img/tiles/door.png').convert_alpha()
		self.image = pygame.transform.scale(self.image, (self.image.get_width() * SCALE, self.image.get_height() * SCALE))
		self.rect = self.image.get_rect(topleft = pos)
		self.flipped_image = pygame.transform.flip(self.image, True, False)
	
		if self.rect.centerx > self.surf.get_width() // 2:
			self.image = self.flipped_image
		else:
			self.image = self.image

class Entity(pygame.sprite.Sprite):
	def __init__(self,groups):
		super().__init__(groups)

	def animate(self, animation_type):
		animation = self.animations[self.state]

		self.frame_index += self.frame_rate
		if animation_type == 'kill':
			if self.frame_index >= len(animation)-1:
				self.kill()

		if animation_type == 'loop':
			if self.frame_index >= len(animation):
				self.frame_index = 0

		right_img = animation[int(self.frame_index)]
		if self.facing == 1:
			self.image = right_img
		else:
			left_img = pygame.transform.flip(right_img, True, False)
			self.image = left_img

class Character(Entity):
	def __init__(self, groups):
		super().__init__(groups)

		self.state = 'idle'
		self.facing = 1
		self.frame_index = 0
		self.frame_rate = 0.12

		self.vel = pygame.math.Vector2()

	def animate(self, animation_type):
		animation = self.animations[self.state]

		self.frame_index += self.frame_rate
		if animation_type == 'kill':
			if self.frame_index >= len(animation)-1:
				self.kill()

		if animation_type == 'loop':
			if self.frame_index >= len(animation):
				self.frame_index = 0

		right_img = animation[int(self.frame_index)]
		if self.facing == 1:
			self.image = right_img
		else:
			left_img = pygame.transform.flip(right_img, True, False)
			self.image = left_img

		if self.on_ground and self.on_right:
			self.rect = self.image.get_rect(bottomright = self.rect.bottomright)
		elif self.on_ground and self.on_left:
			self.rect = self.image.get_rect(bottomleft = self.rect.bottomleft)
		elif self.on_ground:
			self.rect = self.image.get_rect(midbottom = self.rect.midbottom)
		elif self.on_ceiling and self.on_right:
			self.rect = self.image.get_rect(topright = self.rect.topright)
		elif self.on_ceiling and self.on_left:
			self.rect = self.image.get_rect(topleft = self.rect.topleft)
		elif self.on_ceiling:
			self.rect = self.image.get_rect(midtop = self.rect.midtop)
	

	def gravity(self):
		self.vel.y += 0.8
		self.rect.y += self.vel.y
		if self.vel.y > TERMINAL_VELOCITY:
			self.vel.y = TERMINAL_VELOCITY

	def x_collisions(self):
		for sprite in self.obstacle_sprites.sprites():
			if sprite.rect.colliderect(self.rect):
				if self.vel.x > 0:
					self.rect.right = sprite.rect.left		
		
				elif self.vel.x < 0:
					self.rect.left = sprite.rect.right
			
	def y_collisions(self):
		for sprite in self.obstacle_sprites.sprites():
			if sprite.rect.colliderect(self.rect):
				if self.vel.y > 0:
					self.rect.bottom = sprite.rect.top
					self.vel.y = 0
					self.on_ground = True
				elif self.vel.y < 0:
					self.rect.top = sprite.rect.bottom
					self.vel.y = 0
					self.on_ceiling = True

		if self.on_ground and self.vel.y < 0 or self.vel.y > 1:
			self.on_ground = False

	def get_state(self):
		if self.attacking:
			self.state = 'attack'
		elif self.vel.y < 0:
			self.state = 'jump'
		elif self.vel.y > 1:
			self.state = 'fall'
		else:
			if self.vel.x != 0:
				self.state = 'run' 
			else:
				self.state = 'idle'

class Melee(Entity):
	def __init__(self, player, groups, surf):
		super().__init__(groups)
	
		self.import_assets('weapons')

		self.player = player

		self.vel = pygame.math.Vector2()
		self.vel.x = player.vel.x
		self.facing = player.facing
		self.state = 'sword'
		self.frame_index = 0
		self.frame_rate = 0.3

		self.image = self.animations['sword'][self.frame_index]
		self.rect = self.image.get_rect(center = player.rect.center)

	def import_assets(self, name):
		char_path = f'img/{name}/'
		self.animations = {'sword': []}

		for animation in self.animations.keys():
			full_path = char_path + animation
			self.animations[animation] = import_folder(full_path)

	def update(self):
		if self.facing == 1:
			self.rect = self.image.get_rect(midleft = self.player.rect.midright)
		else:
			self.image = pygame.transform.flip(self.image, True, False)
			self.rect = self.image.get_rect(midright = self.player.rect.midleft)

		self.animate('kill')

class Crate(Entity):
	def __init__(self, pos, groups, player, moveable_block_sprites, obstacles_sprites, surf):
		super().__init__(groups)

		self.player = player
		self.moveable_block_sprites = moveable_block_sprites
		self.obstacle_sprites = obstacles_sprites
		self.vel = pygame.math.Vector2()
		self.image = pygame.image.load(f'img/tiles/{surf}.png').convert_alpha()
		self.image = pygame.transform.scale(self.image, (self.image.get_width() * SCALE *1.5, self.image.get_height() * SCALE *1.5))
		self.rect = self.image.get_rect(topleft = pos)

	def x_collisions(self):
		for sprite in self.moveable_block_sprites.sprites():
			if sprite.rect.colliderect(self.player.rect):
				if self.player.vel.x > 0  and self.player.rect.right < sprite.rect.centerx:
					sprite.rect.left = self.player.rect.right
				
				if self.player.vel.x < 0 and self.player.rect.left > sprite.rect.centerx:
					sprite.rect.right = self.player.rect.left
			
		# pushing block collisions
		for sprite in self.obstacle_sprites.sprites():
			if sprite.rect.colliderect(self.rect):
				if self.player.vel.x > 0:
					self.player.vel.x = 0
					self.rect.right = sprite.rect.left
					self.player.rect.right = self.rect.left

				elif self.player.vel.x < 0:
					self.player.vel.x = 0
					self.rect.left = sprite.rect.right
					self.player.rect.left = self.rect.right

	def y_collisions(self):
		for sprite in self.moveable_block_sprites.sprites():
			if sprite.rect.colliderect(self.player.rect):
				if self.player.vel.y > 0:
					self.player.rect.bottom = sprite.rect.top
					self.player.vel.y = 0
					self.player.on_ground = True
				if self.player.vel.y < 0:
					self.player.rect.top = sprite.rect.bottom
					self.player.vel.y = 0

		for sprite in self.obstacle_sprites.sprites():
			if sprite.rect.colliderect(self.rect):
				if self.vel.y > 0:
					self.rect.bottom = sprite.rect.top
					self.vel.y = 0
				elif self.vel.y < 0:
					self.rect.top = sprite.rect.bottom
					self.vel.y = 0


	def gravity(self):
		self.vel.y += 0.8
		self.rect.y += self.vel.y
		if self.vel.y > TERMINAL_VELOCITY:
			self.vel.y = TERMINAL_VELOCITY




	def update(self):
		self.x_collisions()
		self.gravity()
		self.y_collisions()
		self.rect.x += self.vel.x

class Gun(Entity):
	def __init__(self, player, groups, surf):
		super().__init__(groups)

		self.player = player
		self.image = pygame.image.load(list(gun_data.values())[self.player.gun]['gun_img']).convert_alpha()
		self.image = pygame.transform.scale(self.image, (self.image.get_width() * SCALE, self.image.get_height() * SCALE))
		self.right_image = self.image
		self.left_image = pygame.transform.flip(self.image, True, False)
		self.rect = self.image.get_rect(center = player.rect.center)
		self.facing = player.facing

		
	def update(self):
		if self.player.facing == 1:
			self.image = self.right_image
			self.rect = self.image.get_rect(midleft = (self.player.rect.centerx - 4, self.player.rect.centery - 4))
		else:
			self.image = self.left_image
			self.rect = self.image.get_rect(midright = (self.player.rect.centerx + 4, self.player.rect.centery - 4))
	
		if not self.player.gun_showing:
			self.kill()
	
class Bullet(Entity):
	def __init__(self, sprite_type, gun_index, groups, obstacle_sprites, moveable_blocks):
		super().__init__(groups)

		self.image = pygame.image.load(list(gun_data.values())[gun_index]['img']).convert_alpha()
		self.image = pygame.transform.scale(self.image, (self.image.get_width() * SCALE, self.image.get_height() * SCALE))
		self.right_image = self.image
		self.left_image = pygame.transform.flip(self.image, True, False)
		self.rect = self.image.get_rect(center = sprite_type.rect.center)
		self.speed = list(gun_data.values())[gun_index]['bullet_speed']
		self.facing = sprite_type.facing

		if self.facing == 1:
			self.image = self.right_image
			self.rect = self.image.get_rect(midleft = sprite_type.rect.midright)
		else:
			self.image = self.left_image
			self.rect = self.image.get_rect(midright = sprite_type.rect.midleft)

		self.obstacle_sprites = obstacle_sprites
		self.moveable_blocks = moveable_blocks

	def bullet_speed(self):
		if self.facing == 1:
			self.rect.x += self.speed
		else:
			self.rect.x -= self.speed

	def collisions(self):
		for sprite in self.obstacle_sprites.sprites():
			if sprite.rect.colliderect(self.rect):
				self.kill()

		for sprite in self.moveable_blocks.sprites(): 
			if sprite.rect.colliderect(self.rect):
				self.kill()

	def update(self):
		self.collisions()
		self.bullet_speed()

class Pickup(AnimatedTile):
	def __init__(self, pos, groups, path, index):
		super().__init__(pos, groups, path)

		self.index = index


		


	
		
		

		





		


