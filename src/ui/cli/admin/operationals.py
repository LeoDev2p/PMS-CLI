from utils.helpers import ViewHelper

from ..forms import UI, Forms, UIAdmin


class OperationalViews:
    def __init__(self, controller):
        self.controller = controller

    def run(self):
        while True:
            ViewHelper.clear_screen()
            UI.banner()
            UIAdmin.menu_operational()

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