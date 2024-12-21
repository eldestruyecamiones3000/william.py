import pygame
import random

# Inicializar Pygame
pygame.init()

# Configuración de pantalla
ancho_ventana = 800
alto_ventana = 600
ventana = pygame.display.set_mode((ancho_ventana, alto_ventana))
pygame.display.set_caption("Juego de Disparos Espaciales")

# Colores
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
ROJO = (255, 0, 0)
VERDE = (0, 255, 0)

# Clase del jugador (nave espacial)
class Nave(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 40))
        self.image.fill(VERDE)
        self.rect = self.image.get_rect()
        self.rect.center = (ancho_ventana // 2, alto_ventana - 50)
        self.velocidad_x = 0
        self.velocidad_y = 0

    def update(self):
        self.velocidad_x = 0
        self.velocidad_y = 0
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_a]:  # Mover a la izquierda
            self.velocidad_x = -5
        if teclas[pygame.K_d]:  # Mover a la derecha
            self.velocidad_x = 5
        if teclas[pygame.K_w]:  # Mover hacia arribad
            self.velocidad_y = -5
        if teclas[pygame.K_s]:  # Mover hacia abajo
            self.velocidad_y = 5

        self.rect.x += self.velocidad_x
        self.rect.y += self.velocidad_y

        # Limitar el movimiento dentro de la pantalla
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > ancho_ventana:
            self.rect.right = ancho_ventana
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > alto_ventana:
            self.rect.bottom = alto_ventana

    def disparar(self):
        bala = Bala(self.rect.centerx, self.rect.top)
        todas_las_sprites.add(bala)
        balas.add(bala)

# Clase de asteroides
class Asteroide(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(ROJO)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, ancho_ventana - self.rect.width)
        self.rect.y = random.randint(-100, -4) #
        self.velocidad_y = random.randint(3, 8)
        self.velocidad_x = random.randint(-3, 3)

    def update(self):
        self.rect.x += self.velocidad_x
        self.rect.y += self.velocidad_y

        # Si el asteroide sale de la pantalla, reaparece arriba
        if self.rect.top > alto_ventana or self.rect.right < 0 or self.rect.left > ancho_ventana:
            self.rect.x = random.randint(0, ancho_ventana - self.rect.width)
            self.rect.y = random.randint(-100, -40)
            self.velocidad_y = random.randint(3, 8)
            self.velocidad_x = random.randint(-3, 3)

# Clase de balas
class Bala(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((10, 20))
        self.image.fill(BLANCO)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.velocidad_y = -10

    def update(self):
        self.rect.y += self.velocidad_y
        # Eliminar la bala si sale de la pantalla
        if self.rect.bottom < 0:
            self.kill()

# Función principal del juego
def main():
    global todas_las_sprites, balas

    # Crear jugador
    nave = Nave()

    # Grupos de sprites
    todas_las_sprites = pygame.sprite.Group()
    asteroides = pygame.sprite.Group()
    balas = pygame.sprite.Group()

    # Añadir la nave al grupo de sprites
    todas_las_sprites.add(nave)

    # Crear asteroides
    for _ in range(8):
        asteroide = Asteroide()
        todas_las_sprites.add(asteroide)
        asteroides.add(asteroide)

    # Variables del juego
    reloj = pygame.time.Clock()
    puntuacion = 0
    juego_activo = True

    # Bucle principal del juego
    while juego_activo:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                juego_activo = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    nave.disparar()

        # Actualizar sprites
        todas_las_sprites.update()

        # Comprobar colisiones entre balas y asteroides
        colisiones = pygame.sprite.groupcollide(asteroides, balas, True, True)
        for colision in colisiones:
            puntuacion += 10
            asteroide = Asteroide()
            todas_las_sprites.add(asteroide)
            asteroides.add(asteroide)

        # Comprobar colisiones entre la nave y los asteroides
        if pygame.sprite.spritecollideany(nave, asteroides):
            juego_activo = False  # Si la nave choca con un asteroide, el juego termina

        # Dibujar en pantalla
        ventana.fill(NEGRO)
        todas_las_sprites.draw(ventana)

        # Mostrar puntuación
        fuente = pygame.font.SysFont(None, 36)
        texto_puntuacion = fuente.render(f"Puntuación: {puntuacion}", True, BLANCO)
        ventana.blit(texto_puntuacion, (10, 10))

        # Actualizar la pantalla
        pygame.display.flip()

        # Limitar a 60 FPS
        reloj.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()