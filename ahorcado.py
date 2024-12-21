import random

# Lista de palabras para el juego
palabras = ['mbappe', 'neymar', 'messi', 'maradona', 'james rodriguez', 'pepe']

# Dibujos del ahorcado en diferentes etapas
ahorcado_visual = [
    """
       +---+
       |   |
           |
           |
           |
           |
    =========
    """,
    """
       +---+
       |   |
       O   |
           |
           |
           |
    =========
    """,
    """
       +---+
       |   |
       O   |
       |   |
           |
           |
    =========
    """,
    """
       +---+
       |   |
       O   |
      /|   |
           |
           |
    =========
    """,
    """
       +---+
       |   |
       O   |
      /|\\  |
           |
           |
    =========
    """,
    """
       +---+
       |   |
       O   |
      /|\\  |
      /    |
           |
    =========
    """,
    """
       +---+
       |   |
       O   |
      /|\\  |
      / \\  |
           |
    =========
    """
]

# Función para seleccionar una palabra al azar
def seleccionar_palabra():
    return random.choice(palabras)

# Función para mostrar el estado actual de la palabra
def mostrar_palabra(palabra, letras_adivinadas):
    estado = ''
    for letra in palabra:
        if letra in letras_adivinadas:
            estado += letra + ' '
        else:
            estado += '_ '
    return estado.strip()

# Función principal del juego
def jugar():
    palabra = seleccionar_palabra()
    letras_adivinadas = []
    intentos = 6
    ha_ganado = False

    print("🎉 ¡Bienvenido al juego del Ahorcado! 🎉")
    print("¡Intenta adivinar la palabra antes de que el dibujo esté completo!")
    print(ahorcado_visual[0])
    print(mostrar_palabra(palabra, letras_adivinadas))

    while intentos > 0 and not ha_ganado:
        letra = input("Adivina una letra: ").lower()

        if letra in letras_adivinadas:
            print("🔁 Ya has adivinado esa letra. Intenta con otra.")
        elif letra in palabra:
            letras_adivinadas.append(letra)
            print("🎯 ¡Acertaste!")
        else:
            intentos -= 1
            print(f"❌ Letra incorrecta. Te quedan {intentos} intentos.")
       
        print(ahorcado_visual[6 - intentos])  # Muestra el dibujo actualizado
        estado_actual = mostrar_palabra(palabra, letras_adivinadas)
        print(estado_actual)

        if "_" not in estado_actual:
            ha_ganado = True

    if ha_ganado:
        print("🎉 ¡Felicidades, has ganado!")
        print("La palabra era:", palabra)
    else:
        print("💀 Oh no, perdiste. La palabra era:", palabra)
        print("¡Mejor suerte la próxima vez!")

# Iniciar el juego
if __name__ == "__main__":
    jugar()