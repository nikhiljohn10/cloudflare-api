#!/usr/bin/env python3

import json
from typing import Any, Dict, List, Optional
from CloudflareAPI.core import CFBase
from CloudflareAPI.exceptions import CFError
from CloudflareAPI.dataclass.namespace import Namespace


class Storage(CFBase):
    def __init__(self, account_id: str) -> None:
        self.account_id = account_id
        base_path = f"/accounts/{self.account_id}/storage/kv/namespaces"
        self.request = self.get_request(base_path)

    def list(
        self,
        params: Optional[Dict[str, Any]] = None,
    ) -> Any:
        nslist = self.request.get(params=params)
        nslist = [Namespace(self.account_id, ns) for ns in nslist]
        return nslist

    def get_ns(self, id: str) -> Namespace:
        nslist = self.list()
        for ns in nslist:
            if ns.id == id:
                return ns
        raise CFError("Invalid namespace id")

    def get_id(self, namespace: str):
        stores = self.list()
        namespace = namespace.upper()
        if namespace in stores:
            return stores[namespace]
        raise CFError("Namespace not found")

    def create(self, namespace: str) -> bool:
        namespace = namespace.upper()
        result = self.request.post(json=dict(title=namespace))
        if result["title"] == namespace:
            return result["id"]
        raise CFError("Unable to create namespace")

    def rename(self, old_namespace: str, new_namespace: str):
        old_namespace = old_namespace.upper()
        new_namespace = new_namespace.upper()
        store_id = self.get_id(old_namespace)
        return self.request.put(store_id, json={"title": new_namespace})

    def delete(self, namespace: str):
        namespace = namespace.upper()
        store_id = self.get_id(namespace)
        return self.request.delete(store_id)