from fastapi import Depends
from typing import Annotated
from collections import namedtuple
from app.vendors.base.database import Session
from sqlalchemy import select

DBSession = namedtuple('DBSession' , 'session select')

def get_db():
    db = DB(Session(), select)
    try:
        yield db
    finally:
        db.session.close()

DB = Annotated[DBSession, Depends(get_db)]