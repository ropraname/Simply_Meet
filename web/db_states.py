import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from typing import List
from typing import Optional
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy.orm import sessionmaker
import asyncio

import sys
sys.path.append('..')
import secret

from sqlalchemy import *

engine = sqlalchemy.create_engine(secret.SQLALCHEMY_DATABASE_URL)

Base = declarative_base()

class Users(Base):
    __tablename__ = 'users'
    id = Column(BigInteger, primary_key=True, nullable=False)
    interests = Column(Text, nullable=True)
    no_interest = Column(Text, nullable=True)
    self_describe = Column(Text, nullable=True)
    page = Column(Text, nullable=False)
    intention = Column(Text, nullable=True)

class Pairs_Finding(Base):
    __tablename__ = 'pairs_finding'
    id = Column(BigInteger, primary_key=True, nullable=False, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey("users.id"), nullable=False)
    pair_user_id = Column(BigInteger, ForeignKey("users.id"), nullable=True)
    whishes = Column(Text, nullable=False)
    time = Column(Text, nullable=True)
    place = Column(Text, nullable=True)
    description = Column(Text, nullable=True)
    declined_users = Column(Text, nullable=False)
    done = Column(Boolean, nullable=False)


class Events(Base):
    __tablename__ = "events"
    id = Column(BigInteger, primary_key=True, nullable=False, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey("users.id"), nullable=False)
    general_topic = Column(Text, nullable=False)
    topic = Column(Text, nullable=False)
    people_amount = Column(Text, nullable=False)
    time = Column(Text, nullable=False)
    place = Column(Text, nullable=False)
    accepted_users = Column(Text, nullable=False)
    done = Column(Boolean, nullable=False)

class Something_New(Base):
    __tablename__ = "sth_new"
    id = Column(BigInteger, primary_key=True, nullable=False, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey("users.id"), nullable=False)
    pair_user_id = Column(BigInteger, ForeignKey("users.id"), nullable=False)
    important_factor = Column(Text, nullable=False)
    recommend_period = Column(Text, nullable=False)
    declined_users = Column(Text, nullable=False)
    done = Column(Boolean, nullable=False)


Base.metadata.create_all(engine)