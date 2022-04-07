import pygame
from settings import *

class LevelIntro:
	def __init__(self, new_level, msg, surf):

		#setup
		self.display_surf = surf
		self.new_level = new_level

		self.font = pygame.font.Font(FONT, 40)
		self.text_surf = self.font.render(str(msg), True, 'WHITE')
		self.text_rect = self.text_surf.get_rect(center = (WIDTH //2, HEIGHT // 2))

		#self.entry_pos = entry_pos
		#self.current_level = exits[entry_pos]

	def input(self):
		keys = pygame.key.get_pressed()
		pass

		#if keys[pygame.K_SPACE]:
			#self.current_level +=1

	def run(self):
		self.display_surf.blit(self.text_surf, self.text_rect)
		self.input()

class Pause:
	def __init__(self, msg, surf):

		#setup
		self.display_surf = surf

		self.font = pygame.font.Font(FONT, 40)
		self.text_surf = self.font.render(str(msg), True, 'WHITE')
		self.text_rect = self.text_surf.get_rect(center = (WIDTH //2, HEIGHT // 2))

		#self.entry_pos = entry_pos
		#self.current_level = exits[entry_pos]

	def input(self):
		keys = pygame.key.get_pressed()
		pass

		#if keys[pygame.K_SPACE]:
			#self.current_level +=1

	def run(self):
		self.display_surf.blit(self.text_surf, self.text_rect)
		self.input()

class Transition:
	def __init__(self, surf):

		self.counter = 0
		self.display_surf = surf
		
	def run(self):
		self.counter += 10
		for y in range(0,10,2):
			pygame.draw.rect(self.display_surf , BLACK, (WIDTH, y * HEIGHT // 10, WIDTH - self.counter, HEIGHT // 9))
			pygame.draw.rect(self.display_surf , BLACK, (WIDTH, (y + 1) * HEIGHT // 10, 0 + self.counter, HEIGHT // 9))
		#print(self.counter)

# class PauseMenu:
# 	def __init__(self, surf):

# 		#setup
# 		self.index = 'Resume'
# 		self.display_surf = surf
# 		self.can_move = True
# 		self.cursor_rect = pygame.Rect(0,0, 30, 30)
# 		self.offset = - 120

# 		self.font = 'font/failed attempt.ttf'

# 		self.resume_x = self.display_surf.get_width() // 2
# 		self.resume_y = self.display_surf.get_height() // 2 + 30
# 		self.quit_x = self.display_surf.get_width() // 2
# 		self.quit_y = self.display_surf.get_height() // 2 + 60
# 		self.cursor_rect.midtop = (self.resume_x + self.offset, self.resume_y)

# 	def draw_text(self, text, size, pos):
# 		font = pygame.font.Font(self.font, size)
# 		text_surf = font.render(text, True, WHITE)
# 		text_rect = text_surf.get_rect(center = pos)
# 		self.display_surf.blit(text_surf, text_rect)

# 	def draw_cursor(self):
# 		self.draw_text('*', 15, (self.cursor_rect.x, self.cursor_rect.y))

# 	def blit_screen(self, surf):
# 		self.display_surf.blit(surf, (0, 0))
# 		pygame.display.update()

# 	def input(self):
# 		keys = pygame.key.get_pressed()

# 		if self.can_move:
# 			if keys[pygame.K_UP] or keys[pygame.K_DOWN]:
# 				if self.index == 'Resume':
# 					self.index = 'Quit'
# 					self.cursor_rect.midtop = (self.quit_x + self.offset, self.quit_y)
# 					self.selection_time = pygame.time.get_ticks()
# 					self.can_move = False
# 				elif self.index == 'Quit':
# 					self.index = 'Resume'
# 					self.cursor_rect.midtop = (self.resume_x + self.offset, self.resume_y)
# 					self.selection_time = pygame.time.get_ticks()
# 					self.can_move = False

# 		if keys[pygame.K_RETURN]:
# 			if self.index == 'Resume':
# 				self.kill()
# 			elif self.index == 'Quit':
# 				pass

# 	def selection_cooldown(self):
# 		if not self.can_move:
# 			current_time = pygame.time.get_ticks()
# 			if current_time - self.selection_time >= 300:
# 				self.can_move = True

# 	def run(self):
# 		self.selection_cooldown()
# 		self.input()
# 		self.display_surf.fill(BLACK)
# 		self.draw_text('Paused', 50, (self.display_surf.get_width() // 2, self.display_surf.get_height() // 2 - 30))
# 		self.draw_text('Resume', 30, (self.resume_x, self.resume_y))
# 		self.draw_text('Quit', 30, (self.quit_x, self.quit_y))
# 		self.draw_cursor()
# 		self.blit_screen(self.display_surf)








		


