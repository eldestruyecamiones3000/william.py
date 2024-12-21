import random

def juego_piedra_papel_tijera():
    print("¡Bienvenido al juego de Piedra, Papel o Tijera!")
    opciones = ["piedra", "papel", "tijera"]

    while True:
        jugador = input("Elige piedra, papel o tijera (o escribe 'salir' para terminar): ").lower()
        if jugador == "salir":
            print("Gracias por jugar. ¡Hasta la próxima!")
            break
        elif jugador not in opciones:
            print("Opción no válida. Intenta nuevamente.")
            continue

        computadora = random.choice(opciones)
        print(f"La computadora eligió: {computadora}")

        if jugador == computadora:
            print("¡Es un empate!")
        elif (jugador == "piedra" and computadora == "tijera") or \
             (jugador == "papel" and computadora == "piedra") or \
             (jugador == "tijera" and computadora == "papel"):
            print("¡Ganaste!")
        else:
            print("¡Perdiste!")

# Iniciar el juego
if __name__ == "__main__":
    juego_piedra_papel_tijera()
