import time
from typing import Callable
from fastapi import APIRouter, FastAPI, Request, Response
from fastapi.routing import APIRoute
from .request import AppRequest


class AppRouter(APIRoute):
    def get_route_handler(self) -> Callable:
        original_route_handler = super().get_route_handler()
        async def custom_route_handler(request: Request) -> Response:
            request = AppRequest(request.scope, request.receive)
            # before = time.time()
            response: Response = await original_route_handler(request)
            # duration = time.time() - before
            # response.headers["X-Response-Time"] = str(duration)
            # print(f"route duration: {duration}")
            # print(f"route response: {response}")
            # print(f"route response headers: {response.headers}")
            return response

        return custom_route_handler