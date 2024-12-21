# Número par o impar
# Solicitar un número al usuario
numero = int(input("Ingrese un número: "))

# Determinar si el número es par o impar usando una estructura if
if numero % 2 == 0:
    print("El número", numero, "es par.")
else:
    print("El número", numero, "es impar.")


# Contador regresivo
# Solicitar un número entero positivo al usuario
contador = int(input("Ingrese un número entero positivo para la cuenta regresiva: "))

# Verificar que el número sea positivo
if contador >= 0:
    # Realizar la cuenta regresiva usando un bucle while
    while contador >= 0:
        print(contador)
        contador -= 1  # Decrementar el contador en cada iteración
else:
    print("Por favor, ingrese un número entero positivo.")
