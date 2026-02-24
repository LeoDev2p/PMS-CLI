from utils.helpers import ViewHelper

from ..forms import UI, Forms, UIAdmin, FormsTask


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
                    # mostrar que proyecto
                    # Datos de la tarea
                    # mostrar user disponibles
                    r_projects = self.controller.project.get_all_project()
                    print (r_projects)
                    data = ('title', '')  #FormsTask.asigne_task()
                    
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
