import mysql.connector
import hashlib
from typing import Any
import pandas as pd
from log import Logger
import settings
import time


class ManagerDatabase:
    """
    A class for managing database operations using MySQL.

    Attributes:
        _data_is_checked (bool): A class variable to track whether the database has been checked.
        _key (Any): A key parameter for database operations.
        _key_column (str): The column used as the key in database operations.
        _table_name (str): The name of the table in the database.
        _column_names (tuple): Tuple of column names in the database table.
        _mysql_connection (mysql.connector.connection.MySQLConnection): MySQL connection object.

    Methods:
        __init__(self, key: Any = None): Constructor method to initialize the ManagerDatabase instance.
        _set_connector(self): Set up the MySQL connection based on whether the database has been checked.
        _check_database(self): Check if the specified database exists; create if not.
        print_by_pd(self) -> None: Print the entire database using Pandas DataFrame.
        execute(self, query: str, all: bool = True) -> Any: Execute a SQL query on the database.
        drop_table(self) -> None: Drop the database table if it exists.
        add_table(self, name_table: str, column_names: tuple) -> None: Create a new database table.
        drop_database(self) -> None: Drop the entire database.
        check_existence(self) -> bool: Check if a record with the specified key exists.
        add(self, values: tuple) -> None: Insert a new record into the database.
        delete(self) -> None: Delete a record from the database based on the key.
        get_details(self) -> tuple[str, str, str, str, str, int, str]: Retrieve details of a specific record.
        get_value(self, column_value: str) -> str: Get a specific value from the database for the given key.
        update_value(self, column_value: str, new_value) -> None: Update a specific value in the database.
        get_table(self, by_key: tuple = (), by_sort: str = '', by_limit: int = 0): Retrieve records from the database table.

    """

    _data_is_checked = False

    def __init__(self, key: Any = None):
        """
        Constructor method to initialize the ManagerDatabase instance.
        Args:
            key (Any): A key parameter for database operations.
        """
        self._key = key
        self._key_column: str
        self._table_name: str
        self._column_names: tuple
        self._set_connector()

    def _set_connector(self):
        """
        Set up the MySQL connection based on whether the database has been checked.
        """
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
        """
        Check if the specified database exists; create if not.
        """
        main_cursor = self._mysql_connection.cursor()
        main_cursor.execute("SHOW DATABASES")
        databases_names = [name[0] for name in main_cursor]
        if settings.NAME_DATABASE_SQL not in databases_names:
            with open("build_database.sql", "r") as fd:
                sql_instructions = fd.read()
            self.execute(sql_instructions)
            time.sleep(1) # laundry database created
        ManagerDatabase._data_is_checked = True
        self._set_connector()

    def print_by_pd(self) -> None:
        """
        Print the entire database using Pandas DataFrame.
        """
        query = f"SELECT * FROM {self._table_name}"
        database = pd.read_sql(query, self._mysql_connection)
        print(database)

    @Logger.log_record
    def execute(self, query: str, all: bool = True) -> Any:
        """
        Execute a SQL query on the database.
        Args:
            query (str): The SQL query to execute.
            all (bool): Flag to fetch all results or only the first one.
        Returns:
            Any: The result of the query.
        """
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
        """
        Drop the database table if it exists.
        """
        query = f"DROP TABLE IF EXISTS {self._table_name}"
        self.execute(query)

    def add_table(self, name_table: str, column_names: tuple) -> None:
        """
        Create a new database table.
        Args:
            name_table (str): The name of the new table.
            column_names (tuple): Tuple of column names for the new table.
        """
        query = f"CREATE TABLE IF NOT EXISTS {name_table} ({', '.join(column_names)})"
        self.execute(query)

    def drop_database(self) -> None:
        """
        Drop the entire database.
        """
        query = f"DROP DATABASE IF EXISTS {settings.NAME_DATABASE_SQL}"
        self.execute(query)
        ManagerDatabase._data_is_checked = False

    def check_existence(self) -> bool:
        """
        Check if a record with the specified key exists.
        Returns:
            bool: True if the record exists, False otherwise.
        """
        query = f"SELECT {self._key_column} FROM {self._table_name} WHERE {self._key_column} = '{self._key}'"
        return bool(self.execute(query, False))

    def add(self, values: tuple) -> None:
        """
        Insert a new record into the database.
        Args:
            values (tuple): Tuple of values to be inserted.
        """
        query = f"INSERT INTO {self._table_name} ({self._column_names}) VALUES {values}"
        self.execute(query)
        self.print_by_pd()

    def delete(self) -> None:
        """
        Delete a record from the database based on the key.
        """
        query = f"DELETE FROM {self._table_name} WHERE {self._key_column} = '{self._key}'"
        self.execute(query)

    def get_details(self) -> tuple[str, str, str, str, str, int, str]:
        """
        Retrieve details of a specific record.
        Returns:
            tuple: Details of the record.
        """
        query = f"SELECT {self._column_names} FROM {self._table_name} WHERE {self._key_column} = '{self._key}'"
        return self.execute(query)

    def get_value(self, column_value: str) -> str:
        """
        Get a specific value from the database for the given key.
        Args:
            column_value (str): The column for which to retrieve the value.
        Returns:
            str: The value of the specified column for the given key.
        """
        query = f"SELECT {column_value} FROM {self._table_name} WHERE {self._key_column} = '{self._key}'"
        results = self.execute(query, True)
        return results[0][0] if results else None

    def update_value(self, column_value: str, new_value) -> None:
        """
        Update a specific value in the database.
        Args:
            column_value (str): The column to be updated.
            new_value: The new value for the specified column.
        """
        query = f"UPDATE {self._table_name} SET {column_value} = {new_value} WHERE {self._key_column} = '{self._key}'"
        self.execute(query)

    def get_table(self, by_key: tuple = (), by_sort: str = '', by_limit: int = 0):
        """
        Retrieve records from the database table.
        Args:
            by_key (tuple): A tuple containing the key column and its value for filtering.
            by_sort (str): The column by which to sort the results.
            by_limit (int): The maximum number of records to retrieve.

        Returns:
            Any: The result of the query.
        """
        key_select = '' if not by_key else f"WHERE {by_key[0]} = '{by_key[1]}'"
        sorted = '' if not by_sort else f"ORDER BY {by_sort}"
        limited = '' if not by_limit else f"DESC LIMIT {by_limit}"
        query = f"SELECT * FROM {self._table_name} {key_select} {sorted} {limited}"
        results = self.execute(query, True)
        return results
    
    @staticmethod    
    def hash_password(password):
        """
        Hashes a password using the SHA-256 algorithm.

        Args:
            password: The password to hash.

        Returns:
            The hashed password.
        """

        hash_object = hashlib.sha256()
        hash_object.update(password.encode())
        return hash_object.hexdigest()


