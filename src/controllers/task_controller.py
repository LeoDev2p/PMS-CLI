from src.core.exceptions import (
    DataEmptyError,
    NotFoundProjectError,
    NotFoundTaskError,
    NotFoundTaskStatusError,
)
from src.core.logging import get_logger
from src.models.sessions import Session
from utils.validators import validation_data_empty


class TaskController:
    def __init__(self, service):
        self.service = service
        self.log = get_logger("audit", self.__class__.__name__)

    def get_all_tasks_of_user(self, id) -> bool:
        return self.service.fetch_tasks_of_user(id)

    def get_task_by_project_task(self, params):
        validate = validation_data_empty(params)
        if not validate:
            raise DataEmptyError("All fields are required")
        return self.service.fetch_task_by_project_task(params)

    def edit_task_status(self, state_name, task_title, project_title):
        validate = validation_data_empty((state_name, task_title, project_title))
        if not validate:
            raise DataEmptyError("All fields are required")

        try:
            result = self.service.modify_id_taskstatus(
                state_name, task_title, project_title
            )
            self.log.info(
                f"User {Session.get_id()} updated state task of the {task_title}"
            )

            return result
        except (NotFoundTaskError, NotFoundTaskStatusError, NotFoundProjectError) as e:
            self.log.info(
                f"User {Session.get_id()} attempted update task {task_title} in project {project_title} but failed"
            )
            raise e
