from src.core.exceptions import (
    DataEmptyError,
    ModelsError,
    NotFoundProjectError,
    ProjectsExistsError,
)

from .forms import UI, Forms, ViewHelper


class AdminProjectsViews:
    def __init__(self, controller):
        self.controller = controller
        self.project = ManagementProject(controller)

    def project_management(self):
        while True:
            ViewHelper.clear_screen()
            UI.banner()
            UI.menu_admin_project()

            option = Forms.option_forms()
            match option:
                case 1:
                    self.project.run()
                case 2:
                    pass
                case 3:
                    pass
                case 4:
                    break
                case _:
                    UI.show_message("Invalid option")


class ManagementProject:
    def __init__(self, controller):
        self.controller = controller

    def run(self):
        while True:
            ViewHelper.clear_screen()
            UI.banner()
            UI.menu_management_project()

            option = Forms.option_forms()
            match option:
                case 1:
                    data = ("GeoAI", "")  # forms (title, description)
                    try:
                        self.controller.project.add_project(data)
                        UI.show_message("Proyecto agregado con exito")
                    except (DataEmptyError, ProjectsExistsError, ModelsError) as e:
                        UI.show_error(str(e))

                    if Forms.ask_forms() == "S":
                        continue

                case 2:
                    try:
                        result = self.controller.project.get_all_project()
                        print(result)
                    except (NotFoundProjectError, ModelsError) as e:
                        UI.show_error(str(e))

                    if Forms.ask_forms() == "S":
                        continue

                case 3:
                    try:
                        result = self.controller.project.get_all_project()
                        print(result)
                        data = ("geoai", 2)
                        self.controller.project.edit_project(data)
                    except (DataEmptyError, ModelsError) as e:
                        UI.show_error(str(e))

                    if Forms.ask_forms() == "S":
                        continue

                case 4:
                    data = 'GeoAi'
                    try:
                        result = self.controller.project.get_by_project(data)
                        print(result)

                        if Forms.ask_forms(question="Do you want delete?") == "S":
                            self.controller.project.delete_project(result[0])
                            UI.show_message("Proyecto eliminado con exito")
                        else:
                            UI.show_message("Acciona cancelada")
                    except (DataEmptyError, NotFoundProjectError, ModelsError) as e:
                        UI.show_error(str(e))

                    if Forms.ask_forms() == "S":
                        continue

                case 5:
                    break
                case _:
                    UI.show_message("Invalid option")
