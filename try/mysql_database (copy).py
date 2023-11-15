from log import Logger
import mysql.connector
import pandas as pd
import settings

class SqlOrders:
    @staticmethod
    def add_order(order_id: str, email_client: str, phone_client: str, order_amount: float, amount_items: int, order_notes: str) -> None:
        cursor = MysqlDatabase._mysql_connection.cursor()
        query = "INSERT INTO orders (order_id, email_client, phone_client, order_cost, amount_items, order_notes, order_collected) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        values = (order_id, email_client, phone_client, order_amount, amount_items, order_notes, False)
        cursor.execute(query, values)
        MysqlDatabase._mysql_connection.commit()
        MysqlDatabase.print_by_pd("orders")
        

    @staticmethod
    def check_order_existence(order_id: str) -> bool:
        cursor = MysqlDatabase._mysql_connection.cursor()
        cursor.execute(
            "SELECT order_id FROM orders WHERE order_id = %s", (order_id,))
        return bool(cursor.fetchone())
    
    @staticmethod
    def get_orders_by_client_email(email_client: str) -> list[tuple]:
        cursor = MysqlDatabase._mysql_connection.cursor()
        cursor.execute(
            "SELECT * FROM orders WHERE email_client = %s ORDER BY order_entered DESC LIMIT 100",
            (email_client,)
        )
        result = cursor.fetchall()
        cursor.close()
        return result



    @staticmethod
    def check_start_ID_orders():
        # MysqlDatabase.checks_database()
        cursor = MysqlDatabase._mysql_connection.cursor()
        cursor.execute("SELECT MAX(order_id) FROM orders")
        result = cursor.fetchone()
        return settings.START_ORDERS_ID if result[0] is None else int(result[0] + 1)


class SqlClients:
    @staticmethod
    def add_client(name: str, family_name: str, city: str, street: str, house_number: int, phone_client: str, email_client: str, password_client: str, message_type: str) -> None:
        cursor = MysqlDatabase._mysql_connection.cursor()
        query = "INSERT INTO clients (name, family_name, city, street, house_number, phone_client, email_client, password_client, message_type) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
        values = (name, family_name, city, street, house_number, phone_client, email_client, password_client, message_type)
        cursor.execute(query, values)
        MysqlDatabase._mysql_connection.commit()


    @staticmethod
    def check_client_existence(email_client: str) -> bool:
        cursor = MysqlDatabase._mysql_connection.cursor()
        query = "SELECT email_client FROM clients WHERE email_client = %s"
        cursor.execute(query, (email_client,))
        result = bool(cursor.fetchone())
        cursor.close()
        return result
    
    @staticmethod
    def get_client_password(email_client: str) -> str:
        cursor = MysqlDatabase._mysql_connection.cursor()
        query = "SELECT password_client FROM clients WHERE email_client = %s"
        cursor.execute(query, (email_client,))
        result = cursor.fetchone()
        return result[0] if result is not None else ""
    
    @staticmethod
    def get_client_details(email_client: str) -> tuple[str, str, str, str, str, int, str]:
        cursor = MysqlDatabase._mysql_connection.cursor()
        query = "SELECT name, family_name, city, street, house_number, phone_client, message_type FROM clients WHERE email_client = %s"
        cursor.execute(query, (email_client,))
        result = cursor.fetchone()
        cursor.close()
        if result is None:
            return ()
        name, family_name, city, street, house_number, phone_client, message_type = result
        return name, family_name, city, street, house_number, phone_client, message_type





class SqlVariables:
    @staticmethod
    def insert_variable(variable_name: str, variable_value = None) -> None:
        cursor = MysqlDatabase._mysql_connection.cursor()
        insert_query = "INSERT INTO variables (variable_name, variable_value) VALUES (%s, %s)"
        values = (variable_name, variable_value)
        cursor.execute(insert_query, values)
        MysqlDatabase._mysql_connection.commit()

    @staticmethod
    def delete_variable(variable_name: str) -> None:
        cursor = MysqlDatabase._mysql_connection.cursor()
        delete_query = "DELETE FROM variables WHERE variable_name = %s"
        values = (variable_name,)
        cursor.execute(delete_query, values)
        MysqlDatabase._mysql_connection.commit()

    @staticmethod
    def get_variable(variable_name: str) -> str:
        cursor = MysqlDatabase._mysql_connection.cursor()
        select_query = "SELECT variable_value FROM variables WHERE variable_name = %s"
        values = (variable_name,)
        cursor.execute(select_query, values)
        return result[0] if (result := cursor.fetchone()) else None

    @staticmethod
    def update_variable(variable_name: str, new_value: str) -> None:
        cursor = MysqlDatabase._mysql_connection.cursor()
        update_query = "UPDATE variables SET variable_value = %s WHERE variable_name = %s"
        values = (new_value, variable_name)
        cursor.execute(update_query, values)
        MysqlDatabase._mysql_connection.commit()

    @staticmethod
    def check_variable_execute(name_variable) -> bool:
        cursor = MysqlDatabase._mysql_connection.cursor()
        query = "SELECT variable_name FROM variables WHERE variable_name = %s"
        cursor.execute(query, (name_variable,))
        return bool(cursor.fetchone())



    
