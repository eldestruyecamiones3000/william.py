import random
import curses 
import time

class Bus:
    def __init__(self, name, position=0, speed=None):
        self.name = name
        self.position = position
        self.speed = speed if speed is not None else random.randint(1, 3)

    def move(self):

        self.position += self.speed

def draw_buses(carro, buses, finish_line):
    carro.clear()

    bus_design = [
        "_", 
        "|           /",
        "|_°|        _____/",
        " 0  0 || 0  0"
    ]

    max_x = curses.COLS - 1
    max_y = curses.LINES - 1
    road = "=" * max_x

    for idx, bus in enumerate(buses):
        bus_y = idx * 6

        # Asegurarse de que el bus no salga de la pantalla
        if bus_y + len(bus_design) >= max_y:
            break
        
        # Dibujar el bus en su posición
        for i, line in enumerate(bus_design):
            if bus.position + len(line) < max_x:  
                carro.addstr(bus_y + i, bus.position, line)

        # Dibujar la línea de meta
        finish_line_str = "_" * max(0, finish_line - bus.position) + "!"
        if bus.position < finish_line:
            carro.addstr(bus_y + 4, min(bus.position, max_x - 1), finish_line_str)
        else:
            carro.addstr(bus_y + 4, min(finish_line, max_x - 1), "!")

        # Dibujar la carretera
        carro.addstr(bus_y + 4, 0, road)

    carro.refresh()

def race(carro, buses, finish_line):
    curses.curs_set(0)  # Ocultar el cursor
    carro.nodelay(1)  # No bloquear esperando input de teclado

    try:
        while True:
            draw_buses(carro, buses, finish_line)

            for bus in buses:
                bus.move()

            # Verificar si algún bus ha cruzado la línea de meta
            if any(bus.position >= finish_line for bus in buses):
                winner = next(bus for bus in buses if bus.position >= finish_line)
                carro.addstr(len(buses) * 6, 0, f'¡{winner.name} ha ganado la carrera!')
                carro.refresh()
                time.sleep(2)
                break

            time.sleep(0.2)

    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    try:
        buses = [Bus(f'Bus{i + 1}') for i in range(2)]
        finish_line = 50
        curses.wrapper(race, buses, finish_line)
    except KeyboardInterrupt:
        print("Se interrumpió la carrera, saliendo ...")
