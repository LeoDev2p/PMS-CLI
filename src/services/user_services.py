from src.core.exceptions import NotFoundUserError
from src.core.logging import get_logger
from src.models.sessions import Session
from utils.helpers import TextHelper
from utils.security import Hasher
from utils.validators import textvalidator


class UserServices:
    def __init__(self, user_model):
        self.user_model = user_model
        self.log = get_logger("audit", self.__class__.__name__)

    def fetch_profile(self) -> tuple:
        return self.user_model.select_by_users(Session.get_id())
    
    def fetch_all_users(self) -> list[tuple]:
        return self.user_model.select_all()
    
    def fetch_user_or_email(self, user_or_email):
        normalized = TextHelper.normalize(user_or_email)
        if textvalidator(normalized):
            result = self.user_model.like_by_email(normalized)
            if not result:
                raise NotFoundUserError("Usuario no registrado")
            
            return result
        else:
            result = self.user_model.like_by_username(normalized)
            if not result:
                raise NotFoundUserError("Usuario no registrado")
            
            return result

    def modify_profile(self, params):
        normalized = TextHelper.normalize(params[0])
        params = (normalized[0], Hasher.hash_password(params[1]), Session.get_id())
        self.user_model.update_profile(params)
        self.log.info(f"User {Session.get_id()} profile updated successfully")

    # gestion admin OJO: excepciones falt

    def modify_user(self, username, id):
        # username, id_user
        normalized = TextHelper.normalize(username)
        params = (normalized, id)
        self.user_model.update_username(params)

        self.log.info(f"Admin user {Session.get_id()} update user {id}'s username")

    def modify_email(self, email, id):
        normalized = TextHelper.normalize(email)
        print (f"[DEBUG] user serice, email {normalized} | {id}")
        self.user_model.update_email((normalized, id))
        self.log.info(
            f"Admin user {Session.get_id()} updated user {id}'s email address"
        )

    def modify_password(self, password, id):
        normalized = Hasher.hash_password(password)
        self.user_model.update_password((normalized, id))
        self.log.info(f"Admin user {Session.get_id()} updated user {id}'s password")

    def modify_role(self, role, id):
        normalized = TextHelper.normalize(role)
        self.user_model.update_role((normalized, id))
        self.log.info(f"Admin user {Session.get_id()} updated user {id}'s role")

    def remove_user(self, id):
        if not self.user_model.select_by_users(id):
            raise NotFoundUserError("User not found")

        self.user_model.delete(id)
        self.log.info(f"Admin user {Session.get_id()} deleted user {id}")
    
