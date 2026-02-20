from utils.helpers import ViewHelper

from ..forms import UI, Forms, UIAdmin


class SettingsViews:
    def __init__(self, controller):
        self.controller = controller
        self.status_projects_views = StatusProjectsViews(controller)
        self.status_tasks_views = StatusTasksViews(controller)

    def run(self):
        while True:
            ViewHelper.clear_screen()
            UI.banner()
            UIAdmin.menu_system_setting()

            option = Forms.option_forms()
            match option:
                case 1:
                    self.status_projects_views.run()
                case 2:
                    self.status_tasks_views.run()
                case 3:
                    break
                case _:
                    UI.show_message("Invalid option")


class StatusProjectsViews:
    def __init__(self, controller):
        self.controller = controller

    def run(self):
        while True:
            ViewHelper.clear_screen()
            UI.banner()
            UIAdmin.menu_status_projects()

            option = Forms.option_forms()
            match option:
                case 1:
                    pass
                case 2:
                    pass
                case 3:
                    pass
                case 5:
                    pass
                case 6:
                    break
                case _:
                    UI.show_message("Invalid option")

class StatusTasksViews:
    def __init__(self, controller):
        self.controller = controller

    def run(self):
        while True:
            ViewHelper.clear_screen()
            UI.banner()
            UIAdmin.menu_status_tasks()

            option = Forms.option_forms()
            match option:
                case 1:
                    pass
                case 2:
                    pass
                case 3:
                    pass
                case 5:
                    pass
                case 6:
                    break
                case _:
                    UI.show_message("Invalid option")
