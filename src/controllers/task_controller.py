from src.core.exceptions import (
    DataEmptyError,
)
from src.core.logging import get_logger
from utils.validators import validation_data_empty


class TaskController:
    """Controller for task operations."""

    def __init__(self, service):
        self.service = service
        self.log = get_logger("audit", self.__class__.__name__)

    # ── get ─────────────────────────────────────────────────
    def get_by_user(self) -> list[dict]:
        """Returns all tasks assigned to a user."""
        return self.service.fetch_by_user()

    def get_by_project_and_title(self, params: tuple) -> dict:
        """Returns a task by project title and task title."""
        if not validation_data_empty(params):
            raise DataEmptyError("All fields are required")

        return self.service.fetch_by_project_and_title(params)

    def get_details_by_project(self, id_project: int) -> list[dict]:
        """Returns task details for a project."""
        if not validation_data_empty(id_project):
            raise DataEmptyError("All fields are required")

        return self.service.fetch_details_by_project(id_project)

    def get_all_by_project(self, id_project: int) -> list[dict]:
        """Returns all tasks of a project with assignment info."""
        if not validation_data_empty(id_project):
            raise DataEmptyError("All fields are required")

        return self.service.fetch_all_by_project(id_project)

    # ── add ─────────────────────────────────────────────────
    def add(self, params: tuple):
        """Adds a new task.

        Args:
            params: (title, description, id_projects, id_assigned_to)
        """
        params_list = list(params)
        if params_list[1] == "" or params_list[1].isspace():
            params_list.pop(1)

        if not validation_data_empty(params_list):
            raise DataEmptyError("All fields are required")

        if len(params_list) == 3:
            params_list.insert(1, None)
        self.service.create(tuple(params_list))

    # ── edit ────────────────────────────────────────────────
    def edit_status(self, id_status: int, task_id: int, project_id: int):
        """Edits the status of a task."""
        if not validation_data_empty((id_status, task_id, project_id)):
            raise DataEmptyError("All fields are required")

        self.service.modify_status(id_status, task_id, project_id)

    def edit_assigned_user(self, params: tuple):
        """Reassigns a user on a task."""
        if not validation_data_empty(params):
            raise DataEmptyError("All fields are required")

        self.service.modify_assigned_user(params)

    def reassign_user_project(self, params: tuple):
        """Reassigns a user from one project to another."""
        if not validation_data_empty(params):
            raise DataEmptyError("All fields are required")

        # Ensure project source and destination are different
        _, id_project_source, id_project_dest = params
        if id_project_source == id_project_dest:
            raise DataEmptyError("Source and destination project cannot be the same")

        self.service.reassign_user_project(params)

    # -- delete ----------------------------------------------
    def delete_user_project(self, params: tuple):
        """Delete a user from one project."""
        if not validation_data_empty(params):
            raise DataEmptyError("All fields are required")

        self.service.remove_user_project(params)

    # -- stats ----------------------------------------------
    def get_completion_efficiency(self) -> list[dict]:
        """Completion Efficiency: Tasks completed per week/month."""
        return self.service.fetch_completion_efficiency()
    
    def get_orphan_task_alerts(self) -> list[dict]:
        """Returns tasks that are not assigned to any user."""
        return self.service.fetch_orphan_task_alerts()


class TaskStatusController:
    """Controller for task status operations."""

    def __init__(self, service):
        self.service = service

    # ── get ─────────────────────────────────────────────────
    def get_all(self) -> list[dict]:
        """Returns all task statuses."""
        return self.service.fetch_all()

    # ── add ─────────────────────────────────────────────────
    def add(self, params: tuple | list[tuple]):
        """Adds custom task statuses."""
        if not validation_data_empty(params):
            raise DataEmptyError("Se require estados del proyecto")

        self.service.create(params)

    def add_default(self):
        """Adds the default task statuses."""
        self.service.create_default()

    # ── edit ────────────────────────────────────────────────
    def edit(self, params: tuple):
        """Edits a task status name.

        Args:
            params: (id, status_name)
        """
        id, status = params
        if not validation_data_empty(status):
            raise DataEmptyError("Se requiere el nuevo nombre de estado del proyecto")

        self.service.modify(status, id)

    # ── delete ──────────────────────────────────────────────
    def delete(self, id: int):
        """Deletes a task status."""
        if not validation_data_empty(id):
            raise DataEmptyError("Se require el id del estado")

        self.service.remove(id)

    # ── stats ──────────────────────────────────────────────
    def get_state_distribution(self) -> list[dict]:
        """State Distribution: How many tasks are in each global state."""
        return self.service.fetch_state_distribution()

    def get_blocking_rate(self) -> list[dict]:
        """Blocking Rate: Number of tasks paused or blocked."""
        return self.service.fetch_blocking_rate()
