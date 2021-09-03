#!/usr/bin/env python3

from typing import Optional
from CloudflareAPI.core import CFBase, Request
from CloudflareAPI.api import Account, Worker, Storage, User


class Cloudflare(CFBase):
    def __init__(
        self, token: str, account_id: Optional[str] = None, bare: bool = False
    ) -> None:
        self.account = Account()
        # self.user = User()
        # if not bare:
        #     self.worker = self.get_worker()
        #     self.store = self.get_store()

    def get_worker(self):
        return Worker()

    def get_store(self):
        return Storage()
