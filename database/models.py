import sqlalchemy as orm
from sqlalchemy.orm import relationship, declarative_base
from database.connect import Database

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = orm.Column(orm.Integer(), primary_key=True)
    email = orm.Column(orm.String(), nullable=False)
    create_time = orm.Column(orm.DateTime(), nullable=False)
    reminder = relationship('Reminder', backref='user')

class Reminder(Base):
    __tablename__ = 'reminders'

    id = orm.Column(orm.Integer(), primary_key=True)
    content = orm.Column(orm.String(), nullable=False)
    create_time = orm.Column(orm.DateTime(), nullable=False)
    user_id = orm.Column(orm.Integer(), orm.ForeignKey('users.id'))


