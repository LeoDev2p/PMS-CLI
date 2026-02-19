from src.core.exceptions import AuthenticactionError, DataEmptyError, EmailError
from src.core.logging import get_logger
from utils.validators import (
    validation_data_empty,
    validation_email,
    validation_password,
)


class AuthController:
    def __init__(self, service):
        # service = AuthService (user_model)
        self.service = service

    @validation_email
    @validation_password
    def login(self, params: tuple) -> tuple:
        self.log = get_logger("security", self.__class__.__name__)
        # email password
        try:
            result = self.service.login_user(params)
            return result
        except AuthenticactionError as e:
            self.log.warning(f"User {params[0]} {str(e)}")
            raise e

    @validation_email
    @validation_password
    def register(self, params: tuple) -> bool:
        self.log = get_logger("audit", self.__class__.__name__)
        #  email, password, username
        if not validation_data_empty(params):
            # Todos los campos son obligatorios
            raise DataEmptyError("All fields are required")

        try:
            return self.service.create_user(params)
        except EmailError as e:
            self.log.warning(str(e))
            raise e
