import pygame
from settings import *
from support import import_folder

class Particles(pygame.sprite.Sprite):
	def __init__(self, player, groups, type):
		super().__init__(groups)

		self.vel = pygame.math.Vector2()
		self.frame_index = 0
		self.frame_rate = 0.2
		self.facing = player.facing
		
		self.animations = import_folder(f'img/particles/{type}/')
		self.image = self.animations[self.frame_index]
		self.rect = self.image.get_rect(center = player.rect.center)

		if type == 'run':
			if self.facing == 1:
				self.rect = self.image.get_rect(bottomright = player.rect.midbottom)
			else:
				self.image = pygame.transform.flip(self.image, True, False)
				self.rect = self.image.get_rect(bottomleft = player.rect.midbottom)

		if type == 'jump':
			self.rect = self.image.get_rect(midbottom = player.rect.midbottom)	


	def animate(self, animation_type, direction_specific):
		animation = self.animations

		self.frame_index += self.frame_rate
		if animation_type == 'kill':
			if self.frame_index >= len(animation)-1:
				self.kill()

		elif animation_type == 'loop':
			if self.frame_index >= len(animation):
				self.frame_index = 0

		if direction_specific == 'yes':
			right_img = animation[int(self.frame_index)]
			if self.facing == 1:
				self.image = right_img
			else:
				left_img = pygame.transform.flip(right_img, True, False)
				self.image = left_img
		else:
			self.image = animation[int(self.frame_index)]
		
		
	def update(self):
		self.animate('kill', 'yes')

