import mysql.connector
from typing import Any
import pandas as pd
from log import Logger
import settings
import time



class ManagerDatabase:
    _data_is_checked = False
    def __init__(self, key: Any =None):
        self._key = key
        self._key_column: str
        self._table_name: str
        self._column_names: tuple
        self._set_connector()

    def _set_connector(self):
        match ManagerDatabase._data_is_checked:
            case False:
                self._mysql_connection = mysql.connector.connect(
                    host=settings.HOST_SQL,
                    user=settings.USER_SQL,
                    password=settings.PASSWORD_SQL
                )
                self._check_database()
            case True:
                self._mysql_connection = mysql.connector.connect(
                    host=settings.HOST_SQL,
                    user=settings.USER_SQL,
                    password=settings.PASSWORD_SQL,
                    database=settings.NAME_DATABASE_SQL
                )

    def _check_database(self):
        main_cursor = self._mysql_connection.cursor()
        main_cursor.execute("SHOW DATABASES")
        databases_names = [name[0] for name in main_cursor]
        if settings.NAME_DATABASE_SQL not in databases_names:
            with open("build_database.sql", "r") as fd:
                sql_instructions = fd.read()
            self.execute(sql_instructions)
            time.sleep(1)
        ManagerDatabase._data_is_checked = True
        self._set_connector()
 
    def print_by_pd(self) -> None:
        query = f"SELECT * FROM {self._table_name}"
        database = pd.read_sql(query, self._mysql_connection)
        print(database)

    @Logger.log_record
    def execute(self, query: str, all: bool = True) -> Any:
        print(query)
        cursor = None
        result = None
        try:
            cursor = self._mysql_connection.cursor()
            cursor.execute(query)
            if all:
                result = cursor.fetchall()
            else:
                result = cursor.fetchone()
            cursor.nextset()
            self._mysql_connection.commit()
        except Exception as e:
            print(f"Error executing query: {e}")
            result = None
        finally:
            if cursor:
                cursor.close()
            return result

    def drop_table(self) -> None:
        query = f"DROP TABLE IF EXISTS {self._table_name}"
        self.execute(query)

    def add_table(self, name_table: str, column_names: tuple) -> None:
        query = f"CREATE TABLE IF NOT EXISTS {name_table} ({', '.join(column_names)})"
        self.execute(query)

    def drop_database(self) -> None:
        query = f"DROP DATABASE IF EXISTS {settings.NAME_DATABASE_SQL}"
        self.execute(query)
        ManagerDatabase._data_is_checked = False

    def check_existence(self) -> bool:
        query = f"SELECT {self._key_column} FROM {self._table_name} WHERE {self._key_column} = '{self._key}'"
        return bool(self.execute(query, False))

    def add(self, values: tuple) -> None:
        query = f"INSERT INTO {self._table_name} ({self._column_names}) VALUES {values}"
        self.execute(query)
        self.print_by_pd()

    def delete(self) -> None:
        query = f"DELETE FROM {self._table_name} WHERE {self._key_column} = '{self._key}'"
        self.execute(query)

    def get_details(self) -> tuple[str, str, str, str, str, int, str]:
        query = f"SELECT {self._column_names} FROM {self._table_name} WHERE {self._key_column} = '{self._key}'"
        return self.execute(query)

    def get_value(self, column_value: str) -> str:
        query = f"SELECT {column_value} FROM {self._table_name} WHERE {self._key_column} = '{self._key}'"
        results = self.execute(query, True)
        return results[0][0] if results else None

    def update_value(self, column_value: str, new_value) -> None:
        query = f"UPDATE {self._table_name} SET {column_value} = {new_value} WHERE {self._key_column} = '{self._key}'"
        self.execute(query)

    def get_table(self, by_key: tuple = (), by_sort: str = '' , by_limit: int = 0):
        key_select = '' if not by_key else f"WHERE {by_key[0]} = '{by_key[1]}'"
        sorted = '' if not by_sort else f"ORDER BY {by_sort}"
        limited = '' if not by_limit else f"DESC LIMIT {by_limit}"
        query = f"SELECT * FROM {self._table_name} {key_select} {sorted} {limited}"
        results = self.execute(query, True)
        return results



class SqlOrders(ManagerDatabase):
    def __init__(self, ID: int = None):
        super().__init__(ID)
        self._table_name = "orders"
        self._key_column = "order_id"
        self._column_names = "order_id, email_client, phone_client, order_cost, amount_items, order_notes, order_collected"

    def new_order_id(self):
        query = "SELECT MAX(order_id) FROM orders"
        result = self.execute(query)
        ID = settings.START_ORDERS_ID if result[0][0] is None else int(result[0][0]) +1
        self._key = ID
        return ID
    


class SqlClients(ManagerDatabase):
    def __init__(self, email: str = None):
        super().__init__(email)
        self._table_name = "clients"
        self._key_column = "email_client"
        self._column_names = "name, family_name, city, street, house_number, phone_client, email_client, password_client, message_type"

class SqlManagers(ManagerDatabase):
    def __init__(self, email: str = None):
        super().__init__(email)
        self._table_name = "managers"
        self._key_column = "email_manager"
        self._column_names = "name, family_name, city, street, house_number, phone_manager, email_manager, password_manager, message_type"

class SqlVariables(ManagerDatabase):
    def __init__(self, name: str = None):
        super().__init__(name)
        self._table_name = "variables"
        self._key_column = "variable_name"
        self._column_names = "variable_name, variable_value"

class SqlMaterial(ManagerDatabase):
    def __init__(self, name: str = None):
        super().__init__(name)
        self._table_name = "stock"
        self._key_column = "material_name"
        self._column_names = "material_name, material_value"





if __name__ == '__main__':
    # database = ManagerDatabase()
    # database.drop_database()

    # order_sql = SqlOrders(10)
    # order_sql.check_existence()


    # cash = SqlVariables()
    # cash.add(("cash register", 0))

    # client_sql = SqlClients("t0527184022@gmail.com")
    # client_sql.add(("noah", "tzitrenboim", "shemesh", "miryamssss", 3333, "0522645540", "t0527184022@gmail.com", "1", "email"))
    # client_sql.add(("dina", "tzitrenboim", "shemesh", "miryamssss", 333, "0522645540", "isacd1995@gmail.com", "1", "sms"))
    
    
    # print(client_sql.check_existence())
    # print(client_sql.get_details())
    # p = SqlMaterial("stock_powder")
    # s = SqlMaterial("stock_softener")
    # s.add(("stock powder", 80))
    # print(p.check_existence())
    # print(s.check_existence())
    # print(p.get_value("material_value"))
    # print(s.get_value("material_value"))
    # p.delete()
    # s.delete()
    pass
    

    

