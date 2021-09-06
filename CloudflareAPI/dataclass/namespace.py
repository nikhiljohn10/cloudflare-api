#!/usr/bin/env python3


from dataclasses import dataclass
import json
from typing import Dict, List, Optional
from CloudflareAPI.core import CFBase, Request


class Namespace(CFBase):
    id: str
    title: str
    supports_url_encoding: bool

    class Metadata:
        def __init__(self, key: str, value: str) -> None:
            self.data = {key.strip(): value}

        def __call__(self) -> Dict[str, str]:
            return (None, json.dumps(self.data), "application/json")

    class NSBundler:
        def __init__(self) -> None:
            self.list = []

        def add(
            self,
            key: str,
            value: str,
            expiration: Optional[int] = None,
            expiration_ttl: Optional[int] = None,
            metadata: Optional["Namespace.Metadata"] = None,
            base64: Optional[bool] = None,
        ):
            data = {
                "key": key.strip(),
                "value": value,
            }
            if metadata is not None:
                data.update({"metadata": metadata.data})
            params = {
                "expiration": expiration,
                "expiration_ttl": expiration_ttl,
                "base64": base64,
            }
            for key, value in params.items():
                if params[key] is not None:
                    data.update({key: value})
            self.list.append(data)

    def __init__(self, account_id, data) -> None:
        self.id = data["id"]
        self.title = data["title"]
        self.supports_url_encoding = data["supports_url_encoding"]
        base_path = f"/accounts/{account_id}/storage/kv/namespaces/{self.id}"
        self.request = self.get_request(base_path)
        super().__init__()

    def keys(
        self,
        limit: int = 1000,
        cursor: Optional[str] = None,
        prefix: Optional[str] = None,
    ) -> List[Dict[str, str]]:
        params = {"limit": limit, "cursor": cursor, "prefix": prefix}
        params = self.parse_params(params)
        keys = self.request.get("keys", params=params)
        keys = [key["name"] for key in keys]
        return keys

    def read(self, key: str) -> str:
        return self.request.get(f"values/{key}")

    def write(
        self,
        key: str,
        value: str,
        metadata: Optional[Metadata] = None,
        expiration: Optional[str] = None,
        expiration_ttl: Optional[int] = None,
    ) -> bool:
        params = {"expiration": expiration, "expiration_ttl": expiration_ttl}
        params = self.parse_params(params)
        if metadata is None:
            headers = {"Content-Type": "text/plain"}
            return self.request.put(
                f"values/{key}", data=value, params=params, headers=headers
            )
        miltipart_data = {
            "metadata": metadata(),
            "value": value,
        }
        return self.request.put(f"values/{key}", files=miltipart_data)

    def bulk_write(self, bundle: NSBundler) -> bool:
        return self.request.put("bulk", json=bundle.list)

    def delete(self, key: str) -> bool:
        return self.request.delete(f"values/{key}")

    def bulk_delete(self, keys: List[str]) -> bool:
        return self.request.delete("bulk", json=keys)

    def __repr__(self) -> str:
        return json.dumps(
            {
                "id": self.id,
                "title": self.title,
                "supports_url_encoding": self.supports_url_encoding,
            },
            indent=2,
        )

    def __str__(self) -> str:
        return f"{self.title}: {self.id}"
