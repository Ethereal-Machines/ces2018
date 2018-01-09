import uuid

import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker, validates

from app import APP

engine = sa.create_engine(APP.config['DB_URL'], echo=True)
Base = declarative_base()


def create_session(db_url, engine, Base):
    ''' Create and return sqlalchemy scoped_session '''
    session_maker = sessionmaker(bind=engine)
    scopedsession = scoped_session(session_maker)
    Base.metadata.bind = scopedsession
    return scopedsession


def get_token():
    ''' Return a token '''
    return str(uuid.uuid4().hex).lower()[:6]


class User(Base):
    ''' Table for user details '''
    __tablename__ = 'users'

    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.Text, nullable=False)
    address = sa.Column(sa.Text, nullable=False)
    email = sa.Column(sa.String, nullable=False, unique=True)
    contact = sa.Column(sa.String, nullable=False)
    token = sa.Column(sa.String, nullable=False, unique=True, default=get_token)
    token_used = sa.Column(sa.Boolean, nullable=False, default=False)

    @validates('email')
    def validate_email(self, key, address):
        assert '@' in address
        return address

    @classmethod
    def get_user_by_email(cls, session, emailid):
        ''' Get the user from email id '''
        return session.query(cls).filter(cls.email==emailid).first()
