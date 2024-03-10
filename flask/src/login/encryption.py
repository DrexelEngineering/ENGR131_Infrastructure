from cryptography.fernet import Fernet
import base64
import hashlib

class Encryption:
    def __init__(self, input_key):
        # Generating a key from the string
        key = base64.urlsafe_b64encode(hashlib.sha256(input_key.encode()).digest())
        
        # Create a Fernet object with this key
        self.cipher_suite = Fernet(key)

    # Function to encrypt a message
    def encrypt_message(self, message):
        return self.cipher_suite.encrypt(message.encode()).decode()

    # Function to decrypt a message
    def decrypt_message(self, encrypted_message):
        return self.cipher_suite.decrypt(encrypted_message.encode()).decode()