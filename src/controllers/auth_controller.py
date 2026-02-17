from src.core.exceptions import DataEmptyError
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
        self.log = get_logger("audit", "AuthController")

    @validation_email
    @validation_password
    def login(self, params: tuple) -> tuple:
        # email password
        user = self.service.login_user(params)

        return user

    @validation_email
    @validation_password
    def register(self, params: tuple) -> bool:
        #  email, password, username
        if not validation_data_empty(params):
            # Todos los campos son obligatorios
            raise DataEmptyError("All fields are required")

        result = self.service.create_user(params)
        if result:
            self.log.info("User register successfully")

        return result
