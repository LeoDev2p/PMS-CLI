from rich.console import Console

console = Console()


class FormsProjects:
    """
    Class to manage forms projects.
    """

    @staticmethod
    def edit_status():
        try:
            id = int(console.input(r"[bold bright_black]\[Id]: [/bold bright_black]"))
            status = console.input(r"[bold bright_black]\[New name status]: [/bold bright_black]")
            return id, status
        except ValueError as e:
            console.print(str(e), style="bold indian_red")

    @staticmethod
    def system_key_status():
        try:
            key = int(console.input(r"[bold bright_black]\[Id type]: [/bold bright_black]"))
            return key
        except ValueError as e:
            console.print(str(e), style="bold indian_red")

    @staticmethod
    def edit_project_forms():
        try:
            id = int(console.input(r"[bold bright_black]\[Id]: [/bold bright_black]"))
            title = console.input(r"[bold bright_black]\[New title]: [/bold bright_black]")
            return title, id
        except ValueError as e:
            console.print(str(e), style="bold indian_red")

    @staticmethod
    def edit_project_status_forms():
        # eliminar
        try:
            id_project = int(console.input(r"[bold bright_black]\[Id project]: [/bold bright_black]"))
            id_status = int(console.input(r"[bold bright_black]\[Id status]: [/bold bright_black]"))
            return id_status, id_project
        except ValueError as e:
            console.print(str(e), style="bold indian_red")

    @staticmethod
    def project_forms():
        title = console.input(r"[bold bright_black]\[New project]: [/bold bright_black]")
        description = console.input(r"[bold bright_black]\[Description]: [/bold bright_black]")
        return title, description

    @staticmethod
    def search_project_forms():
        try:
            title = console.input(r"[bold bright_black]\[Search by title]: [/bold bright_black]")
            return title
        except ValueError as e:
            console.print(str(e), style="bold indian_red")
