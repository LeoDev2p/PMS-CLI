from argon2 import PasswordHasher


class Hasher:
    @staticmethod
    def hash_password(password: str) -> str:
        ph = PasswordHasher(time_cost=3, memory_cost=65536, parallelism=4, hash_len=32)
        return ph.hash(password)

    @staticmethod
    def verify_password(hash: str, password: str) -> bool:
        ph = PasswordHasher(time_cost=3, memory_cost=65536, parallelism=4, hash_len=32)
        return ph.verify(hash, password)

    @staticmethod
    def check_needs_rehash(hash: str) -> bool:
        ph = PasswordHasher(time_cost=3, memory_cost=65536, parallelism=4, hash_len=32)
        return ph.check_needs_rehash(hash)
