from src.core.exceptions import (
    DatabaseLockedError,
    DatabaseSystemError,
    ModelsError,
    NotFoundProjectError,
    NotFoundStatusProjectError,
    ProjectsExistsError,
    StatusExistsError,
)
from src.core.logging import get_logger
from src.models.sessions import Session
from utils.helpers import TextHelper


class ProjectServices:
    """Business logic for projects."""

    def __init__(self, project_model, status_model):
        self.model = project_model
        self.status_model = status_model
        self.log_audit = get_logger("audit", self.__class__.__name__)
        self.log_error = get_logger("error", self.__class__.__name__)

    # ── fetch ───────────────────────────────────────────────
    def fetch_all(self, search: str = None) -> list[dict]:
        """Returns all projects as list of dicts.

        Keys: id, title, status
        """
        try:
            result = self.model.get_all(search)
        except DatabaseSystemError as e:
            self.log_error.critical(f"Error: {e}")
            raise ModelsError("Technical error in the data server. Contact support.")

        if not result:
            raise NotFoundProjectError("No proyectos registrados")

        return [{"id": r[0], "title": r[1], "status": r[2]} for r in result]

    def fetch_by_title(self, title: str) -> list[dict]:
        """Returns projects matching title.

        Keys: id, title
        """
        normalized = TextHelper.normalize(title)
        try:
            result = self.model.get_by_title(normalized)
        except DatabaseSystemError as e:
            self.log_error.critical(f"Error: {e}")
            raise ModelsError("Technical error in the data server. Contact support.")

        if not result:
            raise NotFoundProjectError(f"No existe {title}")

        return [{"id": r[0], "title": r[1]} for r in result]

    def fetch_search_by_title(self, title: str) -> list[dict]:
        """Returns projects with description matching title, limit 10.

        Keys: id, title, description
        """
        normalized = TextHelper.normalize(title)
        try:
            result = self.model.search_by_title(normalized)
        except DatabaseSystemError as e:
            self.log_error.critical(f"Error: {e}")
            raise ModelsError("Technical error in the data server. Contact support.")

        if not result:
            raise NotFoundProjectError(f"Not exists {title}")

        return [{"id": r[0], "title": r[1], "description": r[2]} for r in result]

    def fetch_count_by_title(self, title: str) -> int:
        """Returns count of projects matching title."""
        normalized = TextHelper.normalize(title)
        try:
            result = self.model.count_by_title(normalized)
        except DatabaseSystemError as e:
            self.log_error.critical(f"Error: {e}")
            raise ModelsError("Technical error in the data server. Contact support.")

        return result[0] if result else 0

    def fetch_new(self) -> list[dict]:
        """Returns all projects with NEW status.

        Keys: id, title, system_key
        """
        try:
            result = self.model.get_new()
        except DatabaseSystemError as e:
            self.log_error.critical(f"Error: {e}")
            raise ModelsError("Technical error in the data server. Contact support.")

        if not result:
            raise NotFoundProjectError("There are no new projects")

        return [{"id": r[0], "title": r[1], "system_key": r[2]} for r in result]

    def fetch_new_active(self) -> list[dict]:
        """Returns all projects with NEW or ACTIVE status.

        Keys: id, title
        """
        try:
            result = self.model.get_new_active()
        except DatabaseSystemError as e:
            self.log_error.critical(f"Error: {e}")
            raise ModelsError("Technical error in the data server. Contact support.")

        if not result:
            raise NotFoundProjectError("No project available")

        return [{"id": r[0], "title": r[1]} for r in result]

    # ── create ──────────────────────────────────────────────
    def create(self, params: tuple):
        """Creates a new project.

        Args:
            params: (title, description)
        """
        id_admin = Session.get_id()
        normalize = TextHelper.normalize(params)
        try:
            if self.model.get_by_title(normalize[0]):
                raise ProjectsExistsError(f"The project '{normalize[0]}' is already registered.")

            status = self.status_model.get_all()
            if not status:
                self._create_default_status()

            id_status_default = self.status_model.get_default_id()
        except DatabaseSystemError as e:
            self.log_error.critical(f"Error: {e}")
            raise ModelsError("Technical error in the data server. Contact support.")

        full_params = (
            normalize[0],
            normalize[1] if normalize[1] else None,
            id_admin,
            id_status_default[0],
        )

        try:
            self.model.create(full_params)
        except (DatabaseLockedError, DatabaseSystemError) as e:
            self.log_error.error(f"Error: {e}")
            raise ModelsError("Technical error in the data server. Contact support.")

        self.log_audit.info(f"Project {params[0]} created successfully")

    def _create_default_status(self):
        """Internal: creates default project statuses when none exist."""
        params = [
            ("new", "NEW", 1),
            ("active", "ACTIVE", 1),
            ("paused", "ON_HOLD", 1),
            ("finalized", "FINALIZED", 1),
            ("cancelled", "CANCELLED", 1),
        ]
        try:
            self.status_model.create(params, is_many=True)
        except (DatabaseLockedError, DatabaseSystemError) as e:
            self.log_error.error(f"Error: {e}")
            raise ModelsError("Technical error in the data server. Contact support.")
        else:
            self.log_audit.info("Default project statuses created successfully")

    # ── modify ──────────────────────────────────────────────
    def modify_title(self, params: tuple):
        """Updates a project title.

        Args:
            params: (title, id)
        """
        title, id = params
        normalized = TextHelper.normalize(title)
        try:
            self.model.update_title((normalized, id))
        except (DatabaseLockedError, DatabaseSystemError) as e:
            self.log_error.critical(f"Error: {e}")
            raise ModelsError("Technical error in the data server. Contact support.")
        else:
            self.log_audit.info(f"Title of project {title} updated successfully")

    def modify_status(self, params: tuple):
        """Updates a project's status.

        Args:
            params: (id_new_status, id_project)
        """
        try:
            self.model.update_status(params)
        except (DatabaseLockedError, DatabaseSystemError) as e:
            self.log_error.critical(f"Error: {e}")
            raise ModelsError("Technical error in the data server. Contact support.")
        else:
            self.log_audit.info(f"Status of project {params[1]} updated successfully")

    # ── remove ──────────────────────────────────────────────
    def remove(self, id: int):
        """Deletes a project."""
        try:
            self.model.delete(id)
        except (DatabaseLockedError, DatabaseSystemError) as e:
            self.log_error.critical(f"Error: {e}")
            raise ModelsError("Technical error in the data server. Contact support.")
        else:
            self.log_audit.info(f"Project {id} deleted successfully")

    # ── stats ──────────────────────────────────────────────
    def fetch_project_progress(self) -> list[dict]:
        """Returns project progress."""
        try:
            result = self.model.project_progress()
        except DatabaseSystemError as e:
            self.log_error.critical(f"Error: {e}")
            raise ModelsError("Technical error in the data server. Contact support.")
        else:
            if not result:
                raise NotFoundProjectError("No projects available")

        return [
            {
                "project": r[0],
                "completed": r[1],
                "total_tasks": r[2],
                "advance": r[3],
            }
            for r in result
        ]

    def fetch_count_users_by_project(self) -> list[dict]:
        """Returns users by project."""
        try:
            result = self.model.count_users_by_project()
        except DatabaseSystemError as e:
            self.log_error.critical(f"Error: {e}")
            raise ModelsError("Technical error in the data server. Contact support.")

        else:
            if not result:
                raise NotFoundProjectError("No projects available")

        return [
            {
                "project": r[0],
                "count_users": r[1],
            }
            for r in result
        ]


