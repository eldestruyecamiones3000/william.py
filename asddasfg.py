import pygame
import random
import sys

# Inicialización de Pygame
pygame.init()

# Configuración de la pantalla
screen_width = 800
screen_height = 300
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Juego del Dinosaurio")

# Cargar y redimensionar imágenes
dino_img = pygame.image.load('dino.png')
dino_img = pygame.transform.scale(dino_img, (50, 50))
cactus_img = pygame.image.load('cactus.png')
cactus_img = pygame.transform.scale(cactus_img, (30, 50))
bird_img = pygame.image.load('bird.png')
bird_img = pygame.transform.scale(bird_img, (50, 30))

# Función para cambiar el clima
def change_weather():
    weather_types = ['sunny', 'snowy']
    current_weather = random.choice(weather_types)
    if current_weather == 'sunny':
        background_img = pygame.image.load('background_sunny.png')
    else:
        background_img = pygame.image.load('background_snowy.png')
    return pygame.transform.scale(background_img, (screen_width, screen_height))

background_img = change_weather()

# Parámetros del dinosaurio
dino_size = dino_img.get_rect().size
dino_pos = [50, screen_height - dino_size[1] - 10]
dino_velocity = 0
gravity = 1
jump_strength = -15
is_jumping = False

# Parámetros de los obstáculos
obstacle_speed = 10
obstacle_list = []

# Parámetros del juego
score = 0
game_over = False
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)

# Función para agregar nuevos obstáculos
def create_obstacle():
    if random.randint(0, 1):
        obstacle_pos = [screen_width, screen_height - cactus_img.get_rect().height - 10]
        obstacle_list.append((cactus_img, obstacle_pos))
    else:
        heights = [screen_height - dino_size[1] - 10 - bird_img.get_rect().height, 
                   screen_height - dino_size[1] - 50 - bird_img.get_rect().height, 
                   screen_height - dino_size[1] - 100 - bird_img.get_rect().height, 
                   screen_height - dino_size[1] - 150 - bird_img.get_rect().height, 
                   screen_height - dino_size[1] - 200 - bird_img.get_rect().height]
        obstacle_pos = [screen_width, random.choice(heights)]
        obstacle_list.append((bird_img, obstacle_pos))

# Función para dibujar los objetos
def draw_objects():
    screen.blit(background_img, (0, 0))
    screen.blit(dino_img, (dino_pos[0], dino_pos[1]))
    for img, pos in obstacle_list:
        screen.blit(img, (pos[0], pos[1]))
    score_text = font.render(f"Puntuación: {score}", True, (0, 0, 0))
    screen.blit(score_text, (screen_width - score_text.get_width() - 10, 10))  # Mostrar puntuación en la esquina superior derecha
    pygame.display.flip()

# Función para detectar colisiones
def check_collision(dino_pos, obstacle_list):
    for img, pos in obstacle_list:
        if (dino_pos[0] < pos[0] + img.get_rect().width and
            dino_pos[0] + dino_size[0] > pos[0] and
            dino_pos[1] < pos[1] + img.get_rect().height and
            dino_pos[1] + dino_size[1] > pos[1]):
            return True
    return False

# Bucle principal del juego
while True:
    background_img = change_weather()
    game_over = False
    score = 0
    dino_pos = [50, screen_height - dino_size[1] - 10]
    obstacle_list = []
    difficulty_increase_rate = 0.1  # Ajustar este valor para cambiar la tasa de aumento de dificultad

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not is_jumping:
                    dino_velocity = jump_strength
                    is_jumping = True

        dino_velocity += gravity
        dino_pos[1] += dino_velocity

        if dino_pos[1] > screen_height - dino_size[1] - 10:
            dino_pos[1] = screen_height - dino_size[1] - 10
            is_jumping = False

        # Ajuste aquí para aumentar la distancia entre obstáculos
        if len(obstacle_list) == 0 or obstacle_list[-1][1][0] < screen_width - 500:  # Cambia 300 a 500 para más distancia
            create_obstacle()

        for img, pos in obstacle_list:
            pos[0] -= obstacle_speed
            if pos[0] < 0:
                obstacle_list.remove((img, pos))

        if check_collision(dino_pos, obstacle_list):
            game_over = True

        score += 1  # Incrementar la puntuación continuamente

        # Aumentar la dificultad con el tiempo
        fps = clock.get_fps()
        if fps > 0:  # Asegurarse de no dividir por cero
            obstacle_speed += difficulty_increase_rate / fps
        draw_objects()
        clock.tick(30)

    # Mensaje de Game Over
    screen.blit(background_img, (0, 0))
    text = font.render("Game Over", True, (0, 0, 0))
    screen.blit(text, (screen_width // 2 - text.get_width() // 2, screen_height // 2 - text.get_height() // 2))
    score_text = font.render(f"Puntuación Final: {score}", True, (0, 0, 0))
    screen.blit(score_text, (screen_width // 2 - score_text.get_width() // 2, screen_height // 2 + 50))
    pygame.display.flip()
    pygame.time.wait(3000)
