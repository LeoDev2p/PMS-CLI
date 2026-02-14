from src.controllers.auth_controller import AuthController
from src.models.user_models import UsersModels
from src.services.auth_services import AuthService
from src.ui.app import View


class Main:
    def __init__(self, view):
        self.view = view

    def run(self):
        self.view.run()


if __name__ == "__main__":
    model = UsersModels()
    service = AuthService(model)
    controller = AuthController(service)
    view = View(controller)
    main = Main(view)
    main.run()
