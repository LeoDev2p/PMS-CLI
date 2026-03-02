from rich.console import Console

console = Console()


class FormsUser:
    """
    Class to manage forms users.
    """

    @staticmethod
    def add_user_forms() -> tuple:
        username = console.input(r"[bold bright_black]\[username]: [/bold bright_black]")
        email = console.input(r"[bold bright_black]\[email]: [/bold bright_black]")
        password = console.input(r"[bold bright_black]\[password]: [/bold bright_black]")
        return email, password, username

    @staticmethod
    def edit_forms(message="new value"):
        try:
            value = console.input(rf"[bold bright_black]\[{message}]: [/bold bright_black]")
            return value
        except ValueError as e:
            console.print(f"Error: {e}", style="bold indian_red")

    @staticmethod
    def search_forms():
        user_email = console.input(r"[bold bright_black]\[Search by useranem or email]: [/bold bright_black]")
        return user_email
