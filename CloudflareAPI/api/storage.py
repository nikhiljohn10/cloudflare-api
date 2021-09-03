#!/usr/bin/env python3

from typing import Any, List, Optional
from CloudflareAPI.core import CFBase
from CloudflareAPI.exceptions import CFError
from CloudflareAPI.dataclass.namespace import Namespace


class Storage(CFBase):
    def __init__(self) -> None:
        self.base_path = f"/accounts/{self.account_id}/storage/kv/namespaces"

    def list(
        self,
        params: Optional[List[Namespace]] = None,
    ) -> Any:
        url = self.build_url()
        nslist: Any = self.req.get(url, params=params)
        nslist = [
            Namespace(ns["id"], ns["title"], ns["supports_url_encoding"])
            for ns in nslist
        ]
        return nslist

    def get_id(self, namespace: str):
        stores = self.list()
        namespace = namespace.upper()
        if namespace in stores:
            return stores[namespace]
        raise CFError("Namespace not found")

    def create(self, namespace: str) -> bool:
        namespace = namespace.upper()
        url = self.build_url()
        result = self.req.post(url, json=dict(title=namespace))
        if result["title"] == namespace:
            return result["id"]
        raise CFError("Unable to create namespace")

    def rename(self, old_namespace: str, new_namespace: str):
        old_namespace = old_namespace.upper()
        new_namespace = new_namespace.upper()
        store_id = self.get_id(old_namespace)
        url = self.build_url(store_id)
        return self.req.put(url, json={"title": new_namespace})

    def delete(self, namespace: str):
        namespace = namespace.upper()
        store_id = self.get_id(namespace)
        url = self.build_url(store_id)
        return self.req.delete(url)
