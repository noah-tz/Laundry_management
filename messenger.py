from log import Logger
import settings
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import requests
from typing import Any


class Sender:
    """
    Base class for sending messages through different channels.
    """
    def __init__(self, address) -> None:
        """
        Initialize the Sender object with the recipient's address.
        Parameters:
            address (str): The recipient's address (email or phone number).
        """
        self._address = address

    def _send_msg(self, subject: str, body: str):
        """
        Abstract method for sending messages. Must be implemented by subclasses.
        Parameters:
            subject (str): The subject of the message.
            body (str): The body of the message.
        """
        raise NotImplementedError

    def _calling_the_server(self, address: str, data: Any):
        """
        Abstract method for calling the messaging server. Must be implemented by subclasses.

        Parameters:
            address (str): The recipient's address (email or phone number).
            data (Any): The data to be sent to the server.
        """
        raise NotImplementedError

    def password_recovery(self, password) -> None:
        """
        Send a password recovery message.
        Parameters:
            password (str): The recovered password.
        """
        subject = "The city laundry - reset password for your account"
        body = f"The password for your account is-\n{password}\nSuccessfully"
        self._send_msg(subject, body)

    def order_summary(self, order_ID: str, items_order: dict, amount: int, time: int) -> None:
        """
        Send an order summary message.
        Parameters:
            order_ID (str): The order ID.
            items_order (dict): A dictionary containing items in the order.
            amount (int): The total order cost.
            time (int): The time required for order completion (in hours).
        """
        subject = f"order summary NO {order_ID}"
        body: str = "".join(f"{item}: {items_order[item]}.\n" for item in items_order)
        body += f"\ntotal order cost {amount}"
        body += f"\nYour order will be ready in {time} hours"
        self._send_msg(subject, body)

    def Your_order_is_ready(self, order_ID: str) -> None:
        """
        Send a notification that the order is ready for pickup.
        Parameters:
            order_ID (str): The order ID.
        """
        subject = f"The city laundry - order NO {order_ID}"
        body = "Your order is ready. You can get to the collection now\nSuccessfully"
        self._send_msg(subject, body)

    def thank_you(self) -> None:
        """
        Send a thank-you message for using the service.
        """
        subject = "Thank you for using our service!"
        body = "We look forward to seeing you using our services again.\nHave a wonderful day!"
        self._send_msg(subject, body)

    def any_msg(self, subject: str, body: str):
        """
        Send a generic message with the given subject and body.
        Parameters:
            subject (str): The subject of the message.
            body (str): The body of the message.
        """
        self._send_msg(subject, body)


class EmailSender(Sender):
    """
    Class for sending messages via email.
    """
    _email_sender = settings.EMAIL_MANAGER
    _password_sender = settings.EMAIL_MANAGER_PASSWORD
    _server = smtplib.SMTP('smtp.gmail.com', 587)
    _server.starttls()
    _server.login(_email_sender, _password_sender)
    def __init__(self, email_client: str) -> None:
        """
        Initialize the EmailSender object.
        Parameters:
            email_client (str): The email client's address.
        """
        super().__init__(email_client)

    @Logger.log_record
    def _calling_the_server(self, data: Any) -> None:
        """
        Call the email server to send the message.

        Parameters:
            data (Any): The data to be sent to the server.
        """
        EmailSender._server.sendmail(EmailSender._email_sender, self._address, data)

    def _send_msg(self, subject: str, body: str):
        """
        Send an email message.
        Parameters:
            subject (str): The subject of the email.
            body (str): The body of the email.
        """
        msg = MIMEMultipart()
        msg['From'] = self._email_sender
        msg['To'] = self._address
        msg['Subject'] = subject
        msg.attach(MIMEText(body))
        text = msg.as_string()
        print(text)
        self._calling_the_server(text)

    @staticmethod
    def close_server() -> None:
        """in end program, closing server
        """
        if EmailSender._server:
            EmailSender._server.close()

class SmsSender(Sender):
    """
    Class for sending messages via SMS.
    """
    def __init__(self, number_phone) -> None:
        """
        Initialize the SmsSender object.
        Parameters:
            number_phone (str): The phone number to send SMS to.
        """
        super().__init__(number_phone)
        self._account_sid = settings.SMS_ACCOUNT_SID_MANAGER
        self._auth_token = settings.SMS_AUTO_TOKEN_MANAGER
        self._from_number = settings.SMS_FROM_NUMBER_MANAGER
        self._url = f'https://api.twilio.com/2010-04-01/Accounts/{self._account_sid}/Messages.json'

    @Logger.log_record
    def _calling_the_server(self, data: Any):
        """
        Call the Twilio server to send the SMS.
        Parameters:
            data (Any): The data to be sent to the server.
        """
        if requests.post(self._url, data=data, auth=(self._account_sid, self._auth_token)).ok:
            return True
        print(f'SMS from {self._from_number} to {self._address} was not sent.')
        return False

    def _send_msg(self, subject: str, body: str):
        """
        Send an SMS message.
        Parameters:
            subject (str): The subject of the SMS.
            body (str): The body of the SMS.
        """
        phone = self._address
        if phone[0] == "0":
            phone = f"+972{phone[1:]}"
        data = {
            'From': self._from_number,
            'To': phone,
            'Body': f"{subject}\n{body}"
        }
        return self._calling_the_server(data)



