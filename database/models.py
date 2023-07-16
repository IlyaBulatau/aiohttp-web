import sqlalchemy as orm
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy.sql import func  

import jwt

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = orm.Column(orm.Integer(), primary_key=True)
    username = orm.Column(orm.String(), nullable=False)
    email = orm.Column(orm.String(), nullable=False)
    password = orm.Column(orm.String(), nullable=False)
    create_time = orm.Column(orm.DateTime(), server_default=func.now())
    reminder = relationship('Reminder', backref='user')

    def __init__(self, **kwargs):
        self.username = kwargs.get('username')
        self.email = kwargs.get('email')
        self.password = jwt.encode(payload={'password': kwargs.get('password')}, key='password', algorithm='HS256')
        

class Reminder(Base):
    __tablename__ = 'reminders'

    id = orm.Column(orm.Integer(), primary_key=True)
    content = orm.Column(orm.String(), nullable=False)
    departure_date = orm.Column(orm.DateTime(), nullable=False)
    create_time = orm.Column(orm.DateTime(), server_default=func.now())
    user_id = orm.Column(orm.Integer(), orm.ForeignKey('users.id'))


