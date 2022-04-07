import pygame, csv, json
from tile import AnimatedTile, Melee, Bullet, Tile, Door, Crate, Gun, Pickup, SavePoint
from settings import *
from player import Player
from enemies import Guard
from support import import_csv, import_folder
from pause import Pause, LevelIntro, Transition
from particles import Particles


class Level:
	def __init__(self, current_level, entry_pos, new_block_position, current_gun, gun_showing, surf, create_level):

		self.game_paused = False
		self.transitioning = False

		# setup level
		self.new_block_position = new_block_position
		self.current_gun = current_gun
		self.gun_showing = gun_showing
		self.entry_pos = entry_pos
		self.display_surf = surf
		self.current_level = current_level
		self.create_level = create_level
		self.current_level = current_level
		self.timer = 0
		self.player_grounded = False

		#get size (length and width) of level in pixels
		with open(f'levels/{self.current_level}/level_{self.current_level}_blocks.csv', newline='') as csvfile:
		    reader = csv.reader(csvfile, delimiter=',')
		    for row in reader:
		        rows = (sum (1 for row in reader) + 1)
		        cols = len(row)
		self.level_length = cols * TILESIZE 
		self.level_height = rows * TILESIZE

		# main sprite groups
		self.visible_sprites = LayerCameraGroup(self.current_level, self.level_length, self.level_height)
		self.active_sprites = pygame.sprite.Group()
		self.obstacle_sprites = pygame.sprite.Group()

		#gun upgrades
		self.pickup_sprites = pygame.sprite.Group()
	
		# moveable blocks
		self.moveable_block_sprites = pygame.sprite.Group()
		self.block_position = self.new_block_position

		#exit doors
		self.exit_sprites = pygame.sprite.Group()
		self.save_sprites = pygame.sprite.Group()

		# gun being held sprite
		self.gun_sprite = pygame.sprite.GroupSingle()

		# pause moments
		self.transition = Transition(self.display_surf)
		self.pause = Pause('Paused', self.display_surf)
		self.intro_text = LevelIntro(self.current_level,(levels[self.current_level]['level_name']), self.display_surf)

		self.create_map()
		
	def create_map(self):

		layouts = {
		'blocks':import_csv(f'levels/{self.current_level}/level_{self.current_level}_blocks.csv'),
		'pickups':import_csv(f'levels/{self.current_level}/level_{self.current_level}_pickups.csv'),
		'enemies':import_csv(f'levels/{self.current_level}/level_{self.current_level}_enemies.csv'),
		'entrances':import_csv(f'levels/{self.current_level}/level_{self.current_level}_entrances.csv'),
		'exits':import_csv(f'levels/{self.current_level}/level_{self.current_level}_exits.csv'),
		'save':import_csv(f'levels/{self.current_level}/level_{self.current_level}_save.csv'),
		}

		images = {
		'blocks':import_folder(f'img/tiles/{self.current_level}/blocks')
		}

		for style, layout in layouts.items():
			for row_index, row in enumerate(layout):
				for col_index, col in enumerate(row):
					if col != '-1':
						x = col_index * TILESIZE
						y = row_index * TILESIZE

						if style == 'blocks':
							surf = images['blocks'][int(col)]
							Tile((x,y), [self.visible_sprites, self.obstacle_sprites], surf)

						if style == 'pickups':
							if col == '0' and not '0' in list(gun_data.keys()): 
								sprite = Pickup((x,y), [self.visible_sprites, self.active_sprites], 'img/pickups/gun', {0:{'bullet_speed': 10, 'cooldown': 300, 'damage': 30, 'img':'img/bullets/bullet_0.png', 'gun_img':'img/pickups/gun/00.png'}})
								self.pickup_sprites.add(sprite)
							if col == '1' and not '1' in list(gun_data.keys()): 
								sprite = Pickup((x,y), [self.visible_sprites, self.active_sprites], 'img/pickups/blaster', {1:{'bullet_speed': 60, 'cooldown': 100, 'damage': 50, 'img':'img/bullets/bullet_2.png', 'gun_img':'img/pickups/blaster/00.png'}})
								self.pickup_sprites.add(sprite)
							if col == '2'  and not '2' in list(gun_data.keys()): 
								sprite = Pickup((x,y), [self.visible_sprites, self.active_sprites], 'img/pickups/rifle', {2:{'bullet_speed': 100, 'cooldown': 500, 'damage': 40, 'img':'img/bullets/bullet_1.png', 'gun_img':'img/pickups/rifle/00.png'}})
								self.pickup_sprites.add(sprite)

						if style == 'enemies':
							if col == '0': Guard((x,y), [self.visible_sprites, self.active_sprites], self.obstacle_sprites,'guard')

						if style == 'entrances':
							if col == str(self.entry_pos):
								self.player = Player(\
									(x, y), \
									[self.visible_sprites, self.active_sprites],\
									 self.obstacle_sprites, \
									 self.create_melee, \
									 self.create_run_particles, \
									 self.create_jump_particles,\
									 self.shoot, \
									 self.current_gun, \
									 self.gun_showing)

						if style == 'save':
							sprite = SavePoint((x,y), [self.visible_sprites])
							self.save_sprites.add(sprite)
								
						if style == 'exits':
							if col == '1': 
								sprite = Door((x,y), [self.visible_sprites], 1)
								self.exit_sprites.add(sprite)
								
							elif col == '2':
								sprite = Door((x,y), [self.visible_sprites], 2)
								self.exit_sprites.add(sprite)

							elif col == '3': 
								sprite = Door((x,y), [self.visible_sprites], 3)
								self.exit_sprites.add(sprite)

							elif col == '4': 
								sprite = Door((x,y), [self.visible_sprites], 4)
								self.exit_sprites.add(sprite)

							elif col == '5':
								sprite = Door((x,y), [self.visible_sprites], 5)
								self.exit_sprites.add(sprite)

		# moveable blocks staying in same place when return to level
		if self.current_level == 0:
			self.moveable_block_sprite = Crate((self.new_block_position), [self.visible_sprites, self.active_sprites], self.player, self.moveable_block_sprites, self.obstacle_sprites, 'crate')
			self.moveable_block_sprites.add(self.moveable_block_sprite)

	# make sure the block stays in the place you left it when returning to new level
	def get_block_pos(self):
		for sprite in self.moveable_block_sprites.sprites():
			self.block_position = sprite.rect.topleft

	def create_melee(self):
		if not self.player.air_attacked:
			Melee(self.player, [self.visible_sprites, self.active_sprites], self.display_surf)
			self.player.air_attacked = True

	def shoot(self, gun):
		if self.player.gun_showing:
			Bullet(self.player, gun, [self.visible_sprites, self.active_sprites], self.obstacle_sprites, self.moveable_block_sprites)

	def show_gun(self):
		if gun_data:
			self.player.gun_showing = not self.player.gun_showing
			self.gun_sprite = Gun(self.player, [self.visible_sprites, self.active_sprites], self.display_surf)

	def gun_equipped(self):
		if gun_data:
			self.gun_sprite = Gun(self.player, [self.visible_sprites, self.active_sprites], self.display_surf)

	def show_new_gun(self):
		if self.player.gun_showing and gun_data:
			self.gun_sprite.kill()
			self.gun_sprite = Gun(self.player, [self.visible_sprites, self.active_sprites], self.display_surf)

	def create_run_particles(self):
		if self.player.vel.x != 0 and self.player.on_ground and not self.player.state == 'idle' and not self.player.state == 'idle_armed':
			self.player.run_particle_timer += 1
		if self.player.run_particle_timer >= 20:
			Particles(self.player, [self.visible_sprites, self.active_sprites], 'run')
			self.player.run_particle_timer = 0

	def create_jump_particles(self):
		Particles(self.player, [self.visible_sprites, self.active_sprites], 'jump')	

	def get_player_grounded(self):
		if self.player.on_ground:
			self.player_grounded = True
		else:
			self.player_grounded = False

	def create_landing_particles(self):
		if not self.player_grounded and self.player.on_ground and not self.player.run_in:
			Particles(self.player, [self.visible_sprites, self.active_sprites], 'jump')
								
	# this gets the data for the new level, then it is called in exit_level func below
	def	new_level_data(self,new_level):
		self.visible_sprites.empty()
		self.active_sprites.empty()
		self.obstacle_sprites.empty()
		self.new_block_position = self.block_position
		self.new_level = levels[self.current_level][new_level]
		self.exit_list = list(levels[self.current_level].keys())
		self.entry_pos = self.exit_list[new_level-1]
		self.current_gun = self.player.gun
		self.gun_showing = self.player.gun_showing
		self.create_level(self.new_level,self.entry_pos, self.new_block_position, self.current_gun, self.gun_showing)

	def exit_level(self):
		if not self.player.run_in:
			collided_exits = pygame.sprite.spritecollide(self.player, self.exit_sprites, False, pygame.sprite.collide_rect_ratio(0.4))
			if collided_exits:
				for exit in collided_exits:
					self.new_level_data(exit.number)

	def save_point(self):
		collided_save = pygame.sprite.spritecollide(self.player, self.save_sprites, False)
		if collided_save:
			for save in collided_save:
				saved_gun_data.update(gun_data)
				load_data.update({'save_point': self.current_level, 'block_position': self.new_block_position, 'current_gun': self.current_gun, 'gun_showing': self.gun_showing})

	def load_point(self):
		self.new_block_position = self.block_position
		self.current_gun = self.player.gun
		gun_data.clear()
		gun_data.update(saved_gun_data)
		self.create_level(load_data['save_point'], 0, load_data['block_position'], load_data['current_gun'], load_data['gun_showing'])

			
	def entry_cooldown(self):
		self.transition.run()
		self.timer += 1
		if self.timer >= 20:
			self.player.run_in = False
		if self.timer <= 100:
			self.intro_text.run()

	def pickup_collision(self):
		collided_pickups = pygame.sprite.spritecollide(self.player, self.pickup_sprites, True)
		if collided_pickups:
			for pickup in collided_pickups:
				gun_data.update(pickup.index)

	def dump_load_data(self):
		with open('progress_data.txt', 'w') as progress_file:
			json.dump(load_data, progress_file)

	def paused(self):
		self.game_paused = not self.game_paused

	def run(self):
		self.pickup_collision()
		self.get_block_pos()
		if self.game_paused:
			self.pause.run()
		else:
			#print(self.block_position)
			#print(self.new_block_position)
			self.get_player_grounded()
			self.create_run_particles()
			self.active_sprites.update()
			self.visible_sprites.offset_draw(self.player)
			if not self.player.state == 'facing':
				self.create_landing_particles()
			self.entry_cooldown()
			self.exit_level()
			self.save_point()


