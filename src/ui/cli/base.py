from utils.helpers import ViewHelper


class BaseUI:
    """
    Class to manage UI views.
    """

    @staticmethod
    def menu():
        print("\t    [1] Login     [2] Register     [3] Exit")

    @staticmethod
    def show_message(message):
        print(message)

    @staticmethod
    def show_error(message):
        print(message)

    @staticmethod
    def banner():
        print(r"""
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
        """)


class BaseTables:
    """
    Class to manage tables dynamically.
    """

    @staticmethod
    def show_table(data, headers=None, title="Results"):
        """Displays a dynamic table for list of tuples or dicts."""
        if not data:
            print(f"\n--- No {title} available ---\n")
            return

        if not isinstance(data, list):
            data = [data]

        first_item = data[0]

        # Determine headers and extract rows
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

        len_data = ViewHelper.length_text_collection(rows)
        len_headers = ViewHelper.length_text_collection(headers)

        length_finally = [max(d, h) for d, h in zip(len_data, len_headers)]

        sum_length = sum(length_finally) + len(headers) * 3 + 1

        print("*" * sum_length)
        print(f"| {title:^{sum_length - 4}} |")
        print("*" * sum_length)

        header_row = "| " + " | ".join(f"{str(h):^{length}}" for h, length in zip(headers, length_finally)) + " |"
        print(header_row)

        for row in rows:
            row_str = "| " + " | ".join(f"{val:^{length}}" for val, length in zip(row, length_finally)) + " |"
            print(row_str)

        print("-" * sum_length)


class BaseForms:
    """
    Class to manage forms.
    """

    @staticmethod
    def option_forms():
        try:
            option = int(input("[option]: "))
            return option
        except ValueError as e:
            print(f"Error: {e}")

    @staticmethod
    def id_forms():
        try:
            id = int(input("\n[select id]: "))
            return id
        except ValueError as e:
            print(f"Error: {e}")

    @staticmethod
    def ask_forms(question="Do you want to continue?"):
        try:
            ask = input(f"\n{question} (Y/N): ").upper()
        except Exception as e:
            print(f"Error: {e}")
            return None
        return ask

    @staticmethod
    def search_forms(title_name="Search"):
        try:
            title = input(f"[{title_name}]: ")
            return title
        except ValueError as e:
            print(f"Error: {e}")
    
    @staticmethod
    def str_forms(message = 'new value'):
        try:
            value = input(f"\n[{message}]: ")
            return value
        except ValueError as e:
            print(f"Error: {e}")
            return None
