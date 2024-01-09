from pydantic import BaseModel, validator
import hashlib


class UserBase(BaseModel):
    username: str
    email_id: str
    password: str
    mobile_number: str
    is_admin: bool = 0
    
    @validator('password')
    def hash_password(cls, password):
        hashed = hashlib.sha256(password.encode()).hexdigest()
        return hashed