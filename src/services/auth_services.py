from src.core.exceptions import AuthenticactionError, EmailError
from src.core.logging import get_logger
from utils.helpers import TextHelper
from utils.security import Hasher


class AuthService:
    def __init__(self, model):
        # model = UsersModels()
        self.model = model

    def login_user(self, params: tuple) -> str:
        log = get_logger("security", self.__class__.__name__)
        # email , password
        normalized = TextHelper.normalize(params[0])
        user = self.model.select_by_email(normalized)
        if not user:
            raise AuthenticactionError("Email not found")

        if not Hasher.verify_password(user[3], params[1]):
            raise AuthenticactionError("Password not found")

        log.info("Successful login")
        return user[0], user[4]  # id, role

    def create_user(self, params: tuple) -> bool:
        log = get_logger("audit", self.__class__.__name__)
        #  email, password, username
        normalized = TextHelper.normalize((params[2], params[0]))
        user = self.model.select_by_email(normalized[1])
        role = "user" if self.model.select_all() else "admin"

        if user:
            raise EmailError("Email already exists")

        # por solucionar orden

        params = (normalized[0], normalized[1], Hasher.hash_password(params[1]), role)

        result = self.model.insert(params)
        log.info("User register successfully")
        return result
