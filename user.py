from laundry import LaundryRoom
from gui import LaundryGui, sg
from auxiliary_functions import AuxiliaryFunctions
from mysql_database import ManagerDatabase, SqlManagers, SqlClients, SqlOrders
from messenger import EmailSender, SmsSender
from order import Order
from log import Logger
from information import StockMaterial, SystemData
import settings

from typing import Type


class User:
    def __init__(self, connector: Type[ManagerDatabase], email: str) -> None:
        """
        Initialize a User object.
        Parameters:
        - connector (Type[ManagerDatabase]): A type of ManagerDatabase for database interaction.
        - email (str): The user's email address.
        """
        self._email = email
        if bool(0):
            self._sql_connector: Type[ManagerDatabase]  # Placeholder for the type of ManagerDatabase

        if connector.check_existence():
            data_of_manager = connector.get_details()[0]
            self._phone = data_of_manager[5]
            self._password = data_of_manager[7]
            self._connect_method = data_of_manager[8]
            self._sender = EmailSender(self._email) if self._connect_method == "email" else SmsSender(self._phone)

    def get_phone(self):
        """
        Get the user's phone number.
        Returns:
        - str: The user's phone number.
        """
        return self._phone
    
    def get_email(self):
        """
        Get the user's email address.
        Returns:
        - str: The user's email address.
        """
        return self._email
    
    def get_password(self):
        """
        Get the user's password.
        Returns:
        - str: The user's password.
        """
        return self._password
    
    def get_connect_method(self):
        """
        Get the user's preferred communication method.
        Returns:
        - str: The user's communication method ("email" or "sms").
        """
        return self._connect_method

    def check_existence(self) -> bool:
        """
        Check if the user exists in the database.
        Returns:
        - bool: True if the user exists, False otherwise.
        """
        return self._sql_connector.check_existence()

    def sign_in(self, laundry_gui: Type[LaundryGui], laundry_room: Type[LaundryRoom] = None):
        """
        Placeholder for the sign-in method. To be implemented by subclasses.
        Parameters:
        - laundry_gui (Type[LaundryGui]): An instance of LaundryGui for GUI interaction.
        - laundry_room (Type[LaundryRoom]): An instance of LaundryRoom for laundry room interaction (optional).
        """
        raise NotImplementedError


class Manager(User):
    def __init__(self, email: str) -> None:
        """
        Initialize a Manager object.
        Parameters:
        - email (str): The manager's email address.
        """
        self._sql_connector = SqlManagers(email)
        super().__init__(self._sql_connector, email)

    def sign_in(self, laundry_gui: Type[LaundryGui], laundry_room: Type[LaundryRoom] = None):
        """
        Sign in as a manager and interact with the manager window.
        Parameters:
        - laundry_gui (Type[LaundryGui]): An instance of LaundryGui for GUI interaction.
        - laundry_room (Type[LaundryRoom]): An instance of LaundryRoom for laundry room interaction (optional).
        """
        laundry_gui.replace_to_manager_window(self._email)
        while True:
            event, value = laundry_gui.read_window()
            if event in [sg.WIN_CLOSED, "close"]:
                break
            match event:
                case '-ADD_MANAGER-':
                    self._add_manager(value)
                case '-ADD_MATERIAL-':
                    self._add_material(value['-TYPE_MATERIAL_TO_ADD-'], value['-AMOUNT_TO_ADD-'])
                case '-WITHDRAW_MONEY-':
                    self._withdraw_money(value['-AMOUNT_TO_WITHDRAW-'])

    def _add_manager(self, values: dict):
        """
        Add a new manager with administrative privileges.
        This method is restricted to the main manager identified by the email address in settings.EMAIL_MAIN_MANAGER.
        Parameters:
        - values (dict): A dictionary containing manager information (name, email, etc.).
        """
        if self._email == settings.EMAIL_MAIN_MANAGER:
            if not AuxiliaryFunctions.is_valid_manager_information(values):
                return
            connector_new_manager = SqlManagers(values['-EMAIL-'])
            if connector_new_manager.check_existence():
                LaundryGui.popup_window("This person is already defined as having administrative privileges.")
                return
            self._sql_connector.add(
                (
                    values['-NAME-'],
                    values['-FAMILY_NAME-'],
                    values['-CITY-'],
                    values['-STREET-'],
                    values['-HOUSE_NUMBER-'],
                    values['-PHONE-'],
                    values['-EMAIL-'],
                    values['-PASSWORD-'],
                    values['-MESSAGE_TYPE-']
                )
            )
            informer_managers_number = SystemData("number of managers")
            informer_managers_number.change_value(1)
            LaundryGui.popup_window(f"You have successfully added access privileges to {values['-NAME-']} {values['-FAMILY_NAME-']} system management")
        else:
            LaundryGui.popup_window("You cannot add administrators because you are not a primary administrator")

    def _add_material(self, name_material: str, amount: str):
        """
        Add material to the stock.
        This method checks if the manager has the necessary privileges and if the entered values are valid.
        Parameters:
        - name_material (str): The type of material to add.
        - amount (str): The amount of material to add.
        """
        if name_material:
            if AuxiliaryFunctions.input_is_number(amount):
                amount = int(amount)
                cost_material = amount / 100 * settings.COST_MATERIAL_PER_100[name_material]
                informer_register = SystemData("cash register")
                if informer_register.get_value() < cost_material:
                    LaundryGui.popup_window(f"The amount in the cash register is less than {cost_material}")
                    return
                material_stock = StockMaterial(name_material)
                material_stock.add_material(amount)
                informer_register.change_value(-cost_material)
                LaundryGui.popup_window(f"You have successfully added a total of {amount} {name_material}\nThe purchase cost is {cost_material}")
            else:
                LaundryGui.popup_window("No valid value was entered.\nPlease enter a whole number", "Enter amount")
        else:
            LaundryGui.popup_window("No material type selected.\nPlease select from the list", "Choose a type")

    def _withdraw_money(self, amount: int):
        """
        Withdraw money from the cash register.
        This method checks if the entered value is valid and if there is sufficient money in the cash register.
        Parameters:
        - amount (int): The amount of money to withdraw.
        """
        if not AuxiliaryFunctions.input_is_number(amount):
            LaundryGui.popup_window("No valid value was entered.\nPlease enter a whole number", "Enter amount")
            return
        amount = int(amount)
        informer_register = SystemData("cash register")
        if informer_register.get_value() < amount:
            LaundryGui.popup_window(f"The amount in the cash register is less than {amount}")
            return
        informer_register.change_value(-amount)
        LaundryGui.popup_window(f"Withdrawal of {amount} from the cash register was carried out successfully.\nThe remaining amount is {informer_register.get_value()}")


