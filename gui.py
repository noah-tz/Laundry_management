import settings
from mysql_database import SqlOrders

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
        sql_client_connector = SqlOrders(email_client)
        layout_tab_order_history = [
            [sg.Table(values=sql_client_connector.get_orders(email_client), headings=column_headings, key='-TABLE-')]
        ]
        self._layout = [
            [sg.TabGroup([
                [sg.Tab("create a new order", layout_tab_create_order, key='-TAB_CREATE_ORDER-')],
                [sg.Tab("Order pick up", layout_tab_order_pickup, key='-TAB_ORDER_PICKUP-')],
                [sg.Tab("Order history", layout_tab_order_history, key='-TAB_ORDER_HISTORY-')]
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
