#!/usr/bin/env python3

from dataclasses import dataclass
from typing import Dict, List, Optional
from CloudflareAPI.core import CFBase


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
