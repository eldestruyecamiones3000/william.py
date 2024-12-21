import pygame
import random

# Inicializar pygame
pygame.init()

# Colores
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
VERDE = (0, 255, 0)
ROJO = (255, 0, 0)
AZUL = (0, 0, 255)
GRIS = (100, 100, 100)
AMARILLO = (255, 255, 0)
MORADO = (255, 0, 255)

# Dimensiones de la pantalla
ANCHO_PANTALLA = 800
ALTO_PANTALLA = 600

# Crear la pantalla
pantalla = pygame.display.set_mode((ANCHO_PANTALLA, ALTO_PANTALLA))
pygame.display.set_caption("Escape del Laberinto Solitario")

# Reloj para controlar la velocidad del juego
reloj = pygame.time.Clock()

# Clase para el jugador
class Jugador(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface([40, 40])
        self.image.fill(VERDE)
        self.rect = self.image.get_rect()
        self.rect.x = 50
        self.rect.y = 50
        self.velocidad = 5
        self.tiempo_powerup = 0

    def update(self):
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_a] and self.rect.x > 0:
            self.rect.x -= self.velocidad
        if teclas[pygame.K_d] and self.rect.x < ANCHO_PANTALLA - 40:
            self.rect.x += self.velocidad
        if teclas[pygame.K_w] and self.rect.y > 0:
            self.rect.y -= self.velocidad
        if teclas[pygame.K_s] and self.rect.y < ALTO_PANTALLA - 40:
            self.rect.y += self.velocidad

        # Descontar tiempo del power-up si está activo
        if self.tiempo_powerup > 0:
            self.tiempo_powerup -= 1
            if self.tiempo_powerup == 0:
                self.velocidad = 5

# Clase para las paredes del laberinto
class Pared(pygame.sprite.Sprite):
    def __init__(self, x, y, ancho, alto):
        super().__init__()
        self.image = pygame.Surface([ancho, alto])
        self.image.fill(GRIS)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

