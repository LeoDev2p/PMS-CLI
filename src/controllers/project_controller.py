from src.core.exceptions import DataEmptyError
from src.core.logging import get_logger
from utils.validators import validation_data_empty


class ProjectController:
    """Controller for project operations."""

    def __init__(self, service):
        self.service = service
        self.log = get_logger("audit", self.__class__.__name__)

    # ── get ─────────────────────────────────────────────────
    def get_all(self, search: str = None) -> list[dict]:
        """Returns all projects."""
        return self.service.fetch_all(search)

    def get_by_title(self, title: str) -> list[dict]:
        """Returns projects matching title."""
        if not validation_data_empty(title):
            raise DataEmptyError("Project title is required")

        return self.service.fetch_by_title(title)

    def get_search_by_title(self, title: str) -> list[dict]:
        """Returns projects with description matching title."""
        if not validation_data_empty(title):
            raise DataEmptyError("The project title is required")

        return self.service.fetch_search_by_title(title)

    def count_by_title(self, title: str) -> int:
        """Counts projects matching title."""
        if not validation_data_empty(title):
            raise DataEmptyError("The project title is required")

        return self.service.fetch_count_by_title(title)

    def get_new(self) -> list[dict]:
        """Returns all new projects."""
        return self.service.fetch_new()

    def get_new_active(self) -> list[dict]:
        """Returns all new or active projects."""
        return self.service.fetch_new_active()

    # ── add ─────────────────────────────────────────────────
    def add(self, params: tuple):
        """Adds a new project.

        Args:
            params: (title, description)
        """
        if not validation_data_empty(params[0]):
            raise DataEmptyError("Project title required")

        self.service.create(params)

    # ── edit ────────────────────────────────────────────────
    def edit_title(self, params: tuple):
        """Edits a project title.

        Args:
            params: (title, id)
        """
        if not validation_data_empty(params[0]):
            raise DataEmptyError("The new project title is required")

        self.service.modify_title(params)

    def edit_status(self, params: tuple):
        """Edits a project's status.

        Args:
            params: (id_new_status, id_project)
        """
        if not validation_data_empty(params):
            raise DataEmptyError("The new project status is required")

        self.service.modify_status(params)

    # ── delete ──────────────────────────────────────────────
    def delete(self, id: int):
        """Deletes a project."""
        if not validation_data_empty(id):
            raise DataEmptyError("Project ID is required")

        self.service.remove(id)

    # ── stats ──────────────────────────────────────────────
    def get_project_progress(self) -> list[dict]:
        """Returns project progress."""
        return self.service.fetch_project_progress()

    def get_count_users_by_project(self) -> list[dict]:
        """Returns users by project."""
        return self.service.fetch_count_users_by_project()

    def get_critical_projects(self) -> list[dict]:
        """Returns projects that are not assigned to any user."""
        return self.service.fetch_critical_projects()


class ProjectStatusController:
    """Controller for project status operations."""

    def __init__(self, service):
        self.service = service

    # ── get ─────────────────────────────────────────────────
    def get_all(self) -> list[dict]:
        """Returns all project statuses."""
        return self.service.fetch_all()

    # ── add ─────────────────────────────────────────────────
    def add(self, params: tuple | list[tuple]):
        """Adds custom project statuses."""
        if not validation_data_empty(params):
            raise DataEmptyError("Project statuses are required")

        self.service.create(params)

    def add_default(self):
        """Adds the default project statuses."""
        self.service.create_default()

    # ── edit ────────────────────────────────────────────────
    def edit(self, params: tuple):
        """Edits a project status name.

        Args:
            params: (id, status_name)
        """
        id, status = params
        if not validation_data_empty(status):
            raise DataEmptyError("The new project status name is required")

        self.service.modify((status, id))

    # ── delete ──────────────────────────────────────────────
    def delete(self, id: int):
        """Deletes a project status."""
        if not validation_data_empty(id):
            raise DataEmptyError("The project status id is required")

        self.service.remove(id)

    # ── stats ──────────────────────────────────────────────


class UserProjectController:
    """Controller for user-project membership operations."""

    def __init__(self, service):
        self.service = service

    def add(self, params: tuple):
        """Adds a user-project membership.

        Args:
            params: (id_user, id_project)
        """
        if not validation_data_empty(params):
            raise DataEmptyError("User and project data are required")

        self.service.create(params)
