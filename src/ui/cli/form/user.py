class FormsUser:
    """
    Class to manage forms users.
    """
    @staticmethod
    def add_user_forms() -> tuple:
        username = input("[username]: ")
        email = input("[email]: ")
        password = input("[password]: ")
        return email, password, username

    @staticmethod
    def edit_forms(message = 'new value'):
        try:
            value = input(f"[{message}]: ")
            return value
        except ValueError as e:
            print(f"Error: {e}")

    @staticmethod
    def search_forms():
        user_email = input("[Search by useranem or email]: ")
        return user_email
