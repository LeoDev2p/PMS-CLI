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
    """
    Controller for task management.
    """
    def __init__(self, service):
        self.t_service = service
        self.log = get_logger("audit", self.__class__.__name__)

    # get
    def get_all_status(self):
        """
        Gets all task statuses.

        Returns:
            list[tuple]: List of task statuses.
        """
        return self.t_service.fetch_all_status()

    def get_all_tasks_of_user(self, id) -> bool:
        """
        Gets all tasks of a user.

        Args:
            id (int): User id.

        Returns:
            list[tuple]: List of tasks.
        """
        return self.t_service.fetch_tasks_of_user(id)

    def get_task_by_project_task(self, params):
        """
        Gets a task by project and task title.

        Args:
            params (tuple): Tuple of (project_title, task_title).

        Returns:
            tuple: Tuple of (task_title, task_description, task_status, project_title).
        """
        validate = validation_data_empty(params)
        if not validate:
            raise DataEmptyError("All fields are required")

        return self.t_service.fetch_task_by_project_task(params)
    
    def get_task_by_title(self, id_project):
        """
        Gets a task by title.

        Args:
            id_project (int): project_id.

        Returns:
            tuple: Tuple of (t.id, t.title, ts.name, p.title, u.username).
        """
        validate = validation_data_empty(id_project)
        if not validate:
            raise DataEmptyError("All fields are required")

        return self.t_service.fetch_task_by_title(id_project)

    # add
    def add_task(self, params):
        """
        Adds a new task.

        Args:
            params (tuple): Tuple of (title, description, id_projects, id_assigned_to).
        """
        params_list = list(params)
        params_list.pop(1)
        validate = validation_data_empty(params_list)
        if not validate:
            raise DataEmptyError("All fields are required")

        params_list.insert(1, None)
        self.t_service.create_task(tuple(params_list))

    def add_task_status(self, params: tuple | list[tuple]):
        """
        Adds a new task status.

        Args:
            params (tuple | list[tuple]): Tuple or list of tuples of task status names.
        """
        if not validation_data_empty(params):
            raise DataEmptyError("Se require estados del proyecto")

        self.t_service.create_task_status(params)

    def add_deafult_status(self):
        """
        Adds default task statuses.
        """
        self.t_service.create_default_status()

    # edit
    def edit_task_state(self, id_status, task_id, project_id):
        """
        Edits the status of a task.

        Args:
            id_status (int): New task status id.
            task_id (int): Task id.
            project_id (int): Project id.
        """
        validate = validation_data_empty((id_status, task_id, project_id))
        if not validate:
            raise DataEmptyError("All fields are required")

        try:
            result = self.t_service.modify_id_taskstatus(
                id_status, task_id, project_id
            )

            return result
        except (NotFoundTaskError, NotFoundTaskStatusError, NotFoundProjectError) as e:
            self.log.info(
                f"User {Session.get_id()} attempted update task {task_id} in project {project_id} but failed"
            )
            raise e

    def edit_status(self, params):
        """
        Edits the status of a task status.

        Args:
            params (tuple): Tuple of (task_status_id, task_status_name).
        """
        id, status = params
        if not validation_data_empty(status):
            raise DataEmptyError("Se requiere el nuevo nombre de estado del proyecto")

        self.t_service.modify_status(status, id)

    # delete

    def delete_status(self, id):
        """
        Deletes a task status.

        Args:
            id (int): Task status id.

        Raises:
            DataEmptyError: If the task status id is empty.
        """
        if not validation_data_empty(id):
            raise DataEmptyError("Se require el id del estado")

        self.t_service.remove_status(id)
