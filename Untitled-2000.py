import pygame 
import random

# Inicializar pygame
pygame.init()

# Colores
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
ROJO = (255, 0, 0)
VERDE = (0, 255, 0)

# Pantalla
ANCHO = 650
ALTO = 500
TAMAÑO_BLOQUE = 20
VELOCIDAD = 9

PANTALLA = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Juego de serpiente🗣️🗣️🗣️📢📢")

# Fondo
try:
    imagen_fondo = pygame.image.load("fondo.jpg")
    imagen_fondo = pygame.transform.scale(imagen_fondo, (ANCHO, ALTO))
except pygame.error:
    # Si no se encuentra la imagen, rellenar con color negro
    imagen_fondo = pygame.Surface(PANTALLA.get_size())
    imagen_fondo.fill(NEGRO)

# Puntaje
fuente_puntaje = pygame.font.SysFont("Bahnschrift", 35)
fuente_fin = pygame.font.SysFont("comicsansms", 45)

def mostrar_puntaje(puntos):
    valor = fuente_puntaje.render("Puntos: " + str(puntos), True, BLANCO) 
    PANTALLA.blit(valor , [10, 10])

# Serpiente
def dibujar_serpiente(tamaño_bloque, lista_serpiente):
    for bloque in lista_serpiente:
        pygame.draw.rect(PANTALLA, VERDE, [bloque[0], bloque[1], tamaño_bloque, tamaño_bloque])

# Juego
def juego():
    game_over = False
    game_close = False

    # Posición inicial de la serpiente (usando enteros)
    x_snake = ANCHO // 2
    y_snake = ALTO // 2
    x_cambio = 0
    y_cambio = 0

    direccion = "STOP"

    Lista_serpiente = []
    longitud_serpiente = 1

    # Comida
    x_comida = round(random.randrange(0, ANCHO - TAMAÑO_BLOQUE) / TAMAÑO_BLOQUE) * TAMAÑO_BLOQUE
    y_comida = round(random.randrange(0, ALTO - TAMAÑO_BLOQUE) / TAMAÑO_BLOQUE) * TAMAÑO_BLOQUE

    # Inicializar el reloj fuera del bucle principal
    reloj = pygame.time.Clock()

    # Bucle principal
    while not game_over:
        while game_close:  
            PANTALLA.blit(imagen_fondo, (0, 0))
            mensaje_fin_juego = fuente_fin.render("Perdiste. Presiona Q para salir o C para repetir", True, NEGRO)
            PANTALLA.blit(mensaje_fin_juego, [ANCHO // 10, ALTO // 2.5])
            mostrar_puntaje(longitud_serpiente - 1)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_over = True
                    game_close = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    elif event.key == pygame.K_c:
                        juego()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and direccion != "RIGHT":
                    x_cambio = -TAMAÑO_BLOQUE
                    y_cambio = 0
                    direccion = "LEFT"
                elif event.key == pygame.K_RIGHT and direccion != "LEFT":
                    x_cambio = TAMAÑO_BLOQUE
                    y_cambio = 0
                    direccion = "RIGHT"
                elif event.key == pygame.K_UP and direccion != "DOWN":
                    y_cambio = -TAMAÑO_BLOQUE
                    x_cambio = 0
                    direccion = "UP"
                elif event.key == pygame.K_DOWN and direccion != "UP": 
                    y_cambio = TAMAÑO_BLOQUE
                    x_cambio = 0
                    direccion = "DOWN"

        # Condiciones para perder
        if x_snake >= ANCHO or x_snake < 0 or y_snake >= ALTO or y_snake < 0:
            game_close = True

        x_snake += x_cambio
        y_snake += y_cambio
        PANTALLA.blit(imagen_fondo, (0, 0))

        # Dibujar la comida
        pygame.draw.rect(PANTALLA, ROJO, [x_comida, y_comida, TAMAÑO_BLOQUE, TAMAÑO_BLOQUE])

        # Serpiente
        cabeza_serpiente = [x_snake, y_snake]
        Lista_serpiente.append(cabeza_serpiente)
        if len(Lista_serpiente) > longitud_serpiente:
            del Lista_serpiente[0]

        for bloque in Lista_serpiente[:-1]:
            if bloque == cabeza_serpiente:
                game_close = True

        dibujar_serpiente(TAMAÑO_BLOQUE, Lista_serpiente)

        # Mostrar puntaje
        mostrar_puntaje(longitud_serpiente - 1)

        pygame.display.update()

        # Comer la comida (revisar colisión exacta)
        if abs(x_snake - x_comida) < TAMAÑO_BLOQUE and abs(y_snake - y_comida) < TAMAÑO_BLOQUE:
            x_comida = round(random.randrange(0, ANCHO - TAMAÑO_BLOQUE) / TAMAÑO_BLOQUE) * TAMAÑO_BLOQUE
            y_comida = round(random.randrange(0, ALTO - TAMAÑO_BLOQUE) / TAMAÑO_BLOQUE) * TAMAÑO_BLOQUE
            longitud_serpiente += 1

        # Control de velocidad
        reloj.tick(VELOCIDAD)

    pygame.quit()
    quit()

# Iniciar el juego
juego()
