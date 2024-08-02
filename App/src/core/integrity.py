import hashlib

class IntegrityManager:
    @staticmethod
    def hash_data(data: bytes) -> str:
        return hashlib.sha256(data).hexdigest()

    @staticmethod
    def verify_data(data: bytes, expected_hash: str) -> bool:
        return hashlib.sha256(data).hexdigest() == expected_hash
