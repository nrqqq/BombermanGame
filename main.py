import pygame
import time
from settings import WIDTH, HEIGHT, WHITE, FPS, TILE_SIZE, MAP_HEIGHT, HEADER_HEIGHT
from player import Player
from game_map import GameMap
from bomb import Bomb
import database  # Импорт модуля для работы с базой данных

def display_highscores():
    pygame.init()
    WIN = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("High Scores")
    font = pygame.font.Font(None, 36)

    top_scores = database.get_top_scores()
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False

        WIN.fill(WHITE)
        title_text = font.render("Таблица рекордов", True, (0, 0, 0))
        WIN.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, 50))

        y_offset = 100
        for idx, (name, score) in enumerate(top_scores, start=1):
            score_text = font.render(f"{idx}. {name}: {score}", True, (0, 0, 0))
            WIN.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, y_offset))
            y_offset += 40

        pygame.display.flip()

def main_menu():
    pygame.init()
    WIN = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Main Menu")
    font = pygame.font.Font(None, 36)

    input_box = pygame.Rect(WIDTH // 4, HEIGHT // 2, WIDTH // 2, 40)
    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('dodgerblue2')
    color = color_inactive
    active = False
    text = ""

    button_rect = pygame.Rect(WIDTH // 3, HEIGHT // 2 + 100, 300, 50)

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return None
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if input_box.collidepoint(event.pos):
                    active = not active
                else:
                    active = False
                color = color_active if active else color_inactive

                if button_rect.collidepoint(event.pos):
                    display_highscores()
            elif event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        return text
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode

        WIN.fill(WHITE)
        title_text = font.render("Главное меню", True, (0, 0, 0))
        WIN.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 4 - 20))

        prompt_text = font.render("Введите имя и нажмите Enter", True, (0, 0, 0))
        WIN.blit(prompt_text, (WIDTH // 2 - prompt_text.get_width() // 2, HEIGHT // 2 - 60))

        pygame.draw.rect(WIN, color, input_box, 2)
        name_text = font.render(text, True, (0, 0, 0))
        WIN.blit(name_text, (input_box.x + 5, input_box.y + 5))
        input_box.w = max(200, name_text.get_width() + 10)

        pygame.draw.rect(WIN, (0, 200, 0), button_rect)
        button_text = font.render("Таблица рекордов", True, (255, 255, 255))
        WIN.blit(button_text, (button_rect.x + (button_rect.width - button_text.get_width()) // 2,
                               button_rect.y + (button_rect.height - button_text.get_height()) // 2))

        pygame.display.flip()

    return None

def main():
    player_name = main_menu()
    if not player_name:
        return

    def add_score(points):
        nonlocal score
        score += points

    pygame.init()
    WIN = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Bomberman Game")
    clock = pygame.time.Clock()

    font = pygame.font.Font(None, 36)

    run = True
    player = Player()
    game_map = GameMap()
    all_sprites = pygame.sprite.Group()
    bombs = pygame.sprite.Group()
    explosions = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    game_map.create_enemies(enemies)
    all_sprites.add(player)
    all_sprites.add(enemies)

    start_time = time.time()
    score = 0

    while run:
        dt = clock.tick(FPS) / 1000
        elapsed_time = int(time.time() - start_time)

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

        # Обновление всех спрайтов
        all_sprites.update(dt, game_map)
        bombs.update(dt, explosions, add_score)
        explosions.update(dt)

        # Проверка взаимодействия взрывов
        for explosion in explosions:
            # Уничтожение врагов
            collided_enemies = pygame.sprite.spritecollide(explosion, enemies, True)
            for enemy in collided_enemies:
                add_score(1000)

            # Разрушение стен
            tile_x = explosion.rect.centerx // TILE_SIZE
            tile_y = explosion.rect.centery // TILE_SIZE
            if 0 <= tile_x < len(game_map.map_data[0]) and 0 <= tile_y < len(game_map.map_data):
                if game_map.map_data[tile_y][tile_x] == '*':
                    game_map.destroy_tile(tile_x, tile_y)
                    add_score(100)

        # Проверка взаимодействия игрока
        if pygame.sprite.spritecollideany(player, enemies):
            run = False
        if pygame.sprite.spritecollideany(player, explosions):
            run = False

        if len(enemies) == 0:
            bonus = max(10000 - elapsed_time * 10, 0)
            add_score(bonus)
            print(f"Игра завершена! Итоговый счет: {score}")
            run = False

        # Отрисовка игры
        WIN.fill(WHITE)
        game_map.draw(WIN)
        all_sprites.draw(WIN)
        explosions.draw(WIN)

        header_y = TILE_SIZE * MAP_HEIGHT
        pygame.draw.rect(WIN, (200, 200, 200), (0, header_y, WIDTH, HEADER_HEIGHT))
        score_text = font.render(f"Счет: {score}", True, (0, 0, 0))
        timer_text = font.render(f"Время: {elapsed_time}", True, (0, 0, 0))
        WIN.blit(score_text, (10, header_y + 10))
        WIN.blit(timer_text, (WIDTH - 150, header_y + 10))

        pygame.display.flip()

    # Сохранение результата в БД
    database.save_score(player_name, score)

    pygame.quit()

if __name__ == "__main__":
    main()
