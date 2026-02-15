from utils.helpers import clear_screen

from .forms import Forms


class UserViews:
    def __init__(self, controller):
        self.controller = controller

    def run(self):
        while True:
            clear_screen()
            Forms.banner()
            self.menu()
            option = Forms.option_forms()
            match option:
                case 1:
                    pass
                case 2:
                    pass
                case 3:
                    pass
                case 4:
                    break
                case _:
                    Forms.show_message("Invalid option")

    def menu(self):
        print("""
        [1] My tasks
        [2] Update task status
        [3] My profile
        [4] Exit
        """)
