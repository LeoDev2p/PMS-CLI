from src.ui.cli.forms import FormsProjects
from src.core.exceptions import (
    DataEmptyError,
    ModelsError,
    NotFoundProjectError,
    NotFoundStatusProjectError,
    ProjectsExistsError,
)

from ..forms import UI, Forms, UIAdmin, ViewHelper


class ManagementProjectViews:
    """
    Class to manage project views.
    """

    def __init__(self, controller):
        self.controller = controller

    def run(self):
        """
        Runs the project management views.
        """
        while True:
            ViewHelper.clear_screen()
            UI.banner()
            UIAdmin.menu_management_project()

            option = Forms.option_forms()
            match option:
                case 1:
                    data = ("GeoAI", "")  # forms (title, description)
                    try:
                        try:
                            self.controller.project.get_all_status()
                        except NotFoundStatusProjectError:
                            UI.show_message(
                                "First you need to create the states in 'system setting' or"
                            )
                            if Forms.ask_forms("Create by default") == "Y":
                                self.controller.project.add_project(data)
                                UI.show_message("Project successfully added")
                            else:
                                UI.show_message("Set status in 'SYSTEM SETTING")
                        else:
                            self.controller.project.add_project(data)
                    except (DataEmptyError, ProjectsExistsError, ModelsError) as e:
                        UI.show_error(str(e))

                    if Forms.ask_forms() == "Y":
                        continue

                case 2:
                    try:
                        result = self.controller.project.get_all_project()
                        print(result)
                    except (NotFoundProjectError, ModelsError) as e:
                        UI.show_error(str(e))

                    if Forms.ask_forms() == "Y":
                        continue

                case 3:
                    self.edit_project()

                case 4:
                    data = "GeoAi"  # Forms
                    try:
                        result = self.controller.project.get_by_project(data)
                        print(result)
                        id_project = Forms.option_forms()
                        if Forms.ask_forms(question="Do you want delete?") == "Y":
                            self.controller.project.delete_project(id_project)
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
        """
        Edits a project.

        Args:
            data (tuple): Tuple of project parameters.
        """
        while True:
            ViewHelper.clear_screen()
            UI.banner()
            print ("""
            [1] Editing title
            [2] Editing status
            [3] Back
            """)
            option = Forms.option_forms()
            match option:
                case 1:
                    try:
                        result = self.controller.project.get_all_project()
                        print(result)
                        data = FormsProjects.edit_project_forms()
                        # separa si editar titulo o estado
                        self.controller.project.edit_title_project(data)
                    except (DataEmptyError, ModelsError) as e:
                        UI.show_error(str(e))

                    if Forms.ask_forms() == "Y":
                        continue

                case 2:
                    try:
                        result = self.controller.project.get_all_project()
                        print(result)
                        result = self.controller.project.get_all_status()
                        print(result)
                        data = FormsProjects.edit_project_status_forms()
                        self.controller.project.edit_project_status_by_project(data)
                        UI.show_message("Project status successfully updated")
                    except (DataEmptyError, ModelsError) as e:
                        UI.show_error(str(e))

                    if Forms.ask_forms() == "Y":
                        continue

                case 3:
                    break
                case _:
                    UI.show_message("Invalid option")
