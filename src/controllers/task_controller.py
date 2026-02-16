from src.core.exceptions import (
    NotFoundProjectError,
    NotFoundTaskError,
    NotFoundTaskStatusError,
)
from src.core.logging import get_logger
from src.models.sessions import Session


class TaskController:
    def __init__(self, service):
        self.service = service
        self.log = get_logger("audit", self.__class__.__name__)

    def get_all_tasks_of_user(self, id) -> bool:
        return self.service.fetch_tasks_of_user(id)

    def edit_task_status(self, task_status_name, task_title, project_title):
        try:
            result = self.service.modify_id_taskstatus(task_status_name, task_title, project_title)
            self.log.info(f"User {Session.get_id()} updated {task_title}")

            return result
        except (NotFoundTaskError, NotFoundTaskStatusError, NotFoundProjectError) as e:
            self.log.info(
                f"User {Session.get_id()} attempted update task {task_title} in project {project_title} but failed"
            )
            raise e
