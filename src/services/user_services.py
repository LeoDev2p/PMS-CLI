from src.core.exceptions import DatabaseLockedError, ModelsError, NotFoundUserError
from src.core.logging import get_logger
from src.models.sessions import Session
from utils.helpers import TextHelper
from utils.security import Hasher
from utils.validators import textvalidator


class UserServices:
    """
    Handles user services
    """

    def __init__(self, user_model):
        self.user_model = user_model
        self.log_audit = get_logger("audit", self.__class__.__name__)
        self.log_error = get_logger("error", self.__class__.__name__)

    # fetch
    def fetch_profile(self) -> tuple:
        """
        Fetches the profile of the current user.
        """
        return self.user_model.select_by_users(Session.get_id())

    def fetch_all_users(self) -> list[tuple]:
        """
        Fetches all users.
        """
        return self.user_model.select_all()

    def fetch_user_or_email(self, user_or_email):
        """
        Fetches a user or email.

        Args:
            user_or_email (str): User or email to search.

        Returns:
            list[tuple]: List of id, username and email.
        """
        normalized = TextHelper.normalize(user_or_email)
        if textvalidator(normalized):
            result = self.user_model.like_by_email(normalized)
            if not result:
                raise NotFoundUserError("Usuario no registrado")

        else:
            result = self.user_model.like_by_username(normalized)
            if not result:
                raise NotFoundUserError("Usuario no registrado")

        return result

    def fetch_free_operational_users(self) -> list[tuple]:
        """
        Fetches all free operational users.

        Returns:
            list[tuple]: List of id, username and title_task.
        """
        return self.user_model.select_free_operational_users()

    def fetch_users_without_active_task(self):
        result = self.user_model.select_users_without_active_tasks()
        if not result:
            raise NotFoundUserError("There are no free users available")

        return result

    # modify
    def modify_profile(self, params):
        """
        Modifies the profile of the current user.

        Args:
            params (tuple): Tuple of username and password.
        """
        normalized = TextHelper.normalize(params[0])
        params = (normalized[0], Hasher.hash_password(params[1]), Session.get_id())
        try:
            self.user_model.update_profile(params)
            self.log_audit.info(f"User {Session.get_id()} profile updated successfully")
        except (DatabaseLockedError, ModelsError) as e:
            self.log_error.critical(f"Error: {e}")
            raise e

    def modify_user(self, username, id):
        """
        Modifies the username of a user.

        Args:
            username (str): Username to modify.
            id (int): Id of the user to modify.
        """
        normalized = TextHelper.normalize(username)
        params = (normalized, id)
        try:
            self.user_model.update_username(params)
            self.log_audit.info(
                f"Admin user {Session.get_id()} update user {id}'s username"
            )
        except (DatabaseLockedError, ModelsError) as e:
            self.log_error.critical(f"Error: {e}")
            raise e

    def modify_email(self, email, id):
        """
        Modifies the email of a user.

        Args:
            email (str): Email to modify.
            id (int): Id of the user to modify.
        """
        normalized = TextHelper.normalize(email)
        try:
            self.user_model.update_email((normalized, id))
            self.log_audit.info(
                f"Admin user {Session.get_id()} updated user {id}'s email address"
            )
        except (DatabaseLockedError, ModelsError) as e:
            self.log_error.critical(f"Error: {e}")
            raise e

    def modify_password(self, password, id):
        """
        Modifies the password of a user.

        Args:
            password (str): Password to modify.
            id (int): Id of the user to modify.
        """
        normalized = Hasher.hash_password(password)
        try:
            self.user_model.update_password((normalized, id))
            self.log_audit.info(
                f"Admin user {Session.get_id()} updated user {id}'s password"
            )
        except (DatabaseLockedError, ModelsError) as e:
            self.log_error.critical(f"Error: {e}")
            raise e

    def modify_role(self, role, id):
        """
        Modifies the role of a user.

        Args:
            role (str): Role to modify.
            id (int): Id of the user to modify.
        """
        normalized = TextHelper.normalize(role)
        try:
            self.user_model.update_role((normalized, id))
            self.log_audit.info(
                f"Admin user {Session.get_id()} updated user {id}'s role"
            )
        except (DatabaseLockedError, ModelsError) as e:
            self.log_error.critical(f"Error: {e}")
            raise e

    def fetch_user_by_project(self, id_project):
        result = self.user_model.select_user_by_project(id_project)
        if not result:
            raise NotFoundUserError("There are no users available for this project")

        return result

    # remove
    def remove_user(self, id_user):
        """
        Removes a user.

        Args:
            id_user (int): Id of the user to remove.
        """
        if not self.user_model.select_by_users(id_user):
            raise NotFoundUserError("User not found")

        try:
            self.user_model.delete(id_user)
            self.log_audit.info(f"Admin user {Session.get_id()} deleted user {id}")
        except (DatabaseLockedError, ModelsError) as e:
            self.log_error.critical(f"Error: {e}")
            raise e
