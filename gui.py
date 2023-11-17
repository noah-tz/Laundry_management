import settings
from mysql_database import SqlOrders, SqlManagers, SqlVariables, SqlClients, SqlMaterial

import PySimpleGUI as sg
from typing import Callable, Type, Any



class LaundryGui:
    def __init__(self, name_laundry: str) -> None:
        self._name_laundry = name_laundry
        self._initial_window()

    def _initial_window(self) -> None:
        self._layout = [[sg.Text("enter your email")],
                              [sg.Input(key= '-email-', justification='center')],
                              [sg.Text("enter your password")],
                              [sg.Input(key= '-password-', justification='center')],
                              [sg.Button("sign in"), sg.Button("sign up"), sg.Button("forgot my password")]]
        self._title = f"welcome to {self._name_laundry}"
        self._size = settings.DEFAULT_SIZE_WINDOW
        self._window = sg.Window(self._title, self._layout, size=self._size)

    def read_window(self) -> tuple:
        return self._window.read()

    def _update_window(self, title: bool = False, size: bool = False) -> None:
        # self._window.Element("_BODY_").update(self._layout)#("_BODY_").Update(self._layout)
        # if title:
        #     self._window.set_title(self._title)
        # if size:
        #     self._window.TKroot.geometry(self._size)
        self._window.close()
        self._window = sg.Window(self._title, self._layout, size=self._size)

    def replace_to_registration_window(self) -> None:
        self._layout = [
            [sg.Text("name"), sg.InputText(key= '-name-', justification='center')],
            [sg.Text("family_name"), sg.InputText(key= '-family_name-', justification='center')],
            [sg.Text("city"), sg.InputText(key= '-city-', justification='center')],
            [sg.Text("street"), sg.InputText(key= '-street-', justification='center')],
            [sg.Text("house_number"), sg.InputText(key= '-house_number-', justification='center')],
            [sg.Text("phone"), sg.InputText(key= '-phone-', justification='center')],
            [sg.Text("email"), sg.InputText(key= '-client_email-', justification='center')],
            [sg.Text("Choose a strong password"), sg.InputText(key= '-client_password-', justification='center')],
            [sg.Text("Choose a preferred method of communication"), sg.DropDown(["email", "sms"], key= '-message_type-')],
            [sg.Button("Sign up")]
        ]
        self._title = "registration window"
        self._update_window(True)

    def replace_to_enter_window(self):
        self._window.close()
        self._initial_window()

    def replace_to_client_window(self, email_client: str):
        layout_tab_create_order = [
            [sg.Text("Please select a quantity of each product")],
            [sg.Text("shirt"), sg.DropDown([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10], key='-shirt-', default_value=0)],
            [sg.Text("pants"), sg.DropDown([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10], key='-pants-', default_value=0)],
            [sg.Text("tank top"), sg.DropDown([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10], key='-tank top-', default_value=0)],
            [sg.Text("underwear"), sg.DropDown([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10], key='-underwear-', default_value=0)],
            [sg.Text("socks"), sg.DropDown([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10], key='-socks-', default_value=0)],
            [sg.Text("coat"), sg.DropDown([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10], key='-coat-', default_value=0)],
            [sg.Text("hat"), sg.DropDown([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10], key='-hat-', default_value=0)],
            [sg.Text("sweater"), sg.DropDown([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10], key='-sweater-', default_value=0)],
            [sg.Text("curtain"), sg.DropDown([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10], key='-curtain-', default_value=0)],
            [sg.Text("tablecloth"), sg.DropDown([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10], key='-tablecloth-', default_value=0)],
            [sg.Button("Create an order", key='CREATE_IN_TAB_CREATE_ORDER')]
        ]
        layout_tab_order_pickup = [
            [sg.Text("Please enter an order number"), sg.InputText(key= '-order number-')],
            [sg.Button("OK", key='-OK_TAB_ORDER_PICKUP-')]
        ]
        column_headings = ['order ID', 'email client', 'phone client', 'order amount', 'amount items', 'order entered','order notes', 'order collected']
        sql_orders_connector = SqlOrders(email_client)
        layout_tab_order_history = [
            [sg.Table(values=sql_orders_connector.get_table(("email_client", email_client), "order_entered", settings.LIMIT_TABLES), headings=column_headings, key='-TABLE-')]
        ]
        self._layout = [
            [sg.TabGroup([
                [sg.Tab("create a new order", layout_tab_create_order, key='-TAB_CREATE_ORDER-')],
                [sg.Tab("Order pick up", layout_tab_order_pickup, key='-TAB_ORDER_PICKUP-')],
                [sg.Tab(f"Order history ({settings.LIMIT_TABLES})", layout_tab_order_history, key='-TAB_ORDER_HISTORY-')]
            ])],
            [sg.Button("close")]
        ]
        self._title = "private area"
        self._update_window(True)

    def replace_to_manager_window(self, email_client: str):
        column_headings_data = ['variable_name', 'variable_value']
        sql_variables_connector = SqlVariables("cash register")
        layout_tab_view_data = [
            [sg.Table(values=sql_variables_connector.get_table(), headings=column_headings_data, key='-TABLE_DATA-')]
        ]
        column_headings_orders = ['order ID', 'email client', 'phone client', 'order amount', 'amount items', 'order entered','order notes', 'order collected']
        sql_orders_connector = SqlOrders()
        layout_tab_order_history = [
            [sg.Table(values=sql_orders_connector.get_table(by_sort="order_entered", by_limit=settings.LIMIT_TABLES), headings=column_headings_orders, key='-TABLE_ALL_ORDERS-')]
        ]
        column_headings_clients = ['name', 'family name', 'city', 'street', 'house number', 'phone client','email client', 'password', 'message type']
        sql_clients_connector = SqlClients()
        layout_tab_clients = [
            [sg.Table(values=sql_clients_connector.get_table(by_sort="family_name", by_limit=settings.LIMIT_TABLES), headings=column_headings_clients, key='-TABLE_ALL_CLIENTS-')]
        ]
        column_headings_stock = ['material name', 'material value']
        sql_stock_connector = SqlMaterial()
        layout_tab_stock = [
            [sg.Table(values=sql_stock_connector.get_table(by_sort="material_name"), headings=column_headings_stock, key='-TABLE_ALL_STOCK-')]
        ]
        column_headings_managers = ['name', 'family name', 'city', 'street', 'house number', 'phone manager','email manager', 'password', 'message type']
        sql_managers_connector = SqlManagers()
        layout_tab_managers = [
            [sg.Table(values=sql_managers_connector.get_table(by_sort="family_name"), headings=column_headings_managers, key='-TABLE_ALL_MANAGERS-')]
        ]
        layout_tab_add_manager = [
            [sg.Text("name"), sg.InputText(key= '-name-', justification='center')],
            [sg.Text("family_name"), sg.InputText(key= '-family_name-', justification='center')],
            [sg.Text("city"), sg.InputText(key= '-city-', justification='center')],
            [sg.Text("street"), sg.InputText(key= '-street-', justification='center')],
            [sg.Text("house_number"), sg.InputText(key= '-house_number-', justification='center')],
            [sg.Text("phone"), sg.InputText(key= '-phone-', justification='center')],
            [sg.Text("email"), sg.InputText(key= '-email-', justification='center')],
            [sg.Text("Choose a strong password"), sg.InputText(key= '-password-', justification='center')],
            [sg.Text("Choose a preferred method of communication"), sg.DropDown(["email", "sms"], key= '-message_type-')],
            [sg.Button("add", key= 'ADD_MANAGER')]
        ]
        layout_tab_add_material = [
            [sg.Text("Select a material type"), sg.DropDown(list(settings.NAMES_MATERIAL), key= '-type material to add-')]
            [sg.Text("Please enter a quantity to add"), sg.InputText(key= '-quantity to add-')],
            [sg.Button("add", key='-ADD_MATERIAL-')]
        ]
        cash_register = sql_variables_connector.get_value("variable_value")
        layout_tab_cash_withdrawal = [
            [sg.Text(f"The amount in the cash register is: {cash_register}\n. Please enter an amount to withdraw"), sg.InputText(key= '-Amount to withdraw-')]
            [sg.Button("withdraw", key='-WITHDRAW_MONEY-')]
        ]
        self._layout = [
            [sg.TabGroup([
                [sg.Tab("General Information", layout_tab_view_data, key='-TAB_GENERAL_DATA-')],
                [sg.Tab(f"Orders history ({settings.LIMIT_TABLES})", layout_tab_order_history, key='-TAB_ORDERS_HISTORY-')],
                [sg.Tab(f"All clients ({settings.LIMIT_TABLES})", layout_tab_clients, key='-TAB_ALL_CLIENTS-')],
                [sg.Tab("Stock", layout_tab_stock, key='-TAB_ALL_STOCK-')],
                [sg.Tab("All managers", layout_tab_managers, key='-TAB_ALL_MANAGERS-')],
                [sg.Tab("Add manager", layout_tab_add_manager, key='-TAB_ADD_MANAGER-')],
                [sg.Tab("Add material", layout_tab_add_material, key='-TAB_ADD_MATERIAL-')],
                [sg.Tab("Cash withdrawal", layout_tab_cash_withdrawal, key='-TAB_CASH_WITHDRAWAL-')],
            ])],
            [sg.Button("close")]
        ]
        self._title = "private area"
        self._update_window(True)

    @staticmethod
    def popup_window(text: str, title: str = "", size: tuple = settings.DEFAULT_SIZE_POPUP, font: tuple = settings.DEFAULT_FONT_POPUP) -> None:
        layout = [
            [sg.Text(text, font=font)],
            [sg.Button('OK')]
        ]
        window = sg.Window(title, layout, size=size, finalize=True)
        while True:
            event, _ = window.read()
            if event in [sg.WINDOW_CLOSED, 'OK']:
                break
        window.close()


if __name__ == '__main__':
    laundry_gui = LaundryGui("My Laundry")
    laundry_gui._initial_window()

    while True:
        event, values = laundry_gui.read_window()

        if event == sg.WIN_CLOSED:
            break
        else:
            laundry_gui.replace_to_client_window("t0527184022@gmail.com")
