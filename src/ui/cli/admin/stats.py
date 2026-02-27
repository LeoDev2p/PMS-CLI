from src.ui.cli.forms import UI, Forms
from utils.helpers import ViewHelper


class StatsViews:
    def __init__(self, controller):
        self.controller = controller

    def run(self):
        while True:
            ViewHelper.clear_screen()
            UI.banner()
            print("""
                [1] Talent Management
                [2] Health Status
                [3] Performance and Averages
                [4] Back
            """)

            option = Forms.option_forms()
            match option:
                case 1:
                    self.view_team_by_project()
                case 2:
                    self.change_task_status()
                case 3:
                    break
                case _:
                    UI.show_message("Invalid option")
