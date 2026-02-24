"""Module with utility functions for the application, including console management, date handling, text length calculation, and a progress bar display."""

import time
from datetime import date


class DateHelper:
    """Class to manage date."""

    @staticmethod
    def today_is():
        """Generate the current date: 'YYYY-MM-DD'"""
        return date.today().strftime("%Y-%m-%d")


class TextHelper:
    """Class to manage text."""

    @staticmethod
    def normalize(data: tuple | str) -> tuple | list | str:
        if isinstance(data, (tuple, list)):
            return type(data)(map(lambda x: str(x).strip().lower(), data))

        return data.strip().lower() if isinstance(data, str) else data


class ViewHelper:
    """Class to manage views."""

    @staticmethod
    def clear_screen():
        """Clear the terminal."""
        # noqa
        import os

        os.system("cls" if os.name == "nt" else "clear")

    @staticmethod
    def progress_bar():
        """Display a progress bar in the console."""
        # El '\r' y el 'end=""' son los que fuerzan la actualización en la misma línea
        print()
        for i in range(101):
            print(f"\r[{'#' * (i // 2):<50}] {i}%", end="", flush=True)
            time.sleep(0.03)
        print("\n")

    @staticmethod
    def length_text_collection(data) -> list | int:
        """Calculate the length of the text in a collection.

        Args:
            data (tuple | list): Collection of data.

        Returns:
            list | int: Length of the text in the collection.
        """
        # [(), ()]
        if isinstance(data, (list, tuple)):
            if isinstance(data[0], (list, tuple)):
                lenght = []
                for index in range(len(data)):
                    lenght.append(max(list(map(lambda x: len(str(x[index])), data))))

                return lenght

            for _ in range(len(data)):
                return list(map(lambda x: len(str(x)), data))
