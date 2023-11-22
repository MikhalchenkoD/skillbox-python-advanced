from typing import List
from pydantic import BaseModel


class RecipeIn(BaseModel):
    name: str
    views: int
    cooking_time: int
    ingredients: str
    descr: str


class RecipeOutFirst(BaseModel):
    name: str
    views: int
    cooking_time: int

    class Config:
        from_attributes = True


class RecipeOutSecond(BaseModel):
    name: str
    cooking_time: int
    ingredients: str
    descr: str

    class Config:
        from_attributes = True
