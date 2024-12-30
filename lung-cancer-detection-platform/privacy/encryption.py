from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64
import os

class AdvancedEncryptionService:
    """
    Comprehensive encryption service with key management
    """
    @staticmethod
    def generate_key(
        salt: bytes = None, 
        iterations: int = 100000
    ) -> bytes:
        """
        Generate a cryptographically secure encryption key
        
        :param salt: Optional salt for key derivation
        :param iterations: Number of key derivation iterations
        :return: Derived encryption key
        """
        # Use system random source if no salt provided
        salt = salt or os.urandom(16)
        
        # Use PBKDF2 for secure key derivation
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=iterations
        )
        
        # Derive key from system entropy
        key = kdf.derive(os.urandom(32))
        return base64.urlsafe_b64encode(key)
    
    @staticmethod
    def encrypt(
        data: bytes, 
        key: bytes = None
    ) -> bytes:
        """
        Encrypt data using Fernet symmetric encryption
        
        :param data: Data to encrypt
        :param key: Optional encryption key
        :return: Encrypted data
        """
        # Generate key if not provided
        encryption_key = key or AdvancedEncryptionService.generate_key()
        
        # Create Fernet cipher
        cipher_suite = Fernet(encryption_key)
        
        return cipher_suite.encrypt(data)
    
    @staticmethod
    def decrypt(
        encrypted_data: bytes, 
        key: bytes
    ) -> bytes:
        """
        Decrypt data using Fernet symmetric encryption
        
        :param encrypted_data: Data to decrypt
        :param key: Decryption key
        :return: Decrypted data
        """
        cipher_suite = Fernet(key)
        return cipher_suite.decrypt(encrypted_data)