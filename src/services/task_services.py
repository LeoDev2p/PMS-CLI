from src.core.exceptions import (
    DatabaseLockedError,
    ModelsError,
    NotFoundProjectError,
    NotFoundTaskError,
    NotFoundTaskStatusError,
)
from src.core.logging import get_logger
from src.models.sessions import Session
from utils.helpers import TextHelper


class TaskServices:
    def __init__(self, task_model, project_model):
        self.task_model = task_model
        self.project_model = project_model
        self.log_audit = get_logger("audit", self.__class__.__name__)
        self.log_error = get_logger("error", self.__class__.__name__)

    def fetch_tasks_of_user(self, id) -> list[tuple]:
        result = self.task_model.select_all_tasks_of_user(id)
        if not result:
            raise NotFoundTaskError("No tasks found for this user.")

        return result

    def fetch_task_by_project_task(self, params):
        normalized = TextHelper.normalize(params)
        result = self.task_model.select_task_by_project_task(normalized)
        if not result:
            raise NotFoundTaskError("No tasks found for this projects.")

        return result

    def modify_id_taskstatus(self, state_name, task_title, project_title) -> bool:
        normalized = TextHelper.normalize((state_name, task_title, project_title))

        id_taskstatus = self.task_model.select_by_task_status(normalized[0])

        if not id_taskstatus:
            raise NotFoundTaskStatusError("The task status could not be found.")

        try:
            id_projects = self.project_model.select_by_projects(normalized[2])
            if not id_projects:
                raise NotFoundProjectError("Project not found.")

            params = (id_taskstatus[0], normalized[1], id_projects[0])

            result = self.task_model.update_by_status_task(params)
        except (DatabaseLockedError, ModelsError) as e:
            self.log_error.critical(f"Error: {e}")
            raise e

        if not result:
            raise NotFoundTaskError("Task not found.")

        self.log.info(f"User {Session.get_id()} updated state task of the {task_title}")
        return result
