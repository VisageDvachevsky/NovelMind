import os
import platform

def get_default_base_directory():
    """Returns the default base directory based on the operating system."""
    system = platform.system()
    if system == 'Windows':
        return os.path.join(os.getenv('TEMP'), 'EditorSystem')
    elif system == 'Linux':
        return os.path.join('/tmp', 'EditorSystem')
    elif system == 'Darwin':  
        return os.path.join('/tmp', 'EditorSystem')
    else:
        raise Exception(f"Unsupported operating system: {system}")

BASE_DIRECTORY = get_default_base_directory()

ENCRYPTION_KEY_LENGTH = 32
KDF_ITERATIONS = 100000