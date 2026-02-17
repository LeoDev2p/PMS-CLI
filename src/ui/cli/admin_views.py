from src.core.exceptions import (
    DataEmptyError,
    EmailError,
    HashCreatingError,
    ModelsError,
    ProjectsError,
)
from utils.helpers import ViewHelper

from .forms import UI, Forms, FormsUser


class AdminViews:
    def __init__(self, controller):
        self.controller = controller

    def run(self):
        while True:
            ViewHelper.clear_screen()
            UI.banner()
            UI.menu_admin()

            option = Forms.option_forms()
            match option:
                case 1:
                    self.user_management()
                case 2:
                    self.project_management()
                case 3:
                    self.statistics_panel()
                case 4:
                    break
                case _:
                    UI.show_message("Invalid option")

    def user_management(self):
        while True:
            ViewHelper.clear_screen()
            UI.banner()
            UI.menu_admin_user_management()

            option = Forms.option_forms()
            match option:
                case 1:
                    while True:
                        data = Forms.register_forms()
                        try:
                            self.controller.auth.register(data)
                        except (
                            EmailError,
                            HashCreatingError,
                            ModelsError,
                            DataEmptyError,
                            ProjectsError,
                        ) as e:
                            UI.show_message(str(e))

                            if Forms.ask_forms() == "S":
                                continue
                            else:
                                break
                case 2:
                    self.edit_user_management()
                case 3:
                    pass
                case 4:
                    break
                case _:
                    UI.show_message("Invalid option")
   
    def edit_user_management(self):
        while True:
            ViewHelper.clear_screen()
            UI.banner()
            UI.menu_admin_edit_user_management()

            option = Forms.option_forms()
            match option:
                case 1:
                    try:
                        data = FormsUser.edit_username_forms()
                        self.controller.user.edit_username(data)
                    except (DataEmptyError, ModelsError) as e:
                        UI.show_message(str(e))
                    
                    if Forms.ask_forms() == "S":
                        continue

                case 2:
                    data = FormsUser.edit_email_forms()
                    try:
                        self.controller.user.edit_email(data)
                    except (DataEmptyError, ModelsError) as e:
                        UI.show_message(str(e))

                    if Forms.ask_forms() == "S":
                        continue

                case 3:
                    data = FormsUser.edit_password_forms()
                    try:
                        self.controller.user.reset_password(data)
                    except (DataEmptyError, ModelsError) as e:
                        UI.show_message(str(e))

                    if Forms.ask_forms() == "S":
                        continue
                case 4:
                    data = FormsUser.edit_role_forms()
                    try:
                        self.controller.user.change_role(data)
                    except (DataEmptyError, ModelsError) as e:
                        UI.show_message(str(e))

                    if Forms.ask_forms() == "S":
                        continue
                case 5:
                    break
                case _:
                    UI.show_message("Invalid option")

    def project_management(self):
        pass

    def statistics_panel(self):
        pass
