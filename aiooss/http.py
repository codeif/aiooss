# -*- coding: utf-8 -*-
import asyncio

from oss2 import defaults, http
from requests.structures import CaseInsensitiveDict

import aiohttp


class Session(object):
    """属于同一个Session的请求共享一组连接池，如有可能也会重用HTTP连接。"""

    def __init__(self, loop=None):
        self._loop = loop or asyncio.get_event_loop()

        psize = defaults.connection_pool_size
        connector = aiohttp.TCPConnector(limit=psize, loop=self._loop)

        self._aio_session = aiohttp.ClientSession(
            connector=connector,
            loop=self._loop)

    async def do_request(self, req, timeout=300):
        resp = await self._aio_session.request(req.method, url=req.url,
                                               data=req.data,
                                               params=req.params,
                                               headers=req.headers,
                                               timeout=timeout)
        return resp

    async def __aenter__(self):
        await self._aio_session.__aenter__()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self._aio_session.__aexit__(exc_type, exc_val, exc_tb)

    async def close(self):
        await self._aio_session.close()


class Request(object):
    def __init__(self, method, url,
                 data=None,
                 params=None,
                 headers=None,
                 app_name=''):
        self.method = method
        self.url = url
        self.data = http._convert_request_body(data)
        self.params = params or {}

        if not isinstance(headers, CaseInsensitiveDict):
            self.headers = CaseInsensitiveDict(headers)
        else:
            self.headers = headers

        # tell requests not to add 'Accept-Encoding: gzip, deflate' by default
        # if 'Accept-Encoding' not in self.headers:
        #     self.headers['Accept-Encoding'] = None

        if 'User-Agent' not in self.headers:
            if app_name:
                self.headers['User-Agent'] = http._USER_AGENT + '/' + app_name
            else:
                self.headers['User-Agent'] = http._USER_AGENT
