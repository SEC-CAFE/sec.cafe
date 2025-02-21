#!/usr/bin/env python
# encoding: utf-8

import typing

from starlette.datastructures import URL
from starlette.types import ASGIApp, Receive, Scope, Send
from fastapi.middleware.trustedhost import TrustedHostMiddleware


class TrustedHostExtMiddleware(TrustedHostMiddleware):
    def __init__(
        self,
        app: ASGIApp,
        allowed_hosts: typing.Optional[typing.Sequence[str]] = None,
        www_redirect: bool = True,
        exclude_apis: list = [],
    ) -> None:
        super().__init__(app, allowed_hosts, www_redirect)
        self.exclude_apis = exclude_apis

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        url = URL(scope=scope)
        path = url.path
        if path in self.exclude_apis:
            await self.app(scope, receive, send)
        else:
            super().__call__(scope, receive, send)
