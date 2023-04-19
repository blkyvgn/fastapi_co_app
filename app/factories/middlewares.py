
def middlewares_factory(app, middlewares):
	for middleware in middlewares:
		app.add_middleware(middleware)