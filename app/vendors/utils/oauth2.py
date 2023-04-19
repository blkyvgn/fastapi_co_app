from fastapi.security import OAuth2PasswordBearer
from app.config import cfg


oauth2_scheme = OAuth2PasswordBearer(tokenUrl=cfg.login_router)