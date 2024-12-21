import tkinter as tk
from tkinter import messagebox
from tkinter.ttk import Progressbar, Style
import random

# Variables globales
tiempo_total = 600
dificultad_config = {
    "fácil": {"rango": (1, 10), "operaciones": ["+", "-"]},
    "normal": {"rango": (1, 50), "operaciones": ["+", "-", "*"]},
    "difícil": {"rango": (1, 100), "operaciones": ["+", "-", "*", "/"]},
}
juego_activo = {"punt": 0, "rondas": 0, "errores": 0, "tiempo_restante": tiempo_total}

# Crear ventana principal
root = tk.Tk()
root.title("Juego Matemático Mejorado")
root.geometry("500x500")
root.config(bg="#f5f5f5")

# Funciones del juego
def nueva_pregunta():
    """Genera una nueva pregunta basada en la dificultad seleccionada."""
    juego_activo["tiempo_restante"] = tiempo_total
    dificultad = dificultad_selector.get()
    config = dificultad_config[dificultad]
    n1, n2 = random.randint(*config["rango"]), random.randint(*config["rango"])
    op = random.choice(config["operaciones"])
    if op == "/":
        n2 = max(1, n2)  # Evitar divisiones por cero
        juego_activo["resultado"] = round(n1 / n2, 1)
    else:
        juego_activo["resultado"] = eval(f"{n1}{op}{n2}")
    label_operacion.config(text=f"{n1} {op} {n2} = ?")
    actualizar_tiempo()

def verificar_respuesta():
    """Verifica la respuesta del usuario y actualiza estadísticas."""
    try:
        respuesta = float(entry_respuesta.get())
        if respuesta == juego_activo["resultado"]:
            juego_activo["punt"] += 1
            messagebox.showinfo("¡Correcto!", "¡Has acertado!")
        else:
            juego_activo["errores"] += 1
            messagebox.showinfo("Incorrecto", f"La respuesta correcta era {juego_activo['resultado']}.")
        juego_activo["rondas"] += 1
        actualizar_estadisticas()
        entry_respuesta.delete(0, tk.END)
        nueva_pregunta()
    except ValueError:
        messagebox.showerror("Error", "Por favor, ingrese un número válido.")

def actualizar_estadisticas():
    """Actualiza las etiquetas de puntuación, rondas y errores."""
    label_puntuacion.config(text=f"Puntuación: {juego_activo['punt']}")
    label_rondas.config(text=f"Rondas: {juego_activo['rondas']}")
    label_errores.config(text=f"Errores: {juego_activo['errores']}")

def actualizar_tiempo():
    """Maneja el temporizador y la barra de progreso."""
    if juego_activo["tiempo_restante"] > 0:
        juego_activo["tiempo_restante"] -= 1
        progreso = (juego_activo["tiempo_restante"] / tiempo_total) * 100
        barra_tiempo["value"] = progreso
        label_tiempo.config(text=f"Tiempo restante: {juego_activo['tiempo_restante']} seg")
        root.after(1000, actualizar_tiempo)
    else:
        messagebox.showinfo("Tiempo agotado", "Se terminó el tiempo. Pasando a la siguiente pregunta.")
        juego_activo["errores"] += 1
        actualizar_estadisticas()
        nueva_pregunta()

def reiniciar_juego():
    """Reinicia el juego a su estado inicial."""
    juego_activo.update({"punt": 0, "rondas": 0, "errores": 0, "tiempo_restante": tiempo_total})
    actualizar_estadisticas()
    nueva_pregunta()

# Configurar widgets
label_operacion = tk.Label(root, text="Presiona 'Nueva Operación' para empezar", font=("Arial", 16), bg="#f5f5f5", fg="#333")
label_operacion.pack(pady=20)

entry_respuesta = tk.Entry(root, font=("Arial", 14), width=20)
entry_respuesta.pack(pady=10)

button_verificar = tk.Button(root, text="Verificar Respuesta", command=verificar_respuesta, bg="#bbdefb", fg="#333", width=20)
button_verificar.pack(pady=5)

button_reiniciar = tk.Button(root, text="Reiniciar Juego", command=reiniciar_juego, bg="#ffccbc", fg="#333", width=20)
button_reiniciar.pack(pady=5)

dificultad_selector = tk.StringVar(value="normal")
dificultad_menu = tk.OptionMenu(root, dificultad_selector, *dificultad_config.keys())
dificultad_menu.pack(pady=10)

label_puntuacion = tk.Label(root, text="Puntuación: 0", font=("Arial", 12), bg="#f5f5f5", fg="#333")
label_puntuacion.pack()

label_rondas = tk.Label(root, text="Rondas: 0", font=("Arial", 12), bg="#f5f5f5", fg="#333")
label_rondas.pack()

label_errores = tk.Label(root, text="Errores: 0", font=("Arial", 12), bg="#f5f5f5", fg="#333")
label_errores.pack()

label_tiempo = tk.Label(root, text=f"Tiempo restante: {tiempo_total} seg", font=("Arial", 12), bg="#f5f5f5", fg="#333")
label_tiempo.pack(pady=10)

barra_tiempo = Progressbar(root, length=300, style="TProgressbar")
barra_tiempo.pack(pady=10)

# Estilo de la barra de progreso5
estilo = Style()
estilo.theme_use("clam")
estilo.configure("TProgressbar", thickness=15, foreground="#1e88e5", background="#1e88e5")

# Iniciar el juego
nueva_pregunta()
root.mainloop()

