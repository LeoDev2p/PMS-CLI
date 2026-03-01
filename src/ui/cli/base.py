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
    Class to manage tables.
    """
    @staticmethod
    def show_table_tasks(data, message="Results"):
        len_data = ViewHelper.length_text_collection(data)
        headers = ViewHelper.length_text_collection(["title", "description", "state", "project"])

        # Compara pares de (ancho_dato, ancho_cabecera) y elige el máximo de cada uno
        length_finally = [max(d, h) for d, h in zip(len_data, headers)]

        print("*" * sum(length_finally))
        print(f"| {message:^{sum(length_finally)}} |")
        print("*" * sum(length_finally))

        print(
            f"| {'title':^{length_finally[0]}} | {'description':^{length_finally[1]}} | {'state':^{length_finally[2]}} | {'project':^{length_finally[3]}} |"
        )

        for i in data:
            print(
                f"|{i[0]:^{length_finally[0]}}|{i[1]:^{length_finally[1]}}|{i[2]:^{length_finally[2]}} {i[3]:^{length_finally[3]}}|"
            )

        print("-" * sum(length_finally))

    @staticmethod
    def show_table_profile(data, message="Result"):
        len_data = ViewHelper.length_text_collection(data[:2])
        headers = ViewHelper.length_text_collection(["username", "email"])

        length_finally = [max(d, h) for d, h in zip(len_data, headers)]

        print("*" * sum(length_finally))
        print(f"| {message:^{sum(length_finally)}} |")
        print("*" * sum(length_finally))

        print(f"| {'username':^{length_finally[0]}} | {'email':^{length_finally[1]}} |")

        print(f"|{data[0]:^{length_finally[0]}}|{data[1]:^{length_finally[1]}}|")

        print("-" * sum(length_finally))

    @staticmethod
    def show_table_users(data, message="Users"):
        len_data = ViewHelper.length_text_collection(data)
        headers = ViewHelper.length_text_collection(["id", "username", "email", "role", "created_by"])

        # Compara pares de (ancho_dato, ancho_cabecera) y elige el máximo de cada uno
        length_finally = [max(d, h) for d, h in zip(len_data, headers)]

        print("*" * sum(length_finally))
        print(f"| {message:^{sum(length_finally)}} |")
        print("*" * sum(length_finally))

        print(
            f"| {'id':^{length_finally[0]}} | {'username':^{length_finally[1]}} | {'email':^{length_finally[2]}} | {'role':^{length_finally[3]}} | {'create_by':^{length_finally[4]}} |"
        )

        for i in data:
            print(
                f"|{i[0]:^{length_finally[0]}}|{i[1]:^{length_finally[1]}}|{i[2]:^{length_finally[2]}} {i[3]:^{length_finally[3]}} {i[4]:^{length_finally[4]}}|"
            )

        print("-" * sum(length_finally))


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
