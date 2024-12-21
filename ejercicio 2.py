# Calculadora básica
# Solicitar dos números al usuario
num1 = float(input("Ingrese el primer número: "))
num2 = float(input("Ingrese el segundo número: "))

# Realizar las operaciones y almacenarlas en variables
suma = num1 + num2
resta = num1 - num2
multiplicacion = num1 * num2
division = num1 / num2 if num2 != 0 else "Indefinido (división por cero)"

# Imprimir los resultados de las operaciones
print("Suma:", suma)
print("Resta:", resta)
print("Multiplicación:", multiplicacion)
print("División:", division)


# Evaluación de expresión lógica
# Solicitar tres números al usuario
x = float(input("Ingrese el valor de x: "))
y = float(input("Ingrese el valor de y: "))
z = float(input("Ingrese el valor de z: "))

# Evaluar las expresiones lógicas
evaluacion1 = (x > y) and (y < z)
evaluacion2 = (x + y) == z

# Imprimir los resultados de las evaluaciones
print("Resultado de (x > y) and (y < z):", evaluacion1)
print("Resultado de (x + y) == z:", evaluacion2)
