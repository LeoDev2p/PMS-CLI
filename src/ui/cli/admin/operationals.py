from src.core.exceptions import (
    DataEmptyError,
    DataNotFoundError,
    ModelsError,
    NotFoundUserError,
)
from src.ui.cli.forms import FormsProjects
from utils.helpers import ViewHelper

from ..forms import UI, Forms, FormsTask, FormsUser, UIAdmin


class OperationalViews:
    def __init__(self, controller):
        self.controller = controller

    def run(self):
        while True:
            ViewHelper.clear_screen()
            UI.banner()
            UIAdmin.menu_operational()

            option = Forms.option_forms()
            match option:
                case 1:
                    # Nueva Asignación / Crear Tarea
                    try:
                        p_result = self.controller.project.get_projects_new()
                        print(p_result)
                        id_project = Forms.id_forms()

                        u_result = self.controller.user.get_free_operational_users()
                        print(u_result)
                        id_user = Forms.id_forms()

                        task, description = FormsTask.task_forms()

                        data = (task, description, id_project, id_user)
                        self.controller.task.add_task(data)
                        UI.show_message("Task added successfully")
                    except (DataEmptyError, ModelsError) as e:
                        UI.show_error(str(e))

                    if Forms.ask_forms() == "Y":
                        continue

                case 2:
                    # Control de Equipos y Monitoreo
                    ViewHelper.clear_screen()
                    UI.banner()
                    print("""
                    [1] View Team by Project
                    [2] Change Task Status
                    [3] Back
                    """)

                    option = Forms.option_forms()
                    match option:
                        case 1:
                            while True:
                                search = FormsProjects.search_project_forms()
                                try:
                                    count = (
                                        self.controller.project.count_projects_by_title(
                                            search
                                        )
                                    )
                                except (DataEmptyError, ModelsError) as e:
                                    UI.show_error(str(e))
                                    continue

                                if count > 10:
                                    UI.show_message("Too many projects found")
                                    UI.show_message(
                                        "View list of completed projects in settings"
                                    )
                                    continue
                                else:
                                    UI.show_message(f"{count} projects were found")
                                    try:
                                        projects = self.controller.project.get_projects_by_title(
                                            search
                                        )
                                        print(projects)
                                    except (DataNotFoundError, ModelsError) as e:
                                        UI.show_error(str(e))
                                        continue

                                if Forms.ask_forms() == "Y":
                                    continue
                        case 2:
                            result = self.controller.task.get_all_status()
                            print(result)
                            data = FormsTask.status_fields(edit=True)

                            try:
                                self.controller.task.edit_status(data)
                            except (DataEmptyError, ModelsError) as e:
                                UI.show_error(str(e))

                            if Forms.ask_forms() == "Y":
                                continue
                        case 3:
                            break
                        case _:
                            UI.show_message("Invalid option")

                case 3:
                    # Mantenimiento de Personal
                    while True:
                        ViewHelper.clear_screen()
                        UI.banner()
                        print("""
                        [1] reassign user
                        [2] remove user
                        [3] Back
                        """)

                        option = Forms.option_forms()
                        match option:
                            case 1:
                                pass
                            case 2:
                                user_email = FormsUser.search_forms()
                                result = self.controller.user.search_user_or_email(
                                    user_email
                                )[0]
                                print(result)

                                id = FormsUser.id_forms()
                                try:
                                    self.controller.user.delete_user(id)
                                except (NotFoundUserError, ModelsError) as e:
                                    UI.show_message(str(e))

                                if Forms.ask_forms() == "Y":
                                    continue
                            case 3:
                                break
                            case _:
                                UI.show_message("Invalid option")
                case 4:
                    break
                case _:
                    UI.show_message("Invalid option")
