import os
import sys
import pytest

# Подключаем main.py как модуль: добавляем корень проекта в путь
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

from main import load_recipes, get_shop_list_by_dishes


@pytest.fixture
def cook_book():
    file_path = os.path.join(os.getcwd(), "recipe.txt")
    return load_recipes(file_path)


def test_correct_calculation_for_one_person(cook_book):
    # Переопределим cook_book внутри теста, чтобы не зависеть от глобального состояния
    # Но для простоты здесь используем фикстуру, а в реальном проекте лучше передавать cook_book аргументом
    shop_list = get_shop_list_by_dishes(["Омлет"], 1)
    assert "Яйцо" in shop_list
    assert shop_list["Яйцо"]["quantity"] == 2
    assert shop_list["Яйцо"]["measure"] == "шт"


def test_calculation_for_multiple_persons(cook_book):
    shop_list = get_shop_list_by_dishes(["Омлет"], 2)
    assert shop_list["Яйцо"]["quantity"] == 4
    assert shop_list["Молоко"]["quantity"] == 200
    assert shop_list["Помидор"]["quantity"] == 4


def test_same_ingredient_in_multiple_dishes(cook_book):
    # Омлет и Фахитос оба используют Помидор
    shop_list = get_shop_list_by_dishes(["Омлет", "Фахитос"], 1)
    # В Омлете: 2 шт, в Фахитосе: 2 шт → итого 4 шт
    assert shop_list["Помидор"]["quantity"] == 4
    assert shop_list["Помидор"]["measure"] == "шт"


def test_missing_dish_raises_error(cook_book):
    with pytest.raises(ValueError) as exc_info:
        get_shop_list_by_dishes(["Неизвестное блюдо"], 1)
    assert "отсутствует" in str(exc_info.value)


def test_empty_dishes_list_returns_empty_dict(cook_book):
    shop_list = get_shop_list_by_dishes([], 1)
    assert shop_list == {}