class ProjectStatusServices:
    """Business logic for project statuses."""

    def __init__(self, status_model):
        self.model = status_model
        self.log_audit = get_logger("audit", self.__class__.__name__)
        self.log_error = get_logger("error", self.__class__.__name__)

    # ── fetch ───────────────────────────────────────────────
    def fetch_all(self) -> list[dict]:
        """Returns all project statuses as list of dicts.

        Keys: id, name, system_key, is_active
        """
        try:
            result = self.model.get_all()
        except DatabaseSystemError as e:
            self.log_error.critical(f"Error: {e}")
            raise ModelsError("Technical error in the data server. Contact support.")
        else:
            if not result:
                raise NotFoundStatusProjectError("No hay estados definidos")

        return [
            {
                "id": r[0],
                "name": r[1],
                "system_key": r[2],
                "is_active": r[3],
            }
            for r in result
        ]

    # ── create ──────────────────────────────────────────────
    def create(self, params: list[tuple]):
        """Creates custom project statuses.

        Args:
            params: [(name, key_number), ...]
        """
        try:
            result_status = self.model.get_all()
        except DatabaseSystemError as e:
            self.log_error.critical(f"Error: {e}")
            raise ModelsError("Technical error in the data server. Contact support.")
        else:
            if not result_status:
                raise NotFoundStatusProjectError("There are no defined states")

            normalized = TextHelper.normalize(params)

            existing_names = {state[1] for state in result_status}
            new_names = {state[0] for state in normalized}

            duplicates = new_names.intersection(existing_names)
            if duplicates:
                raise StatusExistsError(f"States already exist {duplicates}")

            system_key = {
                1: "NEW",
                2: "ACTIVE",
                3: "ON_HOLD",
                4: "FINALIZED",
                5: "CANCELLED",
            }

            new_params = []
            for status, key in normalized:
                new_params.append((status, system_key[key], 1))
        try:
            self.model.create(new_params, is_many=True)
        except (DatabaseLockedError, DatabaseSystemError) as e:
            self.log_error.critical(f"Error: {e}")
            raise ModelsError("Technical error in the data server. Contact support.")
        else:
            self.log_audit.info("Project statuses created successfully")

    def create_default(self):
        """Creates the default set of project statuses."""
        params = [
            ("new", "NEW", 1),
            ("active", "ACTIVE", 1),
            ("paused", "ON_HOLD", 1),
            ("finalized", "FINALIZED", 1),
            ("cancelled", "CANCELLED", 1),
        ]
        try:
            self.model.create(params, is_many=True)
        except (DatabaseLockedError, DatabaseSystemError) as e:
            self.log_error.error(f"Error: {e}")
            raise ModelsError("Technical error in the data server. Contact support.")
        else:
            self.log_audit.info("Default project statuses created successfully")

    # ── modify ──────────────────────────────────────────────
    def modify(self, params: tuple):
        """Updates a project status name.

        Args:
            params: (name, id)
        """
        name, id = params
        normalized = TextHelper.normalize(name)
        try:
            self.model.update((normalized, id))
        except (DatabaseLockedError, DatabaseSystemError) as e:
            self.log_error.critical(f"Error: {e}")
            raise ModelsError("Technical error in the data server. Contact support.")

    # ── remove ──────────────────────────────────────────────
    def remove(self, id: int):
        """Deletes a project status."""
        try:
            self.model.delete(id)
        except (DatabaseLockedError, DatabaseSystemError) as e:
            self.log_error.critical(f"Error: {e}")
            raise ModelsError("Technical error in the data server. Contact support.")


class UserProjectServices:
    """Business logic for user-project memberships."""

    def __init__(self, user_project_model):
        self.model = user_project_model
        self.log_audit = get_logger("audit", self.__class__.__name__)
        self.log_error = get_logger("error", self.__class__.__name__)

    def create(self, params: tuple):
        """Adds a user-project membership.

        Args:
            params: (id_user, id_project)
        """
        try:
            self.model.create_many([params])
        except (DatabaseLockedError, DatabaseSystemError) as e:
            self.log_error.error(f"Error: {e}")
            raise ModelsError("Technical error in the data server. Contact support.")
        else:
            self.log_audit.info(f"User {params[0]} linked to project {params[1]} successfully")
