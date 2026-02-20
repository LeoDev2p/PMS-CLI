from time import sleep

from src.core.exceptions import (
    AuthenticactionError,
    DataEmptyError,
    EmailError,
    HashCreatingError,
    HashInvalidError,
    ModelsError,
    PasswordError,
    ProjectsError,
)
from src.models.sessions import Session
from utils.helpers import ViewHelper

from .admin.admin import AdminViews
from .forms import UI, Forms
from .user.profile import ProfileViews


class View:
    def __init__(self, controller):
        self.controller = controller

        self.admin = AdminViews(controller)
        self.profile = ProfileViews(controller)

    def run(self):
        while True:
            ViewHelper.clear_screen()
            UI.banner()
            UI.show_message("\n")
            self.menu()

            option = Forms.option_forms()
            print()
            match option:
                case 1:
                    data = Forms.login_forms()

                    try:
                        result = self.controller.auth.login(data)
                        #biews (1, 'admin')
                        if result:
                            ViewHelper.progress_bar()
                            Session.start(result[0], result[1], data[0])
                            UI.show_message("Login successful")
                            sleep(2)

                            if (
                                Session.get_role() == "admin"
                                and Session.get_state() is True
                            ):
                                self.admin.run()
                            else:
                                self.profile.run()
                    except (
                        EmailError,
                        PasswordError,
                        HashInvalidError,
                        AuthenticactionError,
                        ModelsError,
                        ProjectsError,
                    ) as e:
                        UI.show_message(str(e))

                        if Forms.ask_forms() == "S":
                            continue
                        else:
                            break

                case 2:
                    data = Forms.register_forms()

                    try:
                        if self.controller.auth.register(data):
                            ViewHelper.progress_bar()
                            UI.show_message("User created successfully")
                            sleep(2)
                    except (
                        EmailError,
                        HashCreatingError,
                        DataEmptyError,
                        ModelsError,
                        ProjectsError,
                    ) as e:
                        UI.show_message(str(e))

                        if Forms.ask_forms() == "S":
                            continue
                        else:
                            break

                case 3:
                    break
                case _:
                    UI.show_message("Invalid option")

    def menu(self):
        print("\t    [1] Login     [2] Register     [3] Exit")
