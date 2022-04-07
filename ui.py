import pygame
from settings import *
from player import Player

class UI:
	def __init__(self, surf):

		self.display_surf = surf
		self.health_bar = pygame.Surface((320,24))
		self.current_weapon = pygame.image.load('img/pickups/rifle/00.png').convert_alpha()
		self.current_weapon = pygame.transform.scale(self.current_weapon, (self.current_weapon.get_width() * SCALE, self.current_weapon.get_height() * SCALE))

		self.font = pygame.font.Font(FONT, 24)

	def show_health(self, current, full):
		self.display_surf.blit(self.health_bar,(24,24))

	def show_current_weapon(self, weapon_type):
		self.weapon_type = weapon_type
		self.display_surf.blit(self.current_weapon,(24,48))
		self.text_surf = self.font.render(str('Type'), True, 'WHITE')
		self.text_rect = self.text_surf.get_rect()
		self.display_surf.blit(self.text_surf,(80,48))

	