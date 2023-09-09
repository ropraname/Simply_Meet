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

from secret import SQLALCHEMY_DATABASE_URL

engine = sqlalchemy.create_engine(SQLALCHEMY_DATABASE_URL)

Base = declarative_base()

from sqlalchemy import *

metadata = MetaData()

user = Table('users', metadata,
    Column('id', BigInteger(), primary_key=True, nullable=False),
    Column('interests', Text(), nullable=False),
    Column('no_interest', Text(), nullable=False),
    Column('self_describe', Text(), nullable=False),
    Column('intention', Text(), nullable=False),
)


pairs_finding = Table('pairs_finding', metadata,
    Column('id', Integer(), primary_key=True, nullable=False),
    Column('user_id', Integer(), ForeignKey("user.id"), nullable=False),
    Column('whishes', Text(), nullable=False),
    Column('time', Text(),  nullable=False),
    Column('place', Text(),  nullable=False),
    Column('description', Text(),  nullable=False),
    Column('declined_users', Text(),  nullable=False),
    Column('done', Boolean(), nullable=False),
)

events = Table('events', metadata,
    Column('id', Integer(), primary_key=True),
    Column('user_id', Integer(), ForeignKey("user.id"), nullable=False),
    Column('general_topic', Text(), nullable=False),
    Column('topic', Text(),  nullable=False),
    Column('people_amount', Text(),  nullable=False),
    Column('time', Text(),  nullable=False),
    Column('place', Text(),  nullable=False),
    Column('accepted_users', Text(),  nullable=False),
    Column('done', Boolean(),  nullable=False),
)

find_new = Table('find_new', metadata,
    Column('id', Integer(), primary_key=True, nullable=False),
    Column('user_id', Integer(), ForeignKey("user.id"), nullable=False),
    Column('important_factor', Text(), nullable=False),
    Column('recommend_period', Integer(),  nullable=False),
    Column('declined_users', Text(),  nullable=False),
    Column('done', Boolean(), nullable=False),
)