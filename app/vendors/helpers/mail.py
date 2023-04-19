from pathlib import Path
from .token import get_user_uid_token
from app.config import cfg
from jinja2 import (
	Environment, 
	PackageLoader, 
	select_autoescape, 
	FileSystemLoader, 
)



def get_chunks_receivers(receivers):
	for i in range(0, len(receivers), cfg.mail_max_emails):
		yield lst[i : i + n]



def get_mail_html_with_data(html_template, **kwargs):
	root_path = cfg.root_path 
	template_path  = root_path / cfg.resources_dir
	env = Environment(
		loader=FileSystemLoader(template_path, encoding='utf-8'),
		autoescape=select_autoescape(['html', 'xml'])
	)
	template = env.get_template(html_template)
	return template.render(**kwargs)



def get_activate_account_mail(request, user, html_template = None, files = []):
	subject = 'Activate account'
	user_uid_token = '/'.join(get_user_uid_token(user))
	activation_account_link = f'{request.base_url}auth/account_activate/{user_uid_token}'
	mail_data = {
		'sender': cfg.mail_default_sender,
		'to': user.email,
		'subject': subject,
		'activation_account_link': activation_account_link,
		'files': files,
	}
	mail_data['html'] = get_mail_html_with_data(
		html_template, 
		subject = subject,
		sender = mail_data['sender'],
		activation_account_link = activation_account_link,
	)
	return mail_data


def get_reset_passwd_account_mail(request, user, html_template = None, files = []):
	subject = 'Reset password'
	user_uid_token = '/'.join(get_user_uid_token(user))
	reset_passwd_account_link = f'{request.base_url}auth/account_reset_password/{user_uid_token}'
	mail_data = {
		'sender': cfg.mail_default_sender,
		'to': user.email,
		'subject': subject,
		'reset_passwd_account_link': reset_passwd_account_link,
		'files': files,
	}
	mail_data['html'] = get_mail_html_with_data(
		html_template, 
		subject = subject,
		sender = mail_data['sender'],
		reset_passwd_account_link = reset_passwd_account_link,
	)
	return mail_data



def get_mail_data(to_emails=[], html_template = None, **kwargs):
	subject = kwargs.get('subject', '--?--')
	files = kwargs.get('files', [])
	mail_data = {
		'sender': cfg.mail_default_sender,
		'to': to_email,
		'subject': subject,
		'files': files,
	}
	try:
		mail_data['html'] = get_mail_html_with_data(html_template, **kwargs)
	except:
		mail_data['html'] = ''
	return mail_data

