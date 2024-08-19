import pygame
import pymunk
import pymunk.pygame_util
import math
import random

from Camera import Camera
from Constants import WIDTH, HEIGHT, GAME_WIDTH, GAME_HEIGHT

pygame.init()

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

def create_ball(space, radius, mass, pos, power, team_id, color = (255, 0, 0, 100)):
	body = pymunk.Body()
	body.position = pos
	shape = pymunk.Circle(body, radius)
	shape.mass = mass
	shape.elasticity = 0.9
	shape.friction = 0.4
	shape.color = color
	shape.power = power
	shape.team_id = team_id
	space.add(body, shape)
	return shape

def draw_text(window, text, position, font_size=20):
    font = pygame.font.Font(None, font_size)
    text_surface = font.render(str(text), True, (0, 0, 0))
    text_rect = text_surface.get_rect(center=position)
    window.blit(text_surface, text_rect)

def draw(space, window, draw_options, balls, multipliers, camera):
    window.fill("white")
	# Transform the drawing options based on the camera's position
    draw_options.transform = pymunk.Transform(tx=-camera.camera.x, ty=-camera.camera.y)
    space.debug_draw(draw_options)
    for ball in balls:
        if camera.camera.colliderect(ball.body.position.x - ball.radius, ball.body.position.y - ball.radius, ball.radius * 2, ball.radius * 2):
            pos = pymunk.pygame_util.to_pygame(ball.body.position, window)
            draw_text(window, str(ball.power), (pos[0] - camera.camera.x, pos[1] - camera.camera.y), 20)
		
    for multiplier in multipliers:
        if camera.camera.colliderect(multiplier.body.position.x - multiplier.radius, multiplier.body.position.y - multiplier.radius, multiplier.radius * 2, multiplier.radius * 2):
            pos = pymunk.pygame_util.to_pygame(multiplier.body.position, window)
            draw_text(window, str(multiplier.multiple), (pos[0] - camera.camera.x, pos[1] - camera.camera.y), 20)
			
    pygame.display.update()

