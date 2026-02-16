from src.models.sessions import Session
from utils.security import Hasher


class UserServices:
    def __init__(self, user_model):
        self.user_model = user_model

    def fetch_profile(self) -> tuple:
        return self.user_model.select_by_users(Session.get_id())

    def modify_profile(self, params):
        params = (params[0], Hasher.hash_password(params[1]), Session.get_id())
        self.user_model.update_profile(params)
