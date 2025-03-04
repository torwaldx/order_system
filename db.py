import sqlite3

conn = sqlite3.connect("pizza.db")
cursor = conn.cursor()


def _init_db():
    """Инициализирует БД"""
    with open("createdb.sql", "r") as f:
        sql = f.read()
    cursor.executescript(sql)
    conn.commit()


def _check_db_exists():
    """Проверяет, инициализирована ли БД, если нет — инициализирует"""
    cursor.execute("SELECT name FROM sqlite_master "
                   "WHERE type='table' AND name='products'")
    table_exists = cursor.fetchall()
    if table_exists:
        return
    _init_db()


def get_all_products_from_db():
    sql = """
SELECT 
    product_name, 
    type_name, 
    PRINTF('%.2f', price) AS price
FROM products
JOIN product_types ON type_id = product_types.id;
"""
    cursor.execute(sql)
    return cursor.fetchall()


def get_products_str() -> str:
    s = ''
    for product_tpl in get_all_products_from_db():
        s += ' | '.join(product_tpl) + '\n'
    return s


_check_db_exists()