import time

from src.core.exceptions import (
    DataEmptyError,
    DataNotFoundError,
    ModelsError,
    StatusExistsError,
)
from src.ui.cli.base import BaseForms, BaseTables, BaseUI
from src.ui.cli.form.project import FormsProjects
from src.ui.cli.form.task import FormsTask
from src.ui.cli.menu.admin_menu import AdminMenus
from utils.helpers import ViewHelper


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
            BaseUI.banner()
            AdminMenus.menu_system_setting()

            option = BaseForms.option_forms()
            match option:
                case 1:
                    self.status_projects_views.run()
                case 2:
                    self.status_tasks_views.run()
                case 3:
                    break
                case _:
                    BaseUI.show_message("Invalid option")


class StatusProjectsViews:
    """Class to manage project status views."""

    def __init__(self, controller):
        self.controller = controller

    def run(self):
        """Runs the project status views."""
        while True:
            ViewHelper.clear_screen()
            BaseUI.banner()
            AdminMenus.menu_status_projects()

            option = BaseForms.option_forms()
            BaseUI.show_message("\n")

            match option:
                case 1:
                    data = []
                    BaseUI.show_message(
                        "Para que el sistema sepa cómo manejar este estado, elija la categoría que mejor lo describa:"
                    )
                    BaseUI.show_message("\n")
                    print("-" * 40)
                    print(" 1. NEW      2. ACTIVE      3. ON HOLD")
                    print(" 4. COMPLETED   5. CANCELLED")
                    print("-" * 40)

                    BaseUI.show_message("\nPara terminar 'N'\n")

                    while True:
                        status = BaseForms.str_forms("New status name")
                        if status.upper() == "N":
                            break

                        key = FormsProjects.system_key_status()
                        data.append((status, key))

                    try:
                        self.controller.project_status.add(data)
                        BaseUI.show_message("\nStatus successfully added")
                    except (StatusExistsError, ModelsError) as e:
                        BaseUI.show_error(str(e))

                        if BaseForms.ask_forms() == "Y":
                            continue

                    time.sleep(3.2)

                case 2:
                    try:
                        result = self.controller.project_status.get_all()
                        BaseTables.show_table(result, title="Settings")
                    except DataNotFoundError as e:
                        BaseUI.show_error(str(e))

                    if BaseForms.ask_forms() == "Y":
                        continue
                case 3:
                    result = self.controller.project_status.get_all()
                    BaseTables.show_table(result, title="Settings")
                    data = FormsProjects.edit_status()

                    try:
                        self.controller.project_status.edit(data)
                        BaseUI.show_message("\nStatus successfully edited")
                    except (DataEmptyError, ModelsError) as e:
                        BaseUI.show_error(str(e))

                        if BaseForms.ask_forms() == "Y":
                            continue

                    time.sleep(3.2)

                case 4:
                    result = self.controller.project_status.get_all()
                    BaseTables.show_table(result, title="Settings")
                    id = BaseForms.id_forms()

                    try:
                        self.controller.project_status.delete(id)
                        BaseUI.show_message("\nStatus successfully deleted")
                    except (DataEmptyError, ModelsError) as e:
                        BaseUI.show_error(str(e))

                        if BaseForms.ask_forms() == "Y":
                            continue

                    time.sleep(3.2)

                case 5:
                    break
                case _:
                    BaseUI.show_message("Invalid option")

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
            BaseUI.banner()
            AdminMenus.menu_status_tasks()

            option = BaseForms.option_forms()
            print()
            match option:
                case 1:
                    data = []
                    BaseUI.show_message(
                        "To let the system know how to handle this status, choose the category that best describes it:"
                    )
                    print("-" * 40)
                    print(" 1. PENDING      2. IN PROGRESS      3. REVIEW")
                    print(" 4. COMPLETED   5. BLOCKED")
                    print("-" * 40)

                    BaseUI.show_message("\nTo end 'N'\n")

                    while True:
                        status = BaseForms.str_forms("New status name")
                        if status.upper() == "N":
                            break

                        system_key = FormsTask.system_key_status()
                        data.append((status, system_key))

                    try:
                        self.controller.task_status.add(data)
                        BaseUI.show_message("\nTask status created successfully")
                    except (StatusExistsError, ModelsError) as e:
                        BaseUI.show_error(str(e))

                        if BaseForms.ask_forms() == "Y":
                            continue

                    time.sleep(3.2)

                case 2:
                    try:
                        result = self.controller.task_status.get_all()
                        BaseTables.show_table(result, title="Settings")

                    except DataNotFoundError as e:
                        BaseUI.show_error(str(e))

                    if BaseForms.ask_forms() == "Y":
                        continue

                case 3:
                    result = self.controller.task_status.get_all()
                    BaseTables.show_table(result, title="Settings")
                    data = FormsTask.status_fields()

                    try:
                        self.controller.task_status.edit(data)
                        BaseUI.show_message("\nTask status edited successfully")
                    except (DataEmptyError, ModelsError) as e:
                        BaseUI.show_error(str(e))

                        if BaseForms.ask_forms() == "Y":
                            continue

                    time.sleep(3.2)

                case 4:
                    result = self.controller.task_status.get_all()
                    BaseTables.show_table(result, title="Settings")
                    id = BaseForms.id_forms()

                    try:
                        self.controller.task_status.delete(id)
                        BaseUI.show_message("\nTask status deleted successfully")
                    except (DataEmptyError, ModelsError) as e:
                        BaseUI.show_error(str(e))

                        if BaseForms.ask_forms() == "Y":
                            continue

                    time.sleep(3.2)

                case 5:
                    break
                case _:
                    BaseUI.show_message("\nInvalid option")

    @staticmethod
    def default_status(controllers):
        controllers.task_status.add_default()
