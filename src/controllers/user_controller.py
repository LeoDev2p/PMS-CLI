from src.core.exceptions import (
    DataEmptyError,
    HashCreatingError,
    PasswordMatchError,
)
from src.core.logging import get_logger
from utils.validators import (
    validation_data_empty,
    validation_email,
    validation_password,
)


class UserController:
    """
    Handles user managemen
    """

    def __init__(self, service):
        self.service = service
        self.log = get_logger("security", self.__class__.__name__)

    # get
    def get_profile(self) -> dict:
        """
        Returns the profile of the current user.
        """
        return self.service.fetch_profile()

    def get_all_users(self) -> list[dict]:
        """
        Returns all users.

        Returns:
            list[dict]: List of id, username, email, role, create_by
        """
        return self.service.fetch_all_users()

    def search_user_or_email(self, user_or_email: str) -> list[dict]:
        """
        Searches for a user or email.

        Args:
            user_or_email (str): User or email to search.

        Returns:
            list[tuple]: List of id, username and email.
        """
        if not validation_data_empty(user_or_email):
            raise DataEmptyError("Email o username requerido")

        return self.service.fetch_user_or_email(user_or_email)

    def get_free_operational_users(self) -> list[dict]:
        """
        Gets all free operational users.

        Returns:
            list[dict]: List of id, username and title_task.
        """
        return self.service.fetch_free_operational_users()

    def get_users_without_active_task(self) -> list[dict]:
        """
        Gets all users without active task.

        Returns:
            list[dict]: List of id, username and title_task.
        """
        return self.service.fetch_users_without_active_task()

    def get_user_by_project(self, id_project: int) -> list[dict]:
        """
        Gets all users by project.

        Returns:
            list[dict]: List of id, username and title_task.
        """
        return self.service.fetch_user_by_project(id_project)

    # edit
    @validation_password
    def edit_profile(self, params: tuple):
        """
        Edits the profile of the current user.

        Args:
            params (tuple): Tuple of username, password and password_confirmation.
        """
        validate = validation_data_empty(params)
        if not validate:
            raise DataEmptyError("All fields are required")

        if params[1] != params[2]:
            raise PasswordMatchError("Passwords do not match")

        try:
            self.service.modify_profile(params[:2])
        except HashCreatingError as e:
            self.log.warning(str(e))
            raise e

    # gestion admin
    def edit_username(self, params: tuple):
        """
        Edits the username of a user.

        Args:
            params (tuple): Tuple of username and id.
        """
        username, id = params
        if not validation_data_empty(username):
            raise DataEmptyError("Fields user are required")

        self.service.modify_user(username, id)

    @validation_email
    def edit_email(self, params: tuple):
        """
        Edits the email of a user.

        Args:
            params (tuple): Tuple of email and id.
        """
        email, id = params
        if not validation_data_empty(email):
            raise DataEmptyError("Fields email are requiered")

        self.service.modify_email(email, id)

    @validation_password
    def reset_password(self, params: tuple):
        """
        Resets the password of a user.

        Args:
            params (tuple): Tuple of id and password.
        """
        id, password = params
        if not validation_data_empty(password):
            raise DataEmptyError("Fields password  are requiered")

        try:
            self.service.modify_password(password, id)
        except HashCreatingError as e:
            self.log.warning(str(e))
            raise e

    def change_role(self, params: tuple):
        """
        Changes the role of a user.

        Args:
            params (tuple): Tuple of role and id.
        """
        role, id = params
        if not validation_data_empty(role):
            raise DataEmptyError("Fields role are requiered")

        self.service.modify_role(role, id)

    # delete
    def delete_user(self, id_user: int):
        """
        Deletes a user.
        """
        self.service.remove_user(id_user)

    # stats
    def get_free_vs_assigned_users(self) -> list[dict]:
        """
        Gets all free vs assigned users.
        """
        return self.service.fetch_free_vs_assigned_users()

    def get_count_tasks_by_user(self) -> list[dict]:
        """
        Gets all count tasks by user.
        """
        return self.service.fetch_count_tasks_by_user()

    def get_top_users(self) -> list[dict]:
        """
        Gets all top users.
        """
        return self.service.fetch_top_users()
