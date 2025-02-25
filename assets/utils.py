from functools import reduce
import json
import time
from assets.item import ItemData


def read_json_from_file(file_path) -> dict:
    """
    Читает данные из текстового файла в формате JSON и возвращает их как словарь Python.

    :param file_path: Путь к текстовому файлу с JSON-данными.
    :return: Словарь Python с данными из файла.
    :raises ValueError: Если файл содержит некорректный JSON.
    :raises FileNotFoundError: Если файл не найден.
    """
    try:
        # Открываем файл для чтения
        with open(file_path, "r", encoding="utf-8") as file:
            # Загружаем данные из файла как JSON
            data = json.load(file)
            return data
    except FileNotFoundError:
        raise FileNotFoundError(f"Файл не найден: {file_path}")
    except json.JSONDecodeError:
        raise ValueError(f"Файл содержит некорректный JSON: {file_path}")


def secundomer(func):
    async def wrapper(*args, **kwargs):
        t1 = time.time()
        data = await func(*args, **kwargs)
        print("Время выполнения: ", time.time() - t1)
        return data

    return wrapper


def construct_inspect_link(item_data: dict, listing_id: str) -> str:
    """Формирует inspect link из данных"""
    raw_inspect_link = item_data.get("asset").get("market_actions")[0].get("link")
    asset_id = item_data.get("asset").get("id")
    return raw_inspect_link.replace("%listingid%", listing_id).replace(
        "%assetid%", asset_id
    )


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
        {"name": "Sticker | G2 Esports (Holo) | Stockholm 2024", "price": 339.85},
        {"name": "Sticker | G2 Esports (Holo) | Stockholm 2024", "price": 339.85},
    ]
    charm = {"name": "Charm | Dragon Lore", "price": 200}

    message = create_message(item_name, price, stickers, charm)
    print(message)
