from src.core.exceptions import (
    HashCreatingError,
    NotFoundProjectError,
    NotFoundTaskError,
    NotFoundTaskStatusError,
)
from src.models.sessions import Session
from utils.helpers import clear_screen

from .forms import Forms, FormsTask, FormsUser


class UserViews:
    def __init__(self, controller, session):
        self.controller = controller
        self.session = session

    def run(self):
        while True:
            clear_screen()
            Forms.banner()
            self.menu()
            option = Forms.option_forms()
            match option:
                case 1:
                    try:
                        data = self.controller.task.get_all_tasks_of_user(
                            Session.get_id()
                        )
                        # momento
                        for k in data:
                            print(k)
                    except NotFoundTaskError as e:
                        Forms.show_message(str(e))

                    if Forms.ask_forms() == "S":
                        continue
                case 2:
                    # params = id, task_name, task_title, project_title
                    inputs = FormsTask.edit_taskstatus_forms()
                    try:
                        # falta mostrar antes de actualizar
                        self.controller.task.edit_task_status(inputs[0], inputs[1], inputs[2])
                    except (
                        NotFoundTaskError,
                        NotFoundTaskStatusError,
                        NotFoundProjectError,
                    ) as e:
                        Forms.show_message(str(e))

                    if Forms.ask_forms() == "S":
                        continue
                case 3:
                    inputs = FormsUser.edit_profile_forms()
                    data = self.controller.user.get_profile()
                    print(data)
                    try:
                        self.controller.user.edit_profile(inputs)
                    except HashCreatingError as e:
                        Forms.show_message(str(e))

                    if Forms.ask_forms() == "S":
                        continue
                case 4:
                    break
                case _:
                    Forms.show_message("Invalid option")

    def menu(self):
        print("""
              USER\n
        [1] My tasks
        [2] Update task status
        [3] My profile
        [4] Exit
        """)

    def my_task(self):
        pass
