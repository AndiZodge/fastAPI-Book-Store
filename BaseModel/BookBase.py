from pydantic import BaseModel, validator


class BookBase(BaseModel):
    book_name: str
    genre: str
    image: str
    description: str
    quantity_available: float
    cost_per_book: int
    
    @validator('image')
    def validate_image(cls, img):
        image = img.encode('utf-8')
        return image