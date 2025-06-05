from cryptography.fernet import Fernet
import os
import base64

def get_cipher_suite():
    """Get the Fernet cipher suite with key from environment"""
    key = os.environ.get('SECRET_MANAGER_KEY', Fernet.generate_key())
    return Fernet(key)

def encrypt_data(data):
    """Encrypt sensitive data"""
    cipher_suite = get_cipher_suite()
    if isinstance(data, str):
        data = data.encode()
    return cipher_suite.encrypt(data).decode()

def decrypt_data(encrypted_data):
    """Decrypt sensitive data"""
    cipher_suite = get_cipher_suite()
    if isinstance(encrypted_data, str):
        encrypted_data = encrypted_data.encode()
    return cipher_suite.decrypt(encrypted_data).decode()