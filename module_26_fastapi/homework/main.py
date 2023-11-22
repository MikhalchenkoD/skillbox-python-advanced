from typing import List

from fastapi import FastAPI
from sqlalchemy import select

from database import session, engine
import uvicorn
import models
import schemas

app = FastAPI()


@app.on_event("startup")
async def shutdown():
    async with engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)


@app.on_event("shutdown")
async def shutdown():
    await session.close()
    await engine.dispose()


@app.get('/recipe', response_model=List[schemas.RecipeOutFirst])
async def get_all_recipe() -> List[models.Recipe]:
    res = await session.execute(select(models.Recipe).order_by(models.Recipe.views.desc(), models.Recipe.cooking_time))
    return res.scalars().all()


@app.get('/recipe/{idx}', response_model=schemas.RecipeOutSecond)
async def get_recipe_by_id(idx: int) -> models.Recipe:
    res = await session.execute(select(models.Recipe).where(models.Recipe.id == idx))
    recipe = res.scalars().one()
    recipe.views += 1
    return recipe


@app.post('/recipe/', response_model=schemas.RecipeIn)
async def add_new_recipe(recipe: schemas.RecipeIn) -> models.Recipe:
    new_recipe = models.Recipe(name=recipe.name, descr=recipe.descr, views=recipe.views, cooking_time=recipe.cooking_time, ingredients=recipe.ingredients)
    async with session.begin():
        session.add(new_recipe)
    return new_recipe



