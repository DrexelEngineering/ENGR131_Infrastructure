import os
import sys
import psycopg2 
from .encryption import Encryption

# Adding the parent directory to the sys.path allows for importing modules from the parent directory.
current_dir = os.path.dirname(__file__)
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

def get_db_connection(DATABASE_URL):
    """
    Establishes a connection to a PostgreSQL database.

    Args:
        DATABASE_URL (str): The database URL that contains connection information.

    Returns:
        psycopg2.connection: A connection object to the database.
    """
    conn = psycopg2.connect(DATABASE_URL)
    return conn

def cipher(password, key):
    """
    Creates an Encryption object using a concatenated password and key as the encryption key.

    Args:
        password (str): The password to be used as part of the encryption key.
        key (str): The key to be concatenated with the password to form the encryption key.

    Returns:
        Encryption: An instance of the Encryption class initialized with the derived encryption key.
    """
    key = f'{password}-{key}'
    encrypt = Encryption(key)
    return encrypt

def admin_login(password):
    """
    Authenticates an admin user and returns a database connection using decrypted credentials.

    Args:
        password (str): The password used for authentication and as part of the encryption key.

    Returns:
        psycopg2.connection: A connection object to the database for the admin user.
    """
    key = "handmade-impeach" #TODO remove hard coded key
    encrypt = cipher(password, key)
    
    # Encrypted login information for admin.
    DATABASE_URL = 'gAAAAABllaRNSFxaCyhb2ChB4UBtOZ5TNVmYIw_uedFuC3YF5B0gUUCRo_4xb5pyyi1-GfZq46VwsEfK9eYeRCio2ddyWlrwleZS4Yqo3ea3FqYwDWdKEASYAg3xCF4Exn_H86bRROpTz5TReWzAgiz4tAyMlvg36Q=='
    
    return get_db_connection(encrypt.decrypt_message(DATABASE_URL))

def student_login(password):
    """
    Authenticates a student user and returns a database connection using decrypted credentials.

    Args:
        password (str): The password used for authentication and as part of the encryption key.

    Returns:
        psycopg2.connection: A connection object to the database for the student user.
    """
    key = "twiddle-overhead" #TODO: remove hard coded key
    encrypt = cipher(password, key)
    
    # Encrypted login information for student.
    DATABASE_URL = 'gAAAAABllaY4MLtSvSMxg4EPsvnI6LUPvIvpuNS4s2SOkcSt13VEJ_a8UT-m7dP0AlgbW5jVOUFeclB2xXl-5zupRCeQnvDDCDSNeN7XLhLGsl54mFRJ7Lg70P1ANeUOY23bjk9MCirXV57PM-Jz16hmd6PJqyeoAwIaLL_x5zE7Dd6ovHfGyzk='

    return get_db_connection(encrypt.decrypt_message(DATABASE_URL))
