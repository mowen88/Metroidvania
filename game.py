import pygame, sys, json
from menu import *
from ui import UI
from settings import *
from level import Level


class Game():
	def __init__(self):
		pygame.init()

		# self.load_load_data()
		# self.load_saved_gun_data()

		self.running = True
		self.playing = False
		self.actions = {'left': False, 'right': False, 'up': False, 'down': False, 'return': False, 'back': False, 'space': False, 'tab': False, 'z': False, 'escape': False, 'l': False}
		self.WIDTH = 960 
		self.HEIGHT = 540
		self.display = pygame.Surface((self.WIDTH, self.HEIGHT))
		self.screen = pygame.display.set_mode(((self.WIDTH, self.HEIGHT)))

		self.font_name = 'font/failed attempt.ttf'
		self.BLACK = (0,0,0)
		self.WHITE = (255, 255, 255)

		self.clock = pygame.time.Clock()

		# states
		self.main_menu = MainMenu(self)
		self.options = OptionsMenu(self)
		self.credits = CreditsMenu(self)
		self.reset = ResetMenu(self)
		self.current_menu = self.main_menu

		# constant player data
		self.save_point = load_data['save_point']
		self.max_health = 100
		self.current_health = 50
		self.current_weapon = None
		self.pickups_collected = None

		self.ui = UI(self.screen)
		self.level = Level(load_data['save_point'], 0, load_data['block_position'], load_data['current_gun'], False, self.screen, self.create_level)

	def create_level(self, new_level, entry_pos, new_block_position, current_gun, gun_showing):
		self.level = Level(new_level, entry_pos, new_block_position, current_gun, gun_showing, self.screen, self.create_level)
		self.level.gun_equipped()

	def game_loop(self):
		while self.playing:
			self.check_events()
			if self.actions['up']:
				self.level.player.jump()
			elif self.actions['space']:
				self.level.paused()
			elif self.actions['tab']:
				self.level.player.change_gun()
				self.level.show_new_gun()
			elif self.actions['z']:
				self.level.show_gun()
			elif self.actions['l']:
				self.level.load_point()
			self.level.run()
			print(load_data['save_point'])
			self.ui.show_health(50, 100)
			self.ui.show_current_weapon(self.current_weapon)
			if self.level.game_paused and self.actions['escape']:
				self.playing = False
				self.level.load_point()
			self.reset_keys()
			self.clock.tick(60)
			pygame.display.update()

	def check_events(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:

				# self.dump_gun_data()
			
				self.running = False
				self.playing = False
				self.current_menu.run_display = False
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_RETURN:
					self.actions['return'] = True
				if event.key == pygame.K_BACKSPACE:
					self.actions['back'] = True
				if event.key == pygame.K_UP:
					self.actions['up'] = True
				if event.key == pygame.K_DOWN:
					self.actions['down'] = True
				if event.key == pygame.K_SPACE:
					self.actions['space'] = True
				if event.key == pygame.K_TAB:
					self.actions['tab'] = True
				if event.key == pygame.K_z:
					self.actions['z'] = True
				if event.key == pygame.K_l:
					self.actions['l'] = True
				if event.key == pygame.K_ESCAPE:
					self.actions['escape'] = True

	def draw_text(self, text, size, pos):
		font = pygame.font.Font(self.font_name, size)
		text_surf = font.render(text, True, self.WHITE)
		text_rect = text_surf.get_rect(center = pos)
		self.display.blit(text_surf, text_rect)

	def reset_keys(self):
		for action in self.actions:
			self.actions[action] = False

	def load_saved_gun_data(self):
		with open('gun_data.txt') as gun_file:
			saved_gun_data = json.load(gun_file)

	def load_load_data(self):
		with open('progress_data.txt') as progress_file:
			load_data = json.load(progress_file)

	def dump_gun_data(self):
		with open('gun_data.txt', 'w') as gun_file:
			json.dump(saved_gun_data, gun_file)

	

if __name__ == "__main__":
	g = Game()
	while g.running:
		g.current_menu.display_menu()
		g.game_loop()