class Client(User):
    def __init__(self, email: str) -> None:
        """
        Initialize a Client object.
        Parameters:
        - email (str): The client's email address.
        """
        self._sql_connector = SqlClients(email)
        super().__init__(self._sql_connector, email)

    def sign_in(self, laundry_gui: Type[LaundryGui], laundry_room: Type[LaundryRoom] = None):
        """
        Sign in as a client and interact with the client window.
        Parameters:
        - laundry_gui (Type[LaundryGui]): An instance of LaundryGui for GUI interaction.
        - laundry_room (Type[LaundryRoom]): An instance of LaundryRoom for laundry room interaction (optional).
        """
        laundry_gui.replace_to_client_window(self._email)
        while True:
            event, value = laundry_gui.read_window()
            if event in [sg.WIN_CLOSED, "close"]:
                break
            elif event == '-OK_TAB_ORDER_PICKUP-':
                self._order_pickup(value['-ORDER_NUMBER-'])
            elif event == 'CREATE_IN_TAB_CREATE_ORDER':
                new_order = Order(self._email, self._phone, self._connect_method, value)
                laundry_room.enter_order(new_order)
                informer_orders = SystemData("number of orders")
                informer_orders.change_value(1)

    @Logger.log_record
    def _order_pickup(self, order_ID: int) -> None:
        """
        Process order pickup for a client.
        This method checks if the order exists, if it belongs to the client, and if it has already been collected.
        Parameters:
        - order_ID (int): The ID of the order to pick up.
        """
        sql_orders_connector = SqlOrders(order_ID)
        email_client_order = sql_orders_connector.get_value("email_client")
        if email_client_order == self._email: 
            if not sql_orders_connector.get_value('order_collected'):
                sql_orders_connector.update_value("order_collected", True)
                order_cost = sql_orders_connector.get_value('order_cost')
                LaundryGui.popup_window(f'Please complete the payment of {order_cost}\nClick OK to pay.')
                LaundryGui.popup_window(f'The payment was successful.\nOrder number {order_ID} has been collected.\nThank you!')
                informer_register = SystemData("cash register")
                informer_register.change_value(order_cost)
                self._sender.thank_you()
            else:
                LaundryGui.popup_window('Your order has already been collected')
        else:
            LaundryGui.popup_window('No order associated with you with this number was found')


