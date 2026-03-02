from rich.console import Console

console = Console()


class FormsTask:
    """
    Class to manage forms tasks.
    """

    @staticmethod
    def edit_taskstatus_forms():
        try:
            project_title = console.input(r"[bold bright_black]\[project title]: [/bold bright_black]")
            task_title = console.input(r"[bold bright_black]\[task title]: [/bold bright_black]")
            state_name = console.input(r"[bold bright_black]\[New task status name]: [/bold bright_black]")
            return state_name, task_title, project_title
        except Exception as e:
            console.print(f"Error: {e}", style="bold indian_red")
            return None

    @staticmethod
    def asigne_task():
        title = console.input(r"[bold bright_black]\[New task]: [/bold bright_black]")
        description = console.input(r"[bold bright_black]\[Description]: [/bold bright_black]")
        return title, description

    @staticmethod
    def edit_status():
        try:
            id = int(console.input(r"[bold bright_black]\[Id]: [/bold bright_black]"))
            status = console.input(r"[bold bright_black]\[New status]: [/bold bright_black]")
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
