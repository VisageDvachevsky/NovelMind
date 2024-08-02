import uuid

def generate_unique_id() -> str:
    """Generates a unique identifier for a file."""
    return str(uuid.uuid4())

def log(message: str):
    """Logs a message (could be extended to log to a file)."""
    print(f"[LOG] {message}")