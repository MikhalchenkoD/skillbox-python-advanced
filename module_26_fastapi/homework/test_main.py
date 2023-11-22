from main import app
from fastapi.testclient import TestClient

client = TestClient(app)


def test_add_new_recipe():
    response = client.post(
        "/recipe/",
        json={
            "name": "плов",
            "views": 0,
            "cooking_time": 30,
            "ingredients": "морковь, мясо, рис",
            "descr": "крутое блюдо"
        },
    )
    assert response.status_code == 200
    assert response.json() == {
        "name": "плов",
        "views": 0,
        "cooking_time": 30,
        "ingredients": "морковь, мясо, рис",
        "descr": "крутое блюдо"
    }


def test_get_recipe_bad_id():
    value = 'one'
    response = client.get(f"/recipe/{value}")
    assert response.status_code == 422
    assert response.json() == {"detail": [{"type": "int_parsing", "loc": ["path", "idx"],
                                           "msg": "Input should be a valid integer, unable to parse string as an integer",
                                           "input": f"{value}",
                                           "url": "https://errors.pydantic.dev/2.4/v/int_parsing"}]}


def test_get_recipe_by_id():
    response = client.get("/recipe/1")
    assert response.status_code == 200
    assert response.json() == {
        "name": "Плов",
        "cooking_time": 30,
        "ingredients": "Морковь,Мясо,Рис",
        "descr": "Крутое блюдо"
    }


def test_get_all_recipe():
    response = client.get("/recipe")
    assert response.status_code == 200
    assert response.json() == [
        {
            "name": "Плов",
            "views": 0,
            "cooking_time": 30
        },
        {
            "name": "плов",
            "views": 0,
            "cooking_time": 30
        },
        {
            "name": "плов",
            "views": 0,
            "cooking_time": 30
        },
        {
            "name": "плов",
            "views": 0,
            "cooking_time": 30
        },
        {
            "name": "плов",
            "views": 0,
            "cooking_time": 30
        },
        {
            "name": "плов",
            "views": 0,
            "cooking_time": 30
        }
    ]
