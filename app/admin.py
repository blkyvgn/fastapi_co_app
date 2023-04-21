from app.vendors.base.app import AppFastApi
from app.http.middlewares import admin_middlewares
from app.http.apps.routers import admin_routers
from app.factories import (
	middlewares_factory, 
	routers_factory,
)

__all__ = ('create_admin_app',)


def create_admin_app():
	admin_app = AppFastApi()
	middlewares_factory(admin_app, admin_middlewares)
	routers_factory(admin_app, admin_routers)
	return admin_app