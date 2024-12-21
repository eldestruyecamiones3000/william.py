import pygame
import sys

# Inicializar Pygame
pygame.init()

# Configuración de la pantalla
ANCHO, ALTO = 800, 600
ventana = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Juego de Dibujo")

# Colores
NEGRO, BLANCO, ROJO, VERDE, AZUL = (0, 0, 0), (255, 255, 255), (255, 0, 0), (0, 255, 0), (0, 0, 255)
color_actual = NEGRO

# Propiedades del pincel
pincel_tamano = 5

# Reloj para el tiempo de juego
reloj = pygame.time.Clock()
TIEMPO_LIMITE = 60  # 60 segundos
tiempo_inicial = pygame.time.get_ticks()

# Bucle principal del juego
jugando = True
while jugando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            jugando = False

        # Cambiar el color del pincel con las teclas
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_r:
                color_actual = ROJO
            elif evento.key == pygame.K_g:
                color_actual = VERDE
            elif evento.key == pygame.K_b:
                color_actual = AZUL
            elif evento.key == pygame.K_w:
                color_actual = BLANCO
            elif evento.key == pygame.K_k:
                color_actual = NEGRO
            elif evento.key == pygame.K_UP:
                pincel_tamano += 1
            elif evento.key == pygame.K_DOWN:
                pincel_tamano -= 1

    # Obtener la posición del mouse y si está presionado
    mouse_pulsado = pygame.mouse.get_pressed()[0]
    mouse_x, mouse_y = pygame.mouse.get_pos()

    if mouse_pulsado:
        pygame.draw.circle(ventana, color_actual, (mouse_x, mouse_y), pincel_tamano)

    # Actualizar la pantalla
    pygame.display.flip()

    # Calcular el tiempo restante
    tiempo_transcurrido = (pygame.time.get_ticks() - tiempo_inicial) / 1000  # Convertir a segundos
    tiempo_restante = TIEMPO_LIMITE - tiempo_transcurrido

    # Mostrar el tiempo restante en pantalla
    ventana.fill(NEGRO, (0, 0, 200, 50))
    fuente = pygame.font.Font(None, 36)
    texto_tiempo = fuente.render(f"Tiempo: {int(tiempo_restante)}", True, BLANCO)
    ventana.blit(texto_tiempo, (10, 10))

    if tiempo_restante <= 0:
        jugando = False

    # Control de FPS
    reloj.tick(60)

# Mostrar mensaje de fin de juego
ventana.fill(NEGRO)
texto_fin = fuente.render("¡Tiempo Terminado!", True, ROJO)
ventana.blit(texto_fin, (ANCHO // 2 - 100, ALTO // 2))
pygame.display.flip()
pygame.time.wait(3000)
pygame.quit()
sys.exit()
    