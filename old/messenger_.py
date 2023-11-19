from mysql_database import MysqlDatabase
from log import Logger
import settings
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import requests





class EmailSender:
    def __init__(self, email_sender: str, password_sender: str) -> None:
        self.email_sender = email_sender # "laundrythecity034@gmail.com"
        self.__password_sender = password_sender # "xrqzlbpruagxljpr"
        self._server = smtplib.SMTP('smtp.gmail.com', 587) # very slow
        self._server.starttls()
        self._server.login(self.email_sender, self.__password_sender)

    def __del__(self):
        self._server.quit()


    @Logger.log_record
    def __calling_the_server(self, to_email: str, text: str) -> None:
        self._server.sendmail(self.email_sender, to_email, text)

    def create_and_send_msg(self, to_email: str, subject: str, body: str) -> str:
        msg = MIMEMultipart()    
        msg['From'] = self.email_sender
        msg['To'] = to_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))
        text = msg.as_string()
        self.__calling_the_server(to_email, text)
    

class SmsSender:
    def __init__(self, account_sid, auth_token, from_number) -> None:
        self.__account_sid = account_sid
        self.__auth_token = auth_token
        self.__from_number = from_number
        self.__url = f'https://api.twilio.com/2010-04-01/Accounts/{self.__account_sid}/Messages.json'

    @Logger.log_record
    def send_sms(self, phone: str, message: str) -> bool:
        if phone[0] == "0":
            phone = f"+972{phone[1:]}"
        data = {
            'From': self.__from_number,
            'To': phone,
            'Body': message
        }
        if requests.post(self.__url, data=data, auth=(self.__account_sid, self.__auth_token)).ok:
            print(f'SMS from {self.__from_number} to {phone} was successfully sent.\nMessage- "{message}"')
            return True
        print(f'SMS from {self.__from_number} to {phone} was not sent.')
        return False


class Messenger:
    email_sender = EmailSender(settings.EMAIL_MANAGER, settings.EMAIL_MANAGER_PASSWORD)
    __sms_sender = SmsSender(settings.SMS_ACCOUNT_SID_MANAGER, settings.SMS_AUTO_TOKEN_MANAGER, settings.SMS_FROM_NUMBER_MANAGER)

    @staticmethod
    def __is_via_email(email_client: str):
        if email_client == settings.EMAIL_MANAGER:
            result = settings.MSG_MANAGER
        else:
            result = MysqlDatabase.get_value_from_table("clients", "message_type", "email_client", email_client)
        return result  == "email"

    @staticmethod
    def __send_msg(subject: str, body: str, email_client: str):
        if Messenger.__is_via_email(email_client):
            Messenger.email_sender.create_and_send_msg(email_client, subject, body)
        else:
            phone_client = MysqlDatabase.get_value_from_table("clients", "phone_client", "email_client", email_client)
            Messenger.__sms_sender.send_sms(phone_client, f"{subject}/n{body}")


    @staticmethod
    def password_recovery(email: str) -> None:
        password = MysqlDatabase.get_client_password(email)
        subject = "The city laundry - reset password for your account"
        body = f"The password for your account is-\n{password}\nSuccessfully"
        Messenger.__send_msg(subject, body, email)

    @staticmethod
    def order_summary(email_client: str, order_ID: str, items_order: dict, amount: int, time: int) -> None:
        subject = f"order summary NO {order_ID}"
        body: str = "".join(f"{item}: {items_order[item]}.\n" for item in items_order)
        body += f"\ntotal order cost {amount}"
        body += f"\nYour order will be ready in {time} hours"
        Messenger.__send_msg(subject, body, email_client)

    @staticmethod
    def Your_order_is_ready(email_client: str, order_ID: str) -> None:
        subject = f"The city laundry - order NO {order_ID}"
        body = "Your order is ready. You can get to the collection now\nSuccessfully"
        Messenger.__send_msg(subject, body, email_client)

    @staticmethod
    def thank_you(email_client: str) -> None:
        subject = "Thank you for using our service!"
        body = "We look forward to seeing you using our services again.\nHave a wonderful day!"
        Messenger.__send_msg(subject, body, email_client)

    @staticmethod
    def any_msg(to_email: str, subject: str, body: str):
        Messenger.__send_msg(subject, body, to_email)





if __name__ == '__main__':
    sms_sender = SmsSender(settings.SMS_ACCOUNT_SID_MANAGER, settings.SMS_AUTO_TOKEN_MANAGER, settings.SMS_FROM_NUMBER_MANAGER)
    sms_sender.send_sms("0522645540", "בדיקה") # 0545964829 0522645540




