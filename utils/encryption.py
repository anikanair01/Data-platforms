
from cryptography.fernet import Fernet
import base64
import os
def generate_key():
    """Generate a new Fernet key."""
    key = Fernet.generate_key()
    return key.decode()  # Return as string for easier storage

def encrypt_message(message: str, key: str) -> str:
    """Encrypt a message using the provided Fernet key."""
    fernet = Fernet(key.encode())
    encrypted_message = fernet.encrypt(message.encode())
    return encrypted_message.decode()  # Return as string for easier handling

def decrypt_message(encrypted_message: str, key: str) -> str:
    """Decrypt a message using the provided Fernet key."""
    fernet = Fernet(key.encode())
    decrypted_message = fernet.decrypt(encrypted_message.encode())
    return decrypted_message.decode()  # Return as string

# Example usage:
if __name__ == "__main__":
    key = generate_key()
    print(f"Generated Key: {key}")

    original_message = "Hello, this is a secret message!"
    encrypted = encrypt_message(original_message, key)
    print(f"Encrypted Message: {encrypted}")

    decrypted = decrypt_message(encrypted, key)
    print(f"Decrypted Message: {decrypted}")

