# NOTE This file is for defining DB settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from .config import DATABASE_URL


DATABASE_URL = DATABASE_URL

# NOTE if echo is True, you can see SQL log
engine = create_engine(DATABASE_URL, echo=False)

sessionLocal = sessionmaker(autocommit=False, autoflush=True, bind=engine)