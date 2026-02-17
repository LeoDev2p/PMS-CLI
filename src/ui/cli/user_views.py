from src.core.exceptions import (
    DataEmptyError,
    HashCreatingError,
    NotFoundProjectError,
    NotFoundTaskError,
    NotFoundTaskStatusError,
)
from src.models.sessions import Session
from utils.helpers import ViewHelper

from .forms import UI, Forms, FormsTask, FormsUser


class UserViews:
    def __init__(self, controller, session):
        self.controller = controller
        self.session = session

    def run(self):
        while True:
            ViewHelper.clear_screen()
            UI.banner()
            self.menu()
            option = Forms.option_forms()
            print()
            match option:
                case 1:
                    try:
                        data = self.controller.task.get_all_tasks_of_user(
                            Session.get_id()
                        )
                        # t.title, t.description, ts.name, p.title
                        UI.show_table_tasks(data)
                    except NotFoundTaskError as e:
                        UI.show_message(str(e))

                    if Forms.ask_forms() == "S":
                        continue
                case 2:
                    # params = id, task_name, task_title, project_title
                    inputs = FormsTask.edit_taskstatus_forms()
                    try:
                        data = self.controller.task.get_task_by_project_task(inputs[1:])
                        UI.show_table_tasks(data, message="TASK")

                        self.controller.task.edit_task_status(
                            inputs[0], inputs[1], inputs[2]
                        )
                    except (
                        NotFoundTaskError,
                        NotFoundTaskStatusError,
                        NotFoundProjectError,
                        DataEmptyError,
                    ) as e:
                        UI.show_message(str(e))

                    if Forms.ask_forms() == "S":
                        continue
                case 3:
                    UI.show_message("Enter your new details\n")
                    try:
                        data = self.controller.user.get_profile()
                        UI.show_table_profile(data)

                        inputs = FormsUser.edit_profile_forms()

                        if Forms.ask_forms(question="Want to update profile?") == "S":
                            self.controller.user.edit_profile(inputs)
                            UI.show_message("Profile updated successfully")
                    except (HashCreatingError, DataEmptyError) as e:
                        UI.show_message(str(e))

                    if Forms.ask_forms() == "S":
                        continue
                case 4:
                    Session.stop()
                    break
                case _:
                    Forms.show_message("Invalid option")

    def menu(self):
        print("""
              USER\n
        [1] My tasks
        [2] Update task status
        [3] My profile
        [4] Logout
        """)

    def my_task(self):
        pass
