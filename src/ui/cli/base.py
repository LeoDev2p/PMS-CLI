from rich.console import Console

from utils.helpers import ViewHelper

console = Console()


class BaseUI:
    """
    Class to manage UI views.
    """

    @staticmethod
    def show_message(message):
        # Auto-detect success patterns to display in green
        lower_msg = message.lower()
        if "success" in lower_msg or "éxito" in lower_msg:
            console.print(message, style="bold spring_green3")
        elif "cancel" in lower_msg or "invalid" in lower_msg:
            console.print(message, style="bold orange3")
        else:
            console.print(message)

    @staticmethod
    def show_error(message):
        console.print(message, style="bold indian_red")

    @staticmethod
    def banner():
        ascii_art = r"""
         ██▓███   ███▄ ▄███▓  ██████  ▄████▄   ██▓     ██▓
        ▓██░  ██▒▓██▒▀█▀ ██▒▒██    ▒ ▒██▀ ▀█  ▓██▒    ▓██▒
        ▓██░ ██▓▒▓██    ▓██░░ ▓██▄   ▒▓█    ▄ ▒██░    ▒██▒
        ▒██▄█▓▒ ▒▒██    ▒██   ▒   ██▒▒▓▓▄ ▄██▒▒██░    ░██░
        ▒██▒ ░  ░▒██▒   ░██▒▒██████▒▒▒ ▓███▀ ░░██████▒░██░
        ▒▓▒░ ░  ░░ ▒░   ░  ░▒ ▒▓▒ ▒ ░░ ░▒ ▒  ░░ ▒░▓  ░░▓
        ░▒ ░     ░  ░      ░░ ░▒  ░ ░  ░  ▒   ░ ░ ▒  ░ ▒ ░
        ░░       ░      ░   ░  ░  ░  ░          ░ ░    ▒ ░
                ░         ░  ░ ░          ░  ░ ░
                             ░                  V1.0.0
                                                By LeoDev2p
        """
        console.print(ascii_art, style="bold sky_blue3")


class BaseTables:
    """
    Class to manage tables dynamically.
    """

    @staticmethod
    def show_table(data, headers=None, title="Results"):
        """Displays a professional dynamic table using Rich for coloring."""
        if not data:
            console.print(f"\n[bold orange3]⚠ No {title} available[/bold orange3]\n")
            return

        if not isinstance(data, list):
            data = [data]

        first_item = data[0]

        # --- 1. DETERMINAR HEADERS Y FILAS ---
        if isinstance(first_item, dict):
            if headers is None:
                headers = list(first_item.keys())
            rows = [[str(item.get(h, "")) for h in headers] for item in data]
        elif isinstance(first_item, (list, tuple)):
            if headers is None:
                headers = [f"Col {i + 1}" for i in range(len(first_item))]
            rows = [[str(val) for val in item] for item in data]
        else:
            if headers is None:
                headers = ["Value"]
            rows = [[str(item)] for item in data]

        # --- 2. CÁLCULO DE ANCHOS (Tu lógica manual) ---
        # Nota: Asegúrate de tener ViewHelper disponible o usa max() directamente
        try:
            len_data = ViewHelper.length_text_collection(rows)
            len_headers = ViewHelper.length_text_collection(headers)
            length_finally = [max(d, h) for d, h in zip(len_data, len_headers)]
        except:
            # Alternativa si ViewHelper no está a mano
            length_finally = []
            for i, h in enumerate(headers):
                col_widths = [len(str(row[i])) for row in rows]
                length_finally.append(max(len(str(h)), max(col_widths if col_widths else [0])))

        # Ancho total exacto (sum de columnas + separadores " | ")
        sum_length = sum(length_finally) + (len(headers) * 3) + 1
        border_c = "[grey50]"  # Color para los bordes
        reset_c = "[/grey50]"

        # --- 3. RENDERIZADO CON COLORES PROFESIONALES ---

        # Banner del Título
        console.print(
            f"[bold white italic]{title.upper():^{sum_length - 4}}[/bold white italic]"
        )
        console.print(f"{border_c}+" + "-" * (sum_length - 2) + f"+{reset_c}")

        # Fila de Encabezados (Headers en Azul Cielo)
        h_content = []
        for h, length in zip(headers, length_finally):
            h_content.append(f"[bold sky_blue3]{str(h):^{length}}[/bold sky_blue3]")

        header_row = f"{border_c}|{reset_c} " + f" {border_c}|{reset_c} ".join(h_content) + f" {border_c}|{reset_c}"
        console.print(header_row)
        console.print(f"{border_c}+" + "-" * (sum_length - 2) + f"+{reset_c}")

        # Filas de Datos
        for row in rows:
            row_content = []
            for i, (val, length) in enumerate(zip(row, length_finally)):
                # Lógica de colores por contenido
                clean_val = val.strip().lower()

                if i == 0:  # ID siempre en Cyan
                    color = "cyan"
                elif clean_val == "admin":  # Roles especiales en Verde
                    color = "bold spring_green3"
                elif clean_val == "user":  # Roles normales en gris claro
                    color = "grey70"
                elif "@" in clean_val:  # Emails en un tono sutil
                    color = "bright_blue"
                else:
                    color = "white"  # Texto por defecto

                row_content.append(f"[{color}]{val:^{length}}[/{color}]")

            row_str = f"{border_c}|{reset_c} " + f" {border_c}|{reset_c} ".join(row_content) + f" {border_c}|{reset_c}"
            console.print(row_str)

        # Línea final
        console.print(f"{border_c}+" + "-" * (sum_length - 2) + f"+{reset_c}")


class BaseForms:
    """
    Class to manage forms.
    """

    @staticmethod
    def option_forms():
        try:
            option = int(console.input(r"[bold bright_black]\[option]: [/bold bright_black]"))
            return option
        except ValueError as e:
            console.print(f"Error: {e}", style="bold indian_red")
            return None

    @staticmethod
    def id_forms():
        try:
            id = int(console.input("\n[bold bright_black]\\[select id]: [/bold bright_black]"))
            return id
        except ValueError as e:
            console.print(f"Error: {e}", style="bold indian_red")
            return None

    @staticmethod
    def ask_forms(question="Do you want to continue?"):
        try:
            ask = console.input(f"\n[bold sky_blue3]{question} (Y/N): [/bold sky_blue3]").upper()
        except Exception as e:
            console.print(f"Error: {e}", style="bold indian_red")
            return None
        return ask

    @staticmethod
    def search_forms(title_name="Search"):
        try:
            title = console.input(rf"[bold bright_black]\[{title_name}]: [/bold bright_black]")
            return title
        except ValueError as e:
            console.print(f"Error: {e}", style="bold indian_red")

    @staticmethod
    def str_forms(message="new value"):
        try:
            value = console.input(f"\n[bold bright_black]\\[{message}]: [/bold bright_black]")
            return value
        except ValueError as e:
            console.print(f"Error: {e}", style="bold indian_red")
            return None
