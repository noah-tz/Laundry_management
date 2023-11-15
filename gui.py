import settings
from mysql_database import SqlOrders

import PySimpleGUI as sg
from typing import Callable, Type, Any


class Window:
    def __init__(self, title: str, layout: list, size: tuple = settings.DEFAULT_SIZE_WINDOW) -> None:
        self.layout = layout
        self.title = title
        self.size = size
        self.window = sg.Window(self.title, self.layout, size=self.size)

    def change_window(self, title: str, layout: list) -> None:
        self.title = title
        self.layout = layout
        self.window.Element("_BODY_").Update(self.layout)



class LaundryGui:

    @staticmethod
    def make_enter_window():
        layout_main_window = [[sg.Text("enter your email")],
                              [sg.Input(key= '-email-', justification='center')],
                              [sg.Text("enter your password")],
                              [sg.Input(key= '-password-', justification='center')],
                              [sg.Button("sign in"), sg.Button("sign up"), sg.Button("forgot my password")]]
        return Window("welcome", layout_main_window)
    
    @staticmethod
    def making_registration_window():
        layout = [ [sg.Text("name"), sg.InputText(key= '-name-', justification='center')],
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
        return Window("enrollment", layout)
    
    @staticmethod
    def making_client_window(email_client) -> Window:
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
        layout_tab_group = [
            [sg.TabGroup([
                [sg.Tab("create a new order", layout_tab_create_order, key='-TAB_CREATE_ORDER-')],
                [sg.Tab("Order pick up", layout_tab_order_pickup, key='-TAB_ORDER_PICKUP-')],
                [sg.Tab("Order history", layout_tab_order_history, key='-TAB_ORDER_HISTORY-')]
            ])],
            [sg.Button("close")]
        ]
        return Window("private area", layout_tab_group)
    
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

    @staticmethod
    def cleaning_boxes(window: type[sg.Window], values: dict) -> None:
        for value in values:
            window.FindElement(value).Update('')

    


    @staticmethod
    def making_new_order_window():
        pass

