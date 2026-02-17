from src.core.exceptions import DataEmptyError, HashCreatingError, PasswordMatchError
from src.core.logging import get_logger
from utils.validators import validation_data_empty, validation_password, validation_email



class UserController:
    def __init__(self, service):
        self.service = service
        self.log = get_logger("audit", self.__class__.__name__)

    def get_profile(self) -> tuple:
        return self.service.fetch_profile()

    # params = username, password
    @validation_password
    def edit_profile(self, params):
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

        self.log.info("profile updated successfully")

    # gestion admin

    # el id todavia no se sabe imlmentar fucniond ebusqueda por like
    def edit_username(self, params):
        # username, id_user
        username, id = params
        if not validation_data_empty(username):
            raise DataEmptyError("Fields user are required")

        self.service.modify_user(username, id)

    @validation_email
    def edit_email(self, params):
        email, id = params
        # observar OJO
        if not validation_data_empty(email):
            raise DataEmptyError("Fields email are requiered")
        
        self.service.modify_email(email, id)

    @validation_password
    def reset_password(self, params):
        password, id = params
        # observar OJO
        if not validation_data_empty(password):
            raise DataEmptyError("Fields password  are requiered")
        
        self.service.modify_password(password, id)

    def change_role(self, params):
        role, id = params
        # observar OJO
        if not validation_data_empty(role):
            raise DataEmptyError("Fields role are requiered")
        
        self.service.modify_role(role, id)


