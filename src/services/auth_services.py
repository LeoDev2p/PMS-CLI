from src.core.exceptions import EmailError, PasswordError
from src.core.logging import get_logger
from utils.security import Hasher


class AuthService:
    def __init__(self, model):
        # model = UsersModels()
        self.model = model
        self.log = get_logger("security", "AuthService")

    def login_user(self, params: tuple) -> bool:
        user = self.model.select_by_email(params[0])
        if not user:
            self.log.warning("Email not found")
            raise EmailError("Email not found")

        if not Hasher.verify_password(user[3], params[1]):
            self.log.warning("Password not found")
            raise PasswordError("Password not found")

        self.log.info("Successful login")
        return user[4]

    def create_user(self, params: tuple) -> bool:
        user = self.model.select_by_email(params[1])
        print(f"[DEBUG] create user {user}")
        print(f"[DEBUG] create user {self.model.select()}")
        role = "User" if self.model.select() else "Admin"

        if user:
            self.log.warning("Email already exists")
            raise EmailError("Email already exists")

        params = (params[2], params[0], Hasher.hash_password(params[1]), role)
        result = self.model.insert(params)
        self.log.info("Successful registration")
        return result
