import pygame
from settings import *
from support import import_folder
from tile import Entity, Character, Gun

class Player(Character):
	def __init__(self, pos, groups, obstacle_sprites, create_melee, create_run_particles, create_jump_particles, shoot, current_gun, gun_showing):
		super().__init__(groups)
		self.display_surf = pygame.display.get_surface()
		
		self.current_x = 0
		# animation setup
		self.import_assets()

		self.image = self.animations['idle'][self.frame_index]
		self.rect = self.image.get_rect(bottomleft = (pos[0], pos[1] + self.image.get_height() + TILESIZE))

		# movement
		self.speed = 6
		self.jump_height = JUMP_HEIGHT
		self.jump_counter = 0
		self.run_in = True
		self.facing = 1
		self.state = 'idle'
		self.on_ground = False
		self.on_ceiling = False
		self.on_left = False
		self.on_right = False
		self.on_wall = False

		# attacking
		self.create_melee = create_melee
		self.attacking = False
		self.air_attacked = False
		self.attack_cooldown = 500
		self.attack_time = None

		#shooting
		self.gun_showing = gun_showing
		self.can_shoot = True
		self.shoot = shoot
		self.shoot_time = None
		self.gun_index = 0
		self.gun = current_gun
		self.shoot_cooldown = None

		# particles
		self.create_jump_particles = create_jump_particles
		self.create_run_particles = create_run_particles
		self.run_particle_timer = 0

		self.obstacle_sprites = obstacle_sprites

	def change_gun(self):
		if self.gun_index < len(list(gun_data.keys()))-1:
			self.gun_index += 1
		else:
			self.gun_index = 0
		self.gun = self.gun_index
	
	def get_state(self):
		if not self.run_in:
			if self.gun_showing:
				if self.vel.x != 0 and self.on_ground  and not self.on_right and not self.on_left:
					self.state = 'run_armed'
				elif self.on_ground:
					self.state = 'idle_armed'
				else:
					self.state = 'jump_armed'
			else:
				if self.on_right and self.vel.y >= 1 and GOT_WALL_SLIDE or self.on_left and self.vel.y >= 1 and GOT_WALL_SLIDE:
					self.state = 'sliding'
				elif self.attacking:
					self.state = 'attack'
				elif self.vel.y < 0:
					self.state = 'jump'
				elif self.vel.y > 1:
					self.state = 'fall'
				else:
					if self.vel.x != 0 and not self.on_right and not self.on_left:
						self.state = 'run' 
					else:
						self.state = 'idle'
			
	def import_assets(self):
		char_path = f'img/player/'
		self.animations = {'idle': [], 'run': [], 'jump': [], 'fall': [], 'attack': [], 'facing': [],'idle_armed': [], 'run_armed': [], 'jump_armed': [], 'fall_armed': [], 'attack_armed': [], 'sliding': []}

		for animation in self.animations.keys():
			full_path = char_path + animation
			self.animations[animation] = import_folder(full_path)

	def input(self):
		if not self.attacking and not self.run_in:
			keys = pygame.key.get_pressed()
			# move input
			if keys[pygame.K_RIGHT]:
				self.vel.x = 1
				self.facing = 1
			elif keys[pygame.K_LEFT]:
				self.vel.x = -1
				self.facing = -1
			else:
				self.vel.x = 0

			if keys[pygame.K_x]:
				if self.gun_showing:
					if self.can_shoot and gun_data:
						self.shoot(self.gun)
						self.can_shoot = False
						self.shoot_time = pygame.time.get_ticks()

				elif not self.air_attacked:
					self.attacking = True
					self.attack_time = pygame.time.get_ticks()
					self.create_melee()


	def cooldowns(self):
		current_time = pygame.time.get_ticks()
		if self.attacking:
			if self.on_ground:
				self.vel = pygame.math.Vector2()
			if current_time - self.attack_time >= self.attack_cooldown:
				self.attacking = False

		if self.can_shoot == False:
			if current_time - self.shoot_time >= self.shoot_cooldown:
				self.can_shoot = True

		if self.on_ground:
			self.air_attacked = False

		#get gun cooldown
		if gun_data:
			self.shoot_cooldown = (list(gun_data.values())[self.gun]['cooldown'])
			

	# auto walk into the level to avoid exit collision
	def enter_level(self):
		self.state = 'run'
		if self.rect.centerx > self.display_surf.get_width() // 2:
			self.facing = -1
			self.rect.x -= 5
		else:
			self.facing = 1
			self.rect.x += 5

	# the player's own x collisions to include 'on_right' and 'on_left' booleans
	def x_collisions(self):
		for sprite in self.obstacle_sprites.sprites():
			if sprite.rect.colliderect(self.rect):
				if self.vel.x > 0:
					self.rect.right = sprite.rect.left
					self.on_right = True
					self.current_x = self.rect.right
					if self.vel.y == 1:
						self.on_wall = True
		
				elif self.vel.x < 0:
					self.rect.left = sprite.rect.right
					self.on_left = True
					self.current_x = self.rect.left
					if self.vel.y == 1:
						self.on_wall = True
					
		if self.on_right and (self.rect.right > self.current_x or self.vel.x <= 0):
			self.on_right = False
			self.on_wall = False

		if self.on_left and (self.rect.left < self.current_x or self.vel.x >= 0):
			self.on_left = False
			self.on_wall = False

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
		if self.on_ceiling and self.vel.y > 0:
			self.on_ceiling = False

	# player inputs passed to event queue, as opposed to get key presses
	def jump(self):
		if self.on_ground:
			self.vel.y = - JUMP_HEIGHT
			self.create_jump_particles()
			self.jump_counter = 1
		elif self.jump_counter == 1 and GOT_DOUBLE_JUMP:
			self.vel.y = - JUMP_HEIGHT
			self.create_jump_particles()
			self.jump_counter = 0
		elif self.on_wall and not self.gun_showing:
			self.wall_jump()

	def wall_jump(self):
		if self.on_wall:
			self.vel.y = - JUMP_HEIGHT
			self.create_jump_particles()
			self.jump_counter = 1
			self.on_wall = False
		
	def wall_slide(self):
		if not self.gun_showing and GOT_WALL_SLIDE:
			if not self.on_ground and self.vel.y > 1 and self.on_right or not self.on_ground and self.vel.y > 1 and self.on_left:
				self.vel.y = 1

	def update(self):
		self.wall_slide()
		self.input()
		self.get_state()
		self.animate('loop')
		self.cooldowns()
		if self.run_in:
			self.enter_level()
		else:
			self.rect.x += self.vel.x * self.speed
		self.x_collisions()
		self.gravity()
		self.y_collisions()


	
		
