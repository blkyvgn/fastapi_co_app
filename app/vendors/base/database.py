from sqlalchemy import create_engine
from .model import BaseModel
from sqlalchemy.orm import (
    declarative_base,
    sessionmaker,
)
from app.config import cfg 


engine = create_engine(
    cfg.database_url,
    connect_args={'check_same_thread': False},
    echo=cfg.database_echo
)

Session = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

BaseModel = declarative_base(cls=BaseModel)