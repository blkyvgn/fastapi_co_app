from .auth.api import auth
from .company.api import company 
from .company.admin.api import company as admin_company
from .category.api import category
from .category.admin.api import category as admin_category
from .account.api import account
from .account.admin.api import account as admin_account
from .article.api import article
from .article.admin.api import article as admin_article
from .media.api import media
from .media.admin.api import media as admin_media
from .chat.api import chat

routers = [
	auth,
	account,
	company,
	category,
	article,
	media,
	chat,
]

admin_routers = [
	admin_company,
	admin_category,
	admin_article,
	admin_account,
	admin_media,
]