
class FormsAuth:
    """
    Class to manage forms auth.
    """

    @staticmethod
    def login_forms() -> tuple:
        email = input("[email]: ")
        password = input("[password]: ")
        return email, password

    @staticmethod
    def register_forms() -> tuple:
        username = input("[username]: ")
        email = input("[email]: ")
        password = input("[password]: ")
        return email, password, username