#!/usr/bin/env python3

from CloudflareAPI.network import Request
from CloudflareAPI.workers import Worker
from CloudflareAPI.storage import Storage


class Cloudflare:
    def __init__(self, token: str, account_id: str) -> None:
        self.__token = token
        self.__id = account_id
        self.base_url = "https://api.cloudflare.com/client/v4"

        self.req = Request(base=self.base_url, token=self.__token)
        self.worker = Worker(request=self.req, account_id=self.__id)
        self.store = Storage(request=self.req, account_id=self.__id)
