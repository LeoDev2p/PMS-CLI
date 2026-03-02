import time

from src.core.exceptions import (
    DataEmptyError,
    DataNotFoundError,
    HashCreatingError,
    ModelsError,
    NotFoundTaskError,
    PasswordMatchError,
)
from src.core.logging import get_logger
from src.models.sessions import Session
from src.ui.cli.base import BaseForms, BaseTables, BaseUI
from src.ui.cli.form.user import FormsUser
from src.ui.cli.menu.user_menu import UserMenus
from utils.helpers import ViewHelper


class ProfileViews:
    """
    Class to manage profile views.
    """

    def __init__(self, controller):
        """
        Initializes the profile views.

        Args:
            controller (object): Controller object.
        """
        self.controller = controller
        self.log = get_logger("audit", self.__class__.__name__)
        self.session = Session.get_id()

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
                    # params = id, task_name, task_title, project_title
                    search = BaseForms.search_forms("Search project")
                    try:
                        # mostrar proyectos especifico
                        projects = self.controller.project.get_search_by_title(search)
                        BaseTables.show_table(projects, title="Found Projects")

                        id_project = BaseForms.id_forms()
                    except (DataNotFoundError, ModelsError) as e:
                        BaseUI.show_error(str(e))

                    try:
                        # mostrara tareas del proyecto especifico
                        project = next((k["title"] for k in projects if k["id"] == id_project), None)

                        BaseUI.show_message(f"\nTasks of the project {project}\n")
                        tasks = self.controller.task.get_details_by_project(id_project)
                        BaseTables.show_table(tasks, title="Project Tasks")
                        id_task = BaseForms.id_forms()

                        # mostrara los estados
                        BaseUI.show_message("\nList of Status\n")
                        status = self.controller.task_status.get_all()
                        BaseTables.show_table(status, title="Task Status")
                        id_status = BaseForms.id_forms()

                        # editar estado
                        self.controller.task.edit_status(id_status, id_task, id_project)
                        BaseUI.show_message("\nTask status edited successfully")
                    except (DataEmptyError, ModelsError) as e:
                        BaseUI.show_error(str(e))

                        if BaseForms.ask_forms() == "Y":
                            continue

                    time.sleep(3.2)

                case 3:
                    BaseUI.show_message("My Profile\n")
                    try:
                        data = self.controller.user.get_profile()
                        BaseUI.show_message(f"[::] Username: {data['username']}")
                        BaseUI.show_message(f"[::] Email: {data['email']}")
                    except (DataEmptyError, ModelsError) as e:
                        BaseUI.show_error(str(e))

                    if BaseForms.ask_forms("Do you want to edit your profile?") == "Y":
                        self.edit_profile()

                case 4:
                    BaseUI.show_message("Logout ............")
                    time.sleep(1)
                    Session.stop()
                    break
                case _:
                    BaseForms.show_message("\nInvalid option")

    def edit_profile(self):
        while True:
            ViewHelper.clear_screen()
            BaseUI.banner()
            UserMenus.menu_edit_profile()

            option = BaseForms.option_forms()
            BaseUI.show_message("\n")

            match option:
                case 1:
                    try:
                        username = FormsUser.str_forms("New username")

                        if BaseForms.ask_forms(question="Want to update username?") == "Y":
                            self.controller.user.edit_username((username, Session.get_id()))
                            BaseUI.show_message("\nUsername updated successfully\n")

                    except DataEmptyError as e:
                        self.log.warning(
                            f"User {self.session} attempted to update the profile with incomplete data: {e}"
                        )
                        BaseUI.show_message(str(e))
                    except (DataEmptyError, ModelsError) as e:
                        BaseUI.show_message(str(e))

                        if BaseForms.ask_forms() == "Y":
                            continue

                    time.sleep(3.2)
                case 2:
                    try:
                        password = FormsUser.str_forms("New Password")

                        if BaseForms.ask_forms(question="Want to update password?") == "Y":
                            self.controller.user.reset_password((Session.get_id(), password))
                            BaseUI.show_message("\nPassword updated successfully\n")

                    except DataEmptyError as e:
                        self.log.warning(
                            f"User {self.session} attempted to update the profile with incomplete data: {e}"
                        )
                        BaseUI.show_message(str(e))
                    except (PasswordMatchError, HashCreatingError, DataEmptyError, ModelsError) as e:
                        BaseUI.show_message(str(e))

                        if BaseForms.ask_forms() == "Y":
                            continue

                    time.sleep(3.2)

                case 3:
                    break
                case _:
                    BaseForms.show_message("\nInvalid option")
