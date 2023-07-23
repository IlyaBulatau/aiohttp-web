import functools
import aiohttp_jinja2
from aiohttp import web
from app.exeption.values_exeption import (PasswordLenghtExeption,
                                        PasswordLetterExeption,
                                        PasswordNotHaveDigit,
                                        PasswordSpaceExeption,
                                        PasswordStrExeption,
                                        UsernameHavePunctuationsExeption,
                                        UsernameLenghtExeption,
                                        UsernameSpaceExeption,
                                        UsernameStrExeption,
                                        ContentLenghtExeption,
                                        ContentSpaceExeption,
                                        ContentStrExeption,
                                        TimePassedExeption,
                                        EmptyDataExeption)


def error_controller(template_name: str, 
                     title:str, 
                     header:str, 
                     username_error:str=None, 
                     password_error:str=None,
                     email_error:str=None,
                     reminder_error:str=None,):

    def wrapper(handler):

        functools.wraps(handler)
        async def inner(*args, **kwargs):

            KEYS = {'title': title, 
                    'header': header, 
                    'username_error': username_error, 
                    'password_error': password_error, 
                    'email_error': email_error, 
                    'reminder_error': reminder_error,}
            
            request: web.Request = args[0]
            method = request.method.upper()
            request['KEYS'] = KEYS

            if method == 'GET':
                return await handler(*args, **kwargs)

            elif method == 'POST':
                try:
                    return await handler(*args, **kwargs)
                #username exeption
                except UsernameStrExeption:
                    KEYS['username_error'] = 'user name is empty or not have letter'
                    return aiohttp_jinja2.render_template(template_name, request, context=KEYS)
                except UsernameLenghtExeption:
                    KEYS['username_error'] = 'username should be lenght more 1 letter'
                    return aiohttp_jinja2.render_template(template_name, request, context=KEYS)
                except UsernameSpaceExeption:
                    KEYS['username_error'] = 'username sould be dont have spaces'
                    return aiohttp_jinja2.render_template(template_name, request, context=KEYS)
                except UsernameHavePunctuationsExeption:
                    KEYS['username_error'] = 'error you user name have punctuation symbols'
                    return aiohttp_jinja2.render_template(template_name, request, context=KEYS)
                
                #password exeption
                except PasswordLenghtExeption:      
                    KEYS['password_error'] = 'passport lenght need be more 8 symbols'
                    return aiohttp_jinja2.render_template(template_name, request, context=KEYS)
                except PasswordLetterExeption:
                    KEYS['password_error'] = 'password must contain at least 4 different English letters'
                    return aiohttp_jinja2.render_template(template_name, request, context=KEYS)
                except PasswordNotHaveDigit:
                    KEYS['password_error'] = 'password most be contain digit'
                    return aiohttp_jinja2.render_template(template_name, request, context=KEYS)
                except PasswordSpaceExeption:
                    KEYS['password_error'] = 'password most be not have space'
                    return aiohttp_jinja2.render_template(template_name, request, context=KEYS)
                except PasswordStrExeption:
                    KEYS['password_error'] = 'you password empty or dont have letter'
                    return aiohttp_jinja2.render_template(template_name, request, context=KEYS)
                except ContentStrExeption:
                    KEYS['reminder_error'] = 'You text in reminder is not valid'
                    return aiohttp_jinja2.render_template(template_name, request, context=KEYS)
                
                # content exeption
                except ContentLenghtExeption:
                    KEYS['reminder_error'] = 'Lenght reminder text should be more 8 letter'
                    return aiohttp_jinja2.render_template(template_name, request, context=KEYS)
                except ContentSpaceExeption:
                    KEYS['reminder_error'] = 'You remonder have more space and less letter, correct pls'
                    return aiohttp_jinja2.render_template(template_name, request, context=KEYS)
                
                # reminder date and data exeption
                except TimePassedExeption:
                    KEYS['reminder_error'] = 'you set time is passed, correct date and time pls'
                    return aiohttp_jinja2.render_template(template_name, request, context=KEYS)
                except EmptyDataExeption:
                    KEYS['reminder_error'] = 'pls set date and time values'
                    return aiohttp_jinja2.render_template(template_name, request, context=KEYS)

                # email exeption
                except Exception:
                    KEYS['email_error'] = 'email invalid'
                    return aiohttp_jinja2.render_template(template_name, request, context=KEYS)

        return inner
    return wrapper                        


            
