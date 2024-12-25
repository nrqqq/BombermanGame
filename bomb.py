import pygame
from settings import TILE_SIZE


class Bomb(pygame.sprite.Sprite):
    def __init__(self, x, y, game_map):
        super().__init__()
        self.image = pygame.image.load('sprites/bomb.png')  # Загрузка изображения бомбы
        self.image = pygame.transform.scale(self.image, (TILE_SIZE, TILE_SIZE))  # Масштабирование под размер тайла
        self.rect = self.image.get_rect(topleft=(x * TILE_SIZE, y * TILE_SIZE))
        self.timer = 2  # Время до взрыва в секундах
        self.exploded = False
        self.game_map = game_map

    def update(self, dt, explosions, score_callback=None):
        self.timer -= dt
        if self.timer <= 0 and not self.exploded:
            self.explode(explosions, score_callback)
            self.exploded = True
            self.kill()  # Удаляем бомбу после взрыва

    def explode(self, explosions, score_callback):
        if not isinstance(explosions, pygame.sprite.Group):  # кастыльный фикс, так и не понял почему explosions иногда меняет тип на gamemap
            explosions = pygame.sprite.Group()
            print("explosions поменял тип")
        # Создаем взрывы в 4 направлениях
        directions = [(0, 0), (1, 0), (-1, 0), (0, 1), (0, -1)]
        for dx, dy in directions:
            x = self.rect.centerx // TILE_SIZE + dx
            y = self.rect.centery // TILE_SIZE + dy

            # Убедимся, что координаты в пределах карты
            if 0 <= x < len(self.game_map.map_data[0]) and 0 <= y < len(self.game_map.map_data):
                tile = self.game_map.map_data[y][x]

                # Взрыв не распространяется через неразрушаемые блоки
                if tile == '#':
                    continue

                # Проверка на разрушаемые блоки
                if tile == '*':
                    self.game_map.destroy_tile(x, y)
                    if score_callback:
                        score_callback(100)  # Добавить 100 очков за блок

                # Создаем взрыв
                explosion = Explosion(x, y)
                explosions.add(explosion)


class Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE))
        self.image.fill((255, 0, 0))  # Красный цвет для взрыва
        self.rect = self.image.get_rect(topleft=(x * TILE_SIZE, y * TILE_SIZE))
        self.timer = 0.5  # Время существования взрыва

    def update(self, dt):
        self.timer -= dt
        if self.timer <= 0:
            self.kill()  # Удаляем взрыв после окончания таймера
