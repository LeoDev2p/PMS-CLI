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
    
    def menu_edit_profile():
        print("""
              EDIT PROFILE\n
        [1] Edit username
        [2] Edit password
        [3] Back
        """)

