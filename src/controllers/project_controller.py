from src.core.exceptions import DataEmptyError
from src.core.logging import get_logger
from utils.validators import validation_data_empty


class ProjectController:
    """
    Class to manage project controller.
    """
    def __init__(self, service):
        self.p_service = service
        self.log = get_logger("audit", self.__class__.__name__)

    # add
    def add_project(self, params):
        """
        Adds a new project.

        Args:
            params (tuple): Tuple of project parameters.
            example: (title, description)
        """
        if not validation_data_empty(params[0]):
            raise DataEmptyError("Project title required")

        self.p_service.create_project(params)

    def add_project_status(self, params: tuple | list[tuple]):
        """
        Adds a new project status.

        Args:
            params (tuple | list[tuple]): Tuple or list of tuples of project statuses.
            example: (name,) or [(name: str, key: int,), (name, key,)]
        """
        if not validation_data_empty(params):
            raise DataEmptyError("Se require estados del proyecto")

        self.p_service.create_projects_status(params)

    def add_default_status(self):
        """
        Adds default project status.
        """
        self.p_service.create_default_status()

    # get
    def get_all_project(self) -> list[tuple]:
        """
        Gets all projects.

        Returns:
            list[tuple]: List of tuples of projects.
        """
        return self.p_service.fetch_all_project()

    def get_all_status(self) -> list[tuple]:
        """
        Gets all project statuses.

        Returns:
            list[tuple]: List of tuples of project statuses.
        """
        return self.p_service.fetch_all_status()

    def get_by_project(self, title: str) -> tuple:
        """
        Gets a project by title.

        Args:
            title (str): Project title.

        Returns:
            tuple: Tuple of the project.
        """
        if not validation_data_empty(title):
            raise DataEmptyError("Se require el titulo del proyecto")

        return self.p_service.fetch_by_project(title)

    # edit
    def edit_title_project(self, params: tuple):
        """
        Edits a project.

        Args:
            params (tuple): Tuple of project parameters.
            example: (title, id)
        """
        if not validation_data_empty(params[0]):
            raise DataEmptyError("The new project title is required")

        self.p_service.modify_title_project(params)
    
    def edit_project_status_by_project(self, params: tuple):
        """
        Edits a project status by project.

        Args:
            params (tuple): Tuple of project status parameters.
            example: (id_new_status, id_project)
        """
        if not validation_data_empty(params):
            raise DataEmptyError("The new project status is required")

        self.p_service.modify_project_status_by_project(params)

    def edit_project_status(self, params: tuple):
        """
        Edits a project status.

        Args:
            params (tuple): Tuple of project status parameters.
            example: (id, status)
        """
        id, status = params
        if not validation_data_empty(status):
            raise DataEmptyError("Se requiere el nuevo nombre de estado del proyecto")

        self.p_service.modify_project_status((status, id))

    # delete
    def delete_project(self, id: int):
        """
        Deletes a project.

        Args:
            id (int): Project id.
        """
        if not validation_data_empty(id):
            raise DataEmptyError("Se require el id del proyecto")

        self.p_service.remove_project(id)

    def delete_project_status(self, id: int):
        """
        Deletes a project status.

        Args:
            id (int): Project status id.
        """
        if not validation_data_empty(id):
            raise DataEmptyError("Se require el id del estado")

        self.p_service.remove_project_status(id)


class StatusProjectsController:
    pass
