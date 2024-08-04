import pygame

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, color, points):
        super().__init__()
        # Calculate the minimal bounding rect and create an image of that size.
        self.min_x = min(point[0] for point in points)
        self.max_x = max(point[0] for point in points)
        self.min_y = min(point[1] for point in points)
        self.max_y = max(point[1] for point in points)
        # Create a transparent surface just big enough to fit the polygon
        self.image = pygame.Surface((self.max_x - self.min_x, self.max_y - self.min_y), pygame.SRCALPHA)
        # Draw polygon on the surface after adjusting points to fit top-left corner
        pygame.draw.polygon(self.image, color, [(x - self.min_x, y - self.min_y) for x, y in points])
        # Set sprite's rectangle to original polygon position in game world
        self.rect = self.image.get_rect(topleft=(self.min_x, self.min_y))
        # Create a mask for pixel-perfect collision detection
        self.mask = pygame.mask.from_surface(self.image)