#!/usr/bin/env python3

from CloudflareAPI.core import CFBase, Request


class User(CFBase):
    def __init__(self) -> None:
        self.base_path = f"/user"

    def details(self, minimal: bool = True):
        url = self.build_url()
        data = self.request.get(url)
        if minimal and "organizations" in data.keys():
            del data["organizations"]
        return data
