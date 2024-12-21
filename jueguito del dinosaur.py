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
def load_and_scale_image(filename, size):
    img = pygame.image.load(filename)
    return pygame.transform.scale(img, size)

dino_run = [load_and_scale_image('dino_run1.png', (70, 70)),
            load_and_scale_image('dino_run2.png', (70, 70))]
dino_duck = [load_and_scale_image('dino_duck1.png', (70, 40)),
             load_and_scale_image('dino_duck2.png', (70, 40))]
dino_jump = load_and_scale_image('dino_jump.png', (70, 70))
cactus_img = load_and_scale_image('cactus.png', (50, 60))  # Cactus más bajo
bird_img = load_and_scale_image('bird.png', (50, 30))  # Ave más pequeña
background_img = load_and_scale_image('background_day.png', (screen_width, screen_height))  # Fondo inicial

# Cargar sonidos
jump_sound = pygame.mixer.Sound('jump.wav')
collision_sound = pygame.mixer.Sound('collision.wav')
score_sound = pygame.mixer.Sound('score.wav')

# Parámetros del dinosaurio
dino_size = dino_run[0].get_rect().size
dino_pos = [50, screen_height - dino_size[1] - 10]
dino_velocity = 0
gravity = 1
jump_strength = -15
is_jumping = False
is_ducking = False
anim_index = 0
anim_timer = 0

# Parámetros de los obstáculos
obstacle_speed = 10
obstacle_list = []
spawn_cooldown = 1500  # Tiempo entre obstáculos en milisegundos
last_spawn_time = pygame.time.get_ticks()

# Parámetros del juego
score = 0
high_score = 0
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
                   screen_height - dino_size[1] - 100 - bird_img.get_rect().height]
        obstacle_pos = [screen_width, random.choice(heights)]
        obstacle_list.append((bird_img, obstacle_pos))

# Función para dibujar los objetos
def draw_objects():
    screen.blit(background_img, (0, 0))
    
    if is_ducking:
        screen.blit(dino_duck[anim_index // 5], (dino_pos[0], dino_pos[1] + 20))
    elif is_jumping:
        screen.blit(dino_jump, (dino_pos[0], dino_pos[1]))
    else:
        screen.blit(dino_run[anim_index // 5], (dino_pos[0], dino_pos[1]))
    
    for img, pos in obstacle_list:
        screen.blit(img, (pos[0], pos[1]))
    
    score_text = font.render(f"Puntuación: {score}", True, (0, 0, 0))
    high_score_text = font.render(f"Mejor Puntuación: {high_score}", True, (0, 0, 0))
    screen.blit(score_text, (screen_width - score_text.get_width() - 10, 10))
    screen.blit(high_score_text, (screen_width - high_score_text.get_width() - 10, 40))
    pygame.display.flip()

# Función para detectar colisiones
def check_collision(dino_pos, obstacle_list):
    dino_rect = pygame.Rect(dino_pos[0], dino_pos[1], dino_size[0], dino_size[1])
    for img, pos in obstacle_list:
        obstacle_rect = pygame.Rect(pos[0], pos[1], img.get_rect().width, img.get_rect().height)
        if dino_rect.colliderect(obstacle_rect):
            return True
    return False

# Bucle principal del juego
while True:
    game_over = False
    score = 0
    dino_pos = [50, screen_height - dino_size[1] - 10]
    obstacle_list = []
    anim_index = 0
    obstacle_speed = 10
    spawn_cooldown = 1500

    while not game_over:
        current_time = pygame.time.get_ticks()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not is_jumping:
                    dino_velocity = jump_strength
                    is_jumping = True
                    jump_sound.play()
                if event.key == pygame.K_DOWN:
                    is_ducking = True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN:
                    is_ducking = False

        dino_velocity += gravity
        dino_pos[1] += dino_velocity

        if dino_pos[1] > screen_height - dino_size[1] - 10:
            dino_pos[1] = screen_height - dino_size[1] - 10
            is_jumping = False

        if current_time - last_spawn_time > spawn_cooldown:
            create_obstacle()
            last_spawn_time = current_time
            spawn_cooldown = max(500, spawn_cooldown - 10)  # Acelera la aparición hasta un límite mínimo

        for img, pos in obstacle_list:
            pos[0] -= obstacle_speed
            if pos[0] < 0:
                obstacle_list.remove((img, pos))

        if check_collision(dino_pos, obstacle_list):
            collision_sound.play()
            game_over = True

        score += 1
        if score % 100 == 0:
            score_sound.play()
            obstacle_speed += 0.5  # Aumenta la velocidad de los obstáculos cada 100 puntos

        anim_timer += 1
        if anim_timer >= 5:
            anim_index = (anim_index + 1) % 10
            anim_timer = 0
        
        draw_objects()
        clock.tick(30)

    if score > high_score:
        high_score = score
    
    screen.blit(background_img, (0, 0))
    text = font.render("Game Over", True, (0, 0, 0))
    screen.blit(text, (screen_width // 2 - text.get_width() // 2, screen_height // 2 - text.get_height() // 2))
    score_text = font.render(f"Puntuación Final: {score}", True, (0, 0, 0))
    screen.blit(score_text, (screen_width // 2 - score_text.get_width() // 2, screen_height // 2 + 50))
    high_score_text = font.render(f"Mejor Puntuación: {high_score}", True, (0, 0, 0))
    screen.blit(high_score_text, (screen_width // 2 - high_score_text.get_width() // 2, screen_height // 2 + 100))
    pygame.display.flip()
    pygame.time.wait(3000)