# Clase para las trampas
class Trampa(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface([40, 40])
        self.image.fill(ROJO)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

# Clase para las llaves
class Llave(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface([20, 20])
        self.image.fill(AMARILLO)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

# Clase para los enemigos en movimiento
class Enemigo(pygame.sprite.Sprite):
    def __init__(self, x, y, velocidad, direccion):
        super().__init__()
        self.image = pygame.Surface([40, 40])
        self.image.fill(AZUL)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.velocidad = velocidad
        self.direccion = direccion

    def update(self):
        if self.direccion == 'horizontal':
            self.rect.x += self.velocidad
            if self.rect.right > ANCHO_PANTALLA or self.rect.left < 0:
                self.velocidad *= -1
        else:
            self.rect.y += self.velocidad
            if self.rect.bottom > ALTO_PANTALLA or self.rect.top < 0:
                self.velocidad *= -1

# Clase para los Power-Ups
class PowerUp(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface([20, 20])
        self.image.fill(MORADO)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

# Crear grupos de sprites
todos_los_sprites = pygame.sprite.Group()
paredes = pygame.sprite.Group()
trampas = pygame.sprite.Group()
llaves = pygame.sprite.Group()
enemigos = pygame.sprite.Group()
powerups = pygame.sprite.Group()

# Crear el jugador
jugador = Jugador()
todos_los_sprites.add(jugador)

# Variables para el juego
tiempo_limite = 60 * 30  # 30 segundos por nivel (60 fps * 30 segundos)
tiempo_restante = tiempo_limite
puerta_correcta = random.choice([True, False])  # Aleatoriamente una puerta será la correcta
en_pantalla_puertas = False
juego_terminado = False
mostrar_mensaje = ""

# Función para crear un nivel
def crear_nivel(nivel):
    global en_pantalla_puertas, puerta_correcta, tiempo_restante

    # Limpiar los grupos de sprites
    paredes.empty()
    trampas.empty()
    llaves.empty()
    enemigos.empty()
    powerups.empty()

    # Reiniciar tiempo y estado de las puertas
    en_pantalla_puertas = False
    puerta_correcta = random.choice([True, False])
    tiempo_restante = tiempo_limite

    # Crear las paredes del laberinto (más complicado a mayor nivel)
    paredes_data = [
        (0, 0, 800, 20),   # Pared superior
        (0, 580, 800, 20), # Pared inferior
        (0, 20, 20, 580),  # Pared izquierda
        (780, 20, 20, 580), # Pared derecha
        (100, 100, 200, 20),
        (400, 200, 200, 20)
    ]
    for pared in paredes_data:
        p = Pared(*pared)
        paredes.add(p)
        todos_los_sprites.add(p)

    # Crear trampas
    trampas_data = [(150, 200), (600, 400)]
    for trampa_pos in trampas_data:
        trampa = Trampa(*trampa_pos)
        trampas.add(trampa)
        todos_los_sprites.add(trampa)

    # Crear llaves
    llaves_data = [(300, 100), (600, 450)]
    for llave_pos in llaves_data:
        llave = Llave(*llave_pos)
        llaves.add(llave)
        todos_los_sprites.add(llave)

    # Crear enemigos en movimiento
    enemigos_data = [(100, 150, 3, 'horizontal')]
    for enemigo_data in enemigos_data:
        enemigo = Enemigo(*enemigo_data)
        enemigos.add(enemigo)
        todos_los_sprites.add(enemigo)

    # Crear Power-Ups
    powerup_data = [(200, 300), (400, 400)]
    for powerup_pos in powerup_data:
        powerup = PowerUp(*powerup_pos)
        powerups.add(powerup)
        todos_los_sprites.add(powerup)

# Crear el primer nivel
nivel_actual = 1
crear_nivel(nivel_actual)

# Fuente para mostrar el mensaje
fuente = pygame.font.SysFont(None, 36)

# Bucle principal del juego
ejecutando = True
llaves_recogidas = 0
puntuacion_necesaria = len(llaves)

while ejecutando:
    # Manejar eventos
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False
        if evento.type == pygame.KEYDOWN and en_pantalla_puertas:
            # Si se escoge una puerta
            if evento.key == pygame.K_LEFT:
                if puerta_correcta:
                    mostrar_mensaje = "¡Correcto! Avanzas al siguiente nivel"
                    nivel_actual += 1
                    crear_nivel(nivel_actual)
                else:
                    mostrar_mensaje = "Incorrecto. Vuelves al primer nivel"
                    nivel_actual = 1
                    crear_nivel(nivel_actual)
                en_pantalla_puertas = False
                llaves_recogidas = 0
            elif evento.key == pygame.K_RIGHT:
                if not puerta_correcta:
                    mostrar_mensaje = "¡Correcto! Avanzas al siguiente nivel"
                    nivel_actual += 1
                    crear_nivel(nivel_actual)
                else:
                    mostrar_mensaje = "Incorrecto. Vuelves al primer nivel"
                    nivel_actual = 1
                    crear_nivel(nivel_actual)
                en_pantalla_puertas = False
                llaves_recogidas = 0

    # Si el juego está terminado, no hacemos nada más
    if juego_terminado:
        pantalla.fill(NEGRO)
        texto_final = fuente.render(mostrar_mensaje, True, BLANCO)
        pantalla.blit(texto_final, [300, 300])
        pygame.display.flip()
        continue

    # Actualizar sprites
    if not en_pantalla_puertas:
        todos_los_sprites.update()

    # Verificar colisiones con trampas o enemigos
    if pygame.sprite.spritecollide(jugador, trampas, False) or pygame.sprite.spritecollide(jugador, enemigos, False):
        juego_terminado = True
        mostrar_mensaje = "¡Has perdido!"

    # Verificar colisiones con llaves
    llaves_colisionadas = pygame.sprite.spritecollide(jugador, llaves, True)
    for llave in llaves_colisionadas:
        llaves_recogidas += 1

    # Verificar colisiones con Power-Ups
    powerups_colisionados = pygame.sprite.spritecollide(jugador, powerups, True)
    for powerup in powerups_colisionados:
        jugador.velocidad = 10
        jugador.tiempo_powerup = 300  # Duración del power-up

    # Dibujar todo
    pantalla.fill(NEGRO)
    todos_los_sprites.draw(pantalla)

    # Mostrar llaves recogidas
    texto_llaves = fuente.render(f"Llaves: {llaves_recogidas}/{puntuacion_necesaria}", True, BLANCO)
    pantalla.blit(texto_llaves, [10, 10])

    # Mostrar tiempo restante
    texto_tiempo = fuente.render(f"Tiempo: {tiempo_restante // 60} s", True, BLANCO)
    pantalla.blit(texto_tiempo, [10, 40])

    # Si el tiempo se acaba
    if tiempo_restante <= 0 and not en_pantalla_puertas:
        texto_puertas = fuente.render("¡Elige una puerta! Izquierda o Derecha", True, BLANCO)
        pantalla.blit(texto_puertas, [200, 300])
        en_pantalla_puertas = True

    # Comprobar si el jugador ha recogido todas las llaves
    if llaves_recogidas >= puntuacion_necesaria and not en_pantalla_puertas:
        nivel_actual += 1
        crear_nivel(nivel_actual)
        llaves_recogidas = 0
        puntuacion_necesaria = len(llaves)

    # Actualizar el tiempo restante
    if tiempo_restante > 0 and not en_pantalla_puertas:
        tiempo_restante -= 1

    # Actualizar la pantalla
    pygame.display.flip()

    # Controlar la velocidad del juego
    reloj.tick(60)

# Cerrar el juego
pygame.quit()
