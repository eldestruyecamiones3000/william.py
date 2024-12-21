import pygame
import socket
import threading
import sys

# Inicialización de Pygame
pygame.init()

# Configuración de la pantalla
screen_width = 800
screen_height = 300
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Geometry Dash Multijugador")

# Parámetros del jugador
player_size = 50
player_color = (255, 0, 0)
player_pos = [50, screen_height - player_size]
player_speed = 5
is_jumping = False
jump_strength = -15
gravity = 1
velocity = 0

# Parámetros del segundo jugador
player2_color = (0, 0, 255)
player2_pos = [50, screen_height - player_size]

# Parámetros de red
is_server = input("¿Quieres ser el servidor? (s/n): ").lower() == 's'
code = input("Ingrese el código de sala: ")

# Configuración del servidor
server_ip = "0.0.0.0"  # Escuchar en todas las interfaces de red
server_port = 12345
max_clients = 2

# Crear socket
socket_conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

if is_server:
    # Iniciar el servidor
    socket_conn.bind((server_ip, server_port))
    socket_conn.listen(max_clients)
    print("Servidor iniciado. Esperando jugadores...")
    codes = {code: []}

    def handle_client(client_socket):
        while True:
            try:
                data = client_socket.recv(1024).decode()
                if not data:
                    break
                for other_client in codes[code]:
                    if other_client != client_socket:
                        other_client.send(data.encode())
            except:
                break

        codes[code].remove(client_socket)
        client_socket.close()

    def accept_clients():
        while True:
            client_socket, addr = socket_conn.accept()
            codes[code].append(client_socket)
            threading.Thread(target=handle_client, args=(client_socket,)).start()

    threading.Thread(target=accept_clients, daemon=True).start()
else:
    # Conectar al servidor
    server_ip = input("Ingrese la IP del servidor: ")
    socket_conn.connect((server_ip, server_port))
    socket_conn.send(code.encode())

def receive_data():
    while True:
        try:
            data = socket_conn.recv(1024).decode()
            x, y = map(int, data.split(','))
            player2_pos[0], player2_pos[1] = x, y
        except:
            break

# Iniciar hilo para recibir datos
threading.Thread(target=receive_data, daemon=True).start()

# Bucle principal del juego
clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            socket_conn.close()
            sys.exit()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE] and not is_jumping:
        velocity = jump_strength
        is_jumping = True
    
    if player_pos[1] >= screen_height - player_size:
        player_pos[1] = screen_height - player_size
        is_jumping = False

    velocity += gravity
    player_pos[1] += velocity

    # Enviar posición del jugador al servidor
    socket_conn.send(f"{player_pos[0]},{player_pos[1]}".encode())
    
    screen.fill((0, 0, 0))
    pygame.draw.rect(screen, player_color, (*player_pos, player_size, player_size))
    pygame.draw.rect(screen, player2_color, (*player2_pos, player_size, player_size))
    pygame.display.flip()
    clock.tick(30)
