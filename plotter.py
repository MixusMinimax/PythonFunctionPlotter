import pygame
from point import Point
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
RESOLUTION = 512
BACKGROUND = (220, 200, 240)
LINE_OFFSET = 32
MIN_X = 0
MAX_X = 10
MIN_Y = 0
MAX_Y = 10
DRAW_POINTS = False

# pygame
game_display = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('2D Function Plotter')
clock = pygame.time.Clock()
font = pygame.font.SysFont('Arial', 12)

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
	# coordinate system
	LINE_EXTEND = 8
	ARROW_SIZE = 8

	top = Point((LINE_OFFSET, LINE_OFFSET))
	right = Point((WIDTH - LINE_OFFSET, HEIGHT - LINE_OFFSET))
	bottom = Point((LINE_OFFSET, HEIGHT - LINE_OFFSET))

	game_display.fill(BACKGROUND)
	pygame.draw.line(game_display, BLACK,\
		top, (LINE_OFFSET, HEIGHT - LINE_OFFSET + LINE_EXTEND), 1)
	pygame.draw.line(game_display, BLACK,\
		(LINE_OFFSET - LINE_EXTEND, HEIGHT - LINE_OFFSET), right, 1)
	pygame.draw.polygon(game_display, BLACK,\
		[top - (0, ARROW_SIZE), top + (ARROW_SIZE / 2, 0), top - (ARROW_SIZE / 2, 0)])
	pygame.draw.polygon(game_display, BLACK,\
		[right - (0, ARROW_SIZE / 2), right + (ARROW_SIZE, 0), right + (0, ARROW_SIZE / 2)])

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
	points = []
	for i in range(RESOLUTION):
		x = i / (RESOLUTION - 1)
		y = map_range(function.sample(map_range(x, 0, 1, MIN_X, MAX_X)), MIN_Y, MAX_Y, 0, 1)
		points.append(uv_to_screen((x, y)))

	# draw graph
	pygame.draw.aalines(game_display, RED, False, points, 1)

	if DRAW_POINTS:
		for point in points:
			pygame.draw.circle(game_display, RED, point, 3)

	pygame.display.update()

def main():
	function = Cos(2 * (X() + 1.4)) + 1
	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()

		# logic
		update(function)
		clock.tick(60)

if __name__ == '__main__':
	main()
