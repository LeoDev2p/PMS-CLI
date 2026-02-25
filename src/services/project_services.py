from src.core.exceptions import (
    DatabaseLockedError,
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
    """
    Class to manage project services.
    """

    def __init__(self, model):
        self.p_model = model
        self.log_audit = get_logger("audit", self.__class__.__name__)
        self.log_error = get_logger("error", self.__class__.__name__)

    # create
    def create_project(self, params: tuple):
        """
        Creates a new project.

        Args:
            params (tuple): Tuple of project parameters.
            example: (title, description)
        """

        self.id_admin = Session.get_id()
        normalize = TextHelper.normalize(params)
        if self.p_model.select_by_project(normalize[0]):
            raise ProjectsExistsError(
                f"The project '{normalize[0]}' is already registered."
            )

        status = self.p_model.select_all_status()
        if not status:
            self.create_default_status()

        id_status_default = self.p_model.default_min_id_status()
        params = (normalize[0], normalize[1], self.id_admin, id_status_default[0])

        try:
            self.p_model.insert_project(params)
        except (DatabaseLockedError, ModelsError) as e:
            self.log_error.error(f"Error: {e}")
            raise ModelsError("Technical error in the data server. Contact support.")

        self.log_audit.info(f"Proyecto {params[0]} creado con exito")

    def create_projects_status(self, params: list[tuple]):
        """
        Creates new project statuses.

        Args:
            params (list[tuple]): List of tuples of project statuses.
            example: [(name,), (name,)]
        """

        try:
            result_status = self.p_model.select_all_status()
            normalized = TextHelper.normalize(params)

            #
            existing_names = {state[1] for state in result_status}
            new_names = {state[0] for state in normalized}

            duplicates = new_names.intersection(existing_names)

            if duplicates:
                raise StatusExistsError(f"States already exist {duplicates}")

            system_key = {
                1: "active",
                2: "on_hold",
                3: "inactive",
            }

            new_params = [(status, system_key[key], 0) for status, key in normalized]

            self.p_model.insert_projects_status(new_params, is_many=True)
        except DatabaseLockedError as e:
            self.log_error(f"Error: {e}")
            raise ModelsError("Technical error in the data server. Contact support.")
        else:
            self.log_audit.info("Estados creados con exito")

    def create_default_status(self):
        """
        Creates default project statuses.
        """
        params = [
            ("new", "active", 1),
            ("active", "active", 0),
            ("paused", "on_hold", 0),
            ("finalized", "inactive", 0),
            ("cancelled", "inactive", 0),
        ]

        try:
            self.p_model.insert_projects_status(params, is_many=True)
        except DatabaseLockedError as e:
            self.log_error(f"Error: {e}")
            raise ModelsError("Technical error in the data server. Contact support.")
        else:
            self.log_audit.info(f"Estados {params} creado con exito")

    # Fetch
    def fetch_all_project(self) -> list[tuple]:
        """
        Gets all projects.

        Returns:
            list[tuple]: List of tuples of projects.
        """
        result = self.p_model.select_all_project()
        if not result:
            raise NotFoundProjectError("No proyectos registrados")

        return result

    def fetch_all_status(self) -> list[tuple]:
        """
        Gets all project statuses.

        Returns:
            list[tuple]: List of tuples of project statuses.
        """
        result = self.p_model.select_all_status()
        if not result:
            raise NotFoundStatusProjectError("No hay estados definidos")

        return result

    def fetch_by_project(self, title: str) -> tuple:
        """
        Gets a project by title.

        Args:
            title (str): Project title.

        Returns:
            tuple: Tuple of the project.
        """
        normalized = TextHelper.normalize(title)
        result = self.p_model.select_by_project(normalized)
        if not result:
            raise NotFoundProjectError(f"No existe {title}")

        return result

    # Modify
    def modify_title_project(self, params: tuple):
        """
        Edits a project.

        Args:
            params (tuple): Tuple of project parameters.
            example: (title, id)
        """
        title, id = params
        normalized = TextHelper.normalize(title)
        try:
            print (f"[DEBUG] {normalized, id}")
            self.p_model.update_project((normalized, id))
            self.log_audit.info(
                f"Admin {Session.get_id()}: Proyecto {title} actualizado con exito"
            )
        except DatabaseLockedError as e:
            self.log_error.critical(f"Error: {e}")
            raise ModelsError("Technical error in the data server. Contact support.")
    
    def modify_project_status_by_project(self, params: tuple):
        """
        Edits a project status by project.

        Args:
            params (tuple): Tuple of project status parameters.
            example: (id_new_status, id_project)
        """
        try:
            self.p_model.update_project_status_by_project(params)
        except (DatabaseLockedError, ModelsError) as e:
            self.log_error.critical(f"Error: {e}")
            raise ModelsError("Technical error in the data server. Contact support.")

    def modify_project_status(self, params: tuple):
        """
        Edits a project status.

        Args:
            params (tuple): Tuple of project status parameters.
            example: (status, id)
        """
        status, id = params
        normalized = TextHelper.normalize(status)
        try:
            params = (normalized, id)
            self.p_model.update_project_status(params)
        except (DatabaseLockedError, ModelsError) as e:
            self.log_error.critical(f"Error: {e}")
            raise ModelsError("Technical error in the data server. Contact support.")

    # Remove
    def remove_project(self, id: int):
        """
        Deletes a project.

        Args:
            id (int): Project id.
        """
        try:
            self.p_model.delete_project(id)
            self.log_audit.info(f"Admin {Session.get_id()}: elimino proyecto {id}")
        except DatabaseLockedError as e:
            self.log_error.critical(f"Error: {e}")
            raise ModelsError("Technical error in the data server. Contact support.")

    def remove_project_status(self, id: int):
        """
        Deletes a project status.

        Args:
            id (int): Project status id.
        """
        try:
            self.p_model.delete_project_status(id)
        except DatabaseLockedError as e:
            self.log_error.critical(f"Error: {e}")
            raise ModelsError("Technical error in the data server. Contact support.")


class StatusProjectsService:
    pass
