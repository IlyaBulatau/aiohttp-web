from aiohttp_security import setup, AbstractAuthorizationPolicy, AbstractIdentityPolicy, SessionIdentityPolicy
from aiohttp import web
from database.models import User
from aiohttp_session import get_session

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
    
        
def setup_seciruty(app: web.Application):
    setup(app, SessionIdentityPolicy(), AuthorizationPolicy())
