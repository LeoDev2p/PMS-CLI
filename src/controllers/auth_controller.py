from utils.validators import validation_email, validation_password


class AuthController:
    def __init__(self, service):
        # service = AuthService (user_model)
        self.service = service

    @validation_email
    @validation_password
    def login(self, params: tuple):
        # email password
        return self.service.login_user(params)

    @validation_email
    @validation_password
    def register(self, params: tuple):
        # username, email, password, role
        return self.service.create_user(params)
