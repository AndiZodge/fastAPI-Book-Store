from pydantic import BaseModel, validator
import hashlib


class UserLoginBase(BaseModel):
    username: str
    password: str
    
    @validator('password')
    def hash_password(cls, password):
        hashed = hashlib.sha256(password.encode()).hexdigest()
        return hashed