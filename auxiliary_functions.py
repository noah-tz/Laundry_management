import PySimpleGUI as sg


class AuxiliaryFunctions:
    @staticmethod
    def is_valid_email(email: str) -> bool:
        """check if the email address is valid"""
        if '@' not in email:
            return False
        username, domain = email.split('@')
        domain_parts = domain.split('.')
        if '.' not in domain or len(domain_parts) < 2 or not username:
            return False
        return all(part.isalnum() for part in domain_parts)
    
    @staticmethod
    def is_valid_password(password) -> bool:
        """check if the password is valid"""
        letters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
        numbers = "1234567890"
        signs = "`~!@#$%^&*?><:;,./"
        from_letters = False
        from_numbers = False
        from_signs = False
        for cher in password:
            if cher in letters:
                from_letters = True
            elif cher in numbers:
                from_numbers = True
            elif cher in signs:
                from_signs = True
        return (
            all(
                char in letters or char in numbers or char in signs
                for char in password
            )
            and len(password) >= 8
            and from_letters
            and from_numbers
            and from_signs
        )
    
    @staticmethod
    def is_valid_user_information(values: dict) -> bool:
        if len(values['-name_registration-']) < 2:
            sg.popup('"Name" must contain at least two letters')
            return False
        if len(values['-family_name_registration-']) < 2:
            sg.popup('"family_name" must contain at least two letters')
            return False
        if len(values['-city_registration-']) < 2:
            sg.popup('"city" must contain at least two letters')
            return False
        if len(values['-street_registration-']) < 2:
            sg.popup('"street" must contain at least two letters')
            return False
        if (len(values['-house_number_registration-']) == 0 or any(figure not in "01234567890" for figure in values['-house_number_registration-']) or int(values['-house_number_registration-']) <= 0):
            sg.popup("invalid house_number")
            return False
        if len(values['-phone_registration-']) < 9 or any(figure not in "0123456789" for figure in values['-phone_registration-']) or values['-phone_registration-'][0] not in ['0', '+']:
            sg.popup("invalid phone number")
            return False
        if not AuxiliaryFunctions.is_valid_email(values['-email_registration-']):
            sg.popup("invalid Email address")
            return False
        if not AuxiliaryFunctions.is_valid_password(values['-password_registration-']):
            sg.popup("The selected password is incorrect. The password must contain at least 8 characters (letters, numbers and special characters), including at least one digit, one number, and one special character (`~!@#$%^&*?><:;,./)")
            return False
        if values['-message_type_registration-'] not in ['sms', 'email']:
            sg.popup("Please select preferred method of communication")
            return False
        return True
    
    @staticmethod
    def is_valid_manager_information(values: dict) -> bool:
        if len(values['-NAME-']) < 2:
            sg.popup('"Name" must contain at least two letters')
            return False
        if len(values['-FAMILY_NAME-']) < 2:
            sg.popup('"family_name" must contain at least two letters')
            return False
        if len(values['-CITY-']) < 2:
            sg.popup('"city" must contain at least two letters')
            return False
        if len(values['-STREET-']) < 2:
            sg.popup('"street" must contain at least two letters')
            return False
        if (len(values['-HOUSE_NUMBER-']) == 0 or any(figure not in "01234567890" for figure in values['-HOUSE_NUMBER-']) or int(values['-HOUSE_NUMBER-']) <= 0):
            sg.popup("invalid house_number")
            return False
        if len(values['-PHONE-']) < 9 or any(figure not in "0123456789" for figure in values['-PHONE-']) or values['-PHONE-'][0] not in ['0', '+']:
            sg.popup("invalid phone number")
            return False
        if not AuxiliaryFunctions.is_valid_email(values['-EMAIL-']):
            sg.popup("invalid Email address")
            return False
        if not AuxiliaryFunctions.is_valid_password(values['-PASSWORD-']):
            sg.popup("The selected password is incorrect. The password must contain at least 8 characters (letters, numbers and special characters), including at least one digit, one number, and one special character (`~!@#$%^&*?><:;,./)")
            return False
        if values['-MESSAGE_TYPE-'] not in ['sms', 'email']:
            sg.popup("Please select preferred method of communication")
            return False
        return True
    
    @staticmethod
    def input_is_number(input: str):
        return all(tag in '0123456789' for tag in input) and input != ''
    
if __name__ == '__main__':
    print(AuxiliaryFunctions.input_is_number("22"))


    

