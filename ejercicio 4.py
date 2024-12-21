import math

# Función de área de un círculo
def calcular_area_circulo(radio):
    """Calcula el área de un círculo dado su radio."""
    area = math.pi * (radio ** 2)
    return area

# Solicitar el radio al usuario y llamar a la función
radio = float(input("Ingrese el radio del círculo: "))
area = calcular_area_circulo(radio)
print(f"El área del círculo con radio {radio} es: {round(area, 2)}")


# Función de conversión de temperatura
def celsius_a_fahrenheit(celsius):
    """Convierte una temperatura de Celsius a Fahrenheit."""
    fahrenheit = celsius * 9 / 5 + 32
    return fahrenheit

# Solicitar la temperatura en Celsius al usuario y llamar a la función
celsius = float(input("Ingrese la temperatura en grados Celsius: "))
fahrenheit = celsius_a_fahrenheit(celsius)
print(f"{celsius} grados Celsius equivalen a {round(fahrenheit, 2)} grados Fahrenheit.")
