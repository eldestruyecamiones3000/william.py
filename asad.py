import random

def adivina_numero():
    numero_secreto = random.randint(1, 100)
    intentos = 0
    adivinado = False

    print("¡Bienvenido al juego de adivinar el número!")
    print("Estoy pensando en un número entre 1 y 100.")

    while not adivinado:
        intento = input("Que numero piensas? ")
        intentos += 1

        try:
            intento = int(intento)
        except ValueError:
            print("Por favor, ingresa un número válido.")
            continue

        if intento < 1 or intento > 100:
            print("El número debe estar entre 1 y 100.")
            continue

        if intento < numero_secreto:
            print("Demasiado bajo. Intenta de nuevo.")
        elif intento > numero_secreto:
            print("Demasiado alto. Intenta de nuevo.")
        else:
            adivinado = True
            print(f"¡Felicidades! Has adivinado el número {numero_secreto} en {intentos} intentos.")

if __name__ == "__main__":
    adivina_numero()
