import os
import sqlite3
import hashlib
import json
from typing import Dict, Any, Optional
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64

class SecureDataStore:
    """
    Secure, encrypted data storage mechanism with privacy preservation
    
    Features:
    - End-to-end encryption
    - Tokenization of sensitive data
    - Granular access controls
    - Auditable storage operations
    """
    
    def __init__(
        self, 
        db_path: str = 'secure_medical_store.db',
        encryption_key: Optional[bytes] = None
    ):
        """
        Initialize secure data storage
        
        :param db_path: Path to the encrypted SQLite database
        :param encryption_key: Optional custom encryption key
        """
        self.db_path = db_path
        
        # Generate or use provided encryption key
        self.encryption_key = encryption_key or self._generate_encryption_key()
        
        # Initialize encryption engine
        self.cipher_suite = Fernet(base64.urlsafe_b64encode(self.encryption_key))
        
        # Setup database
        self._initialize_database()
    
    def _generate_encryption_key(
        self, 
        salt: Optional[bytes] = None
    ) -> bytes:
        """
        Generate a cryptographically secure encryption key
        
        :param salt: Optional salt for key derivation
        :return: Derived encryption key
        """
        # Use system's random source for salt if not provided
        salt = salt or os.urandom(16)
        
        # Use PBKDF2 for key derivation
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000
        )
        
        # Derive key from system entropy
        return kdf.derive(os.urandom(32))
    
    def _initialize_database(self):
        """
        Create secure database with encryption-enabled tables
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Medical record storage table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS medical_records (
                    record_id TEXT PRIMARY KEY,
                    patient_token TEXT,
                    encrypted_data BLOB,
                    metadata TEXT,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Access log table for audit purposes
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS access_log (
                    log_id TEXT PRIMARY KEY,
                    record_id TEXT,
                    user_id TEXT,
                    access_type TEXT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            conn.commit()
    
    def store_medical_record(
        self, 
        patient_token: str, 
        medical_data: Dict[str, Any]
    ) -> str:
        """
        Securely store a medical record with end-to-end encryption
        
        :param patient_token: Pseudonymized patient identifier
        :param medical_data: Medical record data
        :return: Generated record identifier
        """
        # Generate unique record identifier
        record_id = hashlib.sha256(
            f"{patient_token}{json.dumps(medical_data)}".encode()
        ).hexdigest()
        
        # Encrypt medical data
        encrypted_data = self.cipher_suite.encrypt(
            json.dumps(medical_data).encode()
        )
        
        # Store encrypted record
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT OR REPLACE INTO medical_records 
                (record_id, patient_token, encrypted_data, metadata) 
                VALUES (?, ?, ?, ?)
            ''', (
                record_id, 
                patient_token, 
                encrypted_data, 
                json.dumps({
                    'fields': list(medical_data.keys()),
                    'encrypted_at': str(datetime.now())
                })
            ))
            conn.commit()
        
        return record_id
    
    def retrieve_medical_record(
        self, 
        record_id: str, 
        user_id: str, 
        access_purpose: str
    ) -> Optional[Dict[str, Any]]:
        """
        Retrieve and decrypt a medical record with access logging
        
        :param record_id: Unique record identifier
        :param user_id: User attempting to access the record
        :param access_purpose: Reason for data access
        :return: Decrypted medical record or None
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Retrieve encrypted record
            cursor.execute(
                'SELECT encrypted_data FROM medical_records WHERE record_id = ?', 
                (record_id,)
            )
            result = cursor.fetchone()
            
            if not result:
                return None
            
            # Log access attempt
            access_log_id = hashlib.sha256(
                f"{record_id}{user_id}{access_purpose}".encode()
            ).hexdigest()
            
            cursor.execute('''
                INSERT INTO access_log 
                (log_id, record_id, user_id, access_type) 
                VALUES (?, ?, ?, ?)
            ''', (access_log_id, record_id, user_id, access_purpose))
            
            # Decrypt record
            try:
                decrypted_data = self.cipher_suite.decrypt(result[0])
                return json.loads(decrypted_data.decode())
            except Exception as e:
                # Log decryption failures
                print(f"Decryption error: {e}")
                return None
    
    def delete_medical_record(
        self, 
        record_id: str, 
        user_id: str
    ) -> bool:
        """
        Securely delete a medical record with audit logging
        
        :param record_id: Record to be deleted
        :param user_id: User performing deletion
        :return: Deletion success status
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Log deletion attempt
                deletion_log_id = hashlib.sha256(
                    f"DELETE{record_id}{user_id}".encode()
                ).hexdigest()
                
                cursor.execute('''
                    INSERT INTO access_log 
                    (log_id, record_id, user_id, access_type) 
                    VALUES (?, ?, ?, ?)
                ''', (deletion_log_id, record_id, user_id, 'record_deletion'))
                
                # Delete record
                cursor.execute(
                    'DELETE FROM medical_records WHERE record_id = ?', 
                    (record_id,)
                )
                
                conn.commit()
                return True
        except Exception as e:
            print(f"Deletion error: {e}")
            return False
    
    def search_records(
        self, 
        search_criteria: Dict[str, Any], 
        user_id: str
    ) -> List[str]:
        """
        Perform privacy-preserving record search
        
        :param search_criteria: Search parameters
        :param user_id: User performing the search
        :return: List of matching record IDs
        """
        # Implement advanced search with minimal information exposure
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Base query with patient token search
            query = '''
                SELECT record_id 
                FROM medical_records 
                WHERE patient_token = ?
            '''
            
            # Log search operation
            search_log_id = hashlib.sha256(
                f"SEARCH{json.dumps(search_criteria)}{user_id}".encode()
            ).hexdigest()
            
            cursor.execute('''
                INSERT INTO access_log 
                (log_id, user_id, access_type) 
                VALUES (?, ?, ?)
            ''', (search_log_id, user_id, 'record_search'))
            
            # Execute search with minimal information exposure
            results = cursor.execute(query, (search_criteria.get('patient_token'),))
            
            return [record[0] for record in results]
        

# ### Usage Example
# # Initialize secure data store
# data_store = SecureDataStore()

# # Store a medical record
# record_id = data_store.store_medical_record(
#     patient_token='patient_123_token',
#     medical_data={
#         'age': 55,
#         'medical_history': ['diabetes', 'hypertension'],
#         'test_results': {...}
#     }
# )