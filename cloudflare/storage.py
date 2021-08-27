#!/usr/bin/env python3

from cloudflare import Cloudflare
from cloudflare.exceptions import NamespaceError


class Storage:
    def __init__(self, cf: Cloudflare) -> None:
        self.cf = cf
        self.base_url = f"{self.cf.base_url}/accounts/{self.cf.account_id}/storage/kv/namespaces"

    # def list(self):
    #     nslist = self.cf.get(self.base_url)
    #     return nslist

    # def id(self, title: str):
    #     stores = self.list()
    #     store_id = None
    #     for store in stores:
    #         if title.upper() == store["title"]:
    #             store_id = store["id"]
    #             break
    #     if store_id is None:
    #         raise NamespaceError("Namespace not found")
    #     else:
    #         return store_id

    def create(self, title: str):
        title = title.upper()
        result = self.cf.post(self.base_url, json=dict(title=title))
        if result["title"] == title:
            print(f"Created new namespace '{title}' in Cloudflare")

    def delete(self, title: str):
        title = title.upper()
        store_id = self.id(title)
        if self.cf.delete(f"{self.base_url}/{store_id}"):
            print(f"Deleted the namespace '{title}' from Cloudflare")
