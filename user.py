from laundry import LaundryRoom
from gui import LaundryGui,  sg
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
        self._email = email
        if bool(0):
            self._sql_connector: Type[ManagerDatabase]
        if connector.check_existence():
            data_of_manager = connector.get_details()[0]
            self._phone = data_of_manager[5]
            self._password = data_of_manager[7]
            self._connect_method = data_of_manager[8]
            self._sender = EmailSender(self._email) if self._connect_method == "email" else SmsSender(self._phone)

    def get_phone(self):
        return self._phone
    
    def get_email(self):
        return self._email
    
    def get_password(self):
        return self._password
    
    def get_connect_method(self):
        return self._connect_method

    def check_existence(self) -> bool:
        return self._sql_connector.check_existence()

    def sign_in(self, laundry_gui: Type[LaundryGui], laundry_room: Type[LaundryRoom] = None):
        raise NotImplementedError

    def password_recovery(self):
        if AuxiliaryFunctions.is_valid_email(self._email):
            if self._sql_connector.check_existence():
                self._sender.password_recovery(self._password)
                LaundryGui.popup_window("The password has been sent to your email address", "The password has been sent")
            else:
                LaundryGui.popup_window("The email address is not yet registered. Please select the 'sign up' option to register", "No email address found")
        else:
            LaundryGui.popup_window("invalid email address")



class Manager(User):
    def __init__(self, email: str) -> None:
        self._sql_connector = SqlManagers(email)
        super().__init__(self._sql_connector, email)

    def sign_in(self, laundry_gui: Type[LaundryGui], laundry_room: Type[LaundryRoom] = None):
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
        if name_material:
            if amount:
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
                LaundryGui.popup_window("No amount was entered.\nPlease enter a valid amount", "enter amount")
        else:
            LaundryGui.popup_window("No material type selected.\nPlease select from the list", "choose a type")

    def _withdraw_money(self, amount: int):
        if not amount:
            LaundryGui.popup_window("No amount was entered.\nPlease enter a valid amount", "enter amount")
            return
        amount = int(amount)
        informer_register = SystemData("cash register")
        if informer_register.get_value() < amount:
            LaundryGui.popup_window(f"The amount in the cash register is less than {amount}")
            return
        informer_register.change_value(-amount)
        LaundryGui.popup_window(f"Withdrawal of {amount} from the cash register was carried out successfully.\nThe remaining amount is {informer_register.get_value()}.")
        
       
    
class Client(User):
    def __init__(self, email: str) -> None:
        self._sql_connector = SqlClients(email)
        super().__init__(self._sql_connector, email)

    def sign_in(self, laundry_gui: Type[LaundryGui], laundry_room: Type[LaundryRoom] = None):
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
        sql_orders_connector = SqlOrders(order_ID)
        email_client_order = sql_orders_connector.get_value("email_client")
        if email_client_order == self._email: 
            if not sql_orders_connector.get_value('order_collected'):
                sql_orders_connector.update_value("order_collected", True)
                order_cost = sql_orders_connector.get_value('order_cost')
                informer_register = SystemData("cash register")
                informer_register.change_value(order_cost)
                LaundryGui.popup_window(f'Please complete the payment of {order_cost}\nClick OK to pay.')
                LaundryGui.popup_window(f'The payment was successful.\nOrder number {order_ID} has been collected.\nThank you!')
                self._sender.thank_you()
            else:
                LaundryGui.popup_window('Your order has already been collected')
        else:
            LaundryGui.popup_window('No order associated with you with this number was found')
    


if __name__ == '__main__':
    manager = Manager("t0527184022@gmail.com")
    manager.sign_in(LaundryGui("city_laundry"))