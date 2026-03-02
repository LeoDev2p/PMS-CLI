from rich.console import Console

console = Console()


class FormsAuth:
    """
    Class to manage forms auth.
    """

    @staticmethod
    def login_forms() -> tuple:
        email = console.input(r"[bold bright_black]\[email]: [/bold bright_black]")
        password = console.input(r"[bold bright_black]\[password]: [/bold bright_black]")
        return email, password

    @staticmethod
    def register_forms() -> tuple:
        username = console.input(r"[bold bright_black]\[username]: [/bold bright_black]")
        email = console.input(r"[bold bright_black]\[email]: [/bold bright_black]")
        password = console.input(r"[bold bright_black]\[password]: [/bold bright_black]")
        return email, password, username
