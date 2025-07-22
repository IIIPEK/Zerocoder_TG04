import sqlite3

def sql_execute(db_path, query = None, data = None):

    if query:
        try:
            with sqlite3.connect(db_path) as db:
                cursor = db.cursor()
                print(query)
                if data:
                    print(data)
                    cursor.execute(query, data)
                else:
                    cursor.execute(query)
                db.commit()
                return True
        except sqlite3.Error as e:
            print(f"Ошибка при выполнении запроса: {e}")
            return False
        except Exception as e:  # Другие неожиданные ошибки
            print(f"Unexpected error: {e}")
            return False
    else:
        return False

def sql_select(db_path, query, data=None):
    """Функция для выполнения SELECT запросов"""
    if query:
        try:
            with sqlite3.connect(db_path) as db:
                cursor = db.cursor()
                if data:
                    cursor.execute(query, data)
                else:
                    cursor.execute(query)
                results = cursor.fetchall()
                print(results)
                return results
        except sqlite3.Error as e:
            print(f"Ошибка при выполнении запроса: {e}")
            return None
        except Exception as e:
            print(f"Unexpected error: {e}")
            return None
    else:
        return None

def db_create(db_path):
    query = """
     CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id BIGINT UNIQUE,
            name TEXT,
            cat1 TEXT,
            cat2 TEXT,
            cat3 TEXT,
            costs1 real,
            costs2 real,
            costs3 real
        )"""
    return sql_execute(db_path,query)

def db_add(db_path, tabel_name, data):
    columns = ', '.join(data.keys())
    placeholders = ', '.join(['?'] * len(data))
    query = f"INSERT INTO {tabel_name} ({columns}) VALUES ({placeholders})"
    return sql_execute(db_path, query, tuple(data.values()))

def db_update(db_path, tabel_name, data, cond):
    columns = '= ?, '.join(data.keys()) + ' = ?'
    query = f"UPDATE {tabel_name} SET {columns}{generate_conditions(cond)}"
    return sql_execute(db_path, query, tuple(data.values()))

def db_select(db_path, tabel_name = 'users', cond = None,):
    query = f"SELECT * FROM {tabel_name}{generate_conditions(cond)}"
    return sql_select(db_path, query)

def generate_conditions(cond):
    if cond == None:
        return ""
    condition = " and ".join(f" {k} = {v}" for k, v in cond.items())
    return f" WHERE {condition}"
