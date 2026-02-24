from src.core.exceptions import (
    DatabaseLockedError,
    ModelsError,
    NotFoundProjectError,
    NotFoundStatusProjectError,
    NotFoundTaskError,
    NotFoundTaskStatusError,
    StatusExistsError,
)
from src.core.logging import get_logger
from src.models.sessions import Session
from utils.helpers import TextHelper
from utils.validators import validation_match_status


class TaskServices:
    """
    Class to manage task services.
    """

    def __init__(self, task_model, project_model):
        self.t_model = task_model
        self.p_model = project_model
        self.log_audit = get_logger("audit", self.__class__.__name__)
        self.log_error = get_logger("error", self.__class__.__name__)

    # fetch
    def fetch_all_status(self):
        """
        Fetches all task statuses.

        Returns:
            list[tuple]: List of task statuses.

        Raises:
            NotFoundStatusProjectError: If no task statuses are found.
        """
        result = self.t_model.select_all_status()
        if not result:
            raise NotFoundStatusProjectError("No hay estados definidos")

        return result

    def fetch_tasks_of_user(self, id) -> list[tuple]:
        """
        Fetches all tasks of a user.

        Args:
            id (int): User id.

        Returns:
            list[tuple]: List of tasks.
        """
        result = self.t_model.select_all_tasks_of_user(id)
        if not result:
            raise NotFoundTaskError("No tasks found for this user.")

        return result

    def fetch_task_by_project_task(self, params):
        """
        Fetches a task by project and task title.

        Args:
            params (tuple): Tuple of (project_title, task_title).

        Returns:
            tuple: Tuple of (task_title, task_description, task_status, project_title).

        Raises:
            NotFoundTaskError: If no task is found.
        """
        normalized = TextHelper.normalize(params)
        result = self.t_model.select_task_by_project_task(normalized)
        if not result:
            raise NotFoundTaskError("No tasks found for this projects.")

        return result

    # create
    def create_task_status(self, params: list[tuple]):
        """
        Creates a new task status.

        Args:
            params (list[tuple]): List of tuples of task status names.

        Raises:
            StatusExistsError: If task statuses already exist.
            ModelsError: If there is a technical error in the data server.
        """
        try:
            result_status = self.t_model.select_all_status()
            print(f"[DEBUG] task service {result_status}")
            print()
            normalized = TextHelper.normalize(params)

            if result_status:
                validate_match = validation_match_status(result_status, normalized)

                if validate_match:
                    raise StatusExistsError(f"Estados ya existen {validate_match}")

            new_params = [(x,) for x in normalized]
            self.t_model.insert_task_status(new_params, is_many=True)
        except DatabaseLockedError as e:
            self.log_error(f"Error: {e}")
            raise ModelsError("Technical error in the data server. Contact support.")
        else:
            self.log_audit.info("Estados creados con exito")

    def create_default_status(self):
        """
        Creates default task statuses.

        Raises:
            ModelsError: If there is a technical error in the data server.
        """
        params = [
            ("pendiente"),
            ("progreso"),
            ("revision"),
            ("completada"),
            ("bloqueada"),
        ]
        try:
            self.t_model.insert_task_status(params, is_many=True)
        except DatabaseLockedError as e:
            self.log_error(f"Error: {e}")
            raise ModelsError("Technical error in the data server. Contact support.")
        else:
            self.log_audit.info("Estados creados con exito")

    # modify
    def modify_id_taskstatus(self, state_name, task_title, project_title) -> bool:
        """
        Modifies the status of a task.

        Args:
            state_name (str): New task status name.
            task_title (str): Task title.
            project_title (str): Project title.

        Raises:
            NotFoundTaskStatusError: If the task status could not be found.
            NotFoundProjectError: If the project could not be found.
            ModelsError: If there is a technical error in the data server.
        """
        normalized = TextHelper.normalize((state_name, task_title, project_title))

        id_taskstatus = self.t_model.select_by_task_status(normalized[0])

        if not id_taskstatus:
            raise NotFoundTaskStatusError("The task status could not be found.")

        try:
            id_projects = self.p_model.select_by_projects(normalized[2])
            if not id_projects:
                raise NotFoundProjectError("Project not found.")

            params = (id_taskstatus[0], normalized[1], id_projects[0])

            self.t_model.update_by_status_task(params)
        except DatabaseLockedError as e:
            self.log_error.critical(f"Error: {e}")
            raise ModelsError("Technical error in the data server. Contact support.")

        self.log_audit.info(
            f"User {Session.get_id()} updated state task of the {task_title}"
        )

    def modify_status(self, status, id):
        """
        Modifies the status of a task.

        Args:
            status (str): New task status name.
            id (int): Task id.

        Raises:
            ModelsError: If there is a technical error in the data server.
        """
        normalized = TextHelper.normalize(status)
        try:
            params = (normalized, id)
            self.t_model.update_status(params)
        except DatabaseLockedError as e:
            self.log_error.critical(f"Error: {e}")
            raise ModelsError("Technical error in the data server. Contact support.")
        else:
            self.log_audit.info(f"Estado {id} modificado con exito")

    # remove
    def remove_status(self, id):
        """
        Removes a task status.

        Args:
            id (int): Task status id.

        Raises:
            ModelsError: If there is a technical error in the data server.
        """
        try:
            self.t_model.delete_status(id)
        except DatabaseLockedError as e:
            self.log_error.critical(f"Error: {e}")
            raise ModelsError("Technical error in the data server. Contact support.")
        else:
            self.log_audit(f"Estado {id} eliminado con exito")
