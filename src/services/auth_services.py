class AuthService:
    def __init__(self, model):
        self.model = model

    def login_yser (self, params):
        # email password
        pass
    
    def create_user(self, params):
        # username, email, password, role
        self.model.insert(params)

