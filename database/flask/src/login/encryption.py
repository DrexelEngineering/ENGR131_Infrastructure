import base64
import hashlib

from cryptography.fernet import Fernet


class Encryption:
    """
    A class used to encrypt and decrypt messages using Fernet symmetric encryption.

    Attributes:
        cipher_suite (Fernet): An instance of the Fernet class, used for encryption and decryption.

    Args:
        input_key (str): A string from which the encryption key is derived.

    Methods:
        encrypt_message(message: str) -> str:
            Encrypts a plain text message.

        decrypt_message(encrypted_message: str) -> str:
            Decrypts an encrypted message.
    """

    def __init__(self, input_key):
        """
        Initializes the Encryption object by creating a Fernet encryption key from the input string.

        Args:
            input_key (str): The string input from which the encryption key is derived.
        """
        # Generating a key from the string
        key = base64.urlsafe_b64encode(hashlib.sha256(input_key.encode()).digest())

        # Create a Fernet object with this key
        self.cipher_suite = Fernet(key)

    def encrypt_message(self, message):
        """
        Encrypts a given message using the Fernet cipher suite.

        Args:
            message (str): The plain text message to be encrypted.

        Returns:
            str: The encrypted message, encoded in a string format.
        """
        return self.cipher_suite.encrypt(message.encode()).decode()

    def decrypt_message(self, encrypted_message):
        """
        Decrypts a given message using the Fernet cipher suite.

        Args:
            encrypted_message (str): The encrypted message to be decrypted.

        Returns:
            str: The decrypted message, returned as plain text.
        """
        return self.cipher_suite.decrypt(encrypted_message.encode()).decode()
