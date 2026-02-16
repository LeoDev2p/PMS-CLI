from src.core.exceptions import AuthenticactionError, EmailError
from src.core.logging import get_logger
from utils.security import Hasher


class AuthService:
    def __init__(self, model):
        # model = UsersModels()
        self.model = model
        self.log = get_logger("security", "AuthService")

    def login_user(self, params: tuple) -> str:
        user = self.model.select_by_email(params[0])
        if not user:
            self.log.warning("Email not found")
            raise AuthenticactionError("Email not found")

        if not Hasher.verify_password(user[3], params[1]):
            self.log.warning("Password not found")
            raise AuthenticactionError("Password not found")

        self.log.info("Successful login")
        return user[0], user[4]  # id, role

    def create_user(self, params: tuple) -> bool:
        user = self.model.select_by_email(params[1])
        role = "User" if self.model.select() else "Admin"

        if user:
            self.log.warning("Email already exists")
            raise EmailError("Email already exists")

        params = (params[2], params[0], Hasher.hash_password(params[1]), role)

        return self.model.insert(params)
