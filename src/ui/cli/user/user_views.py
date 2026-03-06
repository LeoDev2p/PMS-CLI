import time

from src.core.exceptions import (
    DataEmptyError,
    DataNotFoundError,
    ModelsError,
    NotFoundTaskError,
)
from src.models.sessions import Session
from src.ui.cli.base import BaseForms, BaseTables, BaseUI
from src.ui.cli.menu.user_menu import UserMenus
from utils.helpers import ViewHelper

from .profile import MyProfile


class UserViews:
    """
    Class to manage user views.
    """

    def __init__(self, controller):
        """
        Initializes the profile views.

        Args:
            controller (object): Controller object.
        """
        self.controller = controller
        self.my_profile = MyProfile(controller)

    def run(self):
        """
        Runs the profile views.
        """
        while True:
            ViewHelper.clear_screen()
            BaseUI.banner()
            UserMenus.menu()
            option = BaseForms.option_forms()
            BaseUI.show_message("\n")

            match option:
                case 1:
                    try:
                        data = self.controller.task.get_by_user()
                        BaseTables.show_table(data, title="Your Tasks")
                    except (NotFoundTaskError, ModelsError) as e:
                        BaseUI.show_message(str(e))

                    if BaseForms.ask_forms() == "Y":
                        continue

                case 2:
                    search = BaseForms.search_forms("Search project")

                    try:
                        # --- Buscar Proyectos ---
                        projects = self.controller.project.get_search_by_title(search)
                        BaseTables.show_table(projects, title="Found Projects")
                        id_project = BaseForms.id_forms()

                        try:
                            # --- Mostrar Tareas ---
                            # Buscamos el nombre del proyecto en la lista obtenida anteriormente
                            project_name = next((k["title"] for k in projects if k["id"] == id_project), "Unknown")

                            BaseUI.show_message(f"\nTasks of the project {project_name}\n")
                            tasks = self.controller.task.get_details_by_project(id_project)
                            BaseTables.show_table(tasks, title="Project Tasks")
                            id_task = BaseForms.id_forms()

                            try:
                                # --- Editar Estado ---
                                BaseUI.show_message("\nList of Status\n")
                                status = self.controller.task_status.get_all()
                                BaseTables.show_table(status, title="Task Status")
                                id_status = BaseForms.id_forms()

                                # edición
                                self.controller.task.edit_status(id_status, id_task, id_project)
                                BaseUI.show_message("\nTask status edited successfully")

                            except (DataEmptyError, DataNotFoundError, ModelsError) as e:
                                BaseUI.show_error(f"Error en estados: {e}")
                                if BaseForms.ask_forms("Do you want to try again?") == "Y":
                                    continue

                        except (DataEmptyError, DataNotFoundError, ModelsError) as e:
                            BaseUI.show_error(f"Error en tareas: {e}")
                            if BaseForms.ask_forms("Do you want to try again?") == "Y":
                                continue

                    except (DataEmptyError, DataNotFoundError, ModelsError) as e:
                        BaseUI.show_error(f"Error en proyecto: {e}")
                        if BaseForms.ask_forms("Do you want to try again?") == "Y":
                            continue

                    time.sleep(3.2)

                case 3:
                    self.my_profile.run()

                case 4:
                    BaseUI.show_message("Logout ............")
                    time.sleep(1)
                    Session.stop()
                    break
                case _:
                    BaseForms.show_message("\nInvalid option")
