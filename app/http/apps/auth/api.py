from fastapi.security import OAuth2PasswordRequestForm
from app.vendors.utils.gate import gate
from app.tasks.logger import write_to_log
from fastapi import (
    Depends, 
    APIRouter, 
    Response, 
    Request,
    HTTPException,
    status, 
    BackgroundTasks,
)
from app.vendors.dependencies import (
    Company, 
    DB,
)
from .utils.jwt import CurrentUser
from . import services as srv
from . import schemas as sch
from app.config import cfg

auth = APIRouter(
    prefix = '/auth',
    tags=['auth'], 
)



@auth.post('/sign-in/', 
    response_model=sch.Token, 
    status_code=status.HTTP_200_OK
)
async def auth_signin(
    company: Company, db: DB,
    background_tasks: BackgroundTasks, 
    auth_data: OAuth2PasswordRequestForm = Depends()
):
    user_token = srv.authenticate_user(db, auth_data.username, auth_data.password)
    srv.logger(background_tasks, auth_data.username, message='SIGN-IN')
    return user_token


@auth.post('/sign-up/', 
    response_model=sch.Token, 
    status_code=status.HTTP_201_CREATED
)
async def auth_signup(
    company: Company, db: DB, request: Request,
    account_data: sch.AccountCreate
):
    return srv.register_new_user(request, db, account_data)


@auth.get('/activate-account/{uid}/{token}', 
    status_code=status.HTTP_202_ACCEPTED
)
async def activate_account(
    company: Company, db: DB, 
    uid: str, token: str
):
    return srv.activate_account(db, uid, token)


# @auth.post('/check-email/', 
#     response_model=sch.AccountEmail,
#     status_code=status.HTTP_202_ACCEPTED
# )
# async def account_email_check(
#     company: Company, db: DB, request: Request,
#     bg_tasks: BackgroundTasks,
#     account_email: sch.AccountEmail
# ):
#     return srv.account_email_check(request, db, bg_tasks, account_email)