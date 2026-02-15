from src.controllers.auth_controller import AuthController
from src.controllers.bundle import ControllerBundle
from src.models.user_models import UsersModels
from src.services.auth_services import AuthService
from src.services.bundle import ServicesBundle
from src.ui.cli.app import View


class Main:
    def __init__(self, view):
        self.view = view

    def run(self):
        self.view.run()


if __name__ == "__main__":
    # models
    user_model = UsersModels()

    # services
    service = ServicesBundle(auth=AuthService(user_model), project=None, task=None)

    # controllers
    controller = ControllerBundle(
        auth=AuthController(service.auth), project=None, task=None
    )

    # view
    view = View(controller)
    main = Main(view)
    main.run()
