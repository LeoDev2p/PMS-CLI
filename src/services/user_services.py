from src.core.exceptions import DatabaseLockedError, DatabaseSystemError, ModelsError, NotFoundUserError
from src.core.logging import get_logger
from src.models.sessions import Session
from utils.helpers import TextHelper
from utils.security import Hasher
from utils.validators import textvalidator


class UserServices:
    """
    Handles user services
    """

    def __init__(self, model):
        # model -> UserModels
        self.model = model
        self.log_audit = get_logger("audit", self.__class__.__name__)
        self.log_error = get_logger("error", self.__class__.__name__)

    # fetch
    def fetch_profile(self) -> dict:
        """
        Fetches the profile of the current user.
        """
        try:
            result = self.model.select_by_users(Session.get_id())
        except DatabaseSystemError as e:
            self.log_error.critical(f"Error: {e}")
            raise ModelsError("Technical error in the data server. Contact support.")
        else:
            if not result:
                raise NotFoundUserError("User not found")

            return {
                "username": result[0],
                "email": result[1],
            }

    def fetch_all_users(self) -> list[dict]:
        """
        Fetches all users.
        """
        try:
            result = self.model.select_all()
        except DatabaseSystemError as e:
            self.log_error.critical(f"Error: {e}")
            raise ModelsError("Technical error in the data server. Contact support.")
        else:
            if not result:
                raise NotFoundUserError("No users found")

            return [
                {
                    "id": user[0],
                    "username": user[1],
                    "email": user[2],
                    "role": user[3],
                    "created_by": user[4],
                }
                for user in result
            ]

    def fetch_user_or_email(self, user_or_email):
        """
        Fetches a user or email.

        Args:
            user_or_email (str): User or email to search.

        Returns:
            list[tuple]: List of id, username and email.
        """
        normalized = TextHelper.normalize(user_or_email)
        try:
            if textvalidator(normalized):
                result = self.model.like_by_email(normalized)
                if not result:
                    raise NotFoundUserError("Usuario no registrado")

            else:
                result = self.model.like_by_username(normalized)
                if not result:
                    raise NotFoundUserError("Usuario no registrado")

            return [
                {
                    "id": user[0],
                    "username": user[1],
                    "email": user[2],
                }
                for user in result
            ]
        except DatabaseSystemError as e:
            self.log_error.critical(f"Error: {e}")
            raise ModelsError("Technical error in the data server. Contact support.")

    def fetch_free_operational_users(self) -> list[tuple]:
        """
        Fetches all free operational users.

        Returns:
            list[tuple]: List of id, username and title_task.
        """
        try:
            result = self.model.select_free_operational_users()
        except DatabaseSystemError as e:
            self.log_error.critical(f"Error: {e}")
            raise ModelsError("Technical error in the data server. Contact support.")
        else:
            if not result:
                raise NotFoundUserError("No free operational users found")

            return [
                {
                    "id": user[0],
                    "username": user[1],
                    "email": user[2],
                }
                for user in result
            ]

    def fetch_users_without_active_task(self) -> list[dict]:
        try:
            result = self.model.select_users_without_active_tasks()
        except DatabaseSystemError as e:
            self.log_error.critical(f"Error: {e}")
            raise ModelsError("Technical error in the data server. Contact support.")
        else:
            if not result:
                raise NotFoundUserError("There are no free users available")

            return [
                {
                    "id": user[0],
                    "username": user[1],
                }
                for user in result
            ]

    def fetch_user_by_project(self, id_project: int) -> list[dict]:
        """
        Fetches all users by project.
        """
        try:
            result = self.model.select_user_by_project(id_project)
        except DatabaseSystemError as e:
            self.log_error.critical(f"Error: {e}")
            raise ModelsError("Technical error in the data server. Contact support.")
        else:
            if not result:
                raise NotFoundUserError("There are no users available for this project")

            return [
                {
                    "id": user[0],
                    "username": user[1],
                    "title": user[2],
                }
                for user in result
            ]

    # modify
    def modify_profile(self, params: tuple):
        """
        Modifies the profile of the current user.

        Args:
            params (tuple): Tuple of username and password.
        """
        normalized = TextHelper.normalize(params[0])
        params = (normalized[0], Hasher.hash_password(params[1]), Session.get_id())
        try:
            self.model.update_profile(params)
            self.log_audit.info(f"User {Session.get_id()} profile updated successfully")
        except (DatabaseLockedError, DatabaseSystemError) as e:
            self.log_error.critical(f"Error: {e}")
            raise ModelsError("Technical error in the data server. Contact support.")

    def modify_user(self, username: str, id: int):
        """
        Modifies the username of a user.

        Args:
            username (str): Username to modify.
            id (int): Id of the user to modify.
        """
        normalized = TextHelper.normalize(username)
        params = (normalized, id)
        try:
            self.model.update_username(params)
            self.log_audit.info(f"{Session.get_role()} user {Session.get_id()} update user {id}'s username")
        except (DatabaseLockedError, DatabaseSystemError) as e:
            self.log_error.critical(f"Error: {e}")
            raise ModelsError("Technical error in the data server. Contact support.")

    def modify_email(self, email: str, id: int):
        """
        Modifies the email of a user.

        Args:
            email (str): Email to modify.
            id (int): Id of the user to modify.
        """
        normalized = TextHelper.normalize(email)
        try:
            self.model.update_email((normalized, id))
            self.log_audit.info(f"{Session.get_role()} user {Session.get_id()} updated user {id}'s email address")
        except (DatabaseLockedError, DatabaseSystemError) as e:
            self.log_error.critical(f"Error: {e}")
            raise ModelsError("Technical error in the data server. Contact support.")

    def modify_password(self, password: str, id: int):
        """
        Modifies the password of a user.

        Args:
            password (str): Password to modify.
            id (int): Id of the user to modify.
        """
        normalized = Hasher.hash_password(password)
        try:
            self.model.update_password((normalized, id))
            self.log_audit.info(f"{Session.get_role()} user {Session.get_id()} updated user {id}'s password")
        except (DatabaseLockedError, DatabaseSystemError) as e:
            self.log_error.critical(f"Error: {e}")
            raise ModelsError("Technical error in the data server. Contact support.")

    def modify_role(self, role: str, id: int):
        """
        Modifies the role of a user.

        Args:
            role (str): Role to modify.
            id (int): Id of the user to modify.
        """
        normalized = TextHelper.normalize(role)
        if normalized not in ("admin", "user"):
            raise ValueError("Invalid role")
        try:
            self.model.update_role((normalized, id))
            self.log_audit.info(f"{Session.get_role()} user {Session.get_id()} updated user {id}'s role")
        except (DatabaseLockedError, DatabaseSystemError) as e:
            self.log_error.critical(f"Error: {e}")
            raise ModelsError("Technical error in the data server. Contact support.")

    # remove
    def remove_user(self, id_user: int):
        """
        Removes a user.

        Args:
            id_user (int): Id of the user to remove.
        """
        try:
            if not self.model.select_by_users(id_user):
                raise NotFoundUserError("User not found")
        except DatabaseSystemError as e:
            self.log_error.critical(f"Error: {e}")
            raise ModelsError("Technical error in the data server. Contact support.")

        try:
            self.model.delete(id_user)
            self.log_audit.info(f"{Session.get_role()} user {Session.get_id()} deleted user {id_user}")
        except (DatabaseLockedError, DatabaseSystemError) as e:
            self.log_error.critical(f"Error: {e}")
            raise ModelsError("Technical error in the data server. Contact support.")

    # stats
    def fetch_free_vs_assigned_users(self) -> list[dict]:
        """
        Fetches the number of free vs assigned users.
        """
        try:
            result = self.model.count_free_vs_assigned_users()
        except (DatabaseLockedError, DatabaseSystemError) as e:
            self.log_error.critical(f"Error: {e}")
            raise ModelsError("Technical error in the data server. Contact support.")
        else:
            if not result:
                raise NotFoundUserError("No users available")

        return [
            {
                "free_users": r[0],
                "assigned_users": r[1],
            }
            for r in result
        ]

    def fetch_count_tasks_by_user(self) -> list[dict]:
        """
        Fetches the number of tasks by user.
        """
        try:
            result = self.model.count_tasks_by_user()
        except (DatabaseLockedError, DatabaseSystemError) as e:
            self.log_error.critical(f"Error: {e}")
            raise ModelsError("Technical error in the data server. Contact support.")
        else:
            if not result:
                raise NotFoundUserError("No users available")

        return [
            {
                "username": r[0],
                "pending": r[1],
                "in_progress": r[2],
                "in_review": r[3],
                "completed": r[4],
                "cancelled": r[5],
                "total_tasks": r[6],
            }
            for r in result
        ]

    def fetch_top_users(self) -> list[dict]:
        """
        Fetches Top 3 users with the most completed tasks
        """
        try:
            result = self.model.productivity_ranking()
        except (DatabaseLockedError, DatabaseSystemError) as e:
            self.log_error.critical(f"Error: {e}")
            raise ModelsError("Technical error in the data server. Contact support.")
        else:
            if not result:
                raise NotFoundUserError("No users available")

        return [
            {
                "username": r[0],
                "amount": r[1],
            }
            for r in result
        ]
