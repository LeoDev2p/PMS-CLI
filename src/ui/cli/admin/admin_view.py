import time

from src.core.logging import get_logger
from src.models.sessions import Session
from src.ui.cli.admin.projects import ProjectsViews
from src.ui.cli.admin.stats import StatsViews
from src.ui.cli.admin.users_management import UserManagementViews
from src.ui.cli.base import BaseForms, BaseUI
from src.ui.cli.menu.admin_menu import AdminMenus
from src.ui.cli.user.profile import MyProfile
from utils.helpers import ViewHelper


class AdminViews:
    """
    Handles the admin panel.
    """

    def __init__(self, controller):
        self.controller = controller
        self.user_views = UserManagementViews(controller)
        self.projects_views = ProjectsViews(controller)
        self.stats_views = StatsViews(controller)
        self.my_profile = MyProfile(controller)

        self.log = get_logger("audit", self.__class__.__name__)

    def run(self):
        """Runs the admin panel."""
        while True:
            ViewHelper.clear_screen()
            BaseUI.banner()
            AdminMenus.menu()

            option = BaseForms.option_forms()
            match option:
                case 1:
                    self.user_views.run()
                case 2:
                    self.projects_views.run()
                case 3:
                    self.stats_views.run()
                case 4:
                    self.my_profile.run()
                case 5:
                    BaseUI.show_message("Logout ............")
                    time.sleep(1)
                    Session.stop()
                    break
                case _:
                    BaseUI.show_message("\nInvalid option")
