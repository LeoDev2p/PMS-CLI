from src.core.exceptions import (
    DataNotFoundError,
    ModelsError,
    NotFoundTaskError,
    NotFoundTaskStatusError,
    ProjectsError,
)
from src.ui.cli.base import BaseForms, BaseTables, BaseUI
from src.ui.cli.menu.admin_menu import AdminMenus
from utils.helpers import ViewHelper


class StatsViews:
    def __init__(self, controller):
        self.controller = controller
        self.talent_management_views = TalentManagementViews(controller)
        self.health_status_views = HealthStatusViews(controller)
        self.metrics_views = MetricsViews(controller)
        self.critical_control_panel_views = CriticalControlPanelViews(controller)

    def run(self):
        while True:
            ViewHelper.clear_screen()
            BaseUI.banner()
            AdminMenus.menu_statistics()

            option = BaseForms.option_forms()
            BaseUI.show_message("\n")

            match option:
                case 1:
                    self.talent_management_views.run()
                case 2:
                    self.health_status_views.run()
                case 3:
                    self.metrics_views.run()
                case 4:
                    self.critical_control_panel_views.run()
                case 5:
                    break
                case _:
                    BaseUI.show_message("Invalid option")


class TalentManagementViews:
    def __init__(self, controller):
        self.controller = controller

    def run(self):
        while True:
            ViewHelper.clear_screen()
            BaseUI.banner()
            AdminMenus.menu_talent_management()

            option = BaseForms.option_forms()
            BaseUI.show_message("\n")

            match option:
                case 1:
                    try:
                        result = self.controller.user.get_free_vs_assigned_users()
                        BaseTables.show_table(result, title="Statistics")
                    except (ModelsError, ProjectsError) as e:
                        BaseUI.show_message(str(e))

                    if BaseForms.ask_forms() == "Y":
                        continue
                case 2:
                    try:
                        result = self.controller.user.get_count_tasks_by_user()
                        BaseTables.show_table(result, title="Statistics")
                    except (ModelsError, ProjectsError) as e:
                        BaseUI.show_message(str(e))

                    if BaseForms.ask_forms() == "Y":
                        continue

                case 3:
                    try:
                        BaseUI.show_message("\n--- The 10 users with the most completed tasks ---\n")
                        result = self.controller.user.get_top_users()
                        BaseTables.show_table(result, title="Statistics")
                    except (ModelsError, ProjectsError) as e:
                        BaseUI.show_message(str(e))

                    if BaseForms.ask_forms() == "Y":
                        continue
                case 4:
                    break
                case _:
                    BaseUI.show_message("\nInvalid option")


class HealthStatusViews:
    def __init__(self, controller):
        self.controller = controller

    def run(self):
        while True:
            ViewHelper.clear_screen()
            BaseUI.banner()
            AdminMenus.menu_health_status()

            option = BaseForms.option_forms()
            BaseUI.show_message("\n")

            match option:
                case 1:
                    try:
                        result = self.controller.project.get_project_progress()
                        BaseTables.show_table(result, title="Statistics")
                    except (DataNotFoundError, ModelsError, ProjectsError) as e:
                        BaseUI.show_message(str(e))

                    if BaseForms.ask_forms() == "Y":
                        continue
                case 2:
                    try:
                        result = self.controller.task_status.get_state_distribution()
                        BaseTables.show_table(result, title="Statistics")
                    except (DataNotFoundError, ModelsError, ProjectsError) as e:
                        BaseUI.show_message(str(e))

                    if BaseForms.ask_forms() == "Y":
                        continue
                case 3:
                    try:
                        result = self.controller.project.get_count_users_by_project()
                        BaseTables.show_table(result, title="Statistics")
                    except (DataNotFoundError, ModelsError, ProjectsError) as e:
                        BaseUI.show_message(str(e))

                    if BaseForms.ask_forms() == "Y":
                        continue
                case 4:
                    break
                case _:
                    BaseUI.show_message("\nInvalid option")


class MetricsViews:
    def __init__(self, controller):
        self.controller = controller

    def run(self):
        while True:
            ViewHelper.clear_screen()
            BaseUI.banner()
            AdminMenus.menu_performance_metrics()

            option = BaseForms.option_forms()
            BaseUI.show_message("\n")

            match option:
                case 1:
                    try:
                        BaseUI.show_message("\n--- Blocking rate of tasks ---\n")
                        result = self.controller.task_status.get_blocking_rate()
                        BaseTables.show_table(result, title="Statistics")
                    except (ModelsError, NotFoundTaskStatusError, ProjectsError) as e:
                        BaseUI.show_message(str(e))

                    if BaseForms.ask_forms() == "Y":
                        continue
                case 2:
                    BaseUI.show_message("\n--- Efficiency in task completion last year ---\n")
                    try:
                        result = self.controller.task.get_completion_efficiency()
                        BaseTables.show_table(result, title="Statistics")
                    except (ModelsError, NotFoundTaskError, ProjectsError) as e:
                        BaseUI.show_message(str(e))

                    if BaseForms.ask_forms() == "Y":
                        continue
                case 3:
                    break
                case _:
                    BaseUI.show_message("\nInvalid option")

class CriticalControlPanelViews:
    def __init__(self, controller):
        self.controller = controller

    def run(self):
        while True:
            ViewHelper.clear_screen()
            BaseUI.banner()
            AdminMenus.menu_critical_control_panel()

            option = BaseForms.option_forms()
            BaseUI.show_message("\n")

            match option:
                case 1:
                    try:
                        BaseUI.show_message("\n--- Orphan Task Alerts ---\n")
                        result = self.controller.task.get_orphan_task_alerts()
                        BaseTables.show_table(result, title="Statistics")
                    except (ModelsError, NotFoundTaskStatusError, ProjectsError) as e:
                        BaseUI.show_message(str(e))

                    if BaseForms.ask_forms() == "Y":
                        continue
                case 2:
                    BaseUI.show_message("\n--- Critical Projects ---\n")
                    try:
                        result = self.controller.project.get_critical_projects()
                        BaseTables.show_table(result, title="Statistics")
                    except (ModelsError, NotFoundTaskError, ProjectsError) as e:
                        BaseUI.show_message(str(e))

                    if BaseForms.ask_forms() == "Y":
                        continue
                case 3:
                    break
                case _:
                    BaseUI.show_message("\nInvalid option")
