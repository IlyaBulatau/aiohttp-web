import pydantic
from email_validator import validate_email
from utils import log
from string import digits, ascii_lowercase, punctuation

class UserSignUpForm(pydantic.BaseModel):
    
    username : str
    email: str
    password: str

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
        if len(set(password).intersection(ascii_lowercase)) < 6:
            log.warning('PASSWORD HAVE LESS 6 LOWERCASE LETTER')
            raise SyntaxError

        return password
        

