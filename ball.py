import pygame

class Ball(pygame.sprite.Sprite):
    def __init__(self, color, value, init_velo=[0, 0]):
        super().__init__()
        self.radius = 25 + int(value * 0.7)
        self.color = color
        self.velocity = init_velo
        self.value = value

        self.radius = None
        self.image = None
        self.rect = None

        # Draw the initial ball and text
        self.update_ball()

    def update(self):
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]

        if self.rect.right >= 640 or self.rect.left <= 0:
            self.velocity[0] = -self.velocity[0]
        if self.rect.bottom >= 480 or self.rect.top <= 0:
            self.velocity[1] = -self.velocity[1]

    def value_update(self, other):
        self.value -= other.value
        if self.value <= 0:
            return True
        else:
            self.update_ball()  # Update the text after changing the value
            return False

     # This function handles drawing the ball and text
    def update_ball(self):
        old_center = self.rect.center if self.rect else None
        self.radius = 25 + int(self.value * 0.7)
        self.image = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        # Redraw the circle to clear the old text
        pygame.draw.circle(self.image, self.color, (self.radius, self.radius), self.radius)

        # Draw the new value
        font_size = int(self.radius * 0.9)
        font = pygame.font.Font(None, font_size)
        text_surface = font.render(str(self.value), True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(self.radius, self.radius))
        # Blit the new text onto the ball's surface
        self.image.blit(text_surface, text_rect)

        self.rect = self.image.get_rect()
        if old_center:
            self.rect.center = old_center  # Adjust the rect to maintain position