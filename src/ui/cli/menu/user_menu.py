class UserMenus:
    """
    Class to manage user menus.
    """

    @staticmethod
    def menu():
        print("""
              USER\n
        [1] My tasks
        [2] Update task status
        [3] My profile
        [4] Logout
        """)

    @staticmethod
    def menu_users():
        print("""
                      USER MANAGEMENT\n
        [1] Create user
        [2] Edit user
        [3] Delete user
        [4] View users
        [5] Back
        """)

    @staticmethod
    def menu_edit_users():
        print("""
                      EDIT USER\n
        [1] change username
        [2] change email
        [3] reset password
        [4] change role
        [5] Back
        """)
