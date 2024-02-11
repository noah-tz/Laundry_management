import settings
from mysql_database import SqlOrders, SqlManagers, SqlSystemData, SqlClients, SqlMaterial
from log import Logger

import PySimpleGUI as sg




class LaundryGui:
    def __init__(self, name_laundry: str) -> None:
        """
        Constructor for the LaundryGui class.

        Parameters:
        - name_laundry (str): Name of the laundry.

        Returns:
        None
        """
        self._name_laundry = name_laundry
        self._initial_window()

    @Logger.log_record
    def _initial_window(self) -> None:
        """
        Creates the initial window layout for the LaundryGui.

        Returns:
        None
        """
        size_win = sg.Window.get_screen_size()

        layout_client_enter = [
            [sg.Text("enter your email")],
            [sg.Input(key= '-email_client-', justification='center')],
            [sg.Text("enter your password")],
            [sg.Input(key= '-password_client-', justification='center')],
            [sg.Button("sign in", key='-sign_in_client-')]
        ]
        layout_manager_enter = [
            [sg.Text("enter your email")],
            [sg.Input(key= '-email_manager-', justification='center')],
            [sg.Text("enter your password")],
            [sg.Input(key= '-password_manager-', justification='center')],
            [sg.Button("sign in", key='-sign_in_manager-')]
        ]
        layout_registration = [
            [sg.Text("name"), sg.InputText(key= '-name_registration-', justification='center')],
            [sg.Text("family_name"), sg.InputText(key= '-family_name_registration-', justification='center')],
            [sg.Text("city"), sg.InputText(key= '-city_registration-', justification='center')],
            [sg.Text("street"), sg.InputText(key= '-street_registration-', justification='center')],
            [sg.Text("house_number"), sg.InputText(key= '-house_number_registration-', justification='center')],
            [sg.Text("phone"), sg.InputText(key= '-phone_registration-', justification='center')],
            [sg.Text("email"), sg.InputText(key= '-email_registration-', justification='center')],
            [sg.Text("Choose a strong password"), sg.InputText(key= '-password_registration-', justification='center')],
            [sg.Text("Choose a preferred method of communication"), sg.DropDown(["email", "sms"], key= '-message_type_registration-')],
            [sg.Button("Sign up", key='-registration-')]
        ]
        self._layout = [
            [
                sg.TabGroup(
                    [
                        [sg.Tab("client enter", layout_client_enter, key='-CLIENT ENTER-')],
                        [sg.Tab("manager enter", layout_manager_enter, key='-MANAGER ENTER-')],
                        [sg.Tab("Sign up", layout_registration, key='-REGISTRATION-')]
                    ],
                    size=size_win
                )
            ],
            [sg.Button("close")]
        ]
        self._title = f"welcome to {self._name_laundry}"
        self._size = settings.DEFAULT_SIZE_WINDOW
        self._column = sg.Column(self._layout, key='-COLUMN-')
        self._window = sg.Window(self._title, [[self._column]], size=self._size)

    def read_window(self) -> tuple[str, dict[str, str]]:
        """
        Reads the current window and returns the event and values.

        Returns:
        tuple: Event and values read from the window.
        """
        return self._window.read()

    def _update_window(self, title: str = '', size: tuple = '') -> None:
        """
        Updates the window with a new layout.

        Parameters:
        - title (str): New title for the window.
        - size (tuple): New size for the window.

        Returns:
        None
        """
        self._window.close()
        self._window = sg.Window(self._title, self._layout, size=self._size)

    @Logger.log_record
    def replace_to_registration_window(self) -> None:
        """
        Replaces the current window layout with the registration window layout.

        Returns:
        None
        """
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

    @Logger.log_record
    def replace_to_enter_window(self) -> None:
        """
        Replaces the current window layout with the initial window layout.
        Returns:
        None
        """
        self._window.close()
        self._initial_window()

    @Logger.log_record
    def replace_to_client_window(self, email_client: str) -> None:
        """
        Replaces the current window layout with the client window layout.
        Parameters:
        - email_client (str): Email of the client.

        Returns:
        None
        """

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
            [sg.Text("Please enter an order number"), sg.InputText(key= '-ORDER_NUMBER-')],
            [sg.Button("OK", key='-OK_TAB_ORDER_PICKUP-')]
        ]
        column_headings = [
            'order ID',
            'email client',
            'phone client',
            'order amount',
            'amount items',
            'order entered',
            'order notes',
            'order collected'
        ]
        sql_orders_connector = SqlOrders(email_client)
        layout_tab_order_history = [
            [
                sg.Table(
                    values=sql_orders_connector.get_table(
                        ("email_client", email_client),
                        "order_entered",
                        settings.LIMIT_TABLES
                    ),
                    headings=column_headings,
                    key='-TABLE-'
                )
            ]
        ]
        self._layout = [
            [
                sg.TabGroup(
                    [
                        [sg.Tab("create a new order", layout_tab_create_order, key='-TAB_CREATE_ORDER-')],
                        [sg.Tab("Order pick up", layout_tab_order_pickup, key='-TAB_ORDER_PICKUP-')],
                        [sg.Tab(f"Order history ({settings.LIMIT_TABLES})", layout_tab_order_history, key='-TAB_ORDER_HISTORY-')]
                    ]
                )
            ],
            [sg.Button("close")]
        ]
        self._title = "private area"
        self._update_window(True)

    @Logger.log_record
    def replace_to_manager_window(self, email: str) -> None:
        """
        Replaces the current window layout with the manager window layout.

        Parameters:
        - email (str): Email of the manager.

        Returns:
        None
        """
        column_headings_data = ['variable_name', 'variable_value']
        sql_variables_connector = SqlSystemData("cash register")
        layout_tab_view_data = [
            [sg.Table(values=sql_variables_connector.get_table(), headings=column_headings_data, key='-TABLE_DATA-')]
        ]
        column_headings_orders = [
            'order ID',
            'email client',
            'phone client',
            'order amount',
            'amount items',
            'order entered',
            'order notes',
            'order collected'
        ]
        sql_orders_connector = SqlOrders()
        layout_tab_order_history = [
            [
                sg.Table(
                    values=sql_orders_connector.get_table(
                        by_sort="order_entered",
                        by_limit=settings.LIMIT_TABLES
                    ),
                    headings=column_headings_orders,
                    key='-TABLE_ALL_ORDERS-'
                )
            ]
        ]
        column_headings_clients = [
            'name',
            'family name',
            'city',
            'street',
            'house number',
            'phone client',
            'email client',
            'password',
            'message type'
        ]
        sql_clients_connector = SqlClients()
        layout_tab_clients = [
            [
                sg.Table(
                    values=sql_clients_connector.get_table(
                        by_sort="family_name",
                        by_limit=settings.LIMIT_TABLES
                    ),
                    headings=column_headings_clients,
                    key='-TABLE_ALL_CLIENTS-'
                )
            ]
        ]
        column_headings_stock = ['material name', 'material value']
        sql_stock_connector = SqlMaterial()
        layout_tab_stock = [
            [
                sg.Table(
                    values=sql_stock_connector.get_table(by_sort="material_name"),
                    headings=column_headings_stock,
                    key='-TABLE_ALL_STOCK-'
                )
            ]
        ]
        column_headings_managers = [
            'name',
            'family name',
            'city',
            'street',
            'house number',
            'phone manager',
            'email manager',
            'password',
            'message type'
        ]
        sql_managers_connector = SqlManagers(email)
        layout_tab_managers = [
            [
                sg.Table(
                    values=sql_managers_connector.get_table(by_sort="family_name"),
                    headings=column_headings_managers, key='-TABLE_ALL_MANAGERS-'
                )
            ]
        ]
        layout_tab_add_manager = [
            [sg.Text("name"), sg.InputText(key= '-NAME-', justification='center')],
            [sg.Text("family_name"), sg.InputText(key= '-FAMILY_NAME-', justification='center')],
            [sg.Text("city"), sg.InputText(key= '-CITY-', justification='center')],
            [sg.Text("street"), sg.InputText(key= '-STREET-', justification='center')],
            [sg.Text("house_number"), sg.InputText(key= '-HOUSE_NUMBER-', justification='center')],
            [sg.Text("phone"), sg.InputText(key= '-PHONE-', justification='center')],
            [sg.Text("email"), sg.InputText(key= '-EMAIL-', justification='center')],
            [sg.Text("Choose a strong password"), sg.InputText(key= '-PASSWORD-', justification='center')],
            [sg.Text("Choose a preferred method of communication"), sg.DropDown(["email", "sms"], key= '-MESSAGE_TYPE-')],
            [sg.Button("add", key= '-ADD_MANAGER-')]
        ]
        layout_tab_add_material = [
            [sg.Text("Select a material type"), sg.DropDown(list(settings.NAMES_MATERIAL), key= '-TYPE_MATERIAL_TO_ADD-')],
            [sg.Text("Please enter a quantity to add"), sg.InputText(key= '-AMOUNT_TO_ADD-')],
            [sg.Button("add", key='-ADD_MATERIAL-')]
        ]
        withdraw_amount = sql_variables_connector.get_value("variable_value")
        layout_tab_money_withdrawal = [
            [sg.Text(f"The Withdraw amount is: {withdraw_amount}\n. Please enter an amount to withdraw"), sg.InputText(key= '-AMOUNT_TO_WITHDRAW-')],
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
                [sg.Tab("Withdraw money", layout_tab_money_withdrawal, key='-TAB_WITHDRAW_MONEY-')]
            ])],
            [sg.Button("close")]
        ]
        name_manager = sql_managers_connector.get_value("name")
        family_manager = sql_managers_connector.get_value("family_name")
        self._title = f"private area manager {name_manager} {family_manager}, manager."
        self._update_window(True)

    @Logger.log_record
    @staticmethod
    def popup_window(
        text: str,
        title: str = "",
        size: tuple = settings.DEFAULT_SIZE_POPUP,
        font: tuple = settings.DEFAULT_FONT_POPUP) -> None:
        """
        Displays a popup window with the given text.
        Parameters:
        - text (str): Text to be displayed in the popup window.
        - title (str): Title of the popup window.
        - size (tuple): Size of the popup window.
        - font (tuple): Font settings for the popup window.

        Returns:
        None
        """
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




