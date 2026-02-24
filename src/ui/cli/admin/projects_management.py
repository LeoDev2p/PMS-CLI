from src.core.exceptions import (
    DataEmptyError,
    ModelsError,
    NotFoundProjectError,
    NotFoundStatusProjectError,
    ProjectsExistsError,
)

from ..forms import UI, Forms, UIAdmin, ViewHelper
from .settings import StatusProjectsViews


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
                    try:
                        # title projects, state projects
                        result = self.controller.project.get_all_project()
                        print(result)
                        data = ("geoai", 2)  # forms
                        self.controller.project.edit_project(data)
                    except (DataEmptyError, ModelsError) as e:
                        UI.show_error(str(e))

                    if Forms.ask_forms() == "Y":
                        continue

                case 4:
                    data = "GeoAi"  # Forms
                    try:
                        result = self.controller.project.get_by_project(data)
                        print(result)

                        if Forms.ask_forms(question="Do you want delete?") == "Y":
                            self.controller.project.delete_project(result[0])
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
