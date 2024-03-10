import os
import sys
import psycopg2 
from .encryption import Encryption


# Get the directory of your current script
current_dir = os.path.dirname(__file__)
# Go one folder back
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

def get_db_connection(DATABASE_URL):
    conn = psycopg2.connect(DATABASE_URL)
    return conn

def cipher(password, key):
    key = f'{password}-{key}'

    encrypt = Encryption(key)
    
    return encrypt

def admin_login(password):
    
    key = "handmade-impeach"
    
    encrypt = cipher(password, key)
    
    # encrypted login information
    DATABASE_URL = 'gAAAAABllaRNSFxaCyhb2ChB4UBtOZ5TNVmYIw_uedFuC3YF5B0gUUCRo_4xb5pyyi1-GfZq46VwsEfK9eYeRCio2ddyWlrwleZS4Yqo3ea3FqYwDWdKEASYAg3xCF4Exn_H86bRROpTz5TReWzAgiz4tAyMlvg36Q=='
    
    return get_db_connection(encrypt.decrypt_message(DATABASE_URL))

def student_login(password):
    
    key = "twiddle-overhead"
    
    encrypt = cipher(password, key)
    
    DATABASE_URL = 'gAAAAABllaY4MLtSvSMxg4EPsvnI6LUPvIvpuNS4s2SOkcSt13VEJ_a8UT-m7dP0AlgbW5jVOUFeclB2xXl-5zupRCeQnvDDCDSNeN7XLhLGsl54mFRJ7Lg70P1ANeUOY23bjk9MCirXV57PM-Jz16hmd6PJqyeoAwIaLL_x5zE7Dd6ovHfGyzk='

    
    return get_db_connection(encrypt.decrypt_message(DATABASE_URL))