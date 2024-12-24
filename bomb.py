import pygame
from settings import TILE_SIZE
from explosion import Explosion

class Bomb(pygame.sprite.Sprite):
    def __init__(self, x, y, game_map):
        super().__init__()
        self.image = pygame.image.load("sprites/bomb.png")
        self.image = pygame.transform.scale(self.image, (TILE_SIZE, TILE_SIZE))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x * TILE_SIZE, y * TILE_SIZE)
        self.timer = 3000  # Таймер в миллисекундах
        self.exploded = False
        self.game_map = game_map

    def update(self, dt, explosions):
        self.timer -= dt * 1000
        if self.timer <= 0 and not self.exploded:
            self.explode(explosions)

    def explode(self, explosions):
        self.exploded = True
        x, y = self.rect.topleft
        tile_x, tile_y = x // TILE_SIZE, y // TILE_SIZE

        # Уничтожаем текущую клетку
        self.game_map.destroy_tile(tile_x, tile_y)
        explosions.add(Explosion(tile_x, tile_y))  # Добавляем взрыв

        # Создаём взрывы в четырёх направлениях
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for dx, dy in directions:
            nx, ny = tile_x + dx, tile_y + dy
            if 0 <= nx < len(self.game_map.map_data[0]) and 0 <= ny < len(self.game_map.map_data):
                if self.game_map.map_data[ny][nx] != '#':  # Пропускаем стены
                    self.game_map.destroy_tile(nx, ny)
                    explosions.add(Explosion(nx, ny))

        self.kill()  # Удаляем бомбу после взрыва
