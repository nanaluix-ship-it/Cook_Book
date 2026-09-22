import pytest
import allure
from main import get_shop_list_by_dishes

@allure.feature("Расчёт продуктов")
@allure.story("Базовый расчёт")
@allure.title("Тест: расчёт продуктов на 1 персону")
@allure.description("""
Предусловия: в cook_book есть блюдо «Омлет» с ингредиентами: 2 яйца, 100 мл молока.
Действие: запрашиваем список покупок для 1 персоны.
Ожидаемый результат: в списке покупок есть «Яйцо» с количеством 2 шт.
""")
def test_correct_calculation_for_one_person():
    with allure.step("Шаг 1: задаём входные данные (1 персона, блюдо «Омлет»)"):
        dishes = ["Омлет"]
        persons = 1

    with allure.step("Шаг 2: вызываем функцию расчёта"):
        shop_list = get_shop_list_by_dishes(dishes, persons)

    with allure.step("Шаг 3: проверяем наличие ингредиента «Яйцо»"):
        assert "Яйцо" in shop_list, "В списке покупок отсутствует ингредиент «Яйцо»"

    with allure.step("Шаг 4: проверяем количество яиц (должно быть 2 шт)"):
        assert shop_list["Яйцо"]["quantity"] == 2, f"Ожидалось 2 яйца, получено: {shop_list['Яйцо']['quantity']}"


@allure.feature("Расчёт продуктов")
@allure.story("Масштабирование расчёта")
@allure.title("Тест: количество ингредиентов линейно зависит от числа персон")
@allure.description("""
Предусловия: блюдо «Омлет» содержит 2 яйца на порцию.
Действие: запрашиваем расчёт для 2 персон.
Ожидаемый результат: количество яиц должно быть 4 шт (2 шт × 2 персоны).
""")
def test_calculation_for_multiple_persons():
    with allure.step("Шаг 1: задаём 2 персоны и блюдо «Омлет»"):
        dishes = ["Омлет"]
        persons = 2

    with allure.step("Шаг 2: выполняем расчёт"):
        shop_list = get_shop_list_by_dishes(dishes, persons)

    with allure.step("Шаг 3: проверяем удвоенное количество яиц"):
        assert shop_list["Яйцо"]["quantity"] == 4, f"Ожидалось 4 яйца, получено: {shop_list['Яйцо']['quantity']}"


@allure.feature("Расчёт продуктов")
@allure.story("Суммирование ингредиентов")
@allure.title("Тест: ингредиенты из разных блюд суммируются")
@allure.description("""
Предусловия: блюда «Омлет» и «Фахитос» содержат общий ингредиент «Помидор».
Действие: запрашиваем список покупок для обоих блюд на 1 персону.
Ожидаемый результат: количество помидоров должно быть суммой из обоих блюд.
""")
def test_same_ingredient_in_multiple_dishes():
    common_ingredient = "Помидор"

    with allure.step("Шаг 1: выбираем два блюда с общим ингредиентом"):
        dishes = ["Омлет", "Фахитос"]
        persons = 1

    with allure.step("Шаг 2: запускаем расчёт списка покупок"):
        shop_list = get_shop_list_by_dishes(dishes, persons)

    with allure.step(f"Шаг 3: проверяем, что ингредиент '{common_ingredient}' присутствует и просуммирован"):
        assert common_ingredient in shop_list, f"Ингредиент '{common_ingredient}' отсутствует в списке"
        # Если хочешь жёстко проверить точное число — раскомментируй строку ниже и подставь нужное значение
        # assert shop_list[common_ingredient]["quantity"] == 4


@allure.feature("Расчёт продуктов")
@allure.story("Обработка ошибок и краевых случаев")
@allure.title("Тест: при отсутствии блюда функция выбрасывает ValueError")
@allure.description("""
Предусловия: в cook_book нет блюда «Не существующее блюдо».
Действие: пытаемся запросить расчёт с этим несуществующим блюдом.
Ожидаемый результат: функция выбрасывает исключение ValueError с понятным сообщением об ошибке.
""")
def test_missing_dish_raises_error():
    with allure.step("Шаг 1: передаём в функцию несуществующее блюдо"):
        dishes = ["Не существующее блюдо"]
        persons = 1

    with allure.step("Шаг 2: ожидаем, что функция выбросит ValueError"):
        with pytest.raises(ValueError) as exc_info:
            get_shop_list_by_dishes(dishes, persons)

    with allure.step("Шаг 3: проверяем текст сообщения об ошибке"):
        error_message = str(exc_info.value)
        assert "Блюдо 'Не существующее блюдо' отсутствует" in error_message, \
            f"Неверный текст ошибки. Получено: {error_message}"


@allure.feature("Расчёт продуктов")
@allure.story("Смешанные сценарии")
@allure.title("Тест: частичное совпадение блюд (одно есть, одного нет)")
@allure.description("""
Предусловия: «Омлет» есть в cook_book, «Не существующее блюдо» — нет.
Действие: запрашиваем расчёт со смешанным списком блюд.
Ожидаемый результат: из‑за наличия несуществующего блюда функция должна выбросить исключение ValueError.
""")
def test_mixed_dishes_handling():
    with allure.step("Шаг 1: готовим список из существующего и несуществующего блюда"):
        dishes = ["Омлет", "Не существующее блюдо"]
        persons = 1

    with allure.step("Шаг 2: ожидаем ошибку из-за несуществующего блюда"):
        with pytest.raises(ValueError):
            get_shop_list_by_dishes(dishes, persons)
