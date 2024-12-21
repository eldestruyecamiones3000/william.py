import pygame
import random
import sys

# Inicializar Pygame
pygame.init()

# Configuración de la ventana
ancho, alto = 800, 600
ventana = pygame.display.set_mode((ancho, alto))
pygame.display.set_caption("Atrapa el cuadrado")

# Colores
BLANCO = (255, 255, 255)
ROJO = (255, 0, 0)
VERDE = (0, 255, 0)

# Variables del juego
cuadrado_tamaño = 50
cuadrado_x = random.randint(0, ancho - cuadrado_tamaño)
cuadrado_y = random.randint(0, alto - cuadrado_tamaño)
puntos = 0
fuente = pygame.font.Font(None, 36)
tiempo_maximo = 30  # Tiempo límite en segundos
tiempo_inicio = pygame.time.get_ticks()
color_cuadrado = ROJO
codigo_secreto = "BONUS10"  # Código secreto para puntos
codigo_tiempo = "MAS_TIEMPO"  # Código secreto para obtener tiempo extra

# Función principal del juego
def juego():
    global cuadrado_x, cuadrado_y, puntos, color_cuadrado, tiempo_inicio, tiempo_maximo

    # Bucle principal del juego
    while True:
        ventana.fill(BLANCO)

        # Mostrar el cuadrado
        cuadrado = pygame.Rect(cuadrado_x, cuadrado_y, cuadrado_tamaño, cuadrado_tamaño)
        pygame.draw.rect(ventana, color_cuadrado, cuadrado)

        # Mostrar puntos
        texto_puntos = fuente.render(f"Puntos: {puntos}", True, (0, 0, 0))
        ventana.blit(texto_puntos, (10, 10))

        # Tiempo restante
        tiempo_actual = (pygame.time.get_ticks() - tiempo_inicio) // 1000
        tiempo_restante = tiempo_maximo - tiempo_actual
        texto_tiempo = fuente.render(f"Tiempo: {tiempo_restante}", True, (0, 0, 0))
        ventana.blit(texto_tiempo, (ancho - 150, 10))

        # Comprobar si el tiempo ha terminado
        if tiempo_restante <= 0:
            texto_final = fuente.render("¡Tiempo terminado!", True, (0, 0, 0))
            ventana.blit(texto_final, (ancho // 2 - 100, alto // 2))
            pygame.display.flip()
            pygame.time.delay(2000)
            pygame.quit()
            sys.exit()

        # Eventos del juego
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif evento.type == pygame.KEYDOWN:
                # Detectar códigos secretos
                if evento.unicode.upper() == "B":
                    entrada = input("Introduce el código secreto: ")
                    if entrada.upper() == codigo_secreto:
                        puntos += 10
                        color_cuadrado = VERDE  # Cambia el color del cuadrado a verde
                        print("¡Código secreto activado! +10 puntos")
                    elif entrada.upper() == codigo_tiempo:
                        tiempo_maximo += 10  # Agrega 10 segundos de tiempo extra
                        print("¡Código de tiempo activado! +10 segundos")
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if cuadrado.collidepoint(evento.pos):
                    puntos += 1
                    cuadrado_x = random.randint(0, ancho - cuadrado_tamaño)
                    cuadrado_y = random.randint(0, alto - cuadrado_tamaño)

        pygame.display.flip()
        pygame.time.Clock().tick(30)

# Iniciar el juego
juego()
