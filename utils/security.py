from argon2 import PasswordHasher
from argon2.exceptions import HashingError, VerificationError, VerifyMismatchError

from src.core.exceptions import HashError, HashVerificationError


class Hasher:
    @staticmethod
    def hash_password(password: str) -> str:
        try:
            ph = PasswordHasher(
                time_cost=3, memory_cost=65536, parallelism=4, hash_len=32
            )
            return ph.hash(password)
        except HashingError as e:
            raise HashError(str(e))

    @staticmethod
    def verify_password(hash: str, password: str) -> bool:
        try:
            ph = PasswordHasher(
                time_cost=3, memory_cost=65536, parallelism=4, hash_len=32
            )
            return ph.verify(hash, password)
        except (VerifyMismatchError, VerificationError) as e:
            raise HashVerificationError(str(e))

    @staticmethod
    def check_needs_rehash(hash: str) -> bool:
        ph = PasswordHasher(time_cost=3, memory_cost=65536, parallelism=4, hash_len=32)
        return ph.check_needs_rehash(hash)
