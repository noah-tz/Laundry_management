import mysql.connector
from typing import Any
import pandas as pd
from log import Logger
import settings



class ManagerDatabase:
    def __init__(self):
        self._table_name: str
        self._key_column: str
        self._column_names: tuple
        self._mysql_connection = mysql.connector.connect(
            host=settings.HOST_SQL, user=settings.USER_SQL, password=settings.PASSWORD_SQL)
        self._check_database()

    def _check_database(self):
        main_cursor = self._mysql_connection.cursor()
        main_cursor.execute("SHOW DATABASES")
        databases_names = [name[0] for name in main_cursor]
        if settings.NAME_DATABASE_SQL not in databases_names:
            with open("build_database.sql", "r") as fd:
                sql_instructions = fd.read()
            main_cursor.execute(sql_instructions)
        self._mysql_connection = mysql.connector.connect(
            host=settings.HOST_SQL, user=settings.USER_SQL, password=settings.PASSWORD_SQL, database=settings.NAME_DATABASE_SQL)
        
    def print_by_pd(self) -> None:
        query = f"SELECT * FROM {self._table_name}"
        database = pd.read_sql(query, self._mysql_connection)
        print(database)


    @Logger.log_record
    def execute(self, query: str, all: bool = True) -> Any:
        cursor = None
        result = None
        try:
            cursor = self._mysql_connection.cursor()
            cursor.execute(query)
            if all:
                result = cursor.fetchall()
            else:
                result = cursor.fetchone()
            self._mysql_connection.commit()
        except Exception as e:
            print(f"Error executing query: {e}")
        finally:
            if cursor:
                cursor.close()
            return result

    @Logger.log_record
    def add_table(self, name_table: str, column_names: tuple) -> None:
        query = f"CREATE TABLE IF NOT EXISTS {name_table} ({', '.join(column_names)})"
        self.execute(query)

    @Logger.log_record
    def drop_table(self) -> None:
        query = f"DROP TABLE IF EXISTS {self._table_name}"
        self.execute(query)

    @Logger.log_record
    def drop_database(self) -> None:
        query = f"DROP DATABASE IF EXISTS {settings.NAME_DATABASE_SQL}"
        self.execute(query)
            

    def check_existence(self, key: str) -> bool:
        query = f"SELECT {self._key_column} FROM {self._table_name} WHERE {self._key_column} = {key}"
        return bool(self.execute(query))

    def add(self, values: tuple) -> None:
        query = f"INSERT INTO {self._table_name} ({self._column_names}) VALUES {values}"
        self.execute(query)
        self.print_by_pd(f"{self._table_name}")

    def delete(self, key: str) -> None:
        query = f"DELETE FROM ({self._table_name}) WHERE {self._key_column} = {key}"
        self.execute(query)

    def get_details(self, key: str) -> tuple[str, str, str, str, str, int, str]:
        query = f"SELECT ({self._column_names}) FROM clients WHERE email_client = {key}"
        return self.execute(query)

    def get_value(self, key: str, column_value: str) -> str:
        query = f"SELECT {column_value} FROM {self._table_name} WHERE {self._key_column} = {key}"
        results = self.execute(query, True)
        return results[0][0] if results else None

    def update_value(self, key: str, column_value: str, new_value) -> None:
        query = f"UPDATE {self._table_name} SET {column_value} = {new_value} WHERE {self._key_column} = {key}"
        self.execute(query)


class SqlOrders(ManagerDatabase):
    def __init__(self):
        super().__init__()
        self._table_name = "orders"
        self._key_column = "email_client"
        self._column_names = "order_id, email_client, phone_client, order_cost, amount_items, order_notes, order_collected"

    def check_start_ID_orders(self):
        query = "SELECT MAX(order_id) FROM orders"
        result = self.execute(query)
        return settings.START_ORDERS_ID if result[0] is None else int(result[0] + 1)
    
    def get_orders(self, email_client: str) -> list[tuple]:
        query = f"SELECT * FROM orders WHERE email_client = {email_client} ORDER BY order_entered DESC LIMIT 100"
        results = self.execute(query, True)
        return results



class SqlClients(ManagerDatabase):
    def __init__(self):
        super().__init__()
        self._table_name = "clients"
        self._key_column = "email_client"
        self._column_names = "name, family_name, city, street, house_number, phone_client, email_client, password_client, message_type"


class SqlVariables(ManagerDatabase):
    def __init__(self):
        super().__init__()
        self._table_name = "variables"
        self._key_column = "variable_name"
        self._column_names = "variable_name, variable_value"

class SqlEquipment(ManagerDatabase):
    def __init__(self):
        super().__init__()
        self._table_name = "equipment"
        self._key_column = "equipment_name"
        self._column_names = "equipment_name, equipment_value"



    

