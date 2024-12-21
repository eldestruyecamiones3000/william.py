tareas = []

# Bucle principal del programa que continuará ejecutándose hasta que el usuario elija salir (opción 5).
while True:
    # Mostrar el menú de opciones
    print("\nMenú de Tareas:")
    print("1. Mostrar tareas")
    print("2. Agregar tarea")
    print("3. Completar tarea")
    print("4. Eliminar tarea")
    print("5. Salir")
    
    # Solicitar la opción deseada por el usuario
    opcion = input("Selecciona una opción: ")
    
    # Opción 1: Mostrar la lista de tareas
    if opcion == "1":
        if len(tareas) == 0:  # Si la lista de tareas está vacía
            print("\nNo tienes tareas.")
        else:
            print("\nTareas:")
            indice = 0  # Usamos un índice para recorrer la lista
            while indice < len(tareas):  # Mientras el índice sea menor que el número de tareas
                tarea = tareas[indice]  # Accedemos a cada tarea
                # Comprobamos si la tarea está completada o no y asignamos el símbolo correspondiente
                estado = "✔" if tarea['completada'] else "❌"
                # Mostramos el número de la tarea (1 más el índice) junto con su estado
                print(f"{indice + 1}. {tarea['nombre']} [{estado}]")
                indice += 1  # Incrementamos el índice para la siguiente tarea
    
    # Opción 2: Agregar una nueva tarea
    elif opcion == "2":
        # Solicitamos el nombre de la nueva tarea
        nueva_tarea = input("Escribe la nueva tarea: ")
        # Añadimos la tarea a la lista de tareas como un diccionario con su nombre y estado (incompleta por defecto)
        tareas.append({"nombre": nueva_tarea, "completada": False})
        # Confirmamos que la tarea ha sido agregada
        print(f"Tarea '{nueva_tarea}' agregada.")
    
    # Opción 3: Completar una tarea
    elif opcion == "3":
        if len(tareas) == 0:  # Si no hay tareas, informamos al usuario
            print("\nNo tienes tareas para completar.")
        else:
            # Solicitamos el número de la tarea que se desea completar
            numero_tarea = int(input("Número de la tarea a completar: ")) - 1
            # Comprobamos si el número es válido (dentro del rango de la lista)
            if 0 <= numero_tarea < len(tareas):
                # Marcamos la tarea como completada
                tareas[numero_tarea]['completada'] = True
                # Confirmamos que la tarea ha sido completada
                print(f"Tarea '{tareas[numero_tarea]['nombre']}' completada.")
            else:
                print("Número de tarea inválido.")
    
    # Opción 4: Eliminar una tarea
    elif opcion == "4":
        if len(tareas) == 0:  # Si no hay tareas, informamos al usuario
            print("\nNo tienes tareas para eliminar.")
        else:
            # Solicitamos el número de la tarea que se desea eliminar
            numero_tarea = int(input("Número de la tarea a eliminar: ")) - 1
            # Comprobamos si el número es válido (dentro del rango de la lista)
            if 0 <= numero_tarea < len(tareas):
                # Eliminamos la tarea usando pop y almacenamos la tarea eliminada para mostrarla
                tarea_eliminada = tareas.pop(numero_tarea)
                # Confirmamos que la tarea ha sido eliminada
                print(f"Tarea '{tarea_eliminada['nombre']}' eliminada.")
            else:
                print("Número de tarea inválido.")
    
    # Opción 5: Salir del programa
    elif opcion == "5":
        # Mostramos un mensaje de despedida y salimos del bucle
        print("Saliendo del programa...")
        break
    
    # Si el usuario elige una opción no válida
    else:
        print("Opción no válida. Intenta nuevamente.")