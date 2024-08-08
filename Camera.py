import pygame
from Constants import GAME_WIDTH, GAME_HEIGHT

class Camera:
    def __init__(self, width, height):
        self.camera = pygame.Rect(0, 0, width, height)
        self.width = width
        self.height = height

    def apply(self, entity):
        return entity.rect.move(self.camera.topleft)

    def update(self, target):
        # This method might remain unused if no target is supplied
        self.center_target(target)

    def center_target(self, target):
        x = -target.rect.centerx + int(self.width / 2)
        y = -target.rect.centery + int(self.height / 2)
        self.adjust_camera_position(x, y)

    def adjust_camera_position(self, x, y):
        x = max(0, x)  # Left boundary
        x = min(-(self.width - GAME_WIDTH), x)  # Right boundary
        y = max(0, y)  # Top boundary
        y = min(-(self.height - GAME_HEIGHT), y)  # Bottom boundary
        self.camera = pygame.Rect(x, y, self.width, self.height)

    def move_up(self, pixels):
        self.adjust_camera_position(self.camera.x, self.camera.y - pixels)

    def move_down(self, pixels):
        self.adjust_camera_position(self.camera.x, self.camera.y + pixels)