class SqlEquipment:
    @staticmethod
    def add_type_equipment(equipment_name: str, equipment_value: int = 0) -> None:
        cursor = MysqlDatabase._mysql_connection.cursor()
        insert_query = "INSERT INTO equipment (equipment_name, equipment_value) VALUES (%s, %s)"
        values = (equipment_name, equipment_value)
        cursor.execute(insert_query, values)
        MysqlDatabase._mysql_connection.commit()

    @staticmethod
    def delete_type_equipment(equipment_name: str) -> None:
        cursor = MysqlDatabase._mysql_connection.cursor()
        delete_query = "DELETE FROM equipment WHERE equipment_name = %s"
        values = (equipment_name,)
        cursor.execute(delete_query, values)
        MysqlDatabase._mysql_connection.commit()

    @staticmethod
    def get_equipment_value(equipment_name: str) -> int or None:
        cursor = MysqlDatabase._mysql_connection.cursor()
        select_query = "SELECT equipment_value FROM equipment WHERE equipment_name = %s"
        values = (equipment_name,)
        cursor.execute(select_query, values)
        return result[0] if (result := cursor.fetchone()) else None

    @staticmethod
    def update_equipment_value(equipment_name: str, new_value: int) -> None:
        try:
            cursor = MysqlDatabase._mysql_connection.cursor()
            update_query = "UPDATE equipment SET equipment_value = %s WHERE equipment_name = %s"
            values = (new_value, equipment_name)
            cursor.execute(update_query, values)
            MysqlDatabase._mysql_connection.commit()
        except Exception as e:
            print(f"An error has occurred {e}")
        finally:
            cursor.close

    @staticmethod
    def check_equipment_execute(name_equipment) -> bool:
        cursor = MysqlDatabase._mysql_connection.cursor()
        query = "SELECT equipment_name FROM equipment WHERE equipment_name = %s"
        cursor.execute(query, (name_equipment,))
        return bool(cursor.fetchone())






