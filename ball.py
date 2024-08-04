import pygame

class Ball(pygame.sprite.Sprite):
    def __init__(self, color, value, team, init_velo=[0, 0]):
        super().__init__()
        self.radius = 25 + int(value * 0.7)
        self.color = color
        self.velocity = init_velo
        self.value = value
        self.team = team

        self.image = None
        self.rect = None

        # Draw the initial ball and text
        self.update_ball()

    def update(self, dt = 0):
        gravity_per_frame = 9.8 * dt  # dt is the time delta in seconds
        self.velocity[1] += gravity_per_frame
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]

        if self.rect.right >= 640 or self.rect.left <= 0:
            self.velocity[0] = -self.velocity[0] * 0.8
        # Vertical boundary collision
        if self.rect.bottom >= 480:
            self.rect.bottom = 480
            #print(self.color, abs(self.velocity[1]))
            if abs(self.velocity[1]) > 2.5:
                self.velocity[1] = -self.velocity[1] * 0.65  # Reverse and dampen the vertical velocity
            else:
                self.velocity[1] = 0  # Stop the ball
        elif self.rect.top <= 0:
            self.rect.top = 0
            self.velocity[1] = -self.velocity[1] * 0.65
 


    def value_update(self):
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