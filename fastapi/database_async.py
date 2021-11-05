import os

import databases
from sqlalchemy import create_engine, MetaData, Boolean, Column, Integer, String, Table


SQLALCHEMY_DATABASE_URL = os.environ.get("DATABASE_URL")

database = databases.Database(SQLALCHEMY_DATABASE_URL)
metadata = MetaData()


users = Table(
    "auth_user",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("username", String),
    Column("email", String),
    Column("is_active", Boolean),
)

engine = create_engine(SQLALCHEMY_DATABASE_URL)
metadata.create_all(engine)
