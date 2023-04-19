
def routers_factory(app, routers):
	for router in routers:
		app.include_router(router)