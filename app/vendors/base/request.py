from fastapi import Request


class AppRequest(Request):
	async def body(self) -> bytes:
		if not hasattr(self, '_body'):
			body = await super().body()
			self._body = body
		return self._body