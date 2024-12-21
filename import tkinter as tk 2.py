import tkinter as tk
from tkinter import messagebox
import random
import time
import pickle
import os

puntuacion = 0
mejores_puntuaciones = []
numero_ronda = 0
tiempo_restante = 60
archivo_puntuaciones = "mejores_puntuaciones.pkl"

# Cargar mejores puntuaciones si el archivo existe
if os.path.exists(archivo_puntuaciones):
    with open(archivo_puntuaciones, "rb") as archivo:
        mejores_puntuaciones = pickle.load(archivo)

# Función para actualizar las mejores puntuaciones y guardarlas
def actualizar_mejores_puntuaciones():
    global puntuacion
    mejores_puntuaciones.append(puntuacion)
    mejores_puntuaciones.sort(reverse=True)
    mejores_puntuaciones = mejores_puntuaciones[:5]  # Solo guardamos las 5 mejores
    with open(archivo_puntuaciones, "wb") as archivo:
        pickle.dump(mejores_puntuaciones, archivo)

# Función para mostrar el menú principal
def mostrar_menu():
    lista_mejores_puntuaciones.config(text="\n".join(map(str, mejores_puntuaciones)))
    menu_frame.pack()
    juego_frame.pack_forget()

# Función para iniciar el juego
def iniciar_juego():
    global puntuacion, numero_ronda, tiempo_restante
    puntuacion = 0
    numero_ronda = 0
    tiempo_restante = 60
    label_puntuacion.config(text=f"Puntuación: {puntuacion}")
    label_tiempo.config(text=f"Tiempo restante: {tiempo_restante}s")
    menu_frame.pack_forget()
    juego_frame.pack()
    nueva_operacion()
    iniciar_temporizador()

# Función para generar una nueva operación matemática
def nueva_operacion():
    global numero1, numero2, operacion, resultado_correcto
    numero1 = random.randint(1, 100)
    numero2 = random.randint(1, 10)
    operacion = random.choice(["+", "-", "*", "/"])

    if operacion == "+":
        resultado_correcto = numero1 + numero2
    elif operacion == "-":
        resultado_correcto = numero1 - numero2
    elif operacion == "*":
        resultado_correcto = numero1 * numero2
    elif operacion == "/":
        resultado_correcto = round(numero1 / numero2, 1)

    label_operacion.config(text=f"{numero1} {operacion} {numero2} = ?")

# Comprobamos la respuesta
def verificar_respuesta():
    global puntuacion, numero_ronda
    try:
        respuesta_usuario = float(entry_respuesta.get())
        if respuesta_usuario == resultado_correcto:
            puntuacion += 1
            messagebox.showinfo("¡Correcto!", "😁 ¡Respuesta correcta!")
        else:
            messagebox.showinfo("¡Incorrecto!", f"😒 ¡Respuesta incorrecta! La correcta era {resultado_correcto}")
        numero_ronda += 1
        label_puntuacion.config(text=f"Puntuación: {puntuacion}")
        entry_respuesta.delete(0, tk.END)

        nueva_operacion()
    except ValueError:
        messagebox.showerror("Error", "🚧 Por favor, ingresa un número válido.")

# Iniciar temporizador
def iniciar_temporizador():
    global tiempo_restante
    if tiempo_restante > 0:
        tiempo_restante -= 1
        label_tiempo.config(text=f"Tiempo restante: {tiempo_restante}s")
        root.after(1000, iniciar_temporizador)
    else:
        finalizar_juego()

# Finalizar el juego
def finalizar_juego():
    actualizar_mejores_puntuaciones()
    messagebox.showinfo("Juego terminado", f"¡Se acabó el tiempo!\nTu puntuación final es: {puntuacion}\nÚltima operación: {numero1} {operacion} {numero2} = {resultado_correcto}")
    mostrar_menu()

# Configuración de la interfaz gráfica
root = tk.Tk()
root.title("Juego de Matemáticas 🧠")
root.geometry("400x400")
root.configure(bg="#FFEB99")

# Menú principal
menu_frame = tk.Frame(root, bg="#FFEB99")
label_menu = tk.Label(menu_frame, text="Juego de Matemáticas 🧠", font=("Comic Sans MS", 20), bg='#FFEB99')
label_menu.pack(pady=10)
button_iniciar = tk.Button(menu_frame, text="Iniciar Juego", command=iniciar_juego, font=("Comic Sans MS", 14), bg="#FF6F61")
button_iniciar.pack(pady=10)
button_salir = tk.Button(menu_frame, text="Salir", command=root.quit, font=("Comic Sans MS", 14), bg="#FF6F61")
button_salir.pack(pady=10)
label_mejores_puntuaciones = tk.Label(menu_frame, text="Mejores Puntuaciones", font=("Comic Sans MS", 14), bg="#FFEB99")
label_mejores_puntuaciones.pack(pady=10)
lista_mejores_puntuaciones = tk.Label(menu_frame, text="\n".join(map(str, mejores_puntuaciones)), font=("Comic Sans MS", 12), bg="#FFEB99")
lista_mejores_puntuaciones.pack()

# Pantalla del juego
juego_frame = tk.Frame(root, bg="#FFEB99")
label_titulo = tk.Label(juego_frame, text="¡Resuelve la Operación! 🧮", font=("Comic Sans MS", 20), bg='#FFEB99')
label_titulo.pack(pady=10)
label_operacion = tk.Label(juego_frame, text="", font=("Comic Sans MS", 30), bg='#FFEB99')
label_operacion.pack(pady=20)
entry_respuesta = tk.Entry(juego_frame, font=("Comic Sans MS", 14), width=10)
entry_respuesta.pack(pady=10)
button_enviar = tk.Button(juego_frame, text="Enviar", command=verificar_respuesta, font=("Comic Sans MS", 12), bg="#FF6F61")
button_enviar.pack(pady=10)
label_puntuacion = tk.Label(juego_frame, text="Puntuación: 0", font=("Comic Sans MS", 14), bg='#FFEB99')
label_puntuacion.pack(pady=10)
label_tiempo = tk.Label(juego_frame, text=f"Tiempo restante: {tiempo_restante}s", font=("Comic Sans MS", 14), bg='#FFEB99')
label_tiempo.pack(pady=10)

# Mostrar el menú al inicio
mostrar_menu()

# Ejecutar la aplicación
root.mainloop()
