import os

file_path = os.path.join(os.getcwd(), "recipe.txt")

def load_recipes(filename):
    recipes = {}
    with open(filename, "r", encoding="utf-8") as f:
        lines = [line.rstrip("\n") for line in f]

    i = 0
    while i < len(lines):
        title = lines[i].strip()
        i += 1
        if i >= len(lines):
            break

        count_line = lines[i].strip()
        n = int(count_line)
        i += 1

        ingredients = []
        for _ in range(n):
            ing = (lines[i].strip().split("|"))
            ingredients_name = ing[0]
            quantity = int(ing[1])
            measure = ing[2]
            i += 1
            ingredients.append({'ingredient_name': ingredients_name,
                                'quantity': quantity, 'measure': measure})

        # Пропускаем пустую строку-разделитель
        if i < len(lines) and lines[i] == "":
            i += 1

        recipes[title] = ingredients

    return recipes

# --- Кулинарная книга ---
cook_book = load_recipes(file_path)

def get_shop_list_by_dishes(dishes, person_count):
    shop_list = {}
    for dish in dishes:
        if dish not in cook_book:
            raise ValueError(f"Блюдо '{dish}' отсутствует "
                             f"в кулинарной книге")
        for ingredient in cook_book[dish]:
            name = ingredient['ingredient_name']
            measure = ingredient['measure']
            qty_per_person = int(ingredient['quantity'])
            needed = qty_per_person * person_count
            if name not in shop_list:
                shop_list[name] = {'measure': measure, 'quantity': needed}
            else:
                shop_list[name]['quantity'] += needed
    return shop_list


print(get_shop_list_by_dishes(['Омлет', 'Фахитос'], 2))