class LayerCameraGroup(pygame.sprite.Group):
	def __init__(self, bg, level_length, level_height):
		super().__init__()
		self.display_surf = pygame.display.get_surface()
		self.offset = pygame.math.Vector2(100,150)
		self.level_length = level_length
		self.level_height = level_height

		# upload bg image
		self.bg = bg
		self.bg_surf = pygame.image.load(f'levels/bg/{self.bg}.jpg').convert_alpha()
		self.bg_surf = pygame.transform.scale(self.bg_surf, (self.level_length, self.level_height))

		# centre the camera
		self.half_width = self.display_surf.get_width() // 2
		self.half_height = self.display_surf.get_height() // 2

		# camera
		left = CAMERA_BORDERS['left']
		top = CAMERA_BORDERS['top']
		width = self.display_surf.get_width() - (CAMERA_BORDERS['left'] * 2)
		height = self.display_surf.get_height() - (CAMERA_BORDERS['top'] * 2)

		self.camera_rect = pygame.Rect(left, top, width, height)

	def offset_draw(self, player):
		
		#below is to create a camera box around the player to move the oll instead of the player moving the scroll if wanted
		# # get cam position
		if player.rect.left < self.camera_rect.left:
			self.camera_rect.left = player.rect.left
		if player.rect.right > self.camera_rect.right:
			self.camera_rect.right = player.rect.right
		if player.rect.top < self.camera_rect.top:
			self.camera_rect.top = player.rect.top
		if player.rect.bottom > self.camera_rect.bottom:
			self.camera_rect.bottom = player.rect.bottom
		# cam offset
		self.offset = pygame.math.Vector2(self.camera_rect.left - CAMERA_BORDERS['left'], self.camera_rect.top - CAMERA_BORDERS['top'])

		if self.offset[0] <= 0:
			self.offset[0] = 0
		elif self.offset[0] >= self.level_length - WIDTH:
			self.offset[0] = self.level_length - WIDTH

		if self.offset[1] <= 0:
			self.offset[1] = 0
		elif self.offset[1] >= self.level_height - HEIGHT:
			self.offset[1] = self.level_height - HEIGHT


		# seperate blits to layer player on top of other sprites
		self.bg_rect = self.bg_surf.get_rect(topleft = (0, 0))
		bg_offset_pos = self.bg_rect.topleft - self.offset
		self.display_surf.blit(self.bg_surf, bg_offset_pos)

		for sprite in self.sprites():
				offset = sprite.rect.topleft - self.offset
				self.display_surf.blit(sprite.image, offset)


		

		



		




	

	



		