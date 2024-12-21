#Tarea 1
try:

    num1 = int(input("Introduce un número: "))
    num2 = int(input("Introduce otro número: "))
    resultado = num1 / num2
    print("El resultado es:", resultado)
except ZeroDivisionError:

    print("Error: No se puede dividir entre cero.")

#Tarea 2 
try:
    numero = int(input("Introduce un número entero: "))
    print(f"El número que ingresaste es: {numero}")
except ValueError:
    print("Lo siento, eso no parece ser un número entero válido. Por favor, inténtalo de nuevo.")
#tarea 3 
try:
    # Solicitar al usuario un número entero
    numero = int(input("Por favor, ingresa un número entero: "))
    
    # Calcular el doble del número
    resultado = numero * 2
    
    # Imprimir el resultado
    print(f"El doble de {numero} es {resultado}.")
except ValueError:
    # Capturar el error si el valor no es un número entero
    print("Oops, parece que no ingresaste un número entero válido. Inténtalo de nuevo.")

#tarea 4
try:
    # Solicitar dos números enteros al usuario
    numero1 = int(input("Ingresa el primer número entero: "))
    numero2 = int(input("Ingresa el segundo número entero: "))
    
    # Intentar multiplicar los números
    resultado = numero1 * numero2
    
    # Imprimir el resultado
    print(f"El resultado de la multiplicación es: {resultado}")
except ValueError:
    # Capturar el error si los valores no son números enteros
    print("Oops, parece que no ingresaste números enteros válidos. Inténtalo de nuevo.")
except OverflowError:
    # Capturar el error si el resultado es demasiado grande
    print("El resultado es demasiado grande para manejarlo. ¡Cuidado con los números enormes!")

#tarea 5 
#try:
  #  # Intentar abrir el archivo en modo de lectura
  #  with open("datos.txt", "r") as archivo:
  #      contenido = archivo.read()
 #       print(f"Contenido del archivo:\n{contenido}")
#except FileNotFoundError:
    # Capturar el error si el archivo no existe
 #   print("El archivo 'datos.txt' no fue encontrado. Verifica si existe o crea uno nuevo.")

#tarea 6
#try:
    # Intentar abrir el archivo
 #   with open("mi_archivo.txt", "r") as archivo:
   #     contenido = archivo.read()
 #       print(f"Contenido del archivo:\n{contenido#}")
#except FileNotFoundError:
    # Capturar el error si el archivo no existe
    print("El archivo no fue encontrado. Verifica si existe o crea uno nuevo.")
#except Exception as e:
    # Capturar cualquier otra excepción
  #  print(f"Ocurrió un error: {e}")
#finally:
    # Asegurarse de que el archivo se cierre, incluso si hay una excepción
   # archivos.close()

#tarea 7
try:
    numero = int(input("Introduce un número entero: "))
    print(f"El número ingresado es: {numero}")
except Exception as e:
    print(f"Ocurrió una excepción: {type(e).__name__}")

#tarea 8
class ErrorNumeroNegativo(Exception):
    pass

try:
    numero = int(input("Introduce un número: "))
    if numero < 0:
        raise ErrorNumeroNegativo("No se permiten números negativos")
    print(f"El número ingresado es: {numero}")
except ErrorNumeroNegativo as e:
    print(f"Error personalizado: {e}")
except ValueError:
    print("Oops, parece que no ingresaste un número válido.")
 
#tarea 9
import math

try:
    numero = float(input("Introduce un número: "))
    if numero < 0:
        raise ValueError("No se permite un número negativo para la raíz cuadrada")
    raiz_cuadrada = math.sqrt(numero)
    print(f"La raíz cuadrada de {numero} es: {raiz_cuadrada:.2f}")
except ValueError as e:
    print(f"Error: {e}")

#tarea 10
mi_lista = [10, 20, 30, 40, 50]

try:
    indice = int(input(f"Introduce un índice (0-{len(mi_lista)-1}): "))
    elemento = mi_lista[indice]
    print(f"El elemento en el índice {indice} es: {elemento}")
except IndexError:
    print("El índice está fuera de rango.")
except ValueError:
    print("Oops, parece que no ingresaste un índice válido.")

#tarea 11
mi_diccionario = {"a": 1, "b": 2, "c": 3}

try:
    clave = input("Introduce una clave para buscar en el diccionario: ")
    valor = mi_diccionario[clave]
    print(f"El valor asociado a la clave '{clave}' es: {valor}")
except KeyError:
    print(f"La clave '{clave}' no existe en el diccionario.")

#tarea 12
class ListaVaciaError(Exception):
    pass

try:
    mi_lista_vacia = []
    suma_elementos = sum(mi_lista_vacia)
    print(f"La suma de los elementos es: {suma_elementos}")
except ListaVaciaError:
    print("La lista está vacía. No se puede calcular la suma.")
except ValueError:
    print("Oops, parece que hubo un problema al sumar los elementos.")

#tarea 13
try:
    cadena = input("Introduce una cadena que represente un número entero: ")
    numero_entero = int(cadena)
    print(f"El número entero obtenido es: {numero_entero}")
except ValueError:
    print("Oops, parece que no ingresaste una cadena válida para convertir a entero.")


#tarea 15
try:
    num1 = float(input("Introduce el primer número: "))
    num2 = float(input("Introduce el segundo número: "))
    operacion = input("Introduce la operación (+, -, *, /): ")

    if operacion == "+":
        resultado = num1 + num2
    elif operacion == "-":
        resultado = num1 - num2
    elif operacion == "*":
        resultado = num1 * num2
    elif operacion == "/":
        if num2 == 0:
            raise ZeroDivisionError("No se puede dividir entre cero")
        resultado = num1 / num2
    else:
        raise ValueError("Operación no válida")

    print(f"El resultado de la operación es: {resultado:.2f}")
except ValueError as e:
    print(f"Error: {e}")
except ZeroDivisionError:
    print("Error: No se puede dividir entre cero.")

#tarea 16
try:
    with open("numeros.txt", "r") as archivo:
        for linea in archivo:
            try:
                numero = float(linea.strip())
                print(f"Número leído: {numero:.2f}")
            except ValueError:
                print(f"Error: La línea '{linea.strip()}' no contiene un número válido.")
except FileNotFoundError:
    print("El archivo 'numeros.txt' no fue encontrado.")

#tarea 17

class EmailInvalidoError(Exception):
    pass

try:
    email = input("Introduce tu dirección de correo electrónico: ")
    if "@" not in email:
        raise EmailInvalidoError("La dirección de correo debe contener el símbolo @")
    print(f"Correo electrónico válido: {email}")
except EmailInvalidoError as e:
    print(f"Error: {e}")
