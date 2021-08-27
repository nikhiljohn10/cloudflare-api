#!/usr/bin/env python3

from typing import Any, Dict, Optional
from CloudflareAPI.base import CFBase
from CloudflareAPI.exceptions import CFError
from CloudflareAPI.network import Request


class Storage(CFBase):
    def __init__(self, request: Request, account_id: str) -> None:
        self.req = request
        self.base_path = f"/accounts/{account_id}/storage/kv/namespaces"
        super().__init__()

    def list(
        self, detailed: bool = False, params: Optional[Dict[str, Any]] = None
    ) -> Any:
        url = self.build_url()
        nslist: Any = self.req.get(url, params=params)
        if not detailed:
            nslist = {ns["title"]: ns["id"] for ns in nslist}
        return nslist

    def id(self, title: str):
        stores = self.list()
        title = title.upper()
        if title in stores:
            return stores[title]
        else:
            raise CFError("Namespace not found")

    def create(self, title: str) -> bool:
        title = title.upper()
        url = self.build_url()
        result = self.req.post(url, json=dict(title=title))
        return result["title"] == title

    def delete(self, title: str):
        title = title.upper()
        store_id = self.id(title)
        url = self.build_url(store_id)
        return self.req.delete(url)
