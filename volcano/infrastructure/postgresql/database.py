# NOTE This file is for defining DB settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from ...core.config import DATABASE_URL


DATABASE_URL = DATABASE_URL

# NOTE if echo is True, you can see SQL log
engine = create_engine(DATABASE_URL, echo=False)

sessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=True,
)

BaseModel = declarative_base()


# NOTE Initialize DB I made
def create_tables():
    BaseModel.metadata.create_all(bind=engine)
