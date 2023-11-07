import PySimpleGUI as sg
# from validate_email_address import validate_email




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
        if len(values['-name-']) < 2:
            sg.popup('"Name" must contain at least two letters')
            return False
        if len(values['-family_name-']) < 2:
            sg.popup('"family_name" must contain at least two letters')
            return False
        if len(values['-city-']) < 2:
            sg.popup('"city" must contain at least two letters')
            return False
        if len(values['-street-']) < 2:
            sg.popup('"street" must contain at least two letters')
            return False
        if (len(values['-house_number-']) == 0 or any(figure not in "01234567890" for figure in values['-house_number-']) or int(values['-house_number-']) <= 0):
            sg.popup("invalid house_number")
            return False
        if len(values['-phone-']) < 9 or any(figure not in "0123456789" for figure in values['-phone-']) or values['-phone-'][0] not in ['0', '+']:
            sg.popup("invalid phone number")
            return False
        if not AuxiliaryFunctions.is_valid_email(values['-client_email-']):
            sg.popup("invalid Email address")
            return False
        if not AuxiliaryFunctions.is_valid_password(values['-client_password-']):
            sg.popup("The selected password is incorrect. The password must contain at least 8 characters (letters, numbers and special characters), including at least one digit, one number, and one special character (`~!@#$%^&*?><:;,./)")
            return False
        if values['-message_type-'] not in ['sms', 'email']:
            sg.popup("Please select preferred method of communication")
            return False
        return True
    

