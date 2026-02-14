from utils.validators import validation_email, validation_password


class AuthController:
    def __init__(self, service):
        self.service = service

    @validation_email
    @validation_password
    def login(self, params):
        # email password
        self.services.login(params)

    @validation_email
    @validation_password
    def register(self, params):
        # username, email, password, role
        self.services.register(params)
