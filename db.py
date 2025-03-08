import sqlite3
from typing import Dict, List

def _get_db_connection():
    return sqlite3.connect("pizza.db", check_same_thread=False)


def _init_db(conn):
    """Инициализирует БД"""
    with open("createdb.sql", "r") as f:
        sql = f.read()
    cursor = conn.cursor()
    cursor.executescript(sql)
    conn.commit()
    conn.close()


def _check_db_exists():
    """Проверяет, инициализирована ли БД, если нет — инициализирует"""
    conn = _get_db_connection()
    cursor = conn.cursor()  
    cursor.execute("SELECT name FROM sqlite_master "
                   "WHERE type='table' AND name='products'")
    table_exists = cursor.fetchall()
    if table_exists:
        conn.close()
        return
    _init_db(conn)


def get_all_products_from_db():
    conn = _get_db_connection()
    cursor = conn.cursor()
    sql = """
SELECT 
    product_name, 
    type_name, 
    PRINTF('%.2f', price) AS price
FROM products
JOIN product_types ON type_id = product_types.id;
"""
    cursor.execute(sql)
    data = cursor.fetchall()
    conn.close()
    return data


def get_products_str() -> str:
    s = ''
    for product_tpl in get_all_products_from_db():
        s += ' | '.join(product_tpl) + '\n'
    return s


def get_products_with_prices( order: Dict) -> List[Dict]:
    """
    Получает список продуктов с их ценами из базы данных SQLite.
    :param order: JSON-структура с заказом.
    :return: Список словарей с именами продуктов и их ценами.
    """
    conn = _get_db_connection()
    cursor = conn.cursor()
    
    
    for item in order.get("items", []):
        name = item["name"]
        cursor.execute("SELECT price FROM products WHERE product_name = ?", (name,))
        row = cursor.fetchone()
        
        if row:
            item["price"] = row[0]
        else:
            item["price"] =  0 # Если цена не найдена
    
    conn.close()
    return order


_check_db_exists()