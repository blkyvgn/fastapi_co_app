from app.vendors.base.app import AppFastApi
from app.factories import (
	middlewares_factory, 
	routers_factory,
)
from app.http.middlewares import middlewares
from app.http.apps.routers import routers

__all__ = ('create_app',)

def create_app(admin: bool = True):
	app = AppFastApi()
	middlewares_factory(app, middlewares)
	routers_factory(app, routers)
	if admin:
		from .admin import create_admin_app
		app.mount('/admin', create_admin_app())
	return app