def create_team(space, width_start, width_end, height, balls, power_level, color, team_id):
	while power_level > 0:
		if power_level > 6:
			pwr1 = power_level // 2
			power = random.randint(1, pwr1)
			mass = power // 2 if power > 2 else power
			ball = create_ball(space, power + 10, power, (random.randint(width_start, width_end), random.randint(20, height//3)), power, team_id, color)
			balls.append(ball)
			power_level -= power
		else:
			power = random.randint(1, power_level)
			mass = power // 2 if power > 2 else power
			ball = create_ball(space, power + 10, power, (random.randint(width_start, width_end), random.randint(20, height//3)), power, team_id, color)
			balls.append(ball)
			power_level -= power

def update_ball_properties(shape, space):
    new_mass = shape.power // 2 if shape.power > 2 else shape.power
    new_radius = shape.power + 10
    
    # Update the shape's body mass and moment of inertia
    shape.body.mass = new_mass
    shape.body.moment = pymunk.moment_for_circle(new_mass, 0, new_radius, (0, 0))

    shape.unsafe_set_radius(new_radius)

def collision_handler(arbiter, space, data):
	shape_a, shape_b = arbiter.shapes
	if hasattr(shape_a, 'team_id') and hasattr(shape_b, 'team_id'):
		if shape_a.team_id != shape_b.team_id:
			# Calculate the minimum power between the two shapes
			min_power = min(shape_a.power, shape_b.power)
			# Subtract the minimum power from both shapes' power
			shape_a.power -= min_power
			shape_b.power -= min_power

			# Check if either shape's power is now zero or less; if so, remove it
			if shape_a.power <= 0:
				space.remove(shape_a, shape_a.body)  # Remove both shape and body
				data['balls'].remove(shape_a)
			else:
				update_ball_properties(shape_a, space)

			if shape_b.power <= 0:
				space.remove(shape_b, shape_b.body)
				data['balls'].remove(shape_b)
			else:
				update_ball_properties(shape_b, space)

	elif hasattr(shape_a, 'team_id') and hasattr(shape_b, 'multiple'):
		shape_a.power *= shape_b.multiple
		space.remove(shape_b, shape_b.body)
		data['multipliers'].remove(shape_b)
		update_ball_properties(shape_a, space)

	elif hasattr(shape_b, 'team_id') and hasattr(shape_a, 'multiple'):
		shape_b.power *= shape_a.multiple
		space.remove(shape_a, shape_a.body)
		data['multipliers'].remove(shape_a)
		update_ball_properties(shape_b, space)
	
	return True

def create_obstacle(space, pos, size, elasticity=0.5, friction=0.5):
    """ Creates a rectangular obstacle in the space at a given position and size. """
    body = pymunk.Body(body_type=pymunk.Body.STATIC)
    body.position = pos
    shape = pymunk.Poly.create_box(body, size)
    shape.elasticity = elasticity
    shape.friction = friction
    space.add(body, shape)
    return shape

def create_circular_obstacle(space, pos, radius, elasticity=0.5, friction=0.5):
    body = pymunk.Body(body_type=pymunk.Body.STATIC)
    body.position = pos
    shape = pymunk.Circle(body, radius)
    shape.elasticity = elasticity
    shape.friction = friction
    space.add(body, shape)
    return shape

def create_slope(space, vertices, pos, elasticity=0.5, friction=0.5):
    """ Creates a slanted rectangle or slope with given vertices and position. """
    body = pymunk.Body(body_type=pymunk.Body.STATIC)
    body.position = pos
    transformed_vertices = [(x + pos[0], y + pos[1]) for x, y in vertices]
    shape = pymunk.Poly(body, transformed_vertices)
    shape.elasticity = elasticity
    shape.friction = friction
    space.add(body, shape)
    return shape

def multiplier(space, pos, radius, multiple, elasticity=0.5, friction=0.5):
	body = pymunk.Body(body_type=pymunk.Body.STATIC)
	body.position = pos
	shape = pymunk.Circle(body, radius)
	shape.elasticity = elasticity
	shape.friction = friction
	shape.multiple = multiple
	shape.color = (0, 0, 255, 100)
	space.add(body, shape)
	return shape
	
def run(window, width, height):
	run = True
	clock = pygame.time.Clock()
	fps = 60
	dt = 1 / fps

	space = pymunk.Space()
	space.gravity = (0, 981)

	create_boundaries(space, width, height)
	draw_options = pymunk.pygame_util.DrawOptions(window)

    # Obstacle Course
	create_obstacle(space, (240, 1500), (200, 20))  # Middle platform
	#create_circular_obstacle(space, (100, 1400), 30)  # Small circular obstacle
	create_circular_obstacle(space, (380, 1350), 20)  # Large circular obstacle
	create_slope(space, [(0, 20), (20, 0), (20, 80)], (140, 1200))  # Slope

    # Final Challenge
	create_obstacle(space, (240, 800), (250, 5))  # Upper platform
	create_slope(space, [(0, 0), (10, 0), (20, 30), (30, 30)], (100, 600))  # Steep slope
	create_slope(space, [(0, 0), (-10, 0), (-20, 30), (-30, 30)], (140, 600))  # Inverse steep slope

	multipliers = []
	#multiplier(space, (100, 1400), 30, 3)
	multipliers.append(multiplier(space, (width // 2, 1250), 10, 3))

	balls = []
	create_team(space, 20, width//2, height, balls, 70, (255, 0, 0, 100), 1)
	create_team(space, width//2, width-20, height, balls, 50, (0, 255, 0, 100), 2)

	# setting up the collision handler
	handler = space.add_collision_handler(0, 0)
	handler.begin = collision_handler
	handler.data['balls'] = balls  # Pass the list of balls into the handler
	handler.data['multipliers'] = multipliers

	camera = Camera(GAME_WIDTH, HEIGHT)

	while run:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False
				break

			# if event.type == pygame.MOUSEBUTTONDOWN:
			# 	x, y = pygame.mouse.get_pos()
			# 	ball = create_ball(space, 30, 10, [x, y], 100)
			# 	balls.append(ball)

		# Handle keyboard presses for camera control
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_UP:  # Arrow up
				camera.move_up(20)
			elif event.key == pygame.K_DOWN:  # Arrow down
				camera.move_down(20)
				#print(camera.camera.y)

		draw(space, window, draw_options, balls, multipliers, camera)
		space.step(dt)
		clock.tick(fps)

	pygame.quit()

if __name__ == "__main__":
	run(window, WIDTH, GAME_HEIGHT)