import pygame
from settings import TILE_SIZE, WIDTH, HEIGHT

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        super().__init__()
        self.image = pygame.image.load("sprites/enemy.png")
        self.image = pygame.transform.scale(self.image, (TILE_SIZE, TILE_SIZE))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x * TILE_SIZE, y * TILE_SIZE)
        self.direction = direction  # "horizontal" или "vertical"
        self.speed = 2

    def update(self, dt, game_map):
        if self.direction == "horizontal":
            self.rect.x += self.speed
            if self.rect.left < 0 or self.rect.right > WIDTH or self.collide_with_walls(game_map):
                self.speed = -self.speed
        elif self.direction == "vertical":
            self.rect.y += self.speed
            if self.rect.top < 0 or self.rect.bottom > HEIGHT or self.collide_with_walls(game_map):
                self.speed = -self.speed

    def collide_with_walls(self, game_map):
        for y, row in enumerate(game_map.map_data):
            for x, tile in enumerate(row):
                if tile != '.' and tile != '!':  # Стены и враги не пересекаются
                    tile_rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                    if self.rect.colliderect(tile_rect):
                        return True
        return False

    def kill(self):
        """Удаление врага."""
        super().kill()
