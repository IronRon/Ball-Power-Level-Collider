import pygame

class Ball(pygame.sprite.Sprite):
    def __init__(self, color, radius, value, init_velo = [0, 0]):
        super().__init__()
        
        # Set the radius of the ball
        self.radius = radius
        self.color = color
        self.velocity = init_velo
        self.value = value

        # Create a surface with extra space to draw the circle
        self.image = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
        
        # Draw the circle onto the surface
        pygame.draw.circle(self.image, self.color, (radius, radius), radius)

        font_size = int(radius * 0.9)
        font = pygame.font.Font(None, font_size)  # None uses the default font

        text_surface = font.render(str(self.value), True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(radius, radius))  # Center the text on the ball

        # Blit the text onto the ball's surface
        self.image.blit(text_surface, text_rect)

        # Fetch the rectangle object that has the dimensions of the image.
        self.rect = self.image.get_rect()

    def update(self):
        # Update the position based on the velocity
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]
        
        # Add boundary checking to prevent it from going out of bounds
        if self.rect.right >= 640 or self.rect.left <= 0:
            self.velocity[0] = -self.velocity[0]
        if self.rect.bottom >= 480 or self.rect.top <= 0:
            self.velocity[1] = -self.velocity[1]