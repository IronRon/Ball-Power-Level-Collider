import math
import pygame
import sys
from ball import Ball  # Import the Ball class

# Initialize Pygame
pygame.init()

# Set up the screen
width, height = 640, 480
screen = pygame.display.set_mode((width, height))

# Set up the clock
clock = pygame.time.Clock()

# Create a group for all sprites
all_sprites_list = pygame.sprite.Group()

# Create an instance of Ball and add it to the sprite group
ball = Ball((255, 0, 0), 10)
ball.rect.x = 100
ball.rect.y = 100
ball2 = Ball((0, 255, 0), 5, [1,4])
ball2.rect.x = 200
ball2.rect.y = 200
all_sprites_list.add(ball)
all_sprites_list.add(ball2)

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

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    for ball1 in all_sprites_list:
        for ball2 in all_sprites_list:
            if ball1 != ball2 and pygame.sprite.collide_circle(ball1, ball2):
                resolve_collision(ball1, ball2)
                if ball1.value_update(ball2):
                    ball1.kill()
                if ball2.value_update(ball1):
                    ball2.kill()
        ball1.update()

    # Update all sprites
    all_sprites_list.update()

    # Draw everything
    screen.fill((0, 0, 0))
    all_sprites_list.draw(screen)

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)

# Quit Pygame
pygame.quit()
sys.exit()