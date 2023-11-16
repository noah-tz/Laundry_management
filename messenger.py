from log import Logger
import settings
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import requests
from typing import Any


class Sender:
    def __init__(self, address) -> None:
        self._address = address
    def _send_msg(self, subject: str, body: str, to_email: str):
        raise NotImplementedError
    
    def _calling_the_server(self, address: str, data: Any):
        raise NotImplementedError

    def password_recovery(self, password) -> None:
        subject = "The city laundry - reset password for your account"
        body = f"The password for your account is-\n{password}\nSuccessfully"
        self._send_msg(subject, body)

    def order_summary(self, order_ID: str, items_order: dict, amount: int, time: int) -> None:
        subject = f"order summary NO {order_ID}"
        body: str = "".join(f"{item}: {items_order[item]}.\n" for item in items_order)
        body += f"\ntotal order cost {amount}"
        body += f"\nYour order will be ready in {time} hours"
        self._send_msg(subject, body)

    def Your_order_is_ready(self, order_ID: str) -> None:
        subject = f"The city laundry - order NO {order_ID}"
        body = "Your order is ready. You can get to the collection now\nSuccessfully"
        self._send_msg(subject, body)

    def thank_you(self) -> None:
        subject = "Thank you for using our service!"
        body = "We look forward to seeing you using our services again.\nHave a wonderful day!"
        self._send_msg(subject, body)

    def any_msg(self, subject: str, body: str):
        self._send_msg(subject, body)



class EmailSender(Sender):
    def __init__(self, email_client: str) -> None:
        super().__init__(email_client)
        self._email_sender = settings.EMAIL_MANAGER # "laundrythecity034@gmail.com"
        self._password_sender = settings.EMAIL_MANAGER_PASSWORD # "xrqzlbpruagxljpr"
        self._server = smtplib.SMTP('smtp.gmail.com', 587) # very slow
        self._server.starttls()
        self._server.login(self._email_sender, self._password_sender)

    def __del__(self):
        if self._server:
            self._server.close()

    def _calling_the_server(self, data: Any) -> None:
        self._server.sendmail(self._email_sender, self._address, data)

    @Logger.log_record
    def _send_msg(self, subject: str, body: str):
        msg = MIMEMultipart()    
        msg['From'] = self._email_sender
        msg['To'] = self._address
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))
        text = msg.as_string()
        self._calling_the_server(text)
    

class SmsSender(Sender):
    def __init__(self, number_phone) -> None:
        super().__init__(number_phone)
        self._account_sid = settings.SMS_ACCOUNT_SID_MANAGER
        self._auth_token = settings.SMS_AUTO_TOKEN_MANAGER
        self._from_number = settings.SMS_FROM_NUMBER_MANAGER
        self._url = f'https://api.twilio.com/2010-04-01/Accounts/{self._account_sid}/Messages.json'

    def _calling_the_server(self, data: Any):
        if requests.post(self._url, data=data, auth=(self._account_sid, self._auth_token)).ok:
            print(f'SMS from {self._from_number} to {self._address} was successfully sent.\nMessage- "{data}"')
            return True
        print(f'SMS from {self._from_number} to {self._address} was not sent.')
        return False


    @Logger.log_record
    def _send_msg(self, subject: str, body: str):
        phone = self._address
        if phone[0] == "0":
            phone = f"+972{phone[1:]}"
        data = {
            'From': self._from_number,
            'To': phone,
            'Body': f"{subject}\n{body}"
        }
        return self._calling_the_server(data)





if __name__ == '__main__':
    # sms_sender = SmsSender("0522645540")
    # sms_sender._send_msg("שלום", "בדיקה")
    email_sender = EmailSender("t0527184022@gmail.com")




