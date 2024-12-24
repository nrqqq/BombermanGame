import pygame
from settings import WIDTH, HEIGHT, WHITE, FPS, TILE_SIZE
from player import Player
from game_map import GameMap
from bomb import Bomb

def main():
    pygame.init()
    WIN = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Игровая Анимация")
    clock = pygame.time.Clock()

    run = True
    player = Player()
    game_map = GameMap()
    all_sprites = pygame.sprite.Group()
    bombs = pygame.sprite.Group()
    explosions = pygame.sprite.Group()
    all_sprites.add(player)

    while run:
        dt = clock.tick(FPS) / 1000  # Дельта времени в секундах
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e:
                    bomb_x = player.rect.centerx // TILE_SIZE
                    bomb_y = player.rect.centery // TILE_SIZE
                    bomb = Bomb(bomb_x, bomb_y, game_map)
                    bombs.add(bomb)
                    all_sprites.add(bomb)

        # Обновление объектов
        all_sprites.update(dt, game_map)  # Обновляем всех
        bombs.update(dt, explosions)  # Передаем explosions для работы взрывов
        explosions.update(dt)  # Обновляем взрывы

        # Отрисовка
        WIN.fill(WHITE)
        game_map.draw(WIN)
        all_sprites.draw(WIN)
        explosions.draw(WIN)
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
