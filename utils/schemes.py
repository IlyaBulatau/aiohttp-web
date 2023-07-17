import pydantic
from email_validator import validate_email
from utils import log
from string import digits, ascii_lowercase, punctuation
from datetime import datetime


class UserLoginForm(pydantic.BaseModel):
    email: str
    password: str

    @pydantic.field_validator('email')
    @classmethod
    def email_validator(cls, email):
        try:
            validate_email(email=email)
        except:
            log.warning('EMAIL NOT VALID')
            raise SyntaxError
        
        return email
    
    @pydantic.field_validator('password')
    @classmethod
    def password_validator(cls, password):
        if not isinstance(password, str):
            log.warning('PASSWORD NOT STR TYPE')
            raise AttributeError
        if len(password) < 8:
            log.warning('PASSWORD IS LESS 8 LENGHT')
        if not set(password).intersection(digits):
            log.warning('PASSWORD NOT HAVE  DIGIT')
            raise TypeError
        if set(password).intersection(' '):
            log.warning('PASSWORD HAVE SPACE ERROR')
            raise SyntaxError
        if len(set(password).intersection(ascii_lowercase)) < 4:
            log.warning('PASSWORD HAVE LESS 6 DIFFERENT LOWERCASE LETTER')
            raise SyntaxError

        return password

class UserSignUpForm(UserLoginForm):
    
    username : str

    @pydantic.field_validator('username')
    @classmethod
    def username_verificat(cls, username):
        if not isinstance(username, str):
            log.warning('USERNAME NOT STR TYPE')
            raise TypeError
        if set(username).intersection(punctuation):
            log.warning('USERNAME HAVE PUNCTUANIONS - ERROR')
            raise SyntaxError
        if set(username).intersection(' '):
            log.warning('USERNAME HAVE SPACE ERROR')
            raise SyntaxError
        if len(username) < 2:
            log.warning('USERNAME IS SMALL LENGHT')
            raise AttributeError
        
        return username

class ReminderSaveForm(pydantic.BaseModel):

    content: str
    date_departure: str
    time_departure: str

    @pydantic.field_validator('content')
    @classmethod
    def content_validator(cls, content):
        if not isinstance(content, str):
            log.warning('CONTENT IS NOT STRING TYPE')
            raise TypeError
        if len(content) < 6:
            log.warning('CONTETN LESS 20 LENGHT')
            raise SyntaxError
        if ((content.count(' ') // len(content)) * 100) > 30:
            #percentage of space and letter
            log.warning('MORE SPACE AND LESS LETTER') 
            raise SyntaxError
        return content
    
    @pydantic.root_validator(pre=True)
    @classmethod
    def date_departure_validator(cls, args):
        date_departure = args['date_departure']
        time_departure = args['time_departure']
        if date_departure == '' or time_departure == '':
            log.warning('EMPTY DATATIME')
            raise AttributeError
        datetime_departure = datetime.strptime(date_departure+'/'+time_departure, '%Y-%m-%d/%H:%M')  

        if datetime_departure < datetime.now():
            log.warning('Time has passed')
            raise SyntaxError
        return args