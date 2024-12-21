import tkinter as tk
from tkinter import messagebox
import random
import time

puntuacion = 0
rondas = 0
tiempo_restante = 60

# Función para generar una nueva operación matemática
def nueva_operacion():
    global numero1, numero2, operacion, resultado_correcto
    # Generamos 2 números aleatorios
    numero1 = random.randint(1, 100)
    numero2 = random.randint(1, 10)
    # Elegimos el tipo de operación
    operacion = random.choice(["+", "-", "*", "/"])

    # Calculamos el resultado correcto
    if operacion == "+":
        resultado_correcto = numero1 + numero2
    elif operacion == "-":
        resultado_correcto = numero1 - numero2
    elif operacion == "*":
        resultado_correcto = numero1 * numero2
    elif operacion == "/":
        resultado_correcto = round(numero1 / numero2, 1)  # Redondeo a un decimal

    label_operacion.config(text=f"{numero1} {operacion} {numero2} = ?")

# Comprobamos la respuesta
def verificar_respuesta():
    global puntuacion, rondas
    try:
        respuesta_usuario = float(entry_respuesta.get())
        if respuesta_usuario == resultado_correcto:
            puntuacion += 1
            messagebox.showinfo("¡Correcto!", "😁 ¡Respuesta correcta!")
        else:
            messagebox.showinfo("¡Incorrecto!", f"😒 ¡Respuesta incorrecta! La correcta es {resultado_correcto}")
        rondas += 1
        label_puntuacion.config(text=f"Puntuación: {puntuacion}")
        entry_respuesta.delete(0, tk.END)

        # Verificamos si deben continuar las rondas
        if rondas < 10 and tiempo_restante > 0:  # Jugar 10 rondas o hasta que se acabe el tiempo
            nueva_operacion()
        else:
            finalizar_juego()
    except ValueError:
        messagebox.showerror("Error", "🚧 Por favor, ingresa un número válido.")

# Iniciar temporizador
def iniciar_temporizador():
    global tiempo_restante
    if tiempo_restante > 0:
        tiempo_restante -= 1
        label_tiempo.config(text=f"Tiempo restante: {tiempo_restante}s")
        root.after(1000, iniciar_temporizador)  # Llamamos a iniciar_temporizador cada segundo
    else:
        finalizar_juego()

# Finalizar el juego
def finalizar_juego():
    messagebox.showinfo("Juego terminado", f"¡Se acabó el tiempo!\nTu puntuación final es: {puntuacion}")

# Reiniciar juego
def reiniciar_juego():
    global puntuacion, rondas, tiempo_restante
    puntuacion = 0
    rondas = 0
    tiempo_restante = 60
    label_puntuacion.config(text=f"Puntuación: {puntuacion}")
    label_tiempo.config(text=f"Tiempo restante: {tiempo_restante}s")
    nueva_operacion()
    iniciar_temporizador()

# Pantalla
root = tk.Tk()
root.title("Juego de Matemáticas 🧠")
root.geometry("400x300")
root.configure(bg="#FFEB99")

# Título
label_titulo = tk.Label(root, text="¡Resuelve la Operación! 🧮", font=("Comic Sans MS", 20), bg='#FFEB99')
label_titulo.pack(pady=10)

# Mostrar la operación matemática
label_operacion = tk.Label(root, text="", font=("Comic Sans MS", 30), bg='#FFEB99')
label_operacion.pack(pady=20)

# Campo para la respuesta del jugador
entry_respuesta = tk.Entry(root, font=("Comic Sans MS", 14), width=10)
entry_respuesta.pack(pady=10)

# Botón para enviar la respuesta
button_enviar = tk.Button(root, text="Enviar", command=verificar_respuesta, font=("Comic Sans MS", 12), bg="#FF6F61")
button_enviar.pack(pady=10)

# Mostrar la puntuación
label_puntuacion = tk.Label(root, text="Puntuación: 0", font=("Comic Sans MS", 14), bg='#FFEB99')
label_puntuacion.pack(pady=10)

# Mostrar el temporizador
label_tiempo = tk.Label(root, text=f"Tiempo restante: {tiempo_restante}s", font=("Comic Sans MS", 14), bg='#FFEB99')
label_tiempo.pack(pady=10)

# Comenzar el juego
nueva_operacion()
iniciar_temporizador()

# Ejecutar la aplicación
root.mainloop()
