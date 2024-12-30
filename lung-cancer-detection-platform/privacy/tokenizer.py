import hashlib
import uuid

class Tokenizer:
    def __init__(self, salt: str = None):
        self.salt = salt or str(uuid.uuid4())
    
    def generate_tokens(self, record: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate tokens for sensitive identifiers
        
        :param record: Anonymized medical record
        :return: Record with tokenized identifiers
        """
        tokenized_record = record.copy()
        
        for key, value in record.items():
            if isinstance(value, str):
                # Create a consistent, irreversible token
                tokenized_record[key] = self._create_token(value)
        
        return tokenized_record
    
    def _create_token(self, value: str) -> str:
        """
        Create a consistent token for a given value
        
        :param value: Original value
        :return: Generated token
        """
        return hashlib.sha256(f"{self.salt}{value}".encode()).hexdigest()
