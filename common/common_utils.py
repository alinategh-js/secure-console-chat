import base64
from common.configs import KEY, SALT
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

def generate_key(password: str):
    if password == None or len(password) == 0:
        return KEY

    backend = default_backend()
    salt = SALT

    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=backend
    )

    key = base64.urlsafe_b64encode(kdf.derive(bytes(password, 'utf-8')))
    return key