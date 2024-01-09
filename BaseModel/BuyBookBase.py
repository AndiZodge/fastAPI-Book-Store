from pydantic import BaseModel, validator


class BuyBookBase(BaseModel):
    user_id: int = None
    book_id: int
    quantity: int = 1
    total_cost: int
