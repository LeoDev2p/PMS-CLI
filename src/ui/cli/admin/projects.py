from ..forms import UI, Forms, UIAdmin, ViewHelper
from .operationals import OperationalViews
from .projects_management import ManagementProjectViews
from .settings import SettingsViews


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
            UI.banner()
            UIAdmin.menu_project()

            option = Forms.option_forms()
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
                    UI.show_message("Invalid option")
