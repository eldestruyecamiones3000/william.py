import tkinter as tk
from PIL import Image, ImageTk
import random
import time

# Configuración de la ventana
root = tk.Tk()
root.title("meteor game")
root.geometry("600x600")
root.config(bg="#000000")

# Configuración del lienzo
canvas = tk.Canvas(root, width=600, height=600, bg="#000000")
canvas.pack()

# Variables iniciales
player_size = 30
bullet_size = 5
bullet_speed = 10
enemy_size = 62
enemy_speed = 6
enemies = []
bullets = []
wave = 1
score = 0
enemies_killed = 0
enemies_to_kill = 20
special_ready = True
special_cooldown = 30  # Segundos de recarga
last_special_time = 0

# Variables del jefe
jefe = None
jefe_activo = False
jefe_vida_actual = 0
jefe_tamano = 200
jefe_bullets = []
jefe_bullet_speed = 4

# Cargar imágenes
try:
    meteorito_img = Image.open("meteorito.png").resize((enemy_size, enemy_size))
    meteorito_tk = ImageTk.PhotoImage(meteorito_img)
except FileNotFoundError:
    meteorito_tk = None

player = canvas.create_rectangle(300 - player_size / 2, 500 - player_size / 2, 
                                 300 + player_size / 2, 500 + player_size / 2, fill="red")

# Etiquetas
score_label = tk.Label(root, text=f"Puntaje: {score}", fg="white", bg="#000000", font=("Arial", 14))
score_label.pack(pady=10)
wave_label = tk.Label(root, text=f"Wave: {wave}", fg="white", bg="#000000", font=("Arial", 14))
wave_label.pack(pady=5)
special_label = tk.Label(root, text="Especial: Listo", fg="white", bg="#000000", font=("Arial", 14))
special_label.pack(pady=5)

# Funciones del juego
def mover_jugador(event):
    x, y = event.x, event.y
    canvas.coords(player, x - player_size / 2, y - player_size / 2, x + player_size / 2, y + player_size / 2)

def disparar():
    x1, y1, x2, y2 = canvas.coords(player)
    bullet = canvas.create_oval((x1 + x2) / 2 - bullet_size / 2, y1 - bullet_size, 
                                 (x1 + x2) / 2 + bullet_size / 2, y1, fill="yellow")
    bullets.append(bullet)

def mover_balas():
    for bullet in bullets[:]:
        canvas.move(bullet, 0, -bullet_speed)
        if canvas.coords(bullet)[1] < 0:
            canvas.delete(bullet)
            bullets.remove(bullet)

def crear_enemigos():
    if not jefe_activo and random.random() < 0.05 + (wave * 0.01):
        x = random.randint(0, 550)
        enemy = canvas.create_image(x, 0, image=meteorito_tk)
        enemies.append(enemy)

def mover_enemigos():
    for enemy in enemies[:]:
        canvas.move(enemy, 0, enemy_speed)
        if canvas.coords(enemy)[1] > 600:
            canvas.delete(enemy)
            enemies.remove(enemy)

def verificar_colisiones():
    global score, enemies_killed, jefe_vida_actual, jefe_activo
    for bullet in bullets[:]:
        bullet_coords = canvas.coords(bullet)
        for enemy in enemies[:]:
            enemy_coords = canvas.coords(enemy)
            if (bullet_coords[0] > enemy_coords[0] - enemy_size / 2 and
                bullet_coords[0] < enemy_coords[0] + enemy_size / 2 and
                bullet_coords[1] > enemy_coords[1] - enemy_size / 2 and
                bullet_coords[1] < enemy_coords[1] + enemy_size / 2):
                canvas.delete(bullet)
                canvas.delete(enemy)
                bullets.remove(bullet)
                enemies.remove(enemy)
                score += 10
                enemies_killed += 1
                score_label.config(text=f"Puntaje: {score}")
                break
        if jefe_activo and jefe is not None:
            jefe_coords = canvas.coords(jefe)
            if (bullet_coords[0] > jefe_coords[0] - jefe_tamano / 2 and
                bullet_coords[0] < jefe_coords[0] + jefe_tamano / 2 and
                bullet_coords[1] > jefe_coords[1] - jefe_tamano / 2 and
                bullet_coords[1] < jefe_coords[1] + jefe_tamano / 2):
                canvas.delete(bullet)
                bullets.remove(bullet)
                jefe_vida_actual -= 10
                if jefe_vida_actual <= 0:
                    jefe_activo = False
                    canvas.delete(jefe)
                    jefe_bullets.clear()
                    score += 100
                    score_label.config(text=f"Puntaje: {score}")

