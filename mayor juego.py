import pygame
import random
import sys

# Inicializar Pygame
pygame.init()

# Configuración de la ventana
WIDTH, HEIGHT = 800, 600
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Cazador de Monedas Supremo")

# Colores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
PURPLE = (128, 0, 128)

# Configuración del jugador
player_size = 50
player_pos = [WIDTH // 2, HEIGHT // 2]
player_speed = 6
player_lives = 3

# Configuración de la moneda
coin_size = 20
coin_pos = [random.randint(0, WIDTH - coin_size), random.randint(0, HEIGHT - coin_size)]

# Configuración del enemigo
enemy_size = 50
enemy_speed = 3
enemies = []

# Configuración de obstáculos
obstacle_size = 100
obstacles = []

# Puntuación y Nivel
score = 0
level = 1
high_score = 0
font = pygame.font.SysFont("monospace", 35)

# Estados del juego
START, PLAYING, PAUSED, GAME_OVER = "start", "playing", "paused", "game over"
game_state = START

# Función para mostrar textos en pantalla
def draw_text(surface, text, size, x, y, color):
    font = pygame.font.SysFont("monospace", size)
    text_surface = font.render(text, True, color)
    surface.blit(text_surface, (x, y))

# Pantalla de inicio
def show_start_screen():
    window.fill(BLACK)
    draw_text(window, "Cazador de Monedas Supremo", 50, WIDTH // 2 - 200, HEIGHT // 2 - 50, WHITE)
    draw_text(window, "Presiona cualquier tecla para empezar", 30, WIDTH // 2 - 180, HEIGHT // 2 + 50, WHITE)
    pygame.display.flip()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                waiting = False

# Pantalla de pausa
def show_pause_screen():
    window.fill(BLACK)
    draw_text(window, "Pausado", 50, WIDTH // 2 - 80, HEIGHT // 2 - 50, WHITE)
    draw_text(window, "Presiona P para continuar", 30, WIDTH // 2 - 180, HEIGHT // 2 + 50, WHITE)
    pygame.display.flip()

# Pantalla de Game Over
def show_game_over_screen():
    global high_score
    if score > high_score:
        high_score = score
    window.fill(BLACK)
    draw_text(window, "Game Over", 50, WIDTH // 2 - 100, HEIGHT // 2 - 50, WHITE)
    draw_text(window, f"Puntuación: {score}", 30, WIDTH // 2 - 100, HEIGHT // 2 + 50, WHITE)
    draw_text(window, f"Puntuación Máxima: {high_score}", 30, WIDTH // 2 - 120, HEIGHT // 2 + 100, WHITE)
    draw_text(window, "Presiona R para reiniciar", 25, WIDTH // 2 - 100, HEIGHT // 2 + 150, WHITE)
    pygame.display.flip()

# Función para reiniciar el juego
def reset_game():
    global player_pos, score, level, enemies, coin_pos, obstacles, player_lives
    player_pos = [WIDTH // 2, HEIGHT // 2]
    score = 0
    level = 1
    player_lives = 3
    enemies = []
    obstacles = []
    coin_pos = [random.randint(0, WIDTH - coin_size), random.randint(0, HEIGHT - coin_size)]
    create_level_elements()

# Crear enemigos y obstáculos
def create_level_elements():
    enemies.clear()
    obstacles.clear()
    for _ in range(level):
        enemy_pos = [random.randint(0, WIDTH - enemy_size), random.randint(0, HEIGHT - enemy_size)]
        enemies.append({"pos": enemy_pos, "speed": random.choice([-enemy_speed, enemy_speed]), "direction": random.choice(["H", "V"])})
    for _ in range(level * 2):
        obstacle_pos = [random.randint(0, WIDTH - obstacle_size), random.randint(0, HEIGHT - obstacle_size)]
        obstacles.append(obstacle_pos)

# Bucle principal del juego
reset_game()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if game_state == PLAYING:
                if event.key == pygame.K_p:
                    game_state = PAUSED
            elif game_state == PAUSED:
                if event.key == pygame.K_p:
                    game_state = PLAYING
            elif game_state == GAME_OVER:
                if event.key == pygame.K_r:
                    game_state = START
                    reset_game()
            elif game_state == START:
                if event.key == pygame.K_RETURN:
                    game_state = PLAYING
                    reset_game()

    if game_state == START:
        show_start_screen()
        pygame.display.flip()
        continue

    if game_state == GAME_OVER:
        show_game_over_screen()
        pygame.display.flip()
        continue

    if game_state == PAUSED:
        show_pause_screen()
        pygame.display.flip()
        continue

    # Movimiento del jugador
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_pos[0] > 0:
        player_pos[0] -= player_speed
    if keys[pygame.K_RIGHT] and player_pos[0] < WIDTH - player_size:
        player_pos[0] += player_speed
    if keys[pygame.K_UP] and player_pos[1] > 0:
        player_pos[1] -= player_speed
    if keys[pygame.K_DOWN] and player_pos[1] < HEIGHT - player_size:
        player_pos[1] += player_speed

    # Colisión con la moneda
    if (player_pos[0] < coin_pos[0] < player_pos[0] + player_size or player_pos[0] < coin_pos[0] + coin_size < player_pos[0] + player_size) and \
       (player_pos[1] < coin_pos[1] < player_pos[1] + player_size or player_pos[1] < coin_pos[1] + coin_size < player_pos[1] + player_size):
        score += 1
        level = score // 5 + 1
        coin_pos = [random.randint(0, WIDTH - coin_size), random.randint(0, HEIGHT - coin_size)]
        create_level_elements()

    # Movimiento de los enemigos
    for enemy in enemies:
        if enemy["direction"] == "H":
            enemy["pos"][0] += enemy["speed"]
            if enemy["pos"][0] <= 0 or enemy["pos"][0] >= WIDTH - enemy_size:
                enemy["speed"] *= -1
        else:
            enemy["pos"][1] += enemy["speed"]
            if enemy["pos"][1] <= 0 or enemy["pos"][1] >= HEIGHT - enemy_size:
                enemy["speed"] *= -1

    # Colisión con enemigos y obstáculos
    for enemy in enemies:
        if (player_pos[0] < enemy["pos"][0] < player_pos[0] + player_size or player_pos[0] < enemy["pos"][0] + enemy_size < player_pos[0] + player_size) and \
           (player_pos[1] < enemy["pos"][1] < player_pos[1] + player_size or player_pos[1] < enemy["pos"][1] + enemy_size < player_pos[1] + player_size):
            player_lives -= 1
            if player_lives <= 0:
                game_state = GAME_OVER
            else:
                reset_game()

    # Dibujar todo en pantalla
    window.fill(BLACK)
    pygame.draw.rect(window, GREEN, (player_pos[0], player_pos[1], player_size, player_size))  # Jugador
    pygame.draw.rect(window, YELLOW, (coin_pos[0], coin_pos[1], coin_size, coin_size))  # Moneda
    for enemy in enemies:
        pygame.draw.rect(window, RED, (enemy["pos"][0], enemy["pos"][1], enemy_size, enemy_size))  # Enemigos
    for obstacle_pos in obstacles:
        pygame.draw.rect(window, PURPLE, (obstacle_pos[0], obstacle_pos[1], obstacle_size, obstacle_size))  # Obstáculos

    # Mostrar puntuación y nivel
    draw_text(window, f"Puntos: {score}", 25, 10, 10, WHITE)
    draw_text(window, f"Nivel: {level}", 25, 10, 40, WHITE)
    draw_text(window, f"Vidas: {player_lives}", 25, 10, 70, WHITE)

    pygame.display.flip()
    pygame.time.Clock().tick(30)
