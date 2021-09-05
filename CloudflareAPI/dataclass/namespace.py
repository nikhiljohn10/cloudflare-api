#!/usr/bin/env python3

from dataclasses import dataclass
import json
from typing import Dict, List, Optional
from CloudflareAPI.core import CFBase, Request

@dataclass
class Namespace(CFBase):
    id: str
    title: str
    supports_url_encoding: bool

    def __init__(self, account_id, data) -> None:
        self.id = data["id"]
        self.title = data["title"]
        self.supports_url_encoding = data["supports_url_encoding"]
        base_path = f"/accounts/{account_id}/storage/kv/namespaces/{self.id}"
        self.request = self.get_request(base_path)
        super().__init__()

    def __to_str(self) -> str:
        return json.dumps({
            "id": self.id,
            "title": self.title,
            "supports_url_encoding": self.supports_url_encoding
        })

    def __repr__(self) -> str:
        return self.__to_str()

    def __str__(self) -> str:
        return self.__to_str()

    def list(
        self,
        limit: int = 1000,
        cursor: Optional[str] = None,
        prefix: Optional[str] = None,
    ) -> List[Dict[str, str]]:
        params = {"limit": limit, "cursor": cursor, "prefix": prefix}
        keys = self.request.get("keys", params=params)
        return keys

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
