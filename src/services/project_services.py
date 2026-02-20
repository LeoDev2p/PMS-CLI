from src.core.exceptions import (
    DatabaseLockedError,
    ModelsError,
    NotFoundProjectError,
    NotFoundStatusProjectError,
    ProjectsExistsError,
)
from src.core.logging import get_logger
from src.models.sessions import Session
from utils.helpers import TextHelper


class ProjectServices:
    def __init__(self, model):
        self.project_model = model
        self.log = get_logger("audit", self.__class__.__name__)

    def create_project(self, params):
        self.id_admin = Session.get_id()
        # params = title, description
        normalize = TextHelper.normalize(params)
        if self.project_model.select_by_project(normalize[0]):
            raise ProjectsExistsError(
                f"El proyecto '{normalize[0]}' ya está registrado."
            )

        params = (normalize[0], normalize[1], self.id_admin)
        self.project_model.insert_project(params)

        self.log.info(f"Proyecto {params[0]} creado con exito")

    def fetch_all_project(self) -> list[tuple]:
        result = self.project_model.select_all_project()
        if not result:
            raise NotFoundProjectError("No proyectos registrados")

        return result

    def fetch_all_status(self) -> list[tuple]:
        result = self.project_model.select_all_status()
        if not result:
            raise NotFoundStatusProjectError("No hay estados definidos")

    def fetch_by_project(self, title) -> tuple:
        normalized = TextHelper.normalize(title)
        result = self.project_model.select_by_project(normalized)
        if not result:
            raise NotFoundProjectError(f"No existe {title}")

        return result

    def modify_project(self, params):
        title, id = params
        normalized = TextHelper.normalize(title)
        try:
            self.project_model.update_project((normalized, id))
            self.log.info(
                f"Admin {Session.get_id()}: Proyecto {title} actualizado con exito"
            )
        except (DatabaseLockedError, ModelsError) as e:
            self.log_error.critical(f"Error: {e}")
            raise e

    def remove_project(self, id):
        try:
            self.project_model.delete_project(id)
            self.log.info(f"Admin {Session.get_id()}: elimino proyecto {id}")
        except (DatabaseLockedError, ModelsError) as e:
            self.log_error.critical(f"Error: {e}")
            raise e


class StatusProjectsService:
    pass
