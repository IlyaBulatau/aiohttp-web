from aiohttp import web
import asyncpg
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker


class Database:

    def __init__(self, application: web.Application):
        self.server = application['config']['database_server']
        self.login = application['config']['database_login']
        self.password = application['config']['database_password']
        self.host = application['config']['database_host']
        self.name = application['config']['database_name']
        self.url = f'postgresql+asyncpg://{self.login}:{self.password}@{self.host}/{self.name}'

    def setup(self, application: web.Application):
        application.on_startup.append(self.create_database)
        application.on_cleanup.append()

    
    async def session(self):
        create_session = async_sessionmaker(bind=create_async_engine(url=self.url), autoflush=False, expire_on_commit=False)
        async with create_session() as session:
            return session
        

    async def create_database(self):
        connect = await asyncpg.connect(database=self.server, 
                                  user=self.login,
                                  password=self.password,
                                  host=self.host)
        
        try:
            await connect.execute(f"CREATE DATABASE {self.name}")
        except Exception as e:
            ...

        await connect.close()