class MysqlDatabase(SqlOrders, SqlClients, SqlVariables, SqlEquipment):
    """
    This class provides methods to interact with a MySQL database using the mysql-connector-python package.
    """

    # Initialize a MySQL connection object
    _mysql_connection = mysql.connector.connect(
        host=settings.HOST_SQL, user=settings.USER_SQL, password=settings.PASSWORD_SQL)

    @staticmethod
    def checks_database() -> None:
        main_cursor = MysqlDatabase._mysql_connection.cursor()
        main_cursor.execute("SHOW DATABASES")
        databases_names = [name[0] for name in main_cursor]
        if settings.NAME_DATABASE_SQL not in databases_names:
            with open("build_database.sql", "r") as fd:
                sql_instructions = fd.read()
            main_cursor.execute(sql_instructions)
        MysqlDatabase._mysql_connection = mysql.connector.connect(
            host=settings.HOST_SQL, user=settings.USER_SQL, password=settings.PASSWORD_SQL, database=settings.NAME_DATABASE_SQL)

    @staticmethod
    def read(table_name: str, command: str = "*") -> None:
        cursor = MysqlDatabase._mysql_connection.cursor()
        cursor.execute(f"SELECT {command} FROM {table_name}")
        for row in cursor:
            print(f"row = {row}")

    @staticmethod
    def column_names(table_name: str) -> list:
        cursor = MysqlDatabase._mysql_connection.cursor()
        cursor.execute(f"DESC {table_name}")
        return [row[0] for row in cursor]

    @staticmethod
    def print_by_pd(table_name: str) -> None:
        """
        Select all data from the specified table in the MySQL database using pandas and print the results.

        Args:
            table_name (str): The name of the table to select data from.

        Returns:
            None
        """
        query = f"SELECT * FROM {table_name}"
        database = pd.read_sql(query, MysqlDatabase._mysql_connection)
        print(database)

    @staticmethod
    def create(table_name: str, row_names: tuple[str], values: tuple[str]) -> None:
        cursor = MysqlDatabase._mysql_connection.cursor()
        cursor.execute(f"INSERT INTO {table_name} {row_names} VALUES {values}")
        MysqlDatabase._mysql_connection.commit()
        MysqlDatabase.print_by_pd(table_name)

    @staticmethod
    def update(table_name: str, column_name, to_update: str, column_key: str, row_key: str) -> None:
        print("Update")
        cursor = MysqlDatabase._mysql_connection.cursor()
        cursor.execute(
            f"UPDATE {table_name} SET {column_name}={to_update} WHERE {column_key}={row_key}")
        MysqlDatabase._mysql_connection.commit()
        MysqlDatabase.print_by_pd(table_name)
        cursor.close()


    @staticmethod
    def get_value_from_table(table_name: str, column_name: str, column_key: str, key: str):
        cursor = MysqlDatabase._mysql_connection.cursor()
        query = f"SELECT {column_name} FROM {table_name} WHERE {column_key} = '{key}'"
        cursor.execute(query)
        results = cursor.fetchall()
        return results[0][0] if results else None

    @Logger.log_record
    @staticmethod
    def delete(table_name: str, line_condition: str, value: str) -> None:
        print("Delete")
        cursor = MysqlDatabase._mysql_connection.cursor()
        cursor.execute(
            f"DELETE FROM {table_name} WHERE {line_condition} = '{value}'")
        MysqlDatabase._mysql_connection.commit()
        MysqlDatabase.print_by_pd(table_name)

    @Logger.log_record
    @staticmethod
    def drop_table(table_name: str) -> None:
        with MysqlDatabase._mysql_connection.cursor() as cursor:
            drop_query = f"DROP TABLE IF EXISTS {table_name}"
            cursor.execute(drop_query)
            MysqlDatabase._mysql_connection.commit()

    @Logger.log_record
    @staticmethod
    def drop_database() -> None:
        with MysqlDatabase._mysql_connection.cursor() as cursor:
            drop_query = f"DROP DATABASE IF EXISTS {settings.NAME_DATABASE_SQL}"
            cursor.execute(drop_query)
            MysqlDatabase._mysql_connection.commit()



if __name__ == '__main__':
    MysqlDatabase.checks_database()
    """
    MysqlDatabase.check_client_existence("t0527184022@gmail.com")
    MysqlDatabase.get_value_from_table("clients", "password_client", "email_client", "t0527184022@gmail.com")
    MysqlDatabase.get_client_details("t0527184022@gmail.com")
    MysqlDatabase.get_orders_by_client_email("t0527184022@gmail.com")
    MysqlDatabase.get_value_from_table('orders', 'order_collected', 'order_id', "1028")
    MysqlDatabase.update("orders", "order_collected", True, "order_id", 1027)
    """
    """
    # MysqlDatabase.delete('orders', 'client_email', 't0527184022@gmail.com')
    # MysqlDatabase.delete('clients', 'client_email', 't0527184022@gmail.com')
    # MysqlDatabase.update("clients", "client_password", "1", "client_email", "'t0527184022@gmail.com'")
    # MysqlDatabase.drop_database()
    # MysqlDatabase.checks_database()
    # MysqlDatabase.add_client("noah", "tzitrenboim", "miryamssssss",
                            # "miryam", 4444, "0500000000", "t0527184022@gmail.com", "1", "email")
    # MysqlDatabase.add_order(MysqlDatabase.check_start_ID_orders(), "t0527184022@gmail.com", "0500000000", 128, 12, None)
    # MysqlDatabase.add_order(
    #     MysqlDatabase.check_start_ID_orders(), "teyyycycyyd", 111)
    # print(MysqlDatabase.column_names("clients"))
    # print(MysqlDatabase.column_names("orders"))
    # print(MysqlDatabase.column_names("variables"))"""
    
    # sdd equipment
    """
    MysqlDatabase.add_type_equipment("powder", 20)
    MysqlDatabase.add_type_equipment("softener", 20)
    """
else:
    MysqlDatabase.checks_database()




