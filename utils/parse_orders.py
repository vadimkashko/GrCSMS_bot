import aiohttp
from lxml import etree

from data.config import ORDERS_XML


# Делает запрос для получения xml с текущими заказами, парсинг xml,
# поиск по номеру заказа и возвращает словарь с информацией о заказе,
# либо False, если заказа не существует или номер заказа не принадлежит
# заказчику с указанным УНП (кодом заказчика).
async def find_order(order: dict) -> [dict, bool]:
    async with aiohttp.ClientSession() as session:
        async with session.get(ORDERS_XML) as response:
            orders = await response.text()
    root = etree.XML(orders)

    parent = None
    for element in root.iter("account_id"):
        if element.text == order["account_id"]:
            # Берет родителя элемента из-за кривой структуры xml-файла, т.к.
            # уникальный признак заказа (номер) находится во вложенном элементе,
            # а получить необходимо всю доступную информацию о заказе
            parent = element.getparent()
            break
    else:
        return False

    result = dict(parent.attrib)

    # Собирает всю информацию из найденного элемента в словарь
    for element in parent:
        if element.getchildren():
            for child in element:
                result[child.tag] = child.text
        else:
            result[element.tag] = element.text

    if result["customer_unp"] == order.get("customer_unp") or result["customer_id"] == order.get("customer_id"):
        return result
    return False

