from src.core.exceptions import (
    DatabaseLockedError,
    DatabaseSystemError,
    ModelsError,
    NotFoundTaskError,
    NotFoundTaskStatusError,
    StatusExistsError,
)
from src.core.logging import get_logger
from src.models.sessions import Session
from utils.helpers import TextHelper


class TaskServices:
    """Business logic for tasks."""

    def __init__(self, task_model, user_project_model):
        self.model = task_model
        self.up_model = user_project_model
        self.log_audit = get_logger("audit", self.__class__.__name__)
        self.log_error = get_logger("error", self.__class__.__name__)

    # ── fetch ───────────────────────────────────────────────
    def fetch_by_user(self) -> list[dict]:
        """Returns all tasks assigned to a user as list of dicts.

        Keys: title, description, status, project
        """
        try:
            result = self.model.get_all_by_user(Session.get_id())
        except DatabaseSystemError as e:
            self.log_error.critical(f"Error: {e}")
            raise ModelsError("Technical error in the data server. Contact support.")

        else:
            if not result:
                raise NotFoundTaskError("No tasks found for this user.")

            return [
                {
                    "title": r[0],
                    "description": r[1],
                    "status": r[2],
                    "project": r[3],
                }
                for r in result
            ]

    def fetch_by_project_and_title(self, params: tuple) -> dict:
        """Returns a task matched by project title and task title.

        Keys: title, description, status, project
        """
        normalized = TextHelper.normalize(params)
        try:
            result = self.model.get_by_project_and_title(normalized)
        except DatabaseSystemError as e:
            self.log_error.critical(f"Error: {e}")
            raise ModelsError("Technical error in the data server. Contact support.")
        else:
            if not result:
                raise NotFoundTaskError("No tasks found for this project.")

            return {
                "title": result[0],
                "description": result[1],
                "status": result[2],
                "project": result[3],
            }

    def fetch_details_by_project(self, id_project: int) -> list[dict]:
        """Returns task details for a project.

        Keys: id, title, status, project, assigned_to
        """
        try:
            if Session.get_role() == "admin":
                params = (id_project,)
            else:
                params = (id_project, Session.get_id())

            result = self.model.get_details_by_project(params)
        except DatabaseSystemError as e:
            self.log_error.critical(f"Error: {e}")
            raise ModelsError("Technical error in the data server. Contact support.")
        else:
            if not result:
                raise NotFoundTaskError("No tasks found for this project.")

            return [
                {
                    "id": r[0],
                    "title": r[1],
                    "status": r[2],
                    "project": r[3],
                    "assigned_to": r[4],
                }
                for r in result
            ]

    def fetch_all_by_project(self, id_project: int) -> list[dict]:
        """Returns all tasks of a project with assignment info."""
        try:
            result = self.model.get_all_by_project(id_project)
        except DatabaseSystemError as e:
            self.log_error.critical(f"Error: {e}")
            raise ModelsError("Technical error in the data server. Contact support.")
        else:
            if not result:
                raise NotFoundTaskError("No tasks found for this project.")

            return [
                {
                    "project": r[0],
                    "responsible": r[1],
                    "task_": r[2],
                    "progress": r[3],
                }
                for r in result
            ]

    # ── create ──────────────────────────────────────────────
    def create(self, params: tuple):
        """Creates a new task.

        Args:
            params: (title, description, id_projects, id_assigned_to)
        """
        id_user, id_project = params[3], params[2]
        try:
            is_member = self.up_model.exists(id_user, id_project)
        except DatabaseSystemError as e:
            self.log_error.critical(f"Error: {e}")
            raise ModelsError("Technical error in the data server. Contact support.")
        else:
            if not is_member:
                try:
                    self.up_model.create(id_user, id_project)
                except (DatabaseLockedError, DatabaseSystemError) as e:
                    self.log_error.critical(f"Error: {e}")
                    raise ModelsError("Technical error in the data server. Contact support.")
                else:
                    self.log_audit.info("Project Status added successfully")

        normalized = TextHelper.normalize(params)
        try:
            self.model.create(normalized)
        except (DatabaseLockedError, DatabaseSystemError) as e:
            self.log_error.error(f"Error: {e}")
            raise ModelsError("Technical error in the data server. Contact support.")
        else:
            self.log_audit.info("Task created successfully")

    # ── modify ──────────────────────────────────────────────
    def modify_status(self, id_status: int, task_id: int, project_id: int):
        """Updates the status of a task."""
        try:
            params = (id_status, task_id, project_id)
            self.model.update_status(params)
        except (DatabaseLockedError, DatabaseSystemError) as e:
            self.log_error.critical(f"Error: {e}")
            raise ModelsError("Technical error in the data server. Contact support.")
        else:
            self.log_audit.info(f"User {Session.get_id()} updated state task of the {task_id}")

    def modify_assigned_user(self, params: tuple):
        """Unassigns a user from a task and removes project membership.

        Args:
            params: (id_task, id_user, id_project)
        """
        try:
            self.up_model.delete(params[1:])
            self.model.update_assigned_user((None, params[0]))
        except (DatabaseLockedError, DatabaseSystemError) as e:
            self.log_error.critical(f"Error: {e}")
            raise ModelsError("Technical error in the data server. Contact support.")
        else:
            self.log_audit.info(f"User removed from project {params[2]} and task {params[0]}")

    def reassign_user_project(self, params: tuple):
        """Reassigns a user from one project to another, clearing their tasks in the origin project.

        Args:
            params: (id_user, id_project_source, id_project_dest)
        """
        id_user, id_project_source, id_project_dest = params
        try:
            # 1. Limpieza de Tareas: poner en NULL en project_source
            self.model.unassign_tasks_by_user_project((id_user, id_project_source))
            # 2. Ruptura de Vínculo: eliminar la fila en users_projects del project_source
            self.up_model.delete((id_user, id_project_source))
            # 3. Nuevo Vínculo: insertar en project_dest
            # Solo insertar si el usuario no es ya miembro del proyecto destino
            if not self.up_model.exists(id_user, id_project_dest):
                self.up_model.create(id_user, id_project_dest)
        except (DatabaseLockedError, DatabaseSystemError) as e:
            self.log_error.critical(f"Error: {e}")
            raise ModelsError("Technical error in the data server. Contact support.")
        else:
            self.log_audit.info(f"User {id_user} reassigned from project {id_project_source} to {id_project_dest}")

    # -- remove -------------------------------------------------

    def remove_user_project(self, params: tuple):
        """Remove a user from a project, clearing their tasks in the origin project.

        Args:
            params: (id_user, id_project_source)
        """
        id_user, id_project_source = params
        try:
            # 1. Limpieza de Tareas: poner en NULL en project_source
            self.model.unassign_tasks_by_user_project((id_user, id_project_source))
            # 2. Ruptura de Vínculo: eliminar la fila en users_projects del project_source
            self.up_model.delete((id_user, id_project_source))
        except (DatabaseLockedError, DatabaseSystemError) as e:
            self.log_error.critical(f"Error: {e}")
            raise ModelsError("Technical error in the data server. Contact support.")
        else:
            self.log_audit.info(f"User {id_user} removed from project {id_project_source}")

    # ── stats ──────────────────────────────────────────────
    def fetch_completion_efficiency(self) -> list[dict]:
        """Completion Efficiency: Tasks completed per week/month."""
        try:
            result = self.model.completion_efficiency()
        except DatabaseSystemError as e:
            self.log_error.critical(f"Error: {e}")
            raise ModelsError("Technical error in the data server. Contact support.")
        else:
            if not result:
                raise NotFoundTaskError("No tasks were found.")

            return [{"month": r[0], "total_tasks": r[1]} for r in result]
    
    def fetch_orphan_task_alerts(self) -> list[tuple]:
        """Returns tasks that are not assigned to any user."""
        try:
            result = self.model.orphan_task_alerts()
        except DatabaseSystemError as e:
            self.log_error.critical(f"Error: {e}")
            raise ModelsError("Technical error in the data server. Contact support.")
        else:
            if not result:
                raise NotFoundTaskError("No tasks were found.")

            return [
                {
                    "id": r[0], 
                    "title": r[1], 
                    "status": r[2], 
                    "project": r[3]
                } for r in result]


