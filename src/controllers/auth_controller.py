from src.core.exceptions import AuthenticactionError, DataEmptyError, EmailError
from src.core.logging import get_logger
from src.models.sessions import Session
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
        self.log_security = get_logger("security", self.__class__.__name__)
        self.log_audit = get_logger("audit", self.__class__.__name__)

    @validation_email
    @validation_password
    def login(self, params: tuple) -> tuple:
        """Function that validates the user's credentials for session start.

        Args:
            params (tuple): user credentials (email and password)

        Returns:
            result (tuple): returns (id, role) of the logged in user
        """

        try:
            result = self.service.login_user(params)
            if result:
                Session.start(result[0], result[1], result[2])
            return True
        except AuthenticactionError as e:
            self.log_security.warning(f"User {params[0]} {str(e)}")
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

        #  email, password, username
        if not validation_data_empty(params):
            raise DataEmptyError("All fields are required")

        try:
            result = self.service.create_user(params)
            self.log_audit.info("User created successfully")
            return result
        except EmailError as e:
            self.log_security.warning(str(e))
            raise e

    def logout(self) -> bool:
        """Function that validates the user's credentials for session start.
        """

        self.log_security.info("User logged out successfully")
        Session.stop()
