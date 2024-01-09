from pydantic import BaseModel, validator


class MyBooksBase(BaseModel):
    user_id: int