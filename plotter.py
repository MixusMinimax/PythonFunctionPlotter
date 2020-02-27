import math
import pygame_textinput
import pygame
import re
from point import Point
import functions
from functions import *
from utils import *
pygame.init()

# colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# constants
WIDTH = 800
HEIGHT = 600
INPUT_HEIGHT = 50
RESOLUTION = 256
BACKGROUND = (220, 200, 240)
LINE_OFFSET = 32
MIN_X = -5
MAX_X = 5
MIN_Y = -1
MAX_Y = 6.5
DRAW_POINTS = False

# pygame
textinput = pygame_textinput.TextInput()

game_display = pygame.display.set_mode((WIDTH, HEIGHT + INPUT_HEIGHT))
pygame.display.set_caption('2D Function Plotter')
clock = pygame.time.Clock()
font = pygame.font.SysFont('Arial', 12)
font2 = pygame.font.SysFont('Arial', 16)

# images
text_x = font.render('X', True, BLACK)
text_y = font.render('Y', True, BLACK)

# functions
def uv_to_screen(point):
	copy = Point(point)
	copy.x = copy.x
	copy.y = 1 - copy.y
	copy = copy * (WIDTH - 2 * LINE_OFFSET, HEIGHT - 2 * LINE_OFFSET) + (LINE_OFFSET, LINE_OFFSET)
	return copy

def update(function):

	game_display.fill(BACKGROUND)

	# draw zero lines
	col = (150, 150, 150)
	if MIN_Y <= -0.1 and MAX_Y >= 0.1:
		y = map_range(0, MIN_Y, MAX_Y, 0, 1)
		pygame.draw.line(game_display, col, uv_to_screen((0, y)), uv_to_screen((1, y)), 1)

	if MIN_X <= -0.1 and MAX_X >= 0.1:
		x = map_range(0, MIN_X, MAX_X, 0, 1)
		pygame.draw.line(game_display, col, uv_to_screen((x, 0)), uv_to_screen((x, 1)), 1)

	# draw axes
	LINE_EXTEND = 8
	ARROW_SIZE = 8

	top = Point((LINE_OFFSET, LINE_OFFSET))
	right = Point((WIDTH - LINE_OFFSET, HEIGHT - LINE_OFFSET))
	bottom = Point((LINE_OFFSET, HEIGHT - LINE_OFFSET))

	pygame.draw.line(game_display, BLACK,\
		top, (LINE_OFFSET, HEIGHT - LINE_OFFSET + LINE_EXTEND), 1)
	pygame.draw.line(game_display, BLACK,\
		(LINE_OFFSET - LINE_EXTEND, HEIGHT - LINE_OFFSET), right, 1)
	pygame.draw.polygon(game_display, BLACK,\
		[top - (0, ARROW_SIZE), top + (ARROW_SIZE / 2, 0), top - (ARROW_SIZE / 2, 0)])
	pygame.draw.polygon(game_display, BLACK,\
		[right - (0, ARROW_SIZE / 2), right + (ARROW_SIZE, 0), right + (0, ARROW_SIZE / 2)])

	# draw marks
	first_line = int(math.ceil(MIN_Y + 0.2))
	last_line = int(math.floor(MAX_Y - 0.2))
	step = 1
	amount = int((last_line - first_line + 2) / step)
	while amount > 20:
		step *= 10
		amount = int((last_line - first_line + 2) / step)

	for i in range(amount):
		y = first_line + i * step
		v = map_range(y, MIN_Y, MAX_Y, 0, 1)
		screen_pos = uv_to_screen((0, v))
		pygame.draw.line(game_display, BLACK, screen_pos + (4, 0), screen_pos - (4, 0))
		text = font.render(str(y), True, BLACK)
		game_display.blit(text, screen_pos - (text.get_width() + 8, text.get_height() // 2))

	first_line = int(math.ceil(MIN_X + 0.2))
	last_line = int(math.floor(MAX_X - 0.2))
	step = 1
	amount = int((last_line - first_line + 2) / step)
	while amount > 20:
		step *= 10
		amount = int((last_line - first_line + 2) / step)

	for i in range(amount):
		x = first_line + i * step
		u = map_range(x, MIN_X, MAX_X, 0, 1)
		screen_pos = uv_to_screen((u, 0))
		pygame.draw.line(game_display, BLACK, screen_pos + (0, 4), screen_pos - (0, 4))
		text = font.render(str(x), True, BLACK)
		game_display.blit(text, screen_pos - (text.get_width() // 2, -8))

	# draw labels
	game_display.blit(text_y, top - (text_y.get_width() // 2, text_y.get_height() + 12))
	game_display.blit(text_x, right - (-12, text_x.get_height() // 2))

	text = font.render(str(MIN_Y), True, BLACK)
	game_display.blit(text, bottom - (text.get_width() + 8, text.get_height() // 2))
	text = font.render(str(MAX_Y), True, BLACK)
	game_display.blit(text, top - (text.get_width() + 8, text.get_height() // 2))

	text = font.render(str(MIN_X), True, BLACK)
	game_display.blit(text, bottom - (text.get_width() // 2, -8))
	text = font.render(str(MAX_X), True, BLACK)
	game_display.blit(text, right - (text.get_width() // 2, -8))

	# get points
	points_list = []
	points = []
	exceed = 0 # 1: top, 0: between, -1: bottom
	for i in range(RESOLUTION):
		x = i / (RESOLUTION - 1)
		try:
			y = map_range(function.sample(map_range(x, 0, 1, MIN_X, MAX_X)), MIN_Y, MAX_Y, 0, 1)
		except:
			y = None

		try:
			exceed_new = 1 if y > 1 else -1 if y < 0 else 0
		except:
			exceed_new = 0

		if y == None or exceed * exceed_new == -1:
			if len(points) != 0:
				points_list.append(points)
				points = []
		exceed = exceed_new
		try:
			points.append(uv_to_screen((x, y)))
		except:
			pass

		if i == RESOLUTION - 2 and len(points) != 0:
			points_list.append(points)

	# draw graph
	for points in points_list:
		pygame.draw.aalines(game_display, RED, False, points, True)

	if DRAW_POINTS:
		for point in points:
			pygame.draw.circle(game_display, RED, (int(point[0]), int(point[1])), 3)

	# draw function string
	text = font2.render('f(x) = {}'.format(function), True, BLACK)
	game_display.blit(text, Point((WIDTH - LINE_OFFSET, LINE_OFFSET))\
		- (text.get_width(), text.get_height() // 2))

def main():
	function = eval('(Exp(X()) + Exp(-X())) / 2 + Random(0) * 0.2')
	while True:
		events = pygame.event.get()
		for event in events:
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()

		# input
		if textinput.update(events):
			try:
				function = Function.parse(textinput.get_text())
			except Exception as e:
				print(e)
			
		# logic
		update(function)
		functions.time += 1
		game_display.blit(textinput.get_surface(), (10, HEIGHT + 10))
		pygame.display.update()
		clock.tick(60)

if __name__ == '__main__':
	main()
