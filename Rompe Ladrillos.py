import pygame
import sys
import random

# Inicializar Pygame
pygame.init()

# Configuraciones de la pantalla
ANCHO_PANTALLA, ALTO_PANTALLA = 800, 600
pantalla = pygame.display.set_mode((ANCHO_PANTALLA, ALTO_PANTALLA))
pygame.display.set_caption("Rompe Ladrillos")

# Colores
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
ROJO = (255, 0, 0)
VERDE = (0, 255, 0)
AZUL = (0, 0, 255)
AMARILLO = (255, 255, 0)
GRIS = (169, 169, 169)

# FPS
FPS = 60
reloj = pygame.time.Clock()

# Configuraciones de la pala
ANCHO_PALA, ALTO_PALA = 100, 10
VELOCIDAD_PALA = 10
pala = pygame.Rect(ANCHO_PANTALLA // 2 - ANCHO_PALA // 2, ALTO_PANTALLA - ALTO_PALA - 20, ANCHO_PALA, ALTO_PALA)

# Configuraciones de la pelota
TAMANIO_PELOTA = 10
VELOCIDAD_PELOTA = [0, 0]
pelota = pygame.Rect(ANCHO_PANTALLA // 2 - TAMANIO_PELOTA // 2, ALTO_PANTALLA // 2 - TAMANIO_PELOTA // 2, TAMANIO_PELOTA, TAMANIO_PELOTA)
pelota_lanzada = False

# Configuraciones de los ladrillos
ANCHO_LADRILLO, ALTO_LADRILLO = 60, 20
FILAS, COLUMNAS = 5, ANCHO_PANTALLA // ANCHO_LADRILLO
ladrillos = []

# Generar paredes inquebrantables
def generar_paredes():
    grosor_pared = 10
    paredes = [
        pygame.Rect(50, 50, grosor_pared, 500),  # Pared izquierda
        pygame.Rect(ANCHO_PANTALLA - 50 - grosor_pared, 50, grosor_pared, 500),  # Pared derecha
        pygame.Rect(50, 50, ANCHO_PANTALLA - 100, grosor_pared),  # Pared superior
        pygame.Rect(50, 500, 150, grosor_pared),  # Pared inferior izquierda
        pygame.Rect(ANCHO_PANTALLA - 200, 500, 150, grosor_pared)  # Pared inferior derecha
    ]
    return paredes

paredes = generar_paredes()

def generar_ladrillos():
    global ladrillos
    ladrillos = [pygame.Rect(110 + col * ANCHO_LADRILLO, 60 + row * ALTO_LADRILLO, ANCHO_LADRILLO, ALTO_LADRILLO) 
                 for row in range(FILAS) for col in range(COLUMNAS)]

generar_ladrillos()

# Variables de juego
puntaje = 0
mejoras = []

def dibujar_elementos():
    pantalla.fill(NEGRO)
    pygame.draw.rect(pantalla, BLANCO, pala)
    pygame.draw.ellipse(pantalla, BLANCO, pelota)
    
    for pared in paredes:
        pygame.draw.rect(pantalla, GRIS, pared)  # Dibujar paredes inquebrantables
    
    for ladrillo in ladrillos:
        pygame.draw.rect(pantalla, ROJO, ladrillo)
    
    for mejora in mejoras:
        color = AZUL if mejora[1] == "velocidad" else VERDE if mejora[1] == "pala" else AMARILLO
        pygame.draw.rect(pantalla, color, mejora[0])
    
    fuente = pygame.font.Font(None, 36)
    texto_puntaje = fuente.render(f"Puntaje: {puntaje}", True, BLANCO)
    pantalla.blit(texto_puntaje, (20, 10))
    
    pygame.display.flip()

def mover_pala():
    teclas = pygame.key.get_pressed()
    if teclas[pygame.K_LEFT] and pala.left > 0:
        pala.x -= VELOCIDAD_PALA
    if teclas[pygame.K_RIGHT] and pala.right < ANCHO_PANTALLA:
        pala.x += VELOCIDAD_PALA

    if not pelota_lanzada:
        pelota.x = pala.centerx - pelota.width // 2
        pelota.y = pala.y - pelota.height

def mover_pelota():
    global VELOCIDAD_PELOTA, puntaje, pelota_lanzada

    if pelota_lanzada:
        pelota.x += VELOCIDAD_PELOTA[0]
        pelota.y += VELOCIDAD_PELOTA[1]

        # Rebotes con los bordes de la pantalla
        if pelota.left <= 0 or pelota.right >= ANCHO_PANTALLA:
            VELOCIDAD_PELOTA[0] = -VELOCIDAD_PELOTA[0]
        if pelota.top <= 0:
            VELOCIDAD_PELOTA[1] = -VELOCIDAD_PELOTA[1]

        # Colisión con la pala
        if pelota.colliderect(pala):
            VELOCIDAD_PELOTA[1] = -VELOCIDAD_PELOTA[1]
            posicion_impacto = pelota.centerx - pala.centerx
            VELOCIDAD_PELOTA[0] += (posicion_impacto // 10)
            VELOCIDAD_PELOTA[0] = max(min(VELOCIDAD_PELOTA[0], 7), -7)

        # Rebotes con las paredes inquebrantables
        for pared in paredes:
            if pelota.colliderect(pared):
                if abs(pelota.left - pared.right) < 10 or abs(pelota.right - pared.left) < 10:
                    VELOCIDAD_PELOTA[0] = -VELOCIDAD_PELOTA[0]
                else:
                    VELOCIDAD_PELOTA[1] = -VELOCIDAD_PELOTA[1]

        # Colisión con los ladrillos
        for ladrillo in ladrillos[:]:
            if pelota.colliderect(ladrillo):
                VELOCIDAD_PELOTA[1] = -VELOCIDAD_PELOTA[1]
                ladrillos.remove(ladrillo)
                puntaje += 10
                generar_mejora(ladrillo)
                break

        if pelota.bottom >= ALTO_PANTALLA:
            reiniciar_pelota()

        if not ladrillos:
            generar_ladrillos()

def generar_mejora(ladrillo):
    tipo_mejora = random.choice(["velocidad", "pala", "puntos", None])
    if tipo_mejora:
        mejora = pygame.Rect(ladrillo.x, ladrillo.y, 20, 20)
        mejoras.append((mejora, tipo_mejora))

def reiniciar_pelota():
    global pelota_lanzada
    pelota_lanzada = False
    pelota.center = (ANCHO_PANTALLA // 2, ALTO_PANTALLA - ALTO_PALA - TAMANIO_PELOTA)
    VELOCIDAD_PELOTA[0], VELOCIDAD_PELOTA[1] = 0, 0

def mover_mejoras():
    for mejora, tipo in mejoras[:]:
        mejora.y += 5
        if mejora.colliderect(pala):
            mejoras.remove((mejora, tipo))
            aplicar_mejora(tipo)
        elif mejora.bottom >= ALTO_PANTALLA:
            mejoras.remove((mejora, tipo))

def aplicar_mejora(tipo):
    global pala, VELOCIDAD_PELOTA, puntaje
    if tipo == "velocidad":
        VELOCIDAD_PELOTA[0] *= 2
        VELOCIDAD_PELOTA[1] *= 2
    elif tipo == "pala":
        pala.width += 50
    elif tipo == "puntos":
        puntaje += 50

def comprobar_salida():
    teclas = pygame.key.get_pressed()
    if teclas[pygame.K_q]:
        pygame.quit()
        sys.exit()

def lanzar_pelota():
    global VELOCIDAD_PELOTA, pelota_lanzada
    if not pelota_lanzada:
        VELOCIDAD_PELOTA[0], VELOCIDAD_PELOTA[1] = random.choice([-3, 3]), -3
        pelota_lanzada = True

# Bucle principal del juego
while True:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_SPACE:
                lanzar_pelota()

    mover_pala()
    mover_pelota()
    mover_mejoras()
    dibujar_elementos()
    comprobar_salida()

    reloj.tick(FPS)