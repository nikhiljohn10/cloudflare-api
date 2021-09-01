#!/usr/bin/env python3

from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Union
from CloudflareAPI.core import CFBase, Request
from CloudflareAPI.exceptions import CFError


@dataclass
class Namespace(CFBase):
    def __init__(self, id: str, title: str, supports_url_encoding: bool) -> None:
        self.id = id
        self.title = title
        self.supports_url_encoding = supports_url_encoding
        self.base_path = f"/accounts/{self.account_id}/storage/kv/namespaces/{self.id}/values/:key_name"

    def list(
        self,
        limit: int = 1000,
        cursor: Optional[str] = None,
        prefix: Optional[str] = None,
    ) -> List[Dict[str, str]]:
        ...

    def read(self, key: str) -> str:
        ...

    def write(
        self,
        key: str,
        value: str,
        metadata: Dict[str, str],
        expiration: str = 1578435000,
        expiration_ttl: int = 300,
    ) -> bool:
        ...

    def bulk_write(self, data: Dict[str, str]) -> bool:
        ...

    def delete(self, key: str) -> bool:
        ...

    def __str__(self) -> str:
        return f"{self.title}: {self.id}"

    def __repr__(self) -> str:
        return "%r" % (self.__dict__)

    def dict(self) -> Dict[str, str]:
        return dict(
            id=self.id,
            title=self.title,
            supports_url_encoding=self.supports_url_encoding,
        )


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
