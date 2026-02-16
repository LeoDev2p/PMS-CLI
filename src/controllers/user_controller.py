from src.core.logging import get_logger
from src.core.exceptions import HashCreatingError


class UserController:
    def __init__(self, service):
        self.service = service
        self.log = get_logger("audit", self.__class__.__name__)

    def get_profile(self) -> tuple:
        return self.service.fetch_profile()

    # params = username, password
    def edit_profile(self, params):
        try:
            self.service.modify_profile(params)
        except HashCreatingError as e:
            self.log.warning(str(e))
            raise e
        
        self.log.info("profile updated successfully")
