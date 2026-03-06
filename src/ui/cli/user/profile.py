import time

from src.core.exceptions import (
    DataEmptyError,
    HashCreatingError,
    ModelsError,
    PasswordMatchError,
)
from src.core.logging import get_logger
from src.models.sessions import Session
from src.ui.cli.base import BaseForms, BaseUI
from src.ui.cli.menu.user_menu import UserMenus
from utils.helpers import ViewHelper


class MyProfile:
    def __init__(self, controller):
        self.controller = controller
        self.log = get_logger("audit", self.__class__.__name__)

    def run(self):
        BaseUI.show_message("My Profile\n")
        try:
            data = self.controller.user.get_profile()
            BaseUI.show_message(f"[::] Username: {data['username']}")
            BaseUI.show_message(f"[::] Email: {data['email']}")
        except (DataEmptyError, ModelsError) as e:
            BaseUI.show_error(str(e))

        if BaseForms.ask_forms("Do you want to edit your profile?") == "Y":
            self.edit_profile()

    def edit_profile(self):
        while True:
            ViewHelper.clear_screen()
            BaseUI.banner()
            UserMenus.menu_edit_profile()

            option = BaseForms.option_forms()
            BaseUI.show_message("\n")

            match option:
                case 1:
                    try:
                        username = BaseForms.str_forms("New username")

                        if BaseForms.ask_forms(question="Want to update username?") == "Y":
                            self.controller.user.edit_username((username, Session.get_id()))
                            BaseUI.show_message("\nUsername updated successfully\n")

                    except DataEmptyError as e:
                        self.log.warning(
                            f"User {Session.get_id()} attempted to update the profile with incomplete data: {e}"
                        )
                        BaseUI.show_message(str(e))
                    except (DataEmptyError, ModelsError) as e:
                        BaseUI.show_message(str(e))

                        if BaseForms.ask_forms() == "Y":
                            continue

                    time.sleep(3.2)
                case 2:
                    try:
                        password = BaseForms.str_forms("New Password")

                        if BaseForms.ask_forms(question="Want to update password?") == "Y":
                            self.controller.user.reset_password((Session.get_id(), password))
                            BaseUI.show_message("\nPassword updated successfully\n")

                    except DataEmptyError as e:
                        self.log.warning(
                            f"User {Session.get_id()} attempted to update the profile with incomplete data: {e}"
                        )
                        BaseUI.show_message(str(e))
                    except (PasswordMatchError, HashCreatingError, DataEmptyError, ModelsError) as e:
                        BaseUI.show_message(str(e))

                        if BaseForms.ask_forms() == "Y":
                            continue

                    time.sleep(3.2)

                case 3:
                    break
                case _:
                    BaseForms.show_message("\nInvalid option")
