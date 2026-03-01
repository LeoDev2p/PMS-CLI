from src.core.exceptions import (
    DataEmptyError,
    HashCreatingError,
    NotFoundProjectError,
    NotFoundTaskError,
    NotFoundTaskStatusError,
    PasswordMatchError,
)
from src.core.logging import get_logger
from src.models.sessions import Session
from src.ui.cli.base import BaseForms, BaseTables, BaseUI
from src.ui.cli.form.task import FormsTask
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
            print()

            match option:
                case 1:
                    try:
                        data = self.controller.task.get_by_user(self.session)
                        # t.title, t.description, ts.name, p.title
                        BaseTables.show_table_tasks(data)
                    except NotFoundTaskError as e:
                        BaseUI.show_message(str(e))

                    if BaseForms.ask_forms() == "Y":
                        continue
                case 2:
                    # params = id, task_name, task_title, project_title
                    inputs = FormsTask.edit_taskstatus_forms()
                    try:
                        data = self.controller.task.get_by_project_and_title(inputs[1:])
                        BaseTables.show_table_tasks(data, message="TASK")

                        self.controller.task.edit_status(inputs[0], inputs[1], inputs[2])
                    except (
                        NotFoundTaskError,
                        NotFoundTaskStatusError,
                        NotFoundProjectError,
                    ) as e:
                        BaseUI.show_message(str(e))
                    except DataEmptyError as e:
                        self.log.warning(f"User {self.session} tried to update task status but failed: {e}")
                        BaseUI.show_message(str(e))

                    if BaseForms.ask_forms() == "Y":
                        continue
                case 3:
                    BaseUI.show_message("Enter your new details\n")
                    try:
                        data = self.controller.user.get_profile()
                        BaseTables.show_table_profile(data)

                        inputs = FormsUser.edit_profile_forms()

                        if BaseForms.ask_forms(question="Want to update profile?") == "S":
                            self.controller.user.edit_profile(inputs)
                            BaseUI.show_message("Profile updated successfully")

                    except DataEmptyError as e:
                        self.log.warning(
                            f"User {self.session} attempted to update the profile with incomplete data: {e}"
                        )
                        BaseUI.show_message(str(e))
                    except PasswordMatchError as e:
                        BaseUI.show_message(str(e))
                    except HashCreatingError as e:
                        self.log.warning(f"User {self.session} tried to update profile but failed: {e}")
                        BaseUI.show_message(str(e))

                    if BaseForms.ask_forms() == "Y":
                        continue
                case 4:
                    Session.stop()
                    break
                case _:
                    BaseForms.show_message("Invalid option")

    def my_task(self):
        pass
