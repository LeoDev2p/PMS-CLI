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
    def edit_profile_forms():
        try:
            username = input("[New username]: ")
            password = input("[New password]: ")
            confirm_password = input("[Confirm password]: ")

            return username, password, confirm_password
        except Exception as e:
            print(f"Error: {e}")
            return None

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
