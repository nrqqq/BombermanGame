import pygame
import os  # Добавим импорт os
from settings import TILE_SIZE, WIDTH, HEIGHT

def load_sprites(folder, prefix, count):
    sprites = []
    for i in range(count):
        path = os.path.join(folder, f"{prefix}{i}.png")
        image = pygame.image.load(path)
        scaled_image = pygame.transform.scale(image, (TILE_SIZE, TILE_SIZE))
        sprites.append(scaled_image)
    return sprites

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.sprites = {
            "idle": load_sprites("sprites", "idle", 2),
            "idleback": load_sprites("sprites", "idleback", 2),
            "idleside": load_sprites("sprites", "idleside", 2),
            "walkdown": load_sprites("sprites", "walkdown", 4),
            "walkside": load_sprites("sprites", "walkside", 4),
            "walkup": load_sprites("sprites", "walkup", 4),
        }
        self.current_sprites = self.sprites["idle"]
        self.current_frame = 0
        self.image = self.current_sprites[self.current_frame]
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH // 2, HEIGHT // 2)
        self.animation_speed = 0.2
        self.animation_counter = 0
        self.direction = "down"
        self.facing_left = False

    def update(self, dt, game_map):
        keys = pygame.key.get_pressed()
        dx, dy = 0, 0
        if keys[pygame.K_LEFT]:
            dx = -2
            self.direction = "side"
            self.current_sprites = self.sprites["walkside"]
            self.facing_left = True
        elif keys[pygame.K_RIGHT]:
            dx = 2
            self.direction = "side"
            self.current_sprites = self.sprites["walkside"]
            self.facing_left = False
        elif keys[pygame.K_UP]:
            dy = -2
            self.direction = "up"
            self.current_sprites = self.sprites["walkup"]
            self.facing_left = False
        elif keys[pygame.K_DOWN]:
            dy = 2
            self.direction = "down"
            self.current_sprites = self.sprites["walkdown"]
            self.facing_left = False
        else:
            if self.direction == "side":
                self.current_sprites = self.sprites["idleside"]
            elif self.direction == "up":
                self.current_sprites = self.sprites["idleback"]
            else:
                self.current_sprites = self.sprites["idle"]

        # Проверка столкновений
        self.move(dx, dy, game_map)

        self.animation_counter += self.animation_speed
        if self.animation_counter >= 1:
            self.animation_counter = 0
            self.current_frame = (self.current_frame + 1) % len(self.current_sprites)
            self.image = self.current_sprites[self.current_frame]

            # Отзеркаливание спрайтов при движении влево
            if self.direction == "side" and self.facing_left:
                self.image = pygame.transform.flip(self.image, True, False)

    def move(self, dx, dy, game_map):
        if dx != 0:
            self.rect.x += dx
            if self.collide_with_walls(game_map):
                self.rect.x -= dx

        if dy != 0:
            self.rect.y += dy
            if self.collide_with_walls(game_map):
                self.rect.y -= dy

    def collide_with_walls(self, game_map):
        for y, row in enumerate(game_map.map_data):
            for x, tile in enumerate(row):
                if tile != '.':
                    tile_rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                    if self.rect.colliderect(tile_rect):
                        return True
        return False

    def draw(self, surface):
        surface.blit(self.image, self.rect)
