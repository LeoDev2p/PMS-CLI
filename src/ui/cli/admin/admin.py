from src.core.logging import get_logger
from src.models.sessions import Session
from utils.helpers import ViewHelper

from ..forms import UI, Forms, UIAdmin
from .projects import ProjectsViews
from .users_management import UserManagementViews


class AdminViews:
    def __init__(self, controller):
        self.controller = controller
        self.session = Session.get_id()
        self.user_views = UserManagementViews(controller)
        self.projects_views = ProjectsViews(controller)

        self.log = get_logger("audit", self.__class__.__name__)

    def run(self):
        while True:
            ViewHelper.clear_screen()
            UI.banner()
            UIAdmin.menu_admin()

            option = Forms.option_forms()
            match option:
                case 1:
                    self.user_views.user_management()
                case 2:
                    self.projects_views.project_management()
                case 3:
                    self.statistics_panel()
                case 4:
                    break
                case _:
                    UI.show_message("Invalid option")

    def statistics_panel(self):
        pass
