import uuid

class IdentifierManager:
    def __init__(self):
        pass

    def generate_identifier(self) -> str:
        return str(uuid.uuid4())
