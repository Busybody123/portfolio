import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


# Functions related to key config
def generate_master_key(password, salt):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=480000
    )
    key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
    master_key = Fernet(key)
    return master_key

def rotate_keys(old_key, new_key, ciphertext):
    plaintext = decrypt_msg(old_key, ciphertext)
    ciphertext = encrypt_msg(new_key, plaintext)
    return ciphertext



# Functions related to operations performed regarding keys
def encrypt_msg(master_key, plaintext):
    ciphertext = master_key.encrypt(plaintext.encode())
    return ciphertext

def decrypt_msg(master_key, ciphertext):
    plaintext = master_key.decrypt(ciphertext).decode()
    return plaintext

