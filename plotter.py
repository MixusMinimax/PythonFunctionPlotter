import math
import pygame_textinput
import pygame
import re
import functions
from utils import *
from collections import abc
pygame.init()

# colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# fonts
font = pygame.font.SysFont('Arial', 12)
font2 = pygame.font.SysFont('Arial', 16)

# images
text_x = font.render('X', True, BLACK)
text_y = font.render('Y', True, BLACK)

class Plotter:

	def __init__(self, size, initial_function=None, resolution=256, line_offset=32,\
		x_range=(-5, 5), y_range=(-1, 6.5),\
		draw_points=False, verbose=True):
		if not isinstance(size, abc.Iterable) or len(size) != 2: raise TypeError
		self.size = size
		self.image = pygame.Surface(size, pygame.SRCALPHA)
		self.function = functions.parse(initial_function)
		self.current_time = 0
		self.VERBOSE = verbose

		self.RESOLUTION = resolution
		self.LINE_OFFSET = line_offset
		self.X_RANGE = x_range
		self.Y_RANGE = y_range
		self.DRAW_POINTS = draw_points

	def uv_to_screen(self, point):
		copy = Point(point)
		copy.x = copy.x
		copy.y = 1 - copy.y
		copy = copy * (self.size[0] - 2 * self.LINE_OFFSET, self.size[1] - 2 * self.LINE_OFFSET)\
		+ (self.LINE_OFFSET, self.LINE_OFFSET)
		return copy

	def get_surface(self):
		return self.image

	def set_function(self, f):
		f = functions.parse(f, verbose=self.VERBOSE)
		if f:
			self.function = f

	def update(self, dt):
		self.image.fill((0, 0, 0, 0))

		self.current_time += dt
		function = self.function
		functions.current_time = self.current_time

		# copy readonly attributes into the scope of this function

		RESOLUTION = self.RESOLUTION
		LINE_OFFSET = self.LINE_OFFSET
		MIN_X = self.X_RANGE[0]
		MAX_X = self.X_RANGE[1]
		MIN_Y = self.Y_RANGE[0]
		MAX_Y = self.Y_RANGE[1]
		DRAW_POINTS = self.DRAW_POINTS

		# draw zero lines
		col = (150, 150, 150)
		if MIN_Y <= -0.1 and MAX_Y >= 0.1:
			y = map_range(0, MIN_Y, MAX_Y, 0, 1)
			pygame.draw.line(self.image, col, self.uv_to_screen((0, y)), self.uv_to_screen((1, y)), 1)

		if MIN_X <= -0.1 and MAX_X >= 0.1:
			x = map_range(0, MIN_X, MAX_X, 0, 1)
			pygame.draw.line(self.image, col, self.uv_to_screen((x, 0)), self.uv_to_screen((x, 1)), 1)

		# draw axes
		LINE_EXTEND = 8
		ARROW_SIZE = 8

		top = Point((LINE_OFFSET, LINE_OFFSET))
		right = Point((self.size[0] - LINE_OFFSET, self.size[1] - LINE_OFFSET))
		bottom = Point((LINE_OFFSET, self.size[1] - LINE_OFFSET))

		pygame.draw.line(self.image, BLACK,\
			top, (LINE_OFFSET, self.size[1] - LINE_OFFSET + LINE_EXTEND), 1)
		pygame.draw.line(self.image, BLACK,\
			(LINE_OFFSET - LINE_EXTEND, self.size[1] - LINE_OFFSET), right, 1)
		pygame.draw.polygon(self.image, BLACK,\
			[top - (0, ARROW_SIZE), top + (ARROW_SIZE / 2, 0), top - (ARROW_SIZE / 2, 0)])
		pygame.draw.polygon(self.image, BLACK,\
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
			screen_pos = self.uv_to_screen((0, v))
			pygame.draw.line(self.image, BLACK, screen_pos + (4, 0), screen_pos - (4, 0))
			text = font.render(str(y), True, BLACK)
			self.image.blit(text, screen_pos - (text.get_width() + 8, text.get_height() // 2))

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
			screen_pos = self.uv_to_screen((u, 0))
			pygame.draw.line(self.image, BLACK, screen_pos + (0, 4), screen_pos - (0, 4))
			text = font.render(str(x), True, BLACK)
			self.image.blit(text, screen_pos - (text.get_width() // 2, -8))

		# draw labels
		self.image.blit(text_y, top - (text_y.get_width() // 2, text_y.get_height() + 12))
		self.image.blit(text_x, right - (-12, text_x.get_height() // 2))

		text = font.render(str(MIN_Y), True, BLACK)
		self.image.blit(text, bottom - (text.get_width() + 8, text.get_height() // 2))
		text = font.render(str(MAX_Y), True, BLACK)
		self.image.blit(text, top - (text.get_width() + 8, text.get_height() // 2))

		text = font.render(str(MIN_X), True, BLACK)
		self.image.blit(text, bottom - (text.get_width() // 2, -8))
		text = font.render(str(MAX_X), True, BLACK)
		self.image.blit(text, right - (text.get_width() // 2, -8))

		if not function:
			return

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
				if len(points) > 1:
					points_list.append(points)
					points = []
			exceed = exceed_new
			try:
				points.append(self.uv_to_screen((x, y)))
			except:
				pass

			if i == RESOLUTION - 2 and len(points) > 1:
				points_list.append(points)

		# draw graph
		for points in points_list:
			pygame.draw.aalines(self.image, RED, False, points, True)

		if DRAW_POINTS:
			for point in points:
				pygame.draw.circle(self.image, RED, (int(point[0]), int(point[1])), 3)

		# draw function string
		text = font2.render('f(x) = {}'.format(function), True, BLACK)
		self.image.blit(text, Point((self.size[0] - LINE_OFFSET, LINE_OFFSET))\
			- (text.get_width(), text.get_height() // 2))