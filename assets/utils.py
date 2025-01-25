from functools import reduce
from assets.item import ItemData


def create_message(item: ItemData):

    message = f"🌟 **{item.item_name}** 🌟\n"
    message += f"Предмет #1\n"
    message += f"Ссылка: https://steamcommunity.com/market/listings/730/{item.item_name.replace(' ', '%20')}\n"
    message += f"💲 Цена SM: {item.item_price} Руб\n"

    # Стикеры
    message += f"🔖 Стикеры:\n"
    message += f"💲 Общая стоимость стикеров: {item.stickers_price} Руб\n"
    for sticker in item.stickers:
        message += f"   • {sticker['name']} - 💲 Цена: {sticker['price']} Руб\n"

    # Чары
    charm = item.charm
    if charm:
        message += f"✨ Очарование:\n"
        message += f"   • {charm['name']} - 💲 Цена: {item.charm_price} Руб\n"

    return message


if __name__ == "__main__":

    # Пример использования
    item_name = "AK-47 | Slate (Field-Tested)"
    price = 333.42
    stickers = [
        {'name': "Sticker | G2 Esports (Holo) | Stockholm 2024",
         "price": 339.85},
        {'name': "Sticker | G2 Esports (Holo) | Stockholm 2024",
         "price": 339.85}
    ]
    charm = {"name": "Charm | Dragon Lore", "price": 200}

    message = create_message(item_name, price, stickers, charm)
    print(message)
