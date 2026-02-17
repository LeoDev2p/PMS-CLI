from locale import normalize
from src.models.sessions import Session
from utils.helpers import TextHelper
from utils.security import Hasher


class UserServices:
    def __init__(self, user_model):
        self.user_model = user_model

    def fetch_profile(self) -> tuple:
        return self.user_model.select_by_users(Session.get_id())

    def modify_profile(self, params):
        normalized = TextHelper.normalize(params[0])
        params = (normalized[0], Hasher.hash_password(params[1]), Session.get_id())
        self.user_model.update_profile(params)
    
    # gestion admin OJO: excepciones falt

    def modify_user(self, username, id):
        # username, id_user
        normalized = TextHelper.normalize(username)
        self.user_model.update_username((normalized, id))
    
    def modify_email(self, email, id):
        normalized = TextHelper.normalize(email)
        self.user_model.update_email(normalized, id)

    def modify_password(self, password, id):
        normalized = Hasher.hash_password(password)
        self.user_model.update_email(normalized, id)

    def modify_role(self, role, id):
        normalized = TextHelper.normalize(role)
        self.user_model.update_role(normalized, id)

