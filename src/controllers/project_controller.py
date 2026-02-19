from src.core.exceptions import DataEmptyError
from src.core.logging import get_logger
from utils.validators import validation_data_empty


class ProjectController:
    def __init__(self, service):
        self.project_service = service
        self.log = get_logger("audit", self.__class__.__name__)

    def add_project(self, params):
        # params = title, description
        if not validation_data_empty(params[0]):
            raise DataEmptyError("se require titulo del proyecto")

        self.project_service.create_project(params)

    def get_all_project(self) -> list[tuple]:
        return self.project_service.fetch_all_project()

    def get_all_status(self) -> list[tuple]:
        return self.project_service.fetch_all_status()

    def get_by_project(self, title):
        if not validation_data_empty(title):
            raise DataEmptyError("Se require el titulo del proyecto")

        return self.project_service.fetch_by_project(title)

    def edit_project(self, params):
        if not validation_data_empty(params[0]):
            raise DataEmptyError("Se require el nuevo titulo del proyecto")

        self.project_service.modify_project(params)

    def delete_project(self, id):
        if not validation_data_empty(id):
            raise DataEmptyError("Se require el id del proyecto")

        self.project_service.remove_project(id)


class StatusProjectsController:
    pass
