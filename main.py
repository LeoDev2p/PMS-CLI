from src.controllers.auth_controller import AuthController
from src.controllers.bundle import ControllerBundle
from src.controllers.project_controller import ProjectController
from src.controllers.task_controller import TaskController
from src.controllers.user_controller import UserController
from src.models.project_models import ProjectModels
from src.models.task_models import TaskModels
from src.models.user_models import UsersModels
from src.services.auth_services import AuthService
from src.services.bundle import ServicesBundle
from src.services.project_services import ProjectServices
from src.services.task_services import TaskServices
from src.services.user_services import UserServices
from src.ui.cli.app import View


class Main:
    def __init__(self, view):
        self.view = view

    def run(self):
        self.view.run()


if __name__ == "__main__":
    # models
    user_model = UsersModels()
    task_model = TaskModels()
    project_model = ProjectModels()

    # services
    service = ServicesBundle(
        user=UserServices(user_model),
        auth=AuthService(user_model),
        project=ProjectServices(project_model),
        task=TaskServices(task_model, project_model),
    )

    # controllers
    controller = ControllerBundle(
        user=UserController(service.user),
        auth=AuthController(service.auth),
        project=ProjectController(service.project),
        task=TaskController(service.task),
    )

    # view
    view = View(controller)
    try:
        main = Main(view)
        main.run()
    except KeyboardInterrupt as k:
        print ("\nBye!")
