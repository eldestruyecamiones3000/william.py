import pygame
import random

# Inicialización de Pygame
pygame.init()

# Dimensiones de la pantalla
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Colores
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

# Tamaños
PLAYER_SIZE = 50
RESOURCE_SIZE = 30
ENEMY_SIZE = 50

# Configuración de la pantalla
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Recolección y Combate")

# Reloj para controlar FPS
clock = pygame.time.Clock()

# Jugador
player_x = SCREEN_WIDTH // 2
player_y = SCREEN_HEIGHT // 2
player_speed = 5
score = 0

# Recursos y Enemigos
resources = []
enemies = []

# Generar recursos
def generate_resource():
    x = random.randint(0, SCREEN_WIDTH - RESOURCE_SIZE)
    y = random.randint(0, SCREEN_HEIGHT - RESOURCE_SIZE)
    return pygame.Rect(x, y, RESOURCE_SIZE, RESOURCE_SIZE)

# Generar enemigos
def generate_enemy():
    x = random.randint(0, SCREEN_WIDTH - ENEMY_SIZE)
    y = random.randint(0, SCREEN_HEIGHT - ENEMY_SIZE)
    return pygame.Rect(x, y, ENEMY_SIZE, ENEMY_SIZE)

# Inicializar recursos y enemigos
for _ in range(5):
    resources.append(generate_resource())
for _ in range(3):
    enemies.append(generate_enemy())

# Función principal del juego
def game_loop():
    global player_x, player_y, score, resources, enemies

    running = True
    while running:
        clock.tick(60)  # 60 FPS

        # Manejo de eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Movimiento del jugador
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player_x -= player_speed
        if keys[pygame.K_RIGHT]:
            player_x += player_speed
        if keys[pygame.K_UP]:
            player_y -= player_speed
        if keys[pygame.K_DOWN]:
            player_y += player_speed

        # Crear el rectángulo del jugador
        player_rect = pygame.Rect(player_x, player_y, PLAYER_SIZE, PLAYER_SIZE)

        # Verificar si el jugador ha tocado algún recurso
        for resource in resources[:]:
            if player_rect.colliderect(resource):
                resources.remove(resource)
                score += 1
                resources.append(generate_resource())  # Generar nuevo recurso

        # Verificar si el jugador ha tocado algún enemigo
        for enemy in enemies:
            if player_rect.colliderect(enemy):
                print("¡Game Over! Has sido tocado por un enemigo.")
                running = False  # Terminar el juego si el jugador es tocado por un enemigo

        # Limpiar pantalla
        screen.fill(BLACK)

        # Dibujar recursos
        for resource in resources:
            pygame.draw.rect(screen, YELLOW, resource)

        # Dibujar enemigos
        for enemy in enemies:
            pygame.draw.rect(screen, RED, enemy)

        # Dibujar jugador
        pygame.draw.rect(screen, GREEN, player_rect)

        # Mostrar puntaje
        font = pygame.font.SysFont("Arial", 30)
        text = font.render(f"Puntaje: {score}", True, WHITE)
        screen.blit(text, (10, 10))

        # Actualizar la pantalla
        pygame.display.flip()

    pygame.quit()

# Iniciar el juego
game_loop()
