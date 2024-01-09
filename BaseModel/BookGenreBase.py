from pydantic import BaseModel, validator


class BookGenreBase(BaseModel):
    genre: str
    