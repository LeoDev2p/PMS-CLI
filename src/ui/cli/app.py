from time import sleep

from src.core.exceptions import (
    AuthenticactionError,
    EmailError,
    HashCreatingError,
    HashInvalidError,
    ModelsError,
    PasswordError,
    ProjectsError,
)
from src.models.sessions import Session
from utils.helpers import clear_screen, progress_bar

from .admin_views import AdminViews
from .forms import Forms
from .user_views import UserViews


class View:
    def __init__(self, controller):
        self.controller = controller

        self.admin_view = AdminViews(controller)
        self.user_view = UserViews(controller, Session)

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
                            Session.start(result[0], result[1], data[0])
                            Forms.show_message("Login successful")
                            sleep(2)

                            if (
                                Session.get_role() == "Admin"
                                and Session.get_state() is True
                            ):
                                self.admin_view.run()
                            else:
                                self.user_view.run()
                    except (
                        EmailError,
                        PasswordError,
                        HashInvalidError,
                        AuthenticactionError,
                        ModelsError,
                        ProjectsError,
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
                            progress_bar()
                            Forms.show_message("User created successfully")
                            sleep(2)
                    except (
                        EmailError,
                        HashCreatingError,
                        ModelsError,
                        ProjectsError,
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
