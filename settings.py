# title
TITLE = 'PLATFORMER'

# framerate
FPS = 60

SCALE = 3
TILESIZE = 48
WIDTH = 960
HEIGHT = 540

# player variables
GOT_DOUBLE_JUMP = True
GOT_WALL_SLIDE = True
JUMP_HEIGHT = 16
TERMINAL_VELOCITY = 24
GOT_GUN = True

# colours
BLACK = (20,20,20)
WHITE = (245,245,245)

# fonts
FONT = 'font/failed attempt.ttf'

CAMERA_BORDERS = {
	'left': 400,
	'right': WIDTH - 400,
	'top': 200,
	'bottom': HEIGHT - 200
}

weapon_data = {
	'sword':{'cooldown': 100, 'damage': 15, 'img':'img/weapons/sword.png'},
	'lance':{'cooldown': 150, 'damage': 30, 'img':'img/weapons/sword.png'}
}

gun_data = {
	# 0:{'bullet_speed': 10, 'cooldown': 300, 'damage': 30, 'img':'img/bullets/bullet_0.png', 'gun_img':'img/pickups/gun/00.png'},
	# 1:{'bullet_speed': 60, 'cooldown': 100, 'damage': 50, 'img':'img/bullet s/bullet_2.png', 'gun_img':'img/pickups/blaster/00.png'},
	# 2:{'bullet_speed': 100, 'cooldown': 500, 'damage': 40, 'img':'img/bullets/bullet_1.png', 'gun_img':'img/pickups/rifle/00.png'}
}
saved_gun_data = {}

item_data = {}
saved_item_data = {}

load_data = {
	'save_point': 0,'entry pos': 0, 'block_position': (200, 400), 'current_gun': 0, 'gun_showing': True
}




levels = {
	0: {1:1, 2:1, 3:0, 4:0, 5:0, 'level_name':'Purple level'},
	1: {1:0, 2:0, 3:2, 4:2, 5:0, 'level_name':'Orange level'},
	2: {1:4, 2:0, 3:1, 4:1, 5:3, 'level_name':'Blue level'},
	3: {1:2, 2:0, 3:0, 4:0, 5:2, 'level_name':'Green level'},
	4: {1:2, 2:0, 3:0, 4:0, 5:0, 'level_name':'save level'}
}


exits = {
	0:0, 1:1, 2:1
}

enemy_data = {
	'guard': {'health': 100, 'exp': 100, 'damage': 20, 'attack_type': 'slash', 'attack_sound':'audio/attack/slash.wav', 'speed': 3, 'resistance': 3, 'attack_distance': 80, 'alert_distance': 360}
}