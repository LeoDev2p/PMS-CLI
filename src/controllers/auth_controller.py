from src.core.exceptions import AuthenticactionError, DataEmptyError, EmailError
from src.core.logging import get_logger
from utils.validators import (
    validation_data_empty,
    validation_email,
    validation_password,
)


class AuthController:
    """
    Handles user authentication.
    """

    def __init__(self, service):
        # service = AuthService (user_model)
        self.service = service

    @validation_email
    @validation_password
    def login(self, params: tuple) -> tuple:
        """Function that validates the user's credentials for session start.

        Args:
            params (tuple): user credentials (email and password)

        Returns:
            result (tuple): returns (id, role) of the logged in user
        """

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
        """Validation of the existence of complete user data for registration.

        Args:
            params (tuple): user data (email, password, username)

        Returns:
            result (bool): if the registration was successful, it returns True

        Raises:
            DataEmptyError: if there is empty data
        """

        self.log = get_logger("audit", self.__class__.__name__)
        #  email, password, username
        if not validation_data_empty(params):
            raise DataEmptyError("All fields are required")

        try:
            return self.service.create_user(params)
        except EmailError as e:
            self.log.warning(str(e))
            raise e
