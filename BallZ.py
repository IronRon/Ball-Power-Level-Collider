import pygame
import pymunk
import pymunk.pygame_util
import math
import random

pygame.init()

WIDTH, HEIGHT = 1000, 1000
window = pygame.display.set_mode((WIDTH, HEIGHT))

def create_boundaries(space, width, height):
	rects = [
		[(width/2, height - 10), (width, 20)],
		[(width/2, 10), (width, 20)],
		[(10, height/2), (20, height)],
		[(width - 10, height/2), (20, height)]
	]

	for pos, size in rects:
		body = pymunk.Body(body_type=pymunk.Body.STATIC)
		body.position = pos
		shape = pymunk.Poly.create_box(body, size)
		shape.elasticity = 0.4
		shape.friction = 0.5
		space.add(body, shape)

def create_ball(space, radius, mass, pos, power, color = (255, 0, 0, 100)):
	body = pymunk.Body()
	body.position = pos
	shape = pymunk.Circle(body, radius)
	shape.mass = mass
	shape.elasticity = 0.9
	shape.friction = 0.4
	shape.color = color
	shape.power = power
	space.add(body, shape)
	return shape

def draw_text(window, text, position, font_size=20):
    font = pygame.font.Font(None, font_size)
    text_surface = font.render(str(text), True, (0, 0, 0))
    text_rect = text_surface.get_rect(center=position)
    window.blit(text_surface, text_rect)

def draw(space, window, draw_options, balls):
	window.fill("white")
	space.debug_draw(draw_options)

	for ball in balls:
		if hasattr(ball, 'power'):
			pos = pymunk.pygame_util.to_pygame(ball.body.position, window)
			draw_text(window, str(ball.power), pos, 20)    

	pygame.display.update()

def create_team(space, width_start, width_end, height, balls, power_level, color):
	while power_level > 0:
		power = random.randint(1, power_level)
		mass = power // 2 if power > 2 else power
		ball = create_ball(space, power + 10, power, (random.randint(width_start, width_end), random.randint(20, height//2)), power, color)
		balls.append(ball)
		power_level -= power

	
def run(window, width, height):
	run = True
	clock = pygame.time.Clock()
	fps = 60
	dt = 1 / fps

	space = pymunk.Space()
	space.gravity = (0, 981)

	create_boundaries(space, width, height)
	draw_options = pymunk.pygame_util.DrawOptions(window)

	balls = []
	create_team(space, 20, width//2, height, balls, 70, (255, 0, 0, 100))
	create_team(space, width//2, width-20, height, balls, 50, (0, 255, 0, 100))

	while run:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False
				break

			if event.type == pygame.MOUSEBUTTONDOWN:
				x, y = pygame.mouse.get_pos()
				ball = create_ball(space, 30, 10, [x, y], 100)
				balls.append(ball)

		draw(space, window, draw_options, balls)
		space.step(dt)
		clock.tick(fps)

	pygame.quit()

if __name__ == "__main__":
	run(window, WIDTH, HEIGHT)