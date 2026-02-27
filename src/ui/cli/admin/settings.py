from src.core.exceptions import (
    DataEmptyError,
    DataNotFoundError,
    ModelsError,
    StatusExistsError,
)
from utils.helpers import ViewHelper

from ..forms import UI, Forms, FormsProjects, FormsTask, UIAdmin


class SettingsViews:
    """Class to manage system settings views."""

    def __init__(self, controller):
        self.controller = controller
        self.status_projects_views = StatusProjectsViews(controller)
        self.status_tasks_views = StatusTasksViews(controller)

    def run(self):
        """Runs the system settings views."""
        while True:
            ViewHelper.clear_screen()
            UI.banner()
            UIAdmin.menu_system_setting()

            option = Forms.option_forms()
            match option:
                case 1:
                    self.status_projects_views.run()
                case 2:
                    self.status_tasks_views.run()
                case 3:
                    break
                case _:
                    UI.show_message("Invalid option")


class StatusProjectsViews:
    """Class to manage project status views."""

    def __init__(self, controller):
        self.controller = controller

    def run(self):
        """Runs the project status views."""
        while True:
            ViewHelper.clear_screen()
            UI.banner()
            UIAdmin.menu_status_projects()

            option = Forms.option_forms()
            match option:
                case 1:
                    data = []
                    UI.show_message("Para terminar 'N'")
                    UI.show_message(
                        "Para que el sistema sepa cómo manejar este estado, elija la categoría que mejor lo describa:"
                    )
                    print("-" * 40)
                    print(" 1. NEW      2. ACTIVE      3. ON HOLD")
                    print(" 4. COMPLETED   5. CANCELLED")
                    print("-" * 40)
                    while True:
                        status = FormsProjects.status_fields()
                        if status.upper() == "N":
                            break

                        key = FormsProjects.system_key_status()
                        data.append((status, key))

                    try:
                        self.controller.project_status.add(data)
                    except (StatusExistsError, ModelsError) as e:
                        UI.show_error(str(e))

                    if Forms.ask_forms() == "Y":
                        continue

                case 2:
                    try:
                        result = self.controller.project_status.get_all()
                        print(result)
                    except DataNotFoundError as e:
                        UI.show_error(str(e))

                    if Forms.ask_forms() == "Y":
                        continue
                case 3:
                    result = self.controller.project_status.get_all()
                    print(result)
                    data = FormsProjects.status_fields(edit=True)

                    try:
                        self.controller.project_status.edit(data)
                        UI.show_message("Status successfully edited")
                    except (DataEmptyError, ModelsError) as e:
                        UI.show_error(str(e))

                    if Forms.ask_forms() == "Y":
                        continue

                case 4:
                    result = self.controller.project_status.get_all()
                    print(result)
                    id = FormsProjects.status_fields(delete=True)

                    try:
                        self.controller.project_status.delete(id)
                        UI.show_message("Status successfully deleted")
                    except (DataEmptyError, ModelsError) as e:
                        UI.show_error(str(e))

                    if Forms.ask_forms() == "Y":
                        continue

                case 5:
                    break
                case _:
                    UI.show_message("Invalid option")

    @staticmethod
    def default_status(controllers):
        controllers.project_status.add_default()


class StatusTasksViews:
    """Class to manage task status views."""

    def __init__(self, controller):
        self.controller = controller

    def run(self):
        """Runs the task status views."""
        while True:
            ViewHelper.clear_screen()
            UI.banner()
            UIAdmin.menu_status_tasks()

            option = Forms.option_forms()
            match option:
                case 1:
                    data = []
                    UI.show_message("To end 'N'")
                    UI.show_message(
                        "To let the system know how to handle this status, choose the category that best describes it:"
                    )
                    print("-" * 40)
                    print(" 1. PENDING      2. IN PROGRESS      3. REVIEW")
                    print(" 4. COMPLETED   5. BLOCKED")
                    print("-" * 40)
                    while True:
                        status = FormsTask.status_fields()
                        if status.upper() == "N":
                            break

                        system_key = FormsTask.system_key_status()
                        data.append((status, system_key))

                    try:
                        self.controller.task_status.add(data)
                        UI.show_message("Task status created successfully")
                    except (StatusExistsError, ModelsError) as e:
                        UI.show_error(str(e))

                    if Forms.ask_forms() == "Y":
                        continue

                case 2:
                    try:
                        result = self.controller.task_status.get_all()
                        print(result)

                    except DataNotFoundError as e:
                        UI.show_error(str(e))

                    if Forms.ask_forms() == "Y":
                        continue

                case 3:
                    result = self.controller.task_status.get_all()
                    print(result)
                    data = FormsTask.status_fields(edit=True)

                    try:
                        self.controller.task_status.edit(data)
                        UI.show_message("Task status edited successfully")
                    except (DataEmptyError, ModelsError) as e:
                        UI.show_error(str(e))

                    if Forms.ask_forms() == "Y":
                        continue

                case 4:
                    result = self.controller.task_status.get_all()
                    print(result)
                    id = FormsTask.status_fields(delete=True)

                    try:
                        self.controller.task_status.delete(id)
                        UI.show_message("Task status deleted successfully")
                    except (DataEmptyError, ModelsError) as e:
                        UI.show_error(str(e))

                    if Forms.ask_forms() == "Y":
                        continue

                case 5:
                    break
                case _:
                    UI.show_message("Invalid option")

    @staticmethod
    def default_status(controllers):
        controllers.task_status.add_default()
