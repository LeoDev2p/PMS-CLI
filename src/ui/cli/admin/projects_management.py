from src.core.exceptions import (
    DataEmptyError,
    ModelsError,
    NotFoundProjectError,
    NotFoundStatusProjectError,
    ProjectsExistsError,
)
from src.ui.cli.base import BaseForms, BaseUI
from src.ui.cli.form.project import FormsProjects
from src.ui.cli.menu.admin_menu import AdminMenus
from utils.helpers import ViewHelper


class ManagementProjectViews:
    """Class to manage project views."""

    def __init__(self, controller):
        self.controller = controller

    def run(self):
        """Runs the project management views."""
        while True:
            ViewHelper.clear_screen()
            BaseUI.banner()
            AdminMenus.menu_management_project()

            option = BaseForms.option_forms()
            print()
            match option:
                case 1:
                    data = FormsProjects.project_forms()
                    try:
                        try:
                            self.controller.project_status.get_all()
                        except NotFoundStatusProjectError:
                            BaseUI.show_message("First you need to create the states in 'system setting' or")
                            if BaseForms.ask_forms("Create by default") == "Y":
                                self.controller.project.add(data)
                                BaseUI.show_message("Project successfully added")
                            else:
                                BaseUI.show_message("Set status in 'SYSTEM SETTING")
                        else:
                            self.controller.project.add(data)
                            BaseUI.show_message("\nProject successfully added")
                    except (DataEmptyError, ProjectsExistsError, ModelsError) as e:
                        BaseUI.show_error(str(e))

                    if BaseForms.ask_forms() == "Y":
                        continue

                case 2:
                    try:
                        result = self.controller.project.get_all()
                        print(result)
                    except (NotFoundProjectError, ModelsError) as e:
                        BaseUI.show_error(str(e))

                    if BaseForms.ask_forms() == "Y":
                        continue

                case 3:
                    self.edit_project()

                case 4:
                    data = FormsProjects.search_project_forms()
                    # hacerlo global esa funcion
                    try:
                        result = self.controller.project.get_by_title(data)
                        print(result)
                        id_project = BaseForms.id_forms()  

                        if BaseForms.ask_forms(question="Do you want delete?") == "Y":
                            self.controller.project.delete(id_project)
                            BaseUI.show_message("\nProject successfully deleted")
                        else:
                            BaseUI.show_message("\nAction canceled")
                    except (DataEmptyError, NotFoundProjectError, ModelsError) as e:
                        BaseUI.show_error(str(e))

                    if BaseForms.ask_forms() == "Y":
                        continue

                case 5:
                    break
                case _:
                    BaseUI.show_message("\nInvalid option")

    def edit_project(self):
        """Edits a project."""
        while True:
            ViewHelper.clear_screen()
            BaseUI.banner()
            AdminMenus.menu_edit_project()

            option = BaseForms.option_forms()
            print()

            match option:
                case 1:
                    try:
                        # buscar por like ---------------------
                        result = self.controller.project.get_all()
                        print(result)

                        data = FormsProjects.edit_project_forms()

                        self.controller.project.edit_title(data)
                        BaseUI.show_message("\nProject title successfully updated")
                    except (DataEmptyError, ModelsError) as e:
                        BaseUI.show_error(str(e))

                    if BaseForms.ask_forms() == "Y":
                        continue

                case 2:
                    try:
                        # buscar por like ---------------------
                        result = self.controller.project.get_all()
                        print(result)
                        id_project = BaseForms.option_forms()

                        result = self.controller.project_status.get_all()
                        print(result)
                        id_status = BaseForms.option_forms()

                        data = (id_status, id_project)
                        self.controller.project.edit_status(data)
                        BaseUI.show_message("Project status successfully updated")
                    except (DataEmptyError, ModelsError) as e:
                        BaseUI.show_error(str(e))

                    if BaseForms.ask_forms() == "Y":
                        continue

                case 3:
                    break
                case _:
                    BaseUI.show_message("\nInvalid option")
