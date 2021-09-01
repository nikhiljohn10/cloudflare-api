#!/usr/bin/env python3

from typing import Optional
from CloudflareAPI.core import CFBase, Request
from CloudflareAPI.api import Account, Worker, Storage, User


class Cloudflare(CFBase):
    def __init__(
        self, token: str, account_id: Optional[str] = None, bare: bool = False
    ) -> None:
        self.__class__.account_id = account_id
        self.__class__.request = Request(token=token)
        self.account = Account()
        if not self.account_id or self.account_id is None:
            self.account_id = self.account.get_id()
        self.user = User()
        if not bare:
            self.worker = self.get_worker()
            self.store = self.get_store()

    def get_worker(self):
        return Worker()

    def get_store(self):
        return Storage()
