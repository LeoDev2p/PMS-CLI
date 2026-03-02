import time

from src.core.exceptions import (
    DataEmptyError,
    DataNotFoundError,
    ModelsError,
    NotFoundUserError,
)
from src.ui.cli.base import BaseForms, BaseTables, BaseUI
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
                BaseTables.show_table(p_result, title="Operational Results")
                id_project = BaseForms.id_forms()

                BaseUI.show_message("Free operational users\n")
                u_result = self.controller.user.get_free_operational_users()
                BaseTables.show_table(u_result, title="Operational Results")
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
            AdminMenus.menu_team_monitoring()

            option = BaseForms.option_forms()
            match option:
                case 1:
                    search = BaseForms.search_forms("Search project")
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
                            BaseTables.show_table(projects, title="Projects")

                            id_project = BaseForms.id_forms()
                            tasks = self.controller.task.get_all_by_project(id_project)
                            BaseTables.show_table(tasks, title="Tasks")
                        except (DataNotFoundError, ModelsError) as e:
                            BaseUI.show_error(str(e))

                        if BaseForms.ask_forms() == "Y":
                            continue

                case 2:
                    search = BaseForms.search_forms("Search project")
                    try:
                        # mostrar proyectos especifico
                        projects = self.controller.project.get_search_by_title(search)
                        BaseTables.show_table(projects, title="Projects")

                        id_project = BaseForms.id_forms()
                    except (DataNotFoundError, ModelsError) as e:
                        BaseUI.show_error(str(e))

                    try:
                        # mostrara tareas del proyecto especifico
                        tasks = self.controller.task.get_details_by_project(id_project)
                        BaseTables.show_table(tasks, title="Tasks")
                        id_task = BaseForms.id_forms()

                        # mostrara los estados
                        status = self.controller.task_status.get_all()
                        BaseTables.show_table(status, title="Status")
                        id_status = BaseForms.id_forms()

                        self.controller.task.edit_status(id_status, id_task, id_project)
                        BaseUI.show_message("\nTask status edited successfully")
                    except (DataEmptyError, ModelsError) as e:
                        BaseUI.show_error(str(e))

                        if BaseForms.ask_forms() == "Y":
                            continue

                    time.sleep(3.2)

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
            AdminMenus.menu_personnel_maintenance()

            option = BaseForms.option_forms()
            print()
            match option:
                case 1:
                    # mover a un usuario de un proyecto A a un proyecto B (limpieza automática)
                    try:
                        BaseUI.show_message("--- Origin Project ---\n")
                        p_title_source = FormsProjects.search_project_forms()
                        projects_source = self.controller.project.get_by_title(p_title_source)

                        BaseTables.show_table(projects_source, title="Projects")
                        id_project_source = BaseForms.id_forms()

                        BaseUI.show_message("--- User to be Reassigned---\n")
                        users = self.controller.user.get_user_by_project(id_project_source)

                        BaseTables.show_table(users, title="Users")
                        id_user = BaseForms.id_forms()

                        BaseUI.show_message("--- Destiny Project---\n")
                        p_title_dest = FormsProjects.search_project_forms()
                        projects_dest = self.controller.project.get_by_title(p_title_dest)

                        BaseTables.show_table(projects_dest, title="Projects")
                        id_project_dest = BaseForms.id_forms()

                        BaseUI.show_message("\nReassigning user and updating tables...\n")

                        # reasignando usuario a nuevo proyecto, limpiando tareas en origen
                        params = (
                            id_user,
                            id_project_source,
                            id_project_dest,
                        )
                        self.controller.task.reassign_user_project(params)

                        BaseUI.show_message("User successfully reassigned to the new project")

                        if BaseForms.ask_forms("Add task in the new project now?") == "Y":
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

                    time.sleep(3.2)

                case 2:
                    try:
                        BaseUI.show_message("--- Search project ---\n")
                        p_title_source = FormsProjects.search_project_forms()
                        projects_source = self.controller.project.get_by_title(p_title_source)
                        BaseTables.show_table(projects_source, title="Projects")
                        id_project_source = BaseForms.id_forms()

                        BaseUI.show_message("\n--- Select user ---\n")
                        users = self.controller.user.get_user_by_project(id_project_source)
                        BaseTables.show_table(users, title="Users")
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

                    time.sleep(3.2)

                case 3:
                    break
                case _:
                    BaseUI.show_message("\nInvalid option")