class TaskStatusServices:
    """Business logic for task statuses."""

    def __init__(self, status_model):
        self.model = status_model
        self.log_audit = get_logger("audit", self.__class__.__name__)
        self.log_error = get_logger("error", self.__class__.__name__)

    # ── fetch ───────────────────────────────────────────────
    def fetch_all(self) -> list[dict]:
        """Returns all task statuses as list of dicts.

        Keys: id, name, system_key, is_active
        """
        from src.core.exceptions import NotFoundStatusProjectError

        try:
            result = self.model.get_all()
        except DatabaseSystemError as e:
            self.log_error.critical(f"Error: {e}")
            raise ModelsError("Technical error in the data server. Contact support.")
        else:
            if not result:
                raise NotFoundStatusProjectError("There are no defined states")

            return [{"id": r[0], "name": r[1], "system_key": r[2], "is_active": r[3]} for r in result]

    # ── create ──────────────────────────────────────────────
    def create(self, params: list[tuple]):
        """Creates custom task statuses.

        Args:
            params: [(name, key_number), ...]
        """
        try:
            result_status = self.model.get_all()
        except DatabaseSystemError as e:
            self.log_error.critical(f"Error: {e}")
            raise ModelsError("Technical error in the data server. Contact support.")

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

        try:
            self.model.create(new_params, is_many=True)
        except (DatabaseLockedError, DatabaseSystemError) as e:
            self.log_error.error(f"Error: {e}")
            raise ModelsError("Technical error in the data server. Contact support.")
        else:
            self.log_audit.info("Task statuses created successfully")

    def create_default(self):
        """Creates the default set of task statuses."""
        params = [
            ("pendiente", "PENDING", 1),
            ("progreso", "IN_PROGRESS", 1),
            ("revision", "REVIEW", 1),
            ("completada", "COMPLETED", 1),
            ("bloqueada", "BLOCKED", 1),
        ]
        try:
            self.model.create(params, is_many=True)
        except (DatabaseLockedError, DatabaseSystemError) as e:
            self.log_error.error(f"Error: {e}")
            raise ModelsError("Technical error in the data server. Contact support.")
        else:
            self.log_audit.info("Default task statuses created successfully")

    # ── modify ──────────────────────────────────────────────
    def modify(self, status: str, id: int):
        """Updates a task status name."""
        normalized = TextHelper.normalize(status)
        try:
            self.model.update((normalized, id))
        except (DatabaseLockedError, DatabaseSystemError) as e:
            self.log_error.critical(f"Error: {e}")
            raise ModelsError("Technical error in the data server. Contact support.")
        else:
            self.log_audit.info(f"Task status {id} modified successfully")

    # ── remove ──────────────────────────────────────────────
    def remove(self, id: int):
        """Deletes a task status."""
        try:
            self.model.delete(id)
        except (DatabaseLockedError, DatabaseSystemError) as e:
            self.log_error.critical(f"Error: {e}")
            raise ModelsError("Technical error in the data server. Contact support.")
        else:
            self.log_audit.info(f"Task status {id} deleted successfully")

    # ── stats ──────────────────────────────────────────────
    def fetch_state_distribution(self) -> list[dict]:
        """State Distribution: How many tasks are in each global state."""
        try:
            result = self.model.state_distribution()
        except DatabaseSystemError as e:
            self.log_error.critical(f"Error: {e}")
            raise ModelsError("Technical error in the data server. Contact support.")
        else:
            if not result:
                raise NotFoundTaskStatusError("No states were found for the tasks.")

            return [{"status": r[0], "system_key": r[1], "total_tasks": r[2]} for r in result]

    def fetch_blocking_rate(self) -> list[dict]:
        """Blocking Rate: Number of tasks paused or blocked."""
        try:
            result = self.model.blocking_rate()
        except DatabaseSystemError as e:
            self.log_error.critical(f"Error: {e}")
            raise ModelsError("Technical error in the data server. Contact support.")
        else:
            if not result:
                raise NotFoundTaskStatusError("No states were found for the tasks.")

            return [{"status": r[0], "total_locked": r[1]} for r in result]
