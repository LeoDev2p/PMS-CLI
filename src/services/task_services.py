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
    
    def fetch_task_by_title(self, id_project):
        """
        Fetches a task by title.

        Args:
            id_project (int): Project id.

        Returns:
            tuple: Tuple of (t.id, t.title, ts.name, p.title, u.username).

        Raises:
            NotFoundTaskError: If no task is found.
        """
        result = self.t_model.select_by_task_title(id_project)
        if not result:
            raise NotFoundTaskError("No tasks found for this projects.")

        return result

    # create
    def create_task(self, params):
        """
        Creates a new task.

        Args:
            params (tuple): Tuple of (title, description, id_projects, id_assigned_to).
        """
        normalized = TextHelper.normalize(params)
        try:
            self.t_model.insert_task(normalized)
        except DatabaseLockedError as e:
            self.log_error(f"Error: {e}")
            raise ModelsError("Technical error in the data server. Contact support.")
        else:
            self.log_audit.info("Task created successfully")

    def create_task_status(self, params: list[tuple]):
        """
        Creates a new task status.

        Args:
            params (list[tuple]): List of tuples of task status names.
            example: [("name", "system_key: int")]

        Raises:
            StatusExistsError: If task statuses already exist.
            ModelsError: If there is a technical error in the data server.
        """
        try:
            result_status = self.t_model.select_all_status()
            normalized = TextHelper.normalize(params)

            existing_names = {state[1] for state in result_status}
            new_names = {state[0] for state in normalized}

            duplicates = new_names.intersection(existing_names)

            if duplicates:
                raise StatusExistsError(f"States already exist {duplicates}")

            system_key = {
                1: "PENDING",
                2: "IN_PROGRESS",
                3: "REVIEW",
                4: "COMPLETED",
                5: "BLOCKED",
            }

            new_params = []
            for status, key in normalized:
                new_params.append((status, system_key[key], 1))

            self.t_model.insert_task_status(new_params, is_many=True)
        except (DatabaseLockedError, ModelsError) as e:
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
            ("pendiente", "PENDING", 1),
            ("progreso", "IN_PROGRESS", 1),
            ("revision", "REVIEW", 1),
            ("completada", "COMPLETED", 1),
            ("bloqueada", "BLOCKED", 1),
        ]
        try:
            self.t_model.insert_task_status(params, is_many=True)
        except DatabaseLockedError as e:
            self.log_error(f"Error: {e}")
            raise ModelsError("Technical error in the data server. Contact support.")
        else:
            self.log_audit.info("Estados creados con exito")

    # modify
    def modify_id_taskstatus(self, id_status, task_id, project_id) -> bool:
        """
        Modifies the status of a task.

        Args:
            id_status (int): New task status id.
            task_title (str): Task title.
            project_title (str): Project title.

        Raises:
            NotFoundTaskStatusError: If the task status could not be found.
            NotFoundProjectError: If the project could not be found.
            ModelsError: If there is a technical error in the data server.
        """

        try:
            params = (id_status, task_id, project_id)

            self.t_model.update_by_status_task(params)
        except DatabaseLockedError as e:
            self.log_error.critical(f"Error: {e}")
            raise ModelsError("Technical error in the data server. Contact support.")

        self.log_audit.info(
            f"User {Session.get_id()} updated state task of the {task_id}"
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
            self.log_audit.info(f"Estado {id} eliminado con exito")
