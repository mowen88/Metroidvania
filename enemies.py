import pygame
from settings import *
from support import *
from tile import Character

class Guard(Character):
	def __init__(self, pos, groups, obstacle_sprites, sprite_type):
		super().__init__(groups)

		self.import_assets(sprite_type)
		self.image = self.animations['idle'][self.frame_index]
		self.rect = self.image.get_rect(topleft = pos)
		self.hitbox = self.rect.inflate(-20, -20)
		self.attacking = False
		self.on_ground = False
		self.on_ceiling = False
		self.on_right = False
		self.on_left = False

		self.obstacle_sprites = obstacle_sprites

	def import_assets(self, name):
		char_path = f'img/{name}/'
		self.animations = {'idle': [], 'run': [], 'jump': [], 'fall': [], 'attack': [], 'facing': []}

		for animation in self.animations.keys():
			full_path = char_path + animation
			self.animations[animation] = import_folder(full_path)

	def update(self):
		self.animate('loop')
		self.get_state()
		self.x_collisions()
		self.gravity()
		self.y_collisions()
