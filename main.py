from src.controllers.auth_controller import AuthController
from src.controllers.bundle import ControllerBundle
from src.controllers.project_controller import (
    ProjectController,
    ProjectStatusController,
    UserProjectController,
)
from src.controllers.task_controller import TaskController, TaskStatusController
from src.controllers.user_controller import UserController
from src.core.exceptions import ProjectsError
from src.models.project_models import (
    ProjectModels,
    ProjectStatusModels,
    UserProjectModels,
)
from src.models.task_models import TaskModels, TaskStatusModels
from src.models.user_models import UsersModels
from src.services.auth_services import AuthService
from src.services.bundle import ServicesBundle
from src.services.project_services import (
    ProjectServices,
    ProjectStatusServices,
    UserProjectServices,
)
from src.services.task_services import TaskServices, TaskStatusServices
from src.services.user_services import UserServices
from src.ui.cli.auth.auth_views import AuthView


class Main:
    def __init__(self, view):
        self.view = view

    def run(self):
        self.view.run()


if __name__ == "__main__":
    # models
    user_model = UsersModels()
    task_model = TaskModels()
    task_status_model = TaskStatusModels()
    project_model = ProjectModels()
    project_status_model = ProjectStatusModels()
    user_project_model = UserProjectModels()

    # services
    service = ServicesBundle(
        user=UserServices(user_model),
        auth=AuthService(user_model),
        project=ProjectServices(project_model, project_status_model),
        project_status=ProjectStatusServices(project_status_model),
        task=TaskServices(task_model, user_project_model),
        task_status=TaskStatusServices(task_status_model),
        user_project=UserProjectServices(user_project_model),
    )

    # controllers
    controller = ControllerBundle(
        user=UserController(service.user),
        auth=AuthController(service.auth),
        project=ProjectController(service.project),
        project_status=ProjectStatusController(service.project_status),
        task=TaskController(service.task),
        task_status=TaskStatusController(service.task_status),
        user_project=UserProjectController(service.user_project),
    )

    # view
    view = AuthView(controller)
    try:
        main = Main(view)
        main.run()
    except ProjectsError as e:
        print(str(e))
    except KeyboardInterrupt:
        print("\nBye!")
