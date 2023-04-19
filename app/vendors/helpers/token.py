from six import text_type
from datetime import datetime
from app.config import cfg
import base64



def check_user_token(user, token):
	token_dict = eval(base64.b64decode(token))
	if token_raw := token_dict.get('token', False):
		token_parts = token_raw.split(':')
		return user.id == int(token_parts[0]) and token_parts[-2] == cfg.secret_key and not eval(token_parts[-1])
	return False

def get_user_uid_token(user):
	current_datatime = datetime.timestamp(datetime.now())
	uid = str({'uid': f'{str(user.id)}:{str(current_datatime)}'}).encode('utf-8')
	base64_uid = base64.b64encode(uid).decode('utf-8')
	token_raw = f'{str(user.id)}:{str(current_datatime)}:{cfg.secret_key}:{str(user.is_activated)}'
	token = str({'token': token_raw}).encode('utf-8')
	base64_token = base64.b64encode(token).decode('utf-8')
	return (base64_uid, base64_token,)