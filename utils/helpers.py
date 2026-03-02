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
        """
        Recursively normalizes data (strings, lists, tuples).
        Converts strings to lowercase and removes spaces.
        """
        if isinstance(data, str):
            return data.strip().lower()

        if isinstance(data, (list, tuple)):
            return type(data)(TextHelper.normalize(item) for item in data)

        return data

    @staticmethod
    def normalize_data_models(headers: tuple, data: list[tuple | tuple]) -> list[tuple] | tuple:
        pass


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
        from rich.progress import track

        print()
        for _ in track(range(101), description="[bold sky_blue3]Processing...[/bold sky_blue3]"):
            time.sleep(0.01)  # Faster for better UX during tests
        print("\n")

    @staticmethod
    def length_text_collection(data) -> list | int:
        """Calculate the length of the text in a collection.

        Args:
            data (tuple | list | dict): Collection of data.

        Returns:
            list | int: Length of the text in the collection.
        """
        if not data:
            return 0

        if isinstance(data, (list, tuple)):
            if len(data) == 0:
                return []

            if isinstance(data[0], (list, tuple)):
                return [max(len(str(row[idx])) for row in data if idx < len(row)) for idx in range(len(data[0]))]

            if isinstance(data[0], dict):
                keys = list(data[0].keys())
                return [max(len(str(row.get(k, ""))) for row in data) for k in keys]

            return [len(str(x)) for x in data]

        return len(str(data))
