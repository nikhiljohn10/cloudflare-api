#!/usr/bin/env python3

from CloudflareAPI.core import CFBase


class User(CFBase):
    def __init__(self) -> None:
        self.request = self.get_request("user")

    def details(self, minimal: bool = True):
        data = self.request.get()
        if minimal and "organizations" in data.keys():
            del data["organizations"]
        return data
