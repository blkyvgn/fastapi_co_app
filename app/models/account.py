from app.vendors.base.database import BaseModel
from app.vendors.utils.crypto import password_context
from app.vendors.helpers.image import resize_image
from app.services.celery.tasks import send_email
from app.vendors.helpers import mail as mail_helper
from app.vendors.helpers.file import (
	write_file, 
	get_or_create_storage_dir,
)
from sqlalchemy.orm import (
	relationship,
	column_property,
	synonym,
)
from app.vendors.mixins.model import (
	TimestampsMixin, 
	ValidMixin,
	HelpersMixin,
)
from sqlalchemy import (
	Column, 
	ForeignKey, 
	Integer, 
	String,
	Boolean,
	JSON,
)
from app.config import cfg


class Account(ValidMixin, TimestampsMixin, HelpersMixin, BaseModel):
	__tablename__ = 'accounts'

	username = Column(
		String, 
		unique=True
	)
	email = Column(
		String, 
		unique=True
	)
	password = Column(
		String
	)
	is_activated = Column(
		Boolean,
		default=False,
	)
	permissions = Column(
		JSON,
	)
	articles = relationship(
		'Article', 
		back_populates='account'
	)
	media = relationship(
		'Media', 
		back_populates='account'
	)
	chat_rooms = relationship(
		'Room', 
		back_populates='account'
	)
	profile = relationship(
		'Profile', 
		back_populates='account',
		uselist=False
	)
	roles = relationship('Role', secondary='accounts_roles', back_populates='accounts')

	@staticmethod
	def get_hashed_password(password: str) -> str:
		return password_context.hash(password)

	def verify_password(self, password: str) -> bool:
		return password_context.verify(password, self.password)

	def send_activation_mail(self, request):
		try:
			email_data = mail_helper.get_activate_account_mail(
				request, 
				self, 
				'mail/activate_account.html'
			)
			send_email.apply_async(
				args=[email_data], 
				countdown=60
			)
		except:
			print('------------------------------ mail -----------------------------')
			print(mail_helper.get_activate_account_mail(
				request, 
				self, 
				'mail/activate_account.html')
			)
			print('-----------------------------------------------------------------')

	def send_reset_passwd_mail(self, request):
		try:
			email_data = mail_helper.get_reset_passwd_account_mail(
				request, 
				self, 
				'mail/reset_password.html'
			)
			send_email.apply_async(
				args=[email_data], 
				countdown=60
			)
		except:
			print('------------------------------ mail -----------------------------')
			print(mail_helper.get_reset_passwd_account_mail(
				request, 
				self, 
				'mail/reset_password.html')
			)
			print('-----------------------------------------------------------------')



class Profile(HelpersMixin, BaseModel):
	__tablename__ = 'profiles'

	first_name = Column(
		String(80)
	)
	last_name = Column(
		String(80)
	)
	photo = Column(
		String(255)
	)
	female = Column(
		Boolean,
		default=True
	)
	account_id = Column(
		Integer, 
		ForeignKey('accounts.id')
	)
	account = relationship(
		'Account', 
		back_populates='profile'
	)

	full_name = column_property(first_name + ' ' + last_name)

	# gen = synonym('female')

	# @property
	# def sex(self):
	# 	return 'female' if self._sex else 'male'

	# @sex.setter
	# def sex(self, v):
	# 	self._sex = v == 'female'

	@staticmethod
	def save_and_resize_photo(photo, ext_path: str, photo_width: int):
		if not photo:
			return None
		try:
			storage_path = cfg.root_path / cfg.upload_folder_dir
			dir_path = get_or_create_storage_dir(storage_path, ext_path)
			photo_file_path = write_file(photo, dir_path)
			resize_image(photo_file_path, photo_width)
			photo_file_subpath = f'{ext_path}/{photo.filename}'
		except:
			photo_file_subpath = None

		return photo_file_subpath

class RolePermission(BaseModel):
	__tablename__ = 'roles_permissions'

	role_id = Column(
		Integer, 
		ForeignKey('roles.id')
	)
	permission_id = Column(
		Integer, 
		ForeignKey('permissions.id')
	)

class AccountRole(BaseModel):
	__tablename__ = 'accounts_roles'

	account_id = Column(
		Integer, 
		ForeignKey('accounts.id')
	)
	role_id = Column(
		Integer, 
		ForeignKey('roles.id')
	)

class Role(ValidMixin, TimestampsMixin, BaseModel):
	__tablename__ = 'roles'

	role = Column(
		String(50), 
		unique=True,
	)
	name = Column(
		JSON,
		default = dict
	)
	company_id = Column(
		Integer, 
		ForeignKey('companies.id')
	)
	company = relationship(
		'Company', 
		back_populates='roles'
	)
	permissions = relationship('Permission', secondary='roles_permissions', back_populates='roles')
	accounts = relationship('Account', secondary='accounts_roles', back_populates='roles')

class Permission(HelpersMixin, BaseModel):
	__tablename__ = 'permissions'

	permission = Column(
		String(50), 
		unique=True,
	)
	name = Column(
		JSON,
		default = dict
	)
	roles = relationship('Role', secondary='roles_permissions', back_populates='permissions')