def colision_con_jugador():
    player_coords = canvas.coords(player)
    for enemy in enemies[:]:
        enemy_coords = canvas.coords(enemy)
        if (enemy_coords[0] > player_coords[0] and
            enemy_coords[0] < player_coords[2] and
            enemy_coords[1] > player_coords[1] and
            enemy_coords[1] < player_coords[3]):
            game_over()
            break
    for bullet, _, _ in jefe_bullets[:]:
        bullet_coords = canvas.coords(bullet)
        if (bullet_coords[0] > player_coords[0] and
            bullet_coords[2] < player_coords[2] and
            bullet_coords[1] > player_coords[1] and
            bullet_coords[3] < player_coords[3]):
            game_over()

def disparar_jefe():
    if jefe_activo and jefe is not None:
        jefe_coords = canvas.coords(jefe)
        player_coords = canvas.coords(player)
        dx = (player_coords[0] + player_size / 2) - jefe_coords[0]
        dy = (player_coords[1] + player_size / 2) - jefe_coords[1]
        magnitude = (dx**2 + dy**2)**0.5
        dx /= magnitude
        dy /= magnitude
        bullet = canvas.create_oval(
            jefe_coords[0] - bullet_size, jefe_coords[1] - bullet_size,
            jefe_coords[0] + bullet_size, jefe_coords[1] + bullet_size,
            fill="blue"
        )
        jefe_bullets.append((bullet, dx * jefe_bullet_speed, dy * jefe_bullet_speed))

def mover_balas_jefe():
    for bullet, dx, dy in jefe_bullets[:]:
        canvas.move(bullet, dx, dy)
        x1, y1, x2, y2 = canvas.coords(bullet)
        if x1 < 0 or x2 > 600 or y1 < 0 or y2 > 600:
            canvas.delete(bullet)
            jefe_bullets.remove((bullet, dx, dy))

def usar_especial():
    global special_ready, last_special_time
    if special_ready:
        special_ready = False
        last_special_time = time.time()
        special_label.config(text="Especial: En enfriamiento")
        x1, y1, x2, y2 = canvas.coords(player)
        laser = canvas.create_line((x1 + x2) / 2, y1, (x1 + x2) / 2, 0, fill="cyan", width=5)
        root.after(100, lambda: canvas.delete(laser))
        for enemy in enemies[:]:
            ex, ey = canvas.coords(enemy)
            if abs((x1 + x2) / 2 - ex) < enemy_size / 2:
                canvas.delete(enemy)
                enemies.remove(enemy)
        root.after(3000, actualizar_especial)

def actualizar_especial():
    global special_ready
    special_ready = True
    special_label.config(text="Especial: Listo")

def comprobar_jefe():
    global jefe, jefe_activo, jefe_vida_actual, enemies_killed
    if wave % 5 == 0 and not jefe_activo:
        jefe_vida_actual = 100 + (wave // 5) * 50
        jefe = canvas.create_image(300, 100, image=meteorito_tk)
        jefe_activo = True
        enemies_killed = 0
        root.after(1000, disparar_jefe)

def actualizar_wave():
    global wave, enemies_killed, enemy_speed
    if enemies_killed >= enemies_to_kill and not jefe_activo:
        wave += 1
        enemies_killed = 0
        enemy_speed += 0.5
        wave_label.config(text=f"Wave: {wave}")
        comprobar_jefe()

def game_over():
    canvas.create_text(300, 300, text="GAME OVER", fill="white", font=("Arial", 24))
    root.after(2000, root.quit)

def juego():
    crear_enemigos()
    mover_enemigos()
    mover_balas()
    mover_balas_jefe()
    colision_con_jugador()
    verificar_colisiones()
    actualizar_wave()
    root.after(30, juego)

canvas.bind("<Motion>", mover_jugador)
root.bind("<space>", lambda event: disparar())
root.bind("<Shift_L>", lambda event: usar_especial())

juego()
root.mainloop()
