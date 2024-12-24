import pygame
from settings import TILE_SIZE

# Карта
MAP = [
    "#########################",
    "#.***....*...*..**...***#",
    "#*#*#.#.#.#*#.#.#.#*#.#*#",
    "#.*.*..****.............#",
    "#.#.#.#.#.#.#.#.#.#.#.#.#",
    "#.......................#",
    "#.#.#.#.#.#.#.#.#.#.#.#.#",
    "#.......................#",
    "#.#.#.#.#.#.#.#.#.#.#.#.#",
    "#.......................#",
    "#.#.#.#.#.#.#.#.#.#.#.#.#",
    "#.......................#",
    "#.#.#.#.#.#.#.#.#.#.#.#.#",
    "#.......................#",
    "#########################",
]

class GameMap:
    def __init__(self):
        self.map_data = [list(row) for row in MAP]

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
        if self.map_data[y][x] == '*':
            self.map_data[y][x] = '.'
