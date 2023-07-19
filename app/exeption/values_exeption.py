class BaseExeption(Exception):

    def __init__(self, *args: object) -> None:
        if args:
            self.msg = args[0]
        else:
            self.msg = None

    def __str__(self) -> str:
        if self.msg:
            return self.msg

class PasswordExeption(BaseException):
    ...

class UsernameExeption(BaseException):
    ...    

class ContentExeption(BaseException):
    ...

class TimeExeption(BaseException):
    ...

class EmptyDataExeption(BaseException):

    def __str__(self) -> str:
        return 'EMPTY DATATIME'

class PasswordStrExeption(PasswordExeption):

    def __str__(self) -> str:
        PasswordExeption.__str__(self)
        return 'PASSWORD NOT STR TYPE'         
        
class PasswordLenghtExeption(PasswordExeption):
    
    def __str__(self) -> str:
        PasswordExeption.__str__(self)
        return 'PASSWORD IS LESS 8 LENGHT'
    
class PasswordNotHaveDigit(PasswordExeption):
    
    def __str__(self) -> str:
        
        PasswordExeption.__str__(self)
        return 'PASSWORD NOT HAVE  DIGIT'
    
class PasswordSpaceExeption(PasswordExeption):
    
    def __str__(self):
        PasswordExeption.__str__(self)
        return 'PASSWORD HAVE SPACE ERROR'
    
class PasswordLetterExeption(PasswordExeption):

    def __str__(self) -> str:
        PasswordExeption.__str__(self)
        return 'PASSWORD HAVE LESS 4 DIFFERENT LOWERCASE LETTER'
    

class UsernameStrExeption(UsernameExeption):

    def __str__(self) -> str:
        UsernameExeption.__str__(self)
        return 'USERNAME NOT STR TYPE'         

class UsernameHavePunctuationsExeption(UsernameExeption):

    def __str__(self) -> str:
        UsernameExeption.__str__(self)
        return 'USERNAME HAVE PUNCTUANIONS - ERROR'         

class UsernameSpaceExeption(UsernameExeption):

    def __str__(self) -> str:
        UsernameExeption.__str__(self)
        return 'USERNAME HAVE SPACE ERROR'

class UsernameLenghtExeption(UsernameExeption):

    def __str__(self) -> str:
        UsernameExeption.__str__(self)         
        return 'USERNAME IS SMALL LENGHT'
    
class ContentStrExeption(ContentExeption):

    def __str__(self) -> str:
        ContentExeption.__str__(self)
        return 'CONTENT IS NOT STRING TYPE'
    
class ContentLenghtExeption(ContentExeption):

    def __str__(self) -> str:
        ContentExeption.__str__(self)
        return 'CONTETN LESS 20 LENGHT'
    
class ContentSpaceExeption(ContentExeption):

    def __str__(self) -> str:
        ContentExeption.__str__(self)
        return 'MORE SPACE AND LESS LETTER'
    
class TimePassedExeption(TimeExeption):
    
    def __str__(self) -> str:
        TimeExeption.__str__(self)
        return 'TIME HAS PASSED'