from time import sleep

from src.core.exceptions import (
    EmailError,
    HashError,
    ModelsError,
    PasswordError,
    ProjectsError,
)
from utils.helpers import clear_screen, progress_bar

from .admin_views import AdminViews
from .forms import Forms
from .user_views import UserViews


class View:
    def __init__(self, controller):
        self.controller = controller
        self.session = {"role": None, "status": False, "user": None}  # admin / user

        self.admin_view = AdminViews(controller)
        self.user_view = UserViews(controller)

    def run(self):
        while True:
            clear_screen()
            Forms.banner()
            Forms.show_message("\n")
            self.menu()

            option = Forms.option_forms()
            match option:
                case 1:
                    data = Forms.login_forms()
                    try:
                        result = self.controller.auth.login(data)
                        if result:
                            progress_bar()
                            self.session["role"] = result
                            self.session["status"] = True
                            self.session["user"] = data[0]
                            Forms.show_message("Login successful")
                            sleep(2)

                            if (
                                self.session["role"] == "Admin"
                                and self.session["status"] is True
                            ):
                                self.admin_view.run()
                            else:
                                self.user_view.run()
                    except (
                        EmailError,
                        PasswordError,
                        HashError,
                        ModelsError,
                        ProjectsError
                    ) as e:
                        Forms.show_message(str(e))

                    if Forms.ask_forms() == "S":
                        continue
                    else:
                        break

                case 2:
                    data = Forms.register_forms()
                    try:
                        if self.controller.auth.register(data):
                            Forms.show_message("User created successfully")
                            sleep(2)
                    except (
                        EmailError,
                        HashError,
                        ModelsError,
                        ProjectsError
                    ) as e:
                        Forms.show_message(str(e))

                    if Forms.ask_forms() == "S":
                        continue
                    else:
                        break
                case 3:
                    break
                case _:
                    Forms.show_message("Invalid option")

    def show_auth(self):
        pass

    def menu(self):
        print("""
        [1] Login
        [2] Register
        [3] Exit
        """)
