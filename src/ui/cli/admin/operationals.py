from src.core.exceptions import (
    DataEmptyError,
    DataNotFoundError,
    ModelsError,
    NotFoundUserError,
)
from src.ui.cli.base import BaseForms, BaseUI
from src.ui.cli.form.project import FormsProjects
from src.ui.cli.form.task import FormsTask
from src.ui.cli.menu.admin_menu import AdminMenus
from utils.helpers import ViewHelper


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
            BaseUI.banner()
            AdminMenus.menu_operational()

            option = BaseForms.option_forms()
            print()
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
                    BaseUI.show_message("Invalid option")


class TaskAssignment:
    """Task assignment view."""

    def __init__(self, controller):
        self.controller = controller

    def run(self):
        # Nueva Asignación / Crear Tarea
        while True:
            try:
                BaseUI.show_message("New projects\n")
                p_result = self.controller.project.get_new()
                print(p_result)
                id_project = BaseForms.id_forms()

                BaseUI.show_message("Free operational users\n")
                u_result = self.controller.user.get_free_operational_users()
                print(u_result)
                id_user = BaseForms.id_forms()

                title, description = FormsTask.asigne_task()

                data = (title, description, id_project, id_user)
                self.controller.task.add(data)
                BaseUI.show_message("\nTask added successfully")
            except (DataEmptyError, ModelsError) as e:
                BaseUI.show_error(str(e))

            if BaseForms.ask_forms("\nWould you like to assign more tasks?") == "Y":
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
            BaseUI.banner()
            print("""
                [1] View Team by Project
                [2] Change Task Status
                [3] Back
            """)

            option = BaseForms.option_forms()
            match option:
                case 1:
                    search = FormsProjects.search_project_forms()
                    try:
                        count = self.controller.project.count_by_title(search)
                    except (DataEmptyError, ModelsError) as e:
                        BaseUI.show_error(str(e))
                        continue

                    if count > 10:
                        BaseUI.show_message("Too many projects found")
                        BaseUI.show_message("View list of completed projects in settings")
                        continue
                    else:
                        BaseUI.show_message(f"\n{count} projects were found\n")
                        try:
                            projects = self.controller.project.get_search_by_title(search)
                            print(projects)

                            id_project = BaseForms.id_forms()
                            tasks = self.controller.task.get_all_by_project(id_project)
                            print(tasks)
                        except (DataNotFoundError, ModelsError) as e:
                            BaseUI.show_error(str(e))

                        if BaseForms.ask_forms() == "Y":
                            continue

                case 2:
                    search = FormsProjects.search_project_forms()
                    try:
                        # mostrar proyectos especifico
                        projects = self.controller.project.get_search_by_title(search)
                        print(projects)

                        id_project = BaseForms.id_forms()
                    except (DataNotFoundError, ModelsError) as e:
                        BaseUI.show_error(str(e))

                    try:
                        # mostrara tareas del proyecto especifico
                        tasks = self.controller.task.get_details_by_project(id_project)
                        print(tasks)
                        id_task = BaseForms.id_forms()

                        # mostrara los estados
                        status = self.controller.task_status.get_all()
                        print(status)
                        id_status = BaseForms.id_forms()

                        self.controller.task.edit_status(id_status, id_task, id_project)
                        BaseUI.show_message("\nTask status edited successfully")
                    except (DataEmptyError, ModelsError) as e:
                        BaseUI.show_error(str(e))

                    if BaseForms.ask_forms() == "Y":
                        continue

                case 3:
                    break
                case _:
                    BaseUI.show_message("Invalid option")


class StaffMaintenance:
    """Staff maintenance view."""

    def __init__(self, controller):
        self.controller = controller

    def run(self):
        # Mantenimiento de Personal
        while True:
            ViewHelper.clear_screen()
            BaseUI.banner()
            print("""
                [1] reassign user
                [2] remove user
                [3] Back
            """)

            option = BaseForms.option_forms()
            print()
            match option:
                case 1:
                    # mover a un usuario de un proyecto A a un proyecto B (limpieza automática)
                    try:
                        BaseUI.show_message("--- Proyecto Origen ---\n")
                        p_title_source = FormsProjects.search_project_forms()
                        projects_source = self.controller.project.get_by_title(p_title_source)
                        print(projects_source)
                        id_project_source = FormsTask.id_forms()

                        BaseUI.show_message("--- Usuario a Reasignar ---\n")
                        users = self.controller.user.get_user_by_project(id_project_source)
                        print(users)
                        id_user = FormsTask.id_forms()

                        BaseUI.show_message("--- Proyecto Destino ---\n")
                        p_title_dest = FormsProjects.search_project_forms()
                        projects_dest = self.controller.project.get_by_title(p_title_dest)
                        print(projects_dest)
                        id_project_dest = FormsTask.id_forms()

                        BaseUI.show_message("\nReasignando usuario y actualizando tablas...\n")

                        # reasignando usuario a nuevo proyecto, limpiando tareas en origen
                        params = (
                            id_user,
                            id_project_source,
                            id_project_dest,
                        )
                        self.controller.task.reassign_user_project(params)

                        BaseUI.show_message("Usuario reasignado exitosamente al nuevo proyecto")

                        if BaseForms.ask_forms("Agregar tarea en el nuevo proyecto ya?") == "Y":
                            title, description = FormsTask.asigne_task()

                            data = (
                                title,
                                description,
                                id_project_dest,
                                id_user,
                            )
                            self.controller.task.add(data)
                            BaseUI.show_message("\nTask added successfully")
                    except (
                        DataEmptyError,
                        NotFoundUserError,
                        ModelsError,
                    ) as e:
                        BaseUI.show_error(str(e))

                    if BaseForms.ask_forms() == "Y":
                        continue
                case 2:
                    try:
                        BaseUI.show_message("--- Buscar proyecto ---\n")
                        p_title_source = FormsProjects.search_project_forms()
                        projects_source = self.controller.project.get_by_title(p_title_source)
                        print(projects_source)
                        id_project_source = BaseForms.id_forms()

                        BaseUI.show_message("\n--- Seleccionar usuario ---\n")
                        users = self.controller.user.get_user_by_project(id_project_source)
                        print(users)
                        id_user = BaseForms.id_forms()

                        params = (id_user, id_project_source)
                        self.controller.task.delete_user_project(params)
                        BaseUI.show_message("\nUser removed successfully")
                    except (
                        DataEmptyError,
                        NotFoundUserError,
                        ModelsError,
                    ) as e:
                        BaseUI.show_error(str(e))

                    if BaseForms.ask_forms() == "Y":
                        continue

                case 3:
                    break
                case _:
                    BaseUI.show_message("\nInvalid option")
