from src.ui.cli.admin.operationals import OperationalViews
from src.ui.cli.admin.projects_management import ManagementProjectViews
from src.ui.cli.admin.settings import SettingsViews
from src.ui.cli.base import BaseForms, BaseUI
from src.ui.cli.menu.admin_menu import AdminMenus
from utils.helpers import ViewHelper


class ProjectsViews:
    """
    Handles project management.
    """

    def __init__(self, controller):
        self.controller = controller
        self.m_project = ManagementProjectViews(controller)
        self.settings_views = SettingsViews(controller)
        self.operational = OperationalViews(controller)

    def run(self):
        """Runs the project management panel."""
        while True:
            ViewHelper.clear_screen()
            BaseUI.banner()
            AdminMenus.menu_project()

            option = BaseForms.option_forms()
            BaseUI.show_message("\n")

            match option:
                case 1:
                    self.m_project.run()
                case 2:
                    self.settings_views.run()
                case 3:
                    self.operational.run()
                case 4:
                    break
                case _:
                    BaseUI.show_message("Invalid option")
