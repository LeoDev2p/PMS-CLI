from src.core.exceptions import (
    DataEmptyError,
    EmailError,
    HashCreatingError,
    ModelsError,
    NotFoundUserError,
    ProjectsError,
)
from src.ui.cli.base import BaseForms, BaseTables, BaseUI
from src.ui.cli.form.user import FormsUser
from src.ui.cli.menu.admin_menu import AdminMenus
from utils.helpers import ViewHelper


class UserManagementViews:
    """
    Handles user management.
    """

    def __init__(self, controller):
        self.controller = controller

    def run(self):
        """Runs the user management panel."""
        while True:
            ViewHelper.clear_screen()
            BaseUI.banner()
            AdminMenus.menu_users()

            option = BaseForms.option_forms()
            print()

            match option:
                case 1:
                    while True:
                        data = FormsUser.add_user_forms()
                        try:
                            self.controller.auth.register(data)
                            BaseUI.show_message("\nUser registered successfully")
                        except (
                            EmailError,
                            HashCreatingError,
                            DataEmptyError,
                            ModelsError,
                            ProjectsError,
                        ) as e:
                            BaseUI.show_message(str(e))

                        if BaseForms.ask_forms("create more users?") == "Y":
                            continue
                        else:
                            break

                case 2:
                    self.edit_user()

                case 3:
                    while True:
                        user_email = FormsUser.search_forms()
                        result = self.controller.user.search_user_or_email(user_email)
                        BaseTables.show_table(result, title="User Details")

                        id_user = BaseForms.id_forms()
                        try:
                            self.controller.user.delete_user(id_user)
                            BaseUI.show_message("\nUser deleted successfully")
                        except (DataEmptyError, NotFoundUserError) as e:
                            BaseUI.show_message(str(e))
                            if BaseForms.ask_forms("Do you want to try again?") == "Y":
                                continue
                            else:
                                break

                        except ModelsError as e:
                            BaseUI.show_message(str(e))

                        if BaseForms.ask_forms("Delete more users?") == "Y":
                            continue
                        else:
                            break

                case 4:
                    try:
                        result = self.controller.user.get_all_users()
                        BaseTables.show_table(result, title="All Users")
                    except ModelsError as e:
                        BaseUI.show_message(str(e))

                    if BaseForms.ask_forms() == "Y":
                        continue

                case 5:
                    break
                case _:
                    BaseUI.show_message("Invalid option")

    def edit_user(self):
        """Edits a user."""
        while True:
            ViewHelper.clear_screen()
            BaseUI.banner()
            AdminMenus.menu_edit_users()

            option = BaseForms.option_forms()
            print()
            match option:
                case 1:
                    while True:
                        try:
                            user_email = FormsUser.search_forms()
                            print()

                            result = self.controller.user.search_user_or_email(user_email)
                            BaseTables.show_table(result, title="User Details")
                            id_user = BaseForms.id_forms()

                            data = FormsUser.edit_forms("New username")
                            self.controller.user.edit_username((data, id_user))
                            BaseUI.show_message("\nUser updated successfully")

                        except (DataEmptyError, NotFoundUserError) as e:
                            BaseUI.show_message(str(e))
                            if BaseForms.ask_forms("Do you want to try again?") == "Y":
                                continue
                            else:
                                break

                        except ModelsError as e:
                            BaseUI.show_message(str(e))

                        if BaseForms.ask_forms("Continue editing users?") == "Y":
                            continue
                        else:
                            break

                case 2:
                    while True:
                        try:
                            user_email = FormsUser.search_forms()
                            print()
                            result = self.controller.user.search_user_or_email(user_email)
                            BaseTables.show_table(result, title="User Details")
                            id_user = BaseForms.id_forms()

                            data = FormsUser.edit_forms("\nNew email")
                            self.controller.user.edit_email((data, id_user))
                            BaseUI.show_message("\nEmail updated successfully")

                        except (DataEmptyError, NotFoundUserError) as e:
                            BaseUI.show_message(str(e))
                            if BaseForms.ask_forms("Do you want to try again?") == "Y":
                                continue
                            else:
                                break

                        except ModelsError as e:
                            BaseUI.show_message(str(e))

                        if BaseForms.ask_forms("Continue editing users?") == "Y":
                            continue
                        else:
                            break

                case 3:
                    while True:
                        user_email = FormsUser.search_forms()
                        result = self.controller.user.search_user_or_email(user_email)
                        BaseTables.show_table(result, title="User Details")
                        id_user = BaseForms.id_forms()

                        data = FormsUser.edit_forms("\nNew password")
                        try:
                            self.controller.user.reset_password((id_user, data))
                            BaseUI.show_message("\nPassword updated successfully")
                        except (DataEmptyError, NotFoundUserError) as e:
                            BaseUI.show_message(str(e))
                            if BaseForms.ask_forms("Do you want to try again?") == "Y":
                                continue
                            else:
                                break

                        except ModelsError as e:
                            BaseUI.show_message(str(e))

                        if BaseForms.ask_forms("Continue editing users?") == "Y":
                            continue
                        else:
                            break
                case 4:
                    while True:
                        try:
                            user_email = FormsUser.search_forms()
                            result = self.controller.user.search_user_or_email(user_email)
                            BaseTables.show_table(result, title="User Details")
                            id_user = BaseForms.id_forms()

                            data = FormsUser.edit_forms("New role")
                            self.controller.user.change_role((data, id_user))
                            BaseUI.show_message("\nRole updated successfully")
                        except (DataEmptyError, NotFoundUserError, ValueError) as e:
                            BaseUI.show_message(str(e))
                            if BaseForms.ask_forms("Do you want to try again?") == "Y":
                                continue
                            else:
                                break

                        except ModelsError as e:
                            BaseUI.show_message(str(e))

                        if BaseForms.ask_forms("Continue editing users?") == "Y":
                            continue
                        else:
                            break
                case 5:
                    break
                case _:
                    BaseUI.show_message("Invalid option")
