"""Module with utility functions for the application, including console management, date handling, text length calculation, and a progress bar display."""

import os
import time
from datetime import date


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


# mostrar fecha actualizada
def date_today():
    """Fetch the current date and return it as a string in 'YYYY-MM-DD' format."""
    d = date.today().strftime("%Y-%m-%d")
    return d


# calcular longitud de testo
lengthText = lambda lista, index: max(list(map(lambda x: len(x[index]), lista)))


def progress_bar():
    """Display a progress bar in the console."""
    # El '\r' y el 'end=""' son los que fuerzan la actualización en la misma línea
    print()
    for i in range(101):
        print(f"\r[{'#' * (i // 2):<50}] {i}%", end="", flush=True)
        time.sleep(0.03)
    print("\n")
