"""
Module for validater data from html form
"""

import pydantic
from email_validator import validate_email, exceptions_types
from utils.log import log
from string import digits, ascii_lowercase, punctuation
from datetime import datetime
from app.exeption.values_exeption import (PasswordStrExeption, 
                                          PasswordLenghtExeption, 
                                          PasswordNotHaveDigit, 
                                          PasswordLetterExeption, 
                                          PasswordSpaceExeption,
                                          UsernameHavePunctuationsExeption,
                                          UsernameLenghtExeption,
                                          UsernameSpaceExeption,
                                          UsernameStrExeption,
                                          ContentLenghtExeption,
                                          ContentSpaceExeption,
                                          ContentStrExeption,
                                          EmptyDataExeption,
                                          TimePassedExeption)


class UserLoginForm(pydantic.BaseModel):
    email: str
    password: str

    @pydantic.field_validator('email')
    @classmethod
    def email_validator(cls, email):
        """
        EMAIL validator
        """
        try:
            validate_email(email=email)
        except:
            log.warning('EMAIL NOT VALID')
            raise exceptions_types.EmailNotValidError()
            
        
        return email
    
    @pydantic.field_validator('password')
    @classmethod
    def password_validator(cls, password):
        """
        PASSWORD validator
        """
        if not isinstance(password, str):
            log.warning('PASSWORD NOT STR TYPE')
            raise PasswordStrExeption()
        if len(password) < 8:
            log.warning('PASSWORD IS LESS 8 LENGHT')
            raise PasswordLenghtExeption()
        if not set(password).intersection(digits):
            log.warning('PASSWORD NOT HAVE  DIGIT')
            raise PasswordNotHaveDigit()
        if set(password).intersection(' '):
            log.warning('PASSWORD HAVE SPACE ERROR')
            raise PasswordSpaceExeption()
        if len(set(password).intersection(ascii_lowercase)) < 4:
            log.warning('PASSWORD HAVE LESS 4 DIFFERENT LOWERCASE LETTER')
            raise PasswordLetterExeption()

        return password

class UserSignUpForm(UserLoginForm):
    
    username : str

    @pydantic.field_validator('username')
    @classmethod
    def username_verificat(cls, username):
        """
        USERNAME validator
        """
        if not isinstance(username, str):
            log.warning('USERNAME NOT STR TYPE')
            raise UsernameStrExeption()
        if set(username).intersection(punctuation):
            log.warning('USERNAME HAVE PUNCTUANIONS - ERROR')
            raise UsernameHavePunctuationsExeption()
        if set(username).intersection(' '):
            log.warning('USERNAME HAVE SPACE ERROR')
            raise UsernameSpaceExeption()
        if len(username) < 2:
            log.warning('USERNAME IS SMALL LENGHT')
            raise UsernameLenghtExeption()
        
        return username

class ReminderSaveForm(pydantic.BaseModel):

    content: str
    date_departure: str
    time_departure: str

    @pydantic.field_validator('content')
    @classmethod
    def content_validator(cls, content):
        """
        CONTENT validator
        """
        if not isinstance(content, str) or content == '':
            log.warning('CONTENT IS NOT STRING TYPE')
            raise ContentStrExeption()
        if len(content) < 8:
            log.warning('CONTETN LESS 8 LENGHT')
            raise ContentLenghtExeption()
        if ((content.count(' ') / len(content)) * 100) > 20:
            #percentage of space and letter
            log.warning('MORE SPACE AND LESS LETTER') 
            raise ContentSpaceExeption()
        return content
    
    @pydantic.root_validator(pre=True)
    @classmethod
    def date_departure_validator(cls, args):
        """
        DATETIME validator
        """
        date_departure = args['date_departure']
        time_departure = args['time_departure']
        if date_departure == '' or time_departure == '':
            log.warning('EMPTY DATATIME')
            raise EmptyDataExeption()
        datetime_departure = datetime.strptime(date_departure+'/'+time_departure, '%Y-%m-%d/%H:%M')  

        if datetime_departure < datetime.now():
            log.warning('Time has passed')
            raise TimePassedExeption()
        return args
