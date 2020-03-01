import pygame
import pygame_textinput
from plotter import Plotter

def main():
	WIDTH = 800
	HEIGHT = 600
	INPUT_HEIGHT = 50
	VERBOSE = True

	game_display = pygame.display.set_mode((WIDTH, HEIGHT + INPUT_HEIGHT))
	pygame.display.set_caption('2D Function Plotter')

	clock = pygame.time.Clock()
	p = Plotter((WIDTH, HEIGHT), verbose=VERBOSE)
	textinput = pygame_textinput.TextInput(initial_string='(exp(x) + exp(-x)) / 2 + random(x) * 0.2')
	p.set_function(textinput.get_text())

	while True:
		events = pygame.event.get()
		for event in events:
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()

		# input
		if textinput.update(events):
			p.set_function(textinput.get_text())
			
		# logic
		p.update(1/60)
		game_display.fill((200, 200, 200))
		game_display.blit(p.get_surface(), (0, 0))
		game_display.blit(textinput.get_surface(), (10, HEIGHT + 10))
		pygame.display.update()
		clock.tick(60)

if __name__ == '__main__':
	main()