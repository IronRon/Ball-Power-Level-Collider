import math
import pygame
import time
import sys
from ball import Ball
from obstacle import Obstacle

pygame.init()

# Set up the screen
width, height = 640, 480
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()

# Create a group for all sprites
all_sprites_list = pygame.sprite.Group()

# Create an instance of Ball and add it to the sprite group
ball = Ball((255, 0, 0), 10, 0)
ball.rect.x = 100
ball.rect.y = 100
ball2 = Ball((0, 255, 0), 5, 1, [1,4])
ball2.rect.x = 200
ball2.rect.y = 200
# Adding new balls
ball3 = Ball((255, 0, 0), 8, 0, [2, -3])
ball3.rect.x = 300
ball3.rect.y = 100
ball4 = Ball((0, 255, 0), 7, 1, [-2, 2])
ball4.rect.x = 400
ball4.rect.y = 300
ball5 = Ball((255, 0, 0), 6, 0, [3, 1])
ball5.rect.x = 500
ball5.rect.y = 400

# Add all balls to the sprite group
all_sprites_list.add(ball, ball2, ball3, ball4, ball5)

def resolve_collision(ball1, ball2):
    # Calculate the difference in positions
    dx = ball1.rect.centerx - ball2.rect.centerx
    dy = ball1.rect.centery - ball2.rect.centery
    
    # Calculate distance between balls
    distance = math.sqrt(dx**2 + dy**2)
    if distance == 0:
        return  # Prevent division by zero
    
    # Normalize the difference
    dx /= distance
    dy /= distance
    
    # Calculate velocity components along the normal
    v1n = dx * ball1.velocity[0] + dy * ball1.velocity[1]
    v2n = dx * ball2.velocity[0] + dy * ball2.velocity[1]
    
    # Swap the velocity components
    ball1.velocity[0] += -v1n * dx + v2n * dx
    ball1.velocity[1] += -v1n * dy + v2n * dy
    ball2.velocity[0] += -v2n * dx + v1n * dx
    ball2.velocity[1] += -v2n * dy + v1n * dy

    # Move balls out of overlap
    if distance < (ball1.radius + ball2.radius):
        overlap = 0.5 * (distance - (ball1.radius + ball2.radius))
        ball1.rect.x -= overlap * dx
        #ball1.rect.y -= overlap * dy
        ball2.rect.x += overlap * dx
        #ball2.rect.y += overlap * dy

    if ball1.team != ball2.team:
        temp = ball1.value
        ball1.value -= ball2.value
        ball2.value -= temp


def handle_obstacle_collision(ball, obstacle):
    # Simple reflection logic: reverse velocity
    ball.velocity[0] = -ball.velocity[0]
    ball.velocity[1] = -ball.velocity[1]

    # Move the ball back a bit to prevent sticking to the obstacle
    ball.rect.x += ball.velocity[0] * 0.1
    ball.rect.y += ball.velocity[1] * 0.1

points1 = [(400, 300), (500, 200), (600, 300), (550, 400), (450, 400)]
points2 = [(150, 150), (200, 100), (250, 150), (225, 200), (175, 200)]
polygon_sprite1 = Obstacle((0, 255, 0), points1)
polygon_sprite2 = Obstacle((0, 0, 255), points2)
obstacles = pygame.sprite.Group()
obstacles.add(polygon_sprite1, polygon_sprite2)

# Main game loop
running = True
last_time = time.time()
while running:
    current_time = time.time()
    dt = current_time - last_time
    last_time = current_time

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    for ball in all_sprites_list:
        ball.update(dt)
        # Check collision with obstacles
        for obstacle in obstacles:
            if pygame.sprite.collide_mask(ball, obstacle):
                handle_obstacle_collision(ball, obstacle)
    
    for ball1 in all_sprites_list:
        for ball2 in all_sprites_list:
            if ball1 != ball2 and pygame.sprite.collide_circle(ball1, ball2):
                resolve_collision(ball1, ball2)
                if ball1.value_update():
                    ball1.kill()
                if ball2.value_update():
                    ball2.kill()
        ball1.update(dt)

    # Update all sprites
    all_sprites_list.update(dt)

    # Draw everything
    screen.fill((0, 0, 0))
    all_sprites_list.draw(screen)
    obstacles.draw(screen)
    #pygame.draw.polygon(screen, (255, 165, 0), points)

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)

# Quit Pygame
pygame.quit()
sys.exit()