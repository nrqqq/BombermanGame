import pygame
import os
from settings import TILE_SIZE

def load_image(filename):
    image = pygame.image.load(os.path.join("sprites", filename))
    return pygame.transform.scale(image, (TILE_SIZE, TILE_SIZE))

def load_sprites(folder, prefix, count):
    sprites = []
    for i in range(count):
        path = os.path.join(folder, f"{prefix}{i}.png")
        image = pygame.image.load(path)
        scaled_image = pygame.transform.scale(image, (TILE_SIZE, TILE_SIZE))
        sprites.append(scaled_image)
    return sprites
