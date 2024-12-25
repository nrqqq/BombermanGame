import pygame
from settings import TILE_SIZE
from enemy import Enemy  # Импорт класса Enemy

# Карта
MAP = [
    "#########################",
    "#..**............*...***#",
    "#.#*#.#.#.#*#.#.#.#*#.#*#",
    "#.*.*..****.............#",
    "#.#.#.#.#.#.#.#.#.#.#.#.#",
    "#.......................#",
    "#.#.#.#.#.#.#.#.#!#.#.#.#",
    "#.......................#",
    "#.#.#.#.#.#.#.#.#.#.#.#.#",
    "#.......................#",
    "#.#.#.#.#.#.#.#.#.#.#.#.#",
    "#..........!............#",
    "#.#.#.#.#.#.#.#.#.#.#.#.#",
    "#.......................#",
    "#########################",
]



class GameMap:
    def __init__(self):
        self.map_data = [list(row) for row in MAP]

    def create_enemies(self, enemies_group):
        for y, row in enumerate(self.map_data):
            for x, tile in enumerate(row):
                if tile == '!':
                    direction = "vertical" if y % 2 == 0 else "horizontal"
                    enemy = Enemy(x, y, direction)
                    enemies_group.add(enemy)
                    self.map_data[y][x] = '.'

    def draw(self, surface):
        for y, row in enumerate(self.map_data):
            for x, tile in enumerate(row):
                if tile == '#':
                    color = (0, 0, 0)
                elif tile == '*':
                    color = (139, 69, 19)
                else:
                    continue
                pygame.draw.rect(surface, color, (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))

    def destroy_tile(self, x, y):
        if self.map_data[y][x] == '*':  # Если блок разрушаемый
            self.map_data[y][x] = '.'  # Заменяем на пустую клетку
            return True
        return False
