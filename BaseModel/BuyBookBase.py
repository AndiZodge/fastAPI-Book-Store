from pydantic import BaseModel, validator


# should be bookid and quanity only
class BuyBookBase(BaseModel):
    user_id: int = None
    book_id: int
    quantity: int = 1
    total_cost: int
