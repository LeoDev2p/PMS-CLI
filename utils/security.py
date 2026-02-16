from argon2.exceptions import HashingError, VerificationError, VerifyMismatchError

from src.core.exceptions import HashCreatingError, HashInvalidError
from src.core.setting import PH


class Hasher:
    @staticmethod
    def hash_password(password: str) -> str:
        try:
            return PH.hash(password)
        except HashingError as e:
            raise HashCreatingError(str(e))

    @staticmethod
    def verify_password(hash: str, password: str) -> bool:
        try:
            return PH.verify(hash, password)
        except (VerifyMismatchError, VerificationError) as e:
            raise HashInvalidError(str(e))

    @staticmethod
    def check_needs_rehash(hash: str) -> bool:
        return PH.check_needs_rehash(hash)
