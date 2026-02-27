from src.core.exceptions import (
    DataEmptyError,
    DataNotFoundError,
    ModelsError,
    NotFoundUserError,
)
from src.ui.cli.forms import FormsProjects
from utils.helpers import ViewHelper

from ..forms import UI, Forms, FormsTask, UIAdmin


class OperationalViews:
    """Views for operational users."""

    def __init__(self, controller):
        self.controller = controller
        self.team_monitoring = TeamMonitoring(controller)
        self.staff_maintenance = StaffMaintenance(controller)
        self.task_assignment = TaskAssignment(controller)

    def run(self):
        while True:
            ViewHelper.clear_screen()
            UI.banner()
            UIAdmin.menu_operational()

            option = Forms.option_forms()
            match option:
                case 1:
                    self.task_assignment.run()
                case 2:
                    self.team_monitoring.run()
                case 3:
                    self.staff_maintenance.run()
                case 4:
                    break
                case _:
                    UI.show_message("Invalid option")


class TaskAssignment:
    """Task assignment view."""

    def __init__(self, controller):
        self.controller = controller

    def run(self):
        # Nueva Asignación / Crear Tarea
        while True:
            try:
                UI.show_message("New projects")
                p_result = self.controller.project.get_new()
                print(p_result)
                id_project = Forms.id_forms()

                UI.show_message("Free operational users")
                u_result = self.controller.user.get_free_operational_users()
                print(u_result)
                id_user = Forms.id_forms()

                title, description = FormsTask.asigne_task()

                data = (title, description, id_project, id_user)
                self.controller.task.add(data)
                UI.show_message("Task added successfully")
            except (DataEmptyError, ModelsError) as e:
                UI.show_error(str(e))

            if Forms.ask_forms() == "Y":
                continue
            else:
                break


class TeamMonitoring:
    """Team monitoring view."""

    def __init__(self, controller):
        self.controller = controller

    def run(self):
        while True:
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
                    search = FormsProjects.search_project_forms()
                    try:
                        count = self.controller.project.count_by_title(search)
                    except (DataEmptyError, ModelsError) as e:
                        UI.show_error(str(e))
                        continue

                    if count > 10:
                        UI.show_message("Too many projects found")
                        UI.show_message("View list of completed projects in settings")
                        continue
                    else:
                        UI.show_message(f"{count} projects were found")
                        try:
                            projects = self.controller.project.get_search_by_title(search)
                            print(projects)

                            id_project = Forms.id_forms()
                            tasks = self.controller.task.get_all_by_project(id_project)
                            print(tasks)
                        except (DataNotFoundError, ModelsError) as e:
                            UI.show_error(str(e))

                        if Forms.ask_forms() == "Y":
                            continue

                case 2:
                    search = FormsProjects.search_project_forms()
                    try:
                        # mostrar proyectos especifico
                        projects = self.controller.project.get_search_by_title(search)
                        print(projects)
                        id_project = Forms.id_forms()
                    except (DataNotFoundError, ModelsError) as e:
                        UI.show_error(str(e))

                    try:
                        # mostrara tareas del proyecto especifico
                        tasks = self.controller.task.get_details_by_project(id_project)
                        print(tasks)
                        id_task = Forms.id_forms()

                        # mostrara los estados
                        status = self.controller.task_status.get_all()
                        print(status)
                        id_status = Forms.id_forms()

                        self.controller.task.edit_status(id_status, id_task, id_project)
                    except (DataEmptyError, ModelsError) as e:
                        UI.show_error(str(e))

                    if Forms.ask_forms() == "Y":
                        continue

                case 3:
                    break
                case _:
                    UI.show_message("Invalid option")


class StaffMaintenance:
    """Staff maintenance view."""

    def __init__(self, controller):
        self.controller = controller

    def run(self):
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
                    # mover a un usuario de un proyecto A a un proyecto B (limpieza automática)
                    try:
                        UI.show_message("--- Proyecto Origen ---")
                        p_title_source = FormsProjects.search_project_forms()
                        projects_source = self.controller.project.get_by_title(p_title_source)
                        print(projects_source)
                        id_project_source = FormsTask.id_forms()

                        UI.show_message("--- Usuario a Reasignar ---")
                        users = self.controller.user.get_user_by_project(id_project_source)
                        print(users)
                        id_user = FormsTask.id_forms()

                        UI.show_message("--- Proyecto Destino ---")
                        p_title_dest = FormsProjects.search_project_forms()
                        projects_dest = self.controller.project.get_by_title(p_title_dest)
                        print(projects_dest)
                        id_project_dest = FormsTask.id_forms()

                        UI.show_message("Reasignando usuario y actualizando tablas...")

                        # reasignando usuario a nuevo proyecto, limpiando tareas en origen
                        params = (
                            id_user,
                            id_project_source,
                            id_project_dest,
                        )
                        self.controller.task.reassign_user_project(params)

                        UI.show_message("Usuario reasignado exitosamente al nuevo proyecto")

                        if Forms.ask_forms("Agregar tarea en el nuevo proyecto ya?") == "Y":
                            title, description = FormsTask.asigne_task()

                            data = (
                                title,
                                description,
                                id_project_dest,
                                id_user,
                            )
                            self.controller.task.add(data)
                            UI.show_message("Task added successfully")
                    except (
                        DataEmptyError,
                        NotFoundUserError,
                        ModelsError,
                    ) as e:
                        UI.show_error(str(e))

                    if Forms.ask_forms() == "Y":
                        continue
                case 2:
                    try:
                        UI.show_message("--- Buscar proyecto ---")
                        p_title_source = FormsProjects.search_project_forms()
                        projects_source = self.controller.project.get_by_title(p_title_source)
                        print(projects_source)
                        id_project_source = FormsTask.id_forms()

                        UI.show_message("--- Seleccionar usuario ---")
                        users = self.controller.user.get_user_by_project(id_project_source)
                        print(users)
                        id_user = FormsTask.id_forms()

                        params = (id_user, id_project_source)
                        self.controller.task.delete_user_project(params)
                        UI.show_message("User removed successfully")
                    except (
                        DataEmptyError,
                        NotFoundUserError,
                        ModelsError,
                    ) as e:
                        UI.show_error(str(e))
                case 3:
                    break
                case _:
                    UI.show_message("Invalid option")
