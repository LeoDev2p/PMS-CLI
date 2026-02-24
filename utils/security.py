from argon2.exceptions import HashingError, VerificationError, VerifyMismatchError

from src.core.exceptions import HashCreatingError, HashInvalidError
from src.core.setting import PH


class Hasher:
    """
    Class to manage hash.
    """

    @staticmethod
    def hash_password(password: str) -> str:
        """
        Hashes a password.

        Args:
            password (str): Password to hash.

        Returns:
            str: Hashed password.

        Raises:
            HashCreatingError: If the password cannot be hashed.
        """
        try:
            return PH.hash(password)
        except HashingError as e:
            raise HashCreatingError(str(e))

    @staticmethod
    def verify_password(hash: str, password: str) -> bool:
        """
        Verifies a password.

        Args:
            hash (str): Hashed password.
            password (str): Password to verify.

        Returns:
            bool: True if the password is correct, False otherwise.

        Raises:
            HashInvalidError: If the password is invalid.
        """
        try:
            return PH.verify(hash, password)
        except (VerifyMismatchError, VerificationError) as e:
            raise HashInvalidError(str(e))

    @staticmethod
    def check_needs_rehash(hash: str) -> bool:
        """
        Checks if a password needs to be rehashed.

        Args:
            hash (str): Hashed password.

        Returns:
            bool: True if the password needs to be rehashed, False otherwise.
        """
        return PH.check_needs_rehash(hash)
