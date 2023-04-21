from app.vendors.utils.oauth2 import oauth2_scheme
from pydantic import ValidationError
from typing import Annotated
from datetime import (
	datetime,
	timedelta,
)
from fastapi import (
	Depends,
	HTTPException,
	status,
)
from jose import (
	JWTError,
	jwt,
)
from app import models as mdl
from .. import schemas as sch
from app.config import cfg



def verify_token(token: str) -> sch.Account:
	try:
		payload = jwt.decode(
			token,
			cfg.jwt_secret,
			algorithms=[cfg.jwt_algorithm],
		)
	except JWTError:
		raise HTTPException(
			status_code=status.HTTP_401_UNAUTHORIZED,
			detail='Could not validate credentials',
			headers={'WWW-Authenticate': 'Bearer'},
		)

	account_data = payload.get('user')

	try:
		account = sch.Account.parse_obj(account_data)
	except ValidationError:
		raise HTTPException(
			status_code=status.HTTP_401_UNAUTHORIZED,
			detail='Could not validate credentials',
			headers={'WWW-Authenticate': 'Bearer'},
		)
	if not account.is_activated:
		raise HTTPException(
			status_code=status.HTTP_400_BAD_REQUEST, 
			detail='Not activated user',
			headers={'WWW-Authenticate': 'Bearer'},
		)
	if not account.is_valid:
		raise HTTPException(
			status_code=status.HTTP_400_BAD_REQUEST, 
			detail='Blocked user',
			headers={'WWW-Authenticate': 'Bearer'},
		)
	return account


def create_token(account: mdl.Account) -> sch.Token:
	account_data = sch.Account.from_orm(account)
	now = datetime.utcnow()
	payload = {
		'iat': now,
		'nbf': now,
		'exp': now + timedelta(seconds=cfg.jwt_expires_s),
		'sub': str(account_data.id),
		'user': account_data.dict(),
	}
	token = jwt.encode(
		payload,
		cfg.jwt_secret,
		algorithm=cfg.jwt_algorithm,
	)
	return sch.Token(access_token=token)


async def get_current_user(token: str = Depends(oauth2_scheme)) -> sch.Account:
	return verify_token(token)

CurrentUser = Annotated[sch.Account, Depends(get_current_user)]

	