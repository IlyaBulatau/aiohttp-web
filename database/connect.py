from aiohttp import web
import asyncpg
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker


class Database:

    def __init__(self, application: web.Application, metadata):
        self.metadata = metadata
        self.server = application['config']['database_server']
        self.login = application['config']['database_login']
        self.password = application['config']['database_password']
        self.host = application['config']['database_host']
        self.name = application['config']['database_name']
        self.url = f'postgresql+asyncpg://{self.login}:{self.password}@{self.host}/{self.name}'

    def setup(self, application: web.Application):
        application.on_startup.append(self.create_database)
        application.on_startup.append(self.create_models)
        application.on_cleanup.append()

    def create_engine(self):
        engine = create_async_engine(url=self.url, echo=True)
        return engine
    
    def session(self):
        session_maker = async_sessionmaker(bind=self.create_engine())
        return session_maker
    

    async def create_models(self):
        async with self.create_engine().begin() as conn:
            await conn.run_sync(self.metadata.create_all)


    async def disconnect(self):
        ...

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