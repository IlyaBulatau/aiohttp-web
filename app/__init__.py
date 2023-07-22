from .reminder.routes import setup_routes
from .reminder import views

from .authorization import views
from .authorization.security import setup_seciruty

from .exeption.values_exeption import (PasswordLenghtExeption, 
                                       PasswordLetterExeption, 
                                       PasswordNotHaveDigit, 
                                       PasswordSpaceExeption, 
                                       PasswordStrExeption, 
                                       TimePassedExeption,
                                       UsernameHavePunctuationsExeption,
                                       UsernameLenghtExeption,
                                       UsernameSpaceExeption,
                                       UsernameStrExeption,
                                       EmptyDataExeption,
                                       ContentLenghtExeption,
                                       ContentSpaceExeption,
                                       ContentStrExeption)