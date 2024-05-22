from ..core.database import engine
from sqlalchemy.ext.declarative import declarative_base

BaseModel = declarative_base()

# NOTE Initialize DB I made
def init_db():
    BaseModel.metadata.create_all(bind=engine)