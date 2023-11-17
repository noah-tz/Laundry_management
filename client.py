from log import Logger
from mysql_database import SqlClients, SqlOrders
from messenger import EmailSender, SmsSender

from gui import LaundryGui


class Client:
    clients = {}
    def __init__(self, email: str) -> None:
        self._sql_client_connector = SqlClients(email)
        data_of_client = self._sql_client_connector.get_details()[0]
        self._phone_client = data_of_client[5]
        self._email_client = data_of_client[6]
        self._password = data_of_client[7]
        self._connect_method = data_of_client[8]

    def get_phone(self):
        return self._phone_client
    
    def get_email(self):
        return self._email_client
    
    def get_password(self):
        return self._password
    
    def get_connect_method(self):
        return self._connect_method

    @Logger.log_record    
    def order_pickup(self, order_ID: int) -> None:
        sql_orders_connector = SqlOrders(order_ID)
        email_client_order = sql_orders_connector.get_value("email_client")
        if email_client_order == self._email_client: 
            if not sql_orders_connector.get_value('order_collected'):
                sql_orders_connector.update_value("order_collected", True)
                order_cost = sql_orders_connector.get_value('order_cost')
                LaundryGui.popup_window(f'Please complete the payment of {order_cost}\nClick OK to pay.')
                LaundryGui.popup_window(f'The payment was successful.\nOrder number {order_ID} has been collected.\nThank you!')
                sender = EmailSender(self._email_client) if self._connect_method == "email" else SmsSender(self._phone_client)
                sender.thank_you()
            else:
                LaundryGui.popup_window('Your order has already been collected')
        else:
            LaundryGui.popup_window('No order associated with you with this number was found')
    







if __name__ == '__main__':
    noah = Client("0527184022", "noah", "tzitrenboim", "bet shemesh", "miryam", 12, "t0527184022@gmail.com", "2345")
    noah.open_order()