class SqlOrders(ManagerDatabase):
    """
    A class for managing orders in the database, inheriting from ManagerDatabase.
    Attributes:
        (Inherited attributes from ManagerDatabase)
    Methods:
        __init__(self, ID: int = None): Constructor method to initialize the SqlOrders instance.
        new_order_id(self): Get a new order ID.
    """

    def __init__(self, ID: int = None):
        """
        Constructor method to initialize the SqlOrders instance.
        Args:
            ID (int): The order ID.
        """
        super().__init__(ID)
        self._table_name = "orders"
        self._key_column = "order_id"
        self._column_names = "order_id, email_client, phone_client, order_cost, amount_items, order_notes, order_collected"

    def new_order_id(self):
        """
        Get a new order ID.
        Returns:
            int: The new order ID.
        """
        query = "SELECT MAX(order_id) FROM orders"
        result = self.execute(query)
        ID = settings.START_ORDERS_ID if result[0][0] is None else int(result[0][0]) + 1
        self._key = ID
        return ID

class SqlClients(ManagerDatabase):
    """
    A class for managing clients in the database, inheriting from ManagerDatabase.
    Attributes:
        (Inherited attributes from ManagerDatabase)
    Methods:
        __init__(self, email: str = None): Constructor method to initialize the SqlClients instance.
    """

    def __init__(self, email: str = None):
        """
        Constructor method to initialize the SqlClients instance.
        Args:
            email (str): The email of the client.
        """
        super().__init__(email)
        self._table_name = "clients"
        self._key_column = "email_client"
        self._column_names = "name, family_name, city, street, house_number, phone_client, email_client, password_client, message_type"


class SqlManagers(ManagerDatabase):
    """
    A class for managing managers in the database, inheriting from ManagerDatabase.
    Attributes:
        (Inherited attributes from ManagerDatabase)
    Methods:
        __init__(self, email: str = None): Constructor method to initialize the SqlManagers instance.
    """

    def __init__(self, email: str = None):
        """
        Constructor method to initialize the SqlManagers instance.
        Args:
            email (str): The email of the manager.
        """
        super().__init__(email)
        self._table_name = "managers"
        self._key_column = "email_manager"
        self._column_names = "name, family_name, city, street, house_number, phone_manager, email_manager, password_manager, message_type"


class SqlSystemData(ManagerDatabase):
    """
    A class for managing system data in the database, inheriting from ManagerDatabase.
    Attributes:
        (Inherited attributes from ManagerDatabase)
    Methods:
        __init__(self, name: str = None): Constructor method to initialize the SqlSystemData instance.
    """

    def __init__(self, name: str = None):
        """
        Constructor method to initialize the SqlSystemData instance.
        Args:
            name (str): The name of the system data.
        """
        super().__init__(name)
        self._table_name = "variables"
        self._key_column = "variable_name"
        self._column_names = "variable_name, variable_value"


class SqlMaterial(ManagerDatabase):
    """
    A class for managing materials in the database, inheriting from ManagerDatabase.
    Attributes:
        (Inherited attributes from ManagerDatabase)
    Methods:
        __init__(self, name: str = None): Constructor method to initialize the SqlMaterial instance.
    """

    def __init__(self, name: str = None):
        """
        Constructor method to initialize the SqlMaterial instance.
        Args:
            name (str): The name of the material.
        """
        super().__init__(name)
        self._table_name = "stock"
        self._key_column = "material_name"
        self._column_names = "material_name, material_value"



