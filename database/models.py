import sqlalchemy as orm
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy.sql import func  

from argon2 import PasswordHasher

Base = declarative_base()
ph = PasswordHasher()

class BaseModel(Base):
    __abstract__ = True

    id = orm.Column(orm.Integer(), primary_key=True)
    create_time = orm.Column(orm.DateTime(), server_default=func.now())

class User(BaseModel):
    __tablename__ = 'users'

    username = orm.Column(orm.String(), nullable=False)
    email = orm.Column(orm.String(), nullable=False)
    password = orm.Column(orm.String(), nullable=False)
    reminder = relationship('Reminder', backref='user')

    def __init__(self, **kwargs):
        self.username = kwargs.get('username')
        self.email = kwargs.get('email')
        self.password = ph.hash(kwargs.get('password'))
        

class Reminder(BaseModel):
    __tablename__ = 'reminders'

    content = orm.Column(orm.String(), nullable=False)
    departure_date = orm.Column(orm.DateTime(), nullable=False)
    user_id = orm.Column(orm.Integer(), orm.ForeignKey('users.id'))


