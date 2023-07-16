from aiohttp_security import setup, AbstractAuthorizationPolicy, AbstractIdentityPolicy
from aiohttp import web
from database.models import User


KEY = 'security'

class AuthorizationPolicy(AbstractAuthorizationPolicy):
    async def permits(self, identity: str, permission, context=None):
        """
        Always return True, because thsis is method verificate correct auth
        """
        return True
    
    async def authorized_userid(self, identity: User):
        """
        Return User ID
        """
        return identity

class IdentityPolicy(AbstractIdentityPolicy):

    def __init__(self, app) -> None:
        super().__init__()
        self.app = app


    async def identify(self, request: web.Request):
        """
        Return user ID in app object
        """
        return self.app[KEY] 
    
    async def remember(self, request, response, identity: str, **kwargs):
        """
        Set in key user ID
        """
        request.app[KEY]= identity
    
    async def forget(self, request, response):
        """
        Delete user ID in KEY
        """
        request.app[KEY] = None
    
    
        
def setup_seciruty(app: web.Application):
    app[KEY] = None    
    setup(app, IdentityPolicy(app), AuthorizationPolicy())
