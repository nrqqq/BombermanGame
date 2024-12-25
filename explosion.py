import pygame
from settings import TILE_SIZE

class Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x * TILE_SIZE, y * TILE_SIZE)
        self.timer = 500

    def update(self, dt):
        self.timer -= dt * 1000
        if self.timer <= 0:
            self.kill()
