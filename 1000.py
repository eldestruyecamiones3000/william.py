import pygame
import random
import sys

# Inicialización de Pygame
pygame.init()

# Configuración de la pantalla
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Juego de Saltar Obstáculos")

# Definir colores
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)

# Parámetros del jugador
player_size = 50
player_pos = [100, screen_height - player_size - 100]
player_velocity = 0
gravity = 1
jump_strength = -15

# Parámetros de los obstáculos
obstacle_size = 50
obstacle_speed = 10
obstacle_list = []

# Estado del juego
game_over = False
clock = pygame.time.Clock()

# Fuente para el texto
font = pygame.font.Font(None, 74)

# Función para agregar nuevos obstáculos
def create_obstacle():
    obstacle_pos = [screen_width, screen_height - obstacle_size - 100]
    obstacle_list.append(obstacle_pos)

# Función para dibujar los objetos
def draw_objects():
    screen.fill(black)
    pygame.draw.rect(screen, red, (player_pos[0], player_pos[1], player_size, player_size))
    for obstacle_pos in obstacle_list:
        pygame.draw.rect(screen, red, (obstacle_pos[0], obstacle_pos[1], obstacle_size, obstacle_size))
    pygame.display.flip()

# Bucle principal del juego
while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and player_pos[1] == screen_height - player_size - 100:
                player_velocity = jump_strength
    
    player_velocity += gravity
    player_pos[1] += player_velocity
    
    if player_pos[1] > screen_height - player_size - 100:
        player_pos[1] = screen_height - player_size - 100
    
    if len(obstacle_list) == 0 or obstacle_list[-1][0] < screen_width - 300:
        create_obstacle()
    
    for obstacle_pos in obstacle_list:
        obstacle_pos[0] -= obstacle_speed
        if obstacle_pos[0] < 0:
            obstacle_list.remove(obstacle_pos)
        if player_pos[0] < obstacle_pos[0] < player_pos[0] + player_size or player_pos[0] < obstacle_pos[0] + obstacle_size < player_pos[0] + player_size:
            if player_pos[1] + player_size > obstacle_pos[1]:
                game_over = True
    
    draw_objects()
    clock.tick(30)

# Mensaje de Game Over
screen.fill(black)
text = font.render("Game Over", True, white)
screen.blit(text, (screen_width // 2 - text.get_width() // 2, screen_height // 2 - text.get_height() // 2))
pygame.display.flip()
pygame.time.wait(2000)

pygame.quit()
sys.exit()
