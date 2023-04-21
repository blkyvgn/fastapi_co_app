from .auth.api import auth
from .company.api import company 
from .company.admin.api import company as admin_company
from .category.api import category
from .category.admin.api import category as admin_category
from .account.api import account
from .account.admin.api import account as admin_account

routers = [
	auth,
	account,
	company,
	category,
]

admin_routers = [
	admin_company,
	admin_category,
	admin_account,
]