#!/usr/bin/env python
# encoding: utf-8

import typing
from starlette.types import ASGIApp
from starlette.requests import Request
from starlette.responses import Response
from starlette.middleware.base import BaseHTTPMiddleware

from src.utils.auth import decode_token, create_access_token
from src.models import api_redis


RequestResponseEndpoint = typing.Callable[[Request], typing.Awaitable[Response]]
DispatchFunction = typing.Callable[
    [Request, RequestResponseEndpoint], typing.Awaitable[Response]
]


class AccessTokenCheckMiddleware(BaseHTTPMiddleware):
    def __init__(
        self, app: ASGIApp,
        dispatch: typing.Optional[DispatchFunction] = None,
        secret_key: str = '',
    ) -> None:
        super().__init__(app, dispatch)
        self.secret_key = secret_key

    async def dispatch(self, request, call_next):
        response = await call_next(request)
        headers = request.headers
        access_token = headers.get('Authorization')
        req_auth = headers.get('Req-Auth')
        if access_token and not req_auth:
            access_token = access_token.split('Bearer ', 1)
            if len(access_token) > 1:
                access_token = access_token[1]
                token_data = decode_token(access_token, self.secret_key)
                if not token_data:
                    username = api_redis.check_access_token(access_token)
                    if username:
                        access_token, expire = create_access_token(
                            data={"sub": username},
                            secret_key=self.secret_key
                        )
                        expire = expire.strftime('%Y-%m-%d %H:%M:%S')
                        response.headers['Access-Control-Expose-Headers'] = 'set-access-token,set-access-token-expire'
                        response.headers['set-access-token'] = access_token
                        response.headers['set-access-token-expire'] = expire
        return response
