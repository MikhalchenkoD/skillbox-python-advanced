from sqlalchemy import Column, String, Integer, ARRAY

from database import Base


class Recipe(Base):
    __tablename__ = 'recipe'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    descr = Column(String)
    views = Column(Integer, default=0)
    cooking_time = Column(Integer, nullable=False)
    ingredients = Column(String, nullable=False)