import pygame, json

from ui import UI
from level import Level
from settings import *

class Menu():
	def __init__(self, game):
		self.game = game
		self.center_x = self.game.WIDTH //2
		self.center_y = self.game.HEIGHT // 2
		self.run_display = True
		self.cursor_rect = pygame.Rect(0,0, 30, 30)
		self.offset = - 120

	def draw_cursor(self):
		self.game.draw_text('*', 15, (self.cursor_rect.x, self.cursor_rect.y))

	def blit_screen(self):
		self.game.screen.blit(self.game.display, (0, 0))
		pygame.display.update()
		self.game.reset_keys()

class MainMenu(Menu):
	def __init__(self, game):
		Menu.__init__(self, game)
		self.state = "Load Game"

		self.loadgame_x = self.center_x
		self.loadgame_y = self.center_y + 30

		self.reset_x = self.center_x
		self.reset_y = self.center_y + 60

		self.options_x = self.center_x
		self.options_y = self.center_y + 90

		self.credits_x = self.center_x
		self.credits_y = self.center_y + 120

		self.cursor_rect.midtop = (self.loadgame_x + self.offset, self.loadgame_y)

	def display_menu(self):
		self.run_display = True
		while self.run_display:
			self.game.check_events()
			self.check_input()
			self.game.display.fill(self.game.BLACK)
			self.game.draw_text('Main Menu', 50, (self.game.WIDTH // 2, self.game.HEIGHT // 2 - 30))
			self.game.draw_text('Load Game', 30, (self.loadgame_x, self.loadgame_y))
			self.game.draw_text('Reset', 30, (self.reset_x, self.reset_y))
			self.game.draw_text('Options', 30, (self.options_x, self.options_y))
			self.game.draw_text('Credits', 30, (self.credits_x, self.credits_y))
			self.draw_cursor()
			self.blit_screen()

	def move_cursor(self):
		if self.game.actions['down']:
			if self.state == 'Load Game':
				self.cursor_rect.midtop = (self.reset_x + self.offset, self.reset_y)
				self.state = 'Reset'
			elif self.state == 'Reset':
				self.cursor_rect.midtop = (self.options_x + self.offset, self.options_y)
				self.state = 'Options'
			elif self.state == 'Options':
				self.cursor_rect.midtop = (self.credits_x + self.offset, self.credits_y)
				self.state = 'Credits'
			elif self.state == 'Credits':
				self.cursor_rect.midtop = (self.loadgame_x + self.offset, self.loadgame_y)
				self.state = 'Load Game'

		if self.game.actions['up']:
			if self.state == 'Load Game':
				self.cursor_rect.midtop = (self.credits_x + self.offset, self.credits_y)
				self.state = 'Credits'
			elif self.state == 'Credits':
				self.cursor_rect.midtop = (self.options_x + self.offset, self.options_y)
				self.state = 'Options'
			elif self.state == 'Options':
				self.cursor_rect.midtop = (self.reset_x + self.offset, self.reset_y)
				self.state = 'Reset'
			elif self.state == 'Reset':
				self.cursor_rect.midtop = (self.loadgame_x + self.offset, self.loadgame_y)
				self.state = 'Load Game'

	def check_input(self):
		self.move_cursor()
		if self.game.actions['return']:
			if self.state == 'Load Game':
				self.game.playing = True
			elif self.state == 'Reset':
				self.game.current_menu = self.game.reset
				# self.game.current_menu = self.game.reset
			elif self.state == 'Options':
				self.game.current_menu = self.game.options
			elif self.state == 'Credits':
				self.game.current_menu = self.game.credits
			self.run_display = False

class ResetMenu(Menu):
	def __init__(self, game):
		Menu.__init__(self, game)
		self.state = 'ok'
		self.ok_x = self.center_x
		self.ok_y = self.center_y + 30
		self.cancel_x = self.center_x
		self.cancel_y = self.center_y + 60
		self.cursor_rect.midtop = (self.ok_x + self.offset, self.ok_y)

	def display_menu(self):
		self.run_display = True
		while self.run_display:
			self.game.check_events()
			self.check_input()
			self.game.display.fill(self.game.BLACK)
			self.game.draw_text('Reset all data and start new game?', 50, (self.game.WIDTH // 2, self.game.HEIGHT // 2 - 30))
			self.game.draw_text('OK', 30, (self.ok_x, self.ok_y))
			self.game.draw_text('Cancel', 30, (self.cancel_x, self.cancel_y))
			self.draw_cursor()
			self.blit_screen()

	def check_input(self):
		if self.game.actions['back']:
			self.game.current_menu = self.game.main_menu
			self.run_display = False

		elif self.game.actions['up'] or self.game.actions['down']:
			if self.state == 'ok':
				self.state = 'cancel'
				self.cursor_rect.midtop = (self.cancel_x + self.offset, self.cancel_y)
			elif self.state == 'cancel':
				self.state = 'ok'
				self.cursor_rect.midtop = (self.ok_x + self.offset, self.ok_y)

		elif self.game.actions['return']:
			if self.state == 'ok':
				gun_data.clear()
				self.game.level = Level(0, 0, (200, 400), 0, False, self.game.screen, self.game.create_level)
				load_data.update({'save_point': 0, 'gun_showing': False, 'current_gun': 0})
				

				
				self.game.current_menu = self.game.main_menu
				self.run_display = False
			elif self.state == 'cancel':
				self.game.current_menu = self.game.main_menu
				self.run_display = False


class OptionsMenu(Menu):
	def __init__(self, game):
		Menu.__init__(self, game)
		self.state = 'Volume'
		self.vol_x = self.center_x
		self.vol_y = self.center_y + 30
		self.controls_x = self.center_x
		self.controls_y = self.center_y + 60
		self.cursor_rect.midtop = (self.vol_x + self.offset, self.vol_y)

	def display_menu(self):
		self.run_display = True
		while self.run_display:
			self.game.check_events()
			self.check_input()
			self.game.display.fill(self.game.BLACK)
			self.game.draw_text('Options', 50, (self.game.WIDTH // 2, self.game.HEIGHT // 2 - 30))
			self.game.draw_text('Volume', 30, (self.vol_x, self.vol_y))
			self.game.draw_text('Controls', 30, (self.controls_x, self.controls_y))
			self.draw_cursor()
			self.blit_screen()

	def check_input(self):
		if self.game.actions['back']:
			self.game.current_menu = self.game.main_menu
			self.run_display = False

		elif self.game.actions['up'] or self.game.actions['down']:
			if self.state == 'Volume':
				self.state = 'Controls'
				self.cursor_rect.midtop = (self.controls_x + self.offset, self.controls_y)
			elif self.state == 'Controls':
				self.state = 'Volume'
				self.cursor_rect.midtop = (self.vol_x + self.offset, self.vol_y)

		elif self.game.actions['return']:
			# create controls and volume menus
			pass

class CreditsMenu(Menu):
	def __init__(self, game):
		Menu.__init__(self, game)

	def display_menu(self):
		self.run_display = True
		while self.run_display:
			self.game.check_events()
			if self.game.actions['return'] or self.game.actions['back']:
				self.game.current_menu = self.game.main_menu
				self.run_display = False
			self.game.display.fill(self.game.BLACK)
			self.game.draw_text('Credits', 50, (self.game.WIDTH // 2, self.game.HEIGHT // 2 - 30))
			self.game.draw_text('Made by Matthew Owen', 30, (self.game.WIDTH // 2, self.game.HEIGHT // 2 + 20))
			self.blit_screen()

class PauseMenu(Menu):
	def __init__(self, game):
		Menu.__init__(self, game)
		self.state = 'Resume'
		self.resume_x = self.center_x
		self.resume_y = self.center_y + 30
		self.quit_x = self.center_x
		self.quit_y = self.center_y + 60
		self.cursor_rect.midtop = (self.resume_x + self.offset, self.resume_y)

	def display_menu(self):
		self.run_display = True
		while self.run_display:
			self.game.check_events()
			self.check_input()
			self.game.display.fill(self.game.BLACK)
			self.game.draw_text('Paused', 50, (self.game.WIDTH // 2, self.game.HEIGHT // 2 - 30))
			self.game.draw_text('Resume', 30, (self.resume_x, self.resume_y))
			self.game.draw_text('Quit', 30, (self.quit_x, self.quit_y))
			self.draw_cursor()
			self.blit_screen()

	def check_input(self):
		if self.game.BACK:
			self.run_display = False

		elif self.game.UP or self.game.DOWN:
			if self.state == 'Resume':
				self.state = 'Quit'
				self.cursor_rect.midtop = (self.quit_x + self.offset, self.quit_y)
			elif self.state == 'Quit':
				self.state = 'Resume'
				self.cursor_rect.midtop = (self.resume_x + self.offset, self.resume_y)

		elif self.game.GO:
			if self.state == 'Resume':
				self.run_display = False
			elif self.state == 'Quit':
				self.game.running = False
				self.game.current_menu = self.game.main_menu


			# create controls and volume menus
			pass













