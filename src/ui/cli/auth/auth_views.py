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
from src.ui.cli.admin.admin_view import AdminViews
from src.ui.cli.base import BaseForms, BaseUI
from src.ui.cli.form.auth import FormsAuth
from src.ui.cli.menu.auth_menu import AuthMenus
from src.ui.cli.user.profile import ProfileViews
from utils.helpers import ViewHelper


class AuthView:
    """
    Handles user login and registration and redirects to the appropriate view.
    """

    def __init__(self, controller):
        self.controller = controller

        self.admin = AdminViews(controller)
        self.profile = ProfileViews(controller)

    def run(self):
        while True:
            ViewHelper.clear_screen()
            BaseUI.banner()
            BaseUI.show_message("\n")
            AuthMenus.menu()

            option = BaseForms.option_forms()
            print()
            match option:
                case 1:
                    data = FormsAuth.login_forms()

                    try:
                        result = self.controller.auth.login(data)
                        if result:
                            ViewHelper.progress_bar()
                            BaseUI.show_message("Login successful")
                            sleep(2)

                            if Session.get_role() == "admin" and Session.get_state() is True:
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
                        BaseUI.show_message(str(e))

                        if BaseForms.ask_forms() == "Y":
                            continue
                        else:
                            break

                case 2:
                    data = FormsAuth.register_forms()

                    try:
                        if self.controller.auth.register(data):
                            ViewHelper.progress_bar()
                            BaseUI.show_message("User created successfully")
                            sleep(2)
                    except (
                        EmailError,
                        PasswordError,
                        HashCreatingError,
                        DataEmptyError,
                        ModelsError,
                        ProjectsError,
                    ) as e:
                        BaseUI.show_message(str(e))

                        if BaseForms.ask_forms() == "Y":
                            continue
                        else:
                            break

                case 3:
                    break
                case _:
                    BaseUI.show_message("\nInvalid option")
