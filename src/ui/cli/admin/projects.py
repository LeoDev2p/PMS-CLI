from ..forms import UI, Forms, UIAdmin, ViewHelper
from .projects_management import ManagementProjectViews
from .settings import SettingsViews


class ProjectsViews:
    def __init__(self, controller):
        self.controller = controller
        self.m_project = ManagementProjectViews(controller)
        self.settings_views = SettingsViews(controller)

    def project_management(self):
        while True:
            ViewHelper.clear_screen()
            UI.banner()
            UIAdmin.menu_project()

            option = Forms.option_forms()
            match option:
                case 1:
                    self.m_project.run()
                case 2:
                    pass
                case 3:
                    pass
                case 4:
                    break
                case _:
                    UI.show_message("Invalid option")
