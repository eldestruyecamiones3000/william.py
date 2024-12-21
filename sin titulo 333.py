texto_original = "      Bienvenido, este es un ejemplo de transformación de texto! "

# Eliminar espacios en blanco al principio y al final
texto_2 = texto_original.strip()

# Buscar "transformación"
if "transformación" in texto_2:
    # Convertir todo el texto a mayúsculas
    texto_transformado = texto_2.upper()
else:
    # Solo la primera letra en mayúscula
    texto_transformado = texto_2.capitalize()

# Reemplazar signos de exclamación con puntos
texto_transformado = texto_transformado.replace("!", ".")

# Dividir la cadena en palabras
palabras = texto_transformado.split()

# Unir palabras con separadores
if len(palabras) > 4:
    resultado_final = "/".join(palabras)
else:
   resultado_final = "_".join(palabras)

print(resultado_final)
