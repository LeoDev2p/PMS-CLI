from src.core.exceptions import (
    DataEmptyError,
    ModelsError,
    NotFoundProjectError,
    NotFoundStatusProjectError,
    ProjectsExistsError,
)
from src.ui.cli.forms import FormsProjects

from ..forms import UI, Forms, UIAdmin, ViewHelper


class ManagementProjectViews:
    """Class to manage project views."""

    def __init__(self, controller):
        self.controller = controller

    def run(self):
        """Runs the project management views."""
        while True:
            ViewHelper.clear_screen()
            UI.banner()
            UIAdmin.menu_management_project()

            option = Forms.option_forms()
            match option:
                case 1:
                    data = FormsProjects.project_forms()
                    try:
                        try:
                            self.controller.project_status.get_all()
                        except NotFoundStatusProjectError:
                            UI.show_message(
                                "First you need to create the states in 'system setting' or"
                            )
                            if Forms.ask_forms("Create by default") == "Y":
                                self.controller.project.add(data)
                                UI.show_message("Project successfully added")
                            else:
                                UI.show_message("Set status in 'SYSTEM SETTING")
                        else:
                            self.controller.project.add(data)
                    except (DataEmptyError, ProjectsExistsError, ModelsError) as e:
                        UI.show_error(str(e))

                    if Forms.ask_forms() == "Y":
                        continue

                case 2:
                    try:
                        result = self.controller.project.get_all()
                        print(result)
                    except (NotFoundProjectError, ModelsError) as e:
                        UI.show_error(str(e))

                    if Forms.ask_forms() == "Y":
                        continue

                case 3:
                    self.edit_project()

                case 4:
                    data = FormsProjects.search_project_forms()
                    # hacerlo global esa funcion
                    try:
                        result = self.controller.project.get_by_title(data)
                        print(result)
                        id_project = Forms.option_forms()  # cambiar fucion de id universl
                        if Forms.ask_forms(question="Do you want delete?") == "Y":
                            self.controller.project.delete(id_project)
                            UI.show_message("Project successfully deleted")
                        else:
                            UI.show_message("Action canceled")
                    except (DataEmptyError, NotFoundProjectError, ModelsError) as e:
                        UI.show_error(str(e))

                    if Forms.ask_forms() == "Y":
                        continue

                case 5:
                    break
                case _:
                    UI.show_message("Invalid option")

    def edit_project(self):
        """Edits a project."""
        while True:
            ViewHelper.clear_screen()
            UI.banner()
            print("""
            [1] Editing title
            [2] Editing status
            [3] Back
            """)
            option = Forms.option_forms()
            match option:
                case 1:
                    try:
                        result = self.controller.project.get_all()
                        print(result)
                        data = FormsProjects.edit_project_forms()
                        self.controller.project.edit_title(data)
                    except (DataEmptyError, ModelsError) as e:
                        UI.show_error(str(e))

                    if Forms.ask_forms() == "Y":
                        continue

                case 2:
                    try:
                        result = self.controller.project.get_all()
                        print(result)
                        result = self.controller.project_status.get_all()
                        print(result)
                        # id por separado universalizar ----------------------
                        data = FormsProjects.edit_project_status_forms()
                        self.controller.project.edit_status(data)
                        UI.show_message("Project status successfully updated")
                    except (DataEmptyError, ModelsError) as e:
                        UI.show_error(str(e))

                    if Forms.ask_forms() == "Y":
                        continue

                case 3:
                    break
                case _:
                    UI.show_message("Invalid option")
