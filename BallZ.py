import math
import pygame
import time
import sys
from ball import Ball

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

    if ball1.team != ball2.team:
        temp = ball1.value
        ball1.value -= ball2.value
        ball2.value -= temp

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

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(30)

# Quit Pygame
pygame.quit()
sys.exit()