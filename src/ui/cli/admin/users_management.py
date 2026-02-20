from src.core.exceptions import (
    DataEmptyError,
    EmailError,
    HashCreatingError,
    ModelsError,
    NotFoundUserError,
    ProjectsError,
)
from utils.helpers import ViewHelper

from ..forms import UI, Forms, FormsUser, UIAdmin


class UserManagementViews:
    def __init__(self, controller):
        self.controller = controller

    def user_management(self):
        while True:
            ViewHelper.clear_screen()
            UI.banner()
            UIAdmin.menu_users()

            option = Forms.option_forms()
            match option:
                case 1:
                    while True:
                        data = Forms.register_forms()
                        try:
                            self.controller.auth.register(data)
                            UI.show_message("User registered successfully")
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
                case 2:
                    self.edit_user()
                case 3:
                    user_email = FormsUser.search_forms()
                    result = self.controller.user.search_user_or_email(user_email)[0]
                    print(result)

                    id = FormsUser.id_forms()
                    try:
                        self.controller.user.delete_user(id)
                    except (NotFoundUserError, ModelsError) as e:
                        UI.show_message(str(e))

                    if Forms.ask_forms() == "S":
                        continue
                    else:
                        break

                case 4:
                    result = self.controller.user.get_all_users()
                    print(result)

                    if Forms.ask_forms() == "S":
                        continue
                    else:
                        break

                case 5:
                    break
                case _:
                    UI.show_message("Invalid option")

    def edit_user(self):
        while True:
            ViewHelper.clear_screen()
            UI.banner()
            UIAdmin.menu_edit_users()

            option = Forms.option_forms()
            match option:
                case 1:
                    try:
                        user_email = FormsUser.search_forms()
                        result = self.controller.user.search_user_or_email(user_email)[
                            0
                        ]
                        print(result)

                        data = FormsUser.edit_username_forms()
                        self.controller.user.edit_username((data, result[0]))
                        UI.show_message("User updated successfully")
                    except (DataEmptyError, NotFoundUserError, ModelsError) as e:
                        UI.show_message(str(e))

                    if Forms.ask_forms() == "S":
                        continue

                case 2:
                    user_email = FormsUser.search_forms()
                    result = self.controller.user.search_user_or_email(user_email)[0]
                    print(result)

                    data = FormsUser.edit_email_forms()
                    try:
                        self.controller.user.edit_email((data, result[0]))
                    except (DataEmptyError, NotFoundUserError, ModelsError) as e:
                        UI.show_message(str(e))

                    if Forms.ask_forms() == "S":
                        continue

                case 3:
                    user_email = FormsUser.search_forms()
                    result = self.controller.user.search_user_or_email(user_email)[0]
                    print(result)

                    data = FormsUser.edit_password_forms()
                    try:
                        self.controller.user.reset_password((data, result[0]))
                    except (DataEmptyError, NotFoundUserError, ModelsError) as e:
                        UI.show_message(str(e))

                    if Forms.ask_forms() == "S":
                        continue
                case 4:
                    user_email = FormsUser.search_forms()
                    result = self.controller.user.search_user_or_email(user_email)[0]
                    print(result)

                    data = FormsUser.edit_role_forms()
                    try:
                        self.controller.user.change_role((data, result[0]))
                    except (DataEmptyError, NotFoundUserError, ModelsError) as e:
                        UI.show_message(str(e))

                    if Forms.ask_forms() == "S":
                        continue
                case 5:
                    break
                case _:
                    UI.show_message("Invalid option")
