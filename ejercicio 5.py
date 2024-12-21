# División segura
try:
    # Solicitar dos números al usuario
    num1 = float(input("Ingrese el primer número: "))
    num2 = float(input("Ingrese el segundo número: "))
    
    # Intentar realizar la división
    resultado = num1 / num2
    print(f"El resultado de la división es: {resultado}")
except ZeroDivisionError:
    print("Error: No se puede dividir entre cero.")
except ValueError:
    print("Error: Debe ingresar un número válido.")


# Conversión segura de cadenas
try:
    # Solicitar una cadena que debería representar un número entero
    cadena = input("Ingrese un número entero: ")
    
    # Intentar convertir la cadena a entero
    numero_entero = int(cadena)
    print(f"El número entero ingresado es: {numero_entero}")
except ValueError:
    print("Error: El valor ingresado no es un número entero válido.")
