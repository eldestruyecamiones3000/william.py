# Solicitar el nombre, edad y altura del usuario y convertir al tipo de dato adecuado
nombre = input("Ingrese su nombre: ")
edad = int(input("Ingrese su edad: "))
altura = float(input("Ingrese su altura en metros: "))

# Imprimir los valores con los tipos de datos convertidos
print("Nombre:", nombre, "(tipo:", type(nombre), ")")
print("Edad:", edad, "(tipo:", type(edad), ")")
print("Altura:", altura, "(tipo:", type(altura), ")")

# Solicitar el peso y calcular el IMC
peso = float(input("Ingrese su peso en kilogramos: "))
imc = peso / (altura ** 2)

# Imprimir el resultado del IMC redondeado a dos decimales
print("Su IMC es:", round(imc, 2))
