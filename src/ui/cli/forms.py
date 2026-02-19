from utils.helpers import ViewHelper


class UI:
    @staticmethod
    def show_message(message):
        print(message)

    @staticmethod
    def show_error(message):
        print(message)

    @staticmethod
    def menu_user():
        print("""
              USER\n
        [1] My tasks
        [2] Update task status
        [3] My profile
        [4] Logout
        """)

    @staticmethod
    def menu_admin():
        print("""
                      ADMIN\n
        [1] Gestion de usuario
        [2] Gestion de proyecctos
        [3] Panel de Estadísticas (Ver carga de trabajo)
        [4] Logout
        """)

    # GESTION DE USUARIOS
    @staticmethod
    def menu_admin_user_management():
        print("""
                      USER MANAGEMENT\n
        [1] Create user
        [2] Edit user
        [3] Delete user
        [4] View users
        [5] Back
        """)

    @staticmethod
    def menu_admin_edit_user_management():
        print("""
                      USER MANAGEMENT\n
        [1] cambiar username
        [2] cambiar email
        [3] resetear password
        [4] cambiar role
        [5] Back
        """)

    # GESTION DE PROYECTOS
    @staticmethod
    def menu_admin_project():
        print("""
                      ADMIN MANAGEMENT\n
        [1] projects
        [2] system setting
        [3] asignar usuario-proyecto
        [4] Back
        """)

    @staticmethod
    def menu_management_project():
        print("""
                      PROJECTS MANAGEMENT\n
        [1] nuevo proyecto
        [2] listar proyecto
        [3] editar proyecto
        [4] eliminar proyecto
        [5] Back
        """)

    @staticmethod
    def menu_system_setting():
        print("""
                      SYSTEM SETTING\n
        [1] gestionar estados de proyectos
        [2] gestionar estados de tareas
        [3] Back
        """)

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
                             ░                  By LeoDev2p
        """)

    @staticmethod
    def show_table_tasks(data, message="Results"):
        len_data = ViewHelper.length_text_collection(data)
        headers = ViewHelper.length_text_collection(
            ["title", "description", "state", "project"]
        )

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
        headers = ViewHelper.length_text_collection(
            ["id", "username", "email", "role", "created_by"]
        )

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


class Forms:
    @staticmethod
    def login_forms() -> tuple:
        email = input("[email]: ")
        password = input("[password]: ")
        return email, password

    @staticmethod
    def register_forms() -> tuple:
        username = input("[username]: ")
        email = input("[email]: ")
        password = input("[password]: ")
        return email, password, username

    @staticmethod
    def option_forms():
        try:
            option = int(input("[option]: "))
            return option
        except ValueError as e:
            print(f"Error: {e}")

    @staticmethod
    def ask_forms(question="Do you want to continue?"):
        try:
            ask = input(f"{question} (S/N): ").upper()
        except Exception as e:
            print(f"Error: {e}")
            return None
        return ask


class FormsTask:
    @staticmethod
    def edit_taskstatus_forms():
        try:
            project_title = input("[project title]: ")
            task_title = input("[task title]: ")
            state_name = input("[New task status name]: ")
            return state_name, task_title, project_title
        except Exception as e:
            print(f"Error: {e}")
            return None


class FormsUser:
    @staticmethod
    def edit_profile_forms():
        try:
            username = input("[New username]: ")
            password = input("[New password]: ")
            confirm_password = input("[Confirm password]: ")

            return username, password, confirm_password
        except Exception as e:
            print(f"Error: {e}")
            return None

    @staticmethod
    def edit_username_forms():
        try:
            username = input("[new username]: ")
            return username
        except ValueError as e:
            print(f"Error: {e}")

    @staticmethod
    def edit_email_forms():
        try:
            email = input("[new email]: ")

            return email
        except ValueError as e:
            print(f"Error: {e}")

    @staticmethod
    def edit_password_forms():
        try:
            password = input("[new password]: ")

            return password
        except ValueError as e:
            print(f"Error: {e}")

    @staticmethod
    def edit_role_forms():
        try:
            role = input("[new role]: ")

            return role
        except ValueError as e:
            print(f"Error: {e}")

    @staticmethod
    def id_forms():
        try:
            id = int(input("[Id]: "))
            return id
        except ValueError as e:
            print(f"Error: {e}")

    @staticmethod
    def search_forms():
        user_email = input("[Search by useranem or email]: ")
        return user_email
