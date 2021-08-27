#!/usr/bin/env python3

from typing import Any, Dict, List, Optional
from CloudflareAPI.network import Request

class CFBase:
    def __init__(self) -> None:
        self.base_url = "https://api.cloudflare.com/client/v4"

    def build_url(self, path: Optional[str] = None) -> str:
        if path is None:
            return f"{self.base_url}{self.base_path}"
        else:
            if path.startswith("/"):
                return f"{self.base_url}{self.base_path}{path}"
            return f"{self.base_url}{self.base_path}/{path}"

class Worker(CFBase):
    def __init__(self, request: Request, account_id: str) -> None:
        self.req = request
        self.base_path = f"/accounts/{account_id}/workers/scripts"
        super().__init__()

    def list(self, detailed: bool = False, params: Optional[Dict[str, Any]] = None) -> List:
        _url = self.build_url()
        _workers = self.req.get(_url, params=params)
        if detailed:
            wlist = [
                {
                    worker["id"]: [
                        {item["script"]: item["pattern"]} for item in worker["routes"]
                    ]
                }
                if worker["routes"] is not None
                else {worker["id"]: "No routes"}
                for worker in _workers
            ]
        else:
            wlist = [worker["id"] for worker in _workers]
        return wlist

class Storage(CFBase):
    def __init__(self, request: Request, account_id: str) -> None:
        self.req = request
        self.base_path = f"/accounts/{account_id}/storage/kv/namespaces"
        super().__init__()

class Cloudflare:

    def __init__(self, token: str, account_id: str) -> None:
        self.__token = token
        self.__id = account_id
        self.base_url = "https://api.cloudflare.com/client/v4"

        self.req = Request(base=self.base_url, token=self.__token)

        self.worker = Worker(request=self.req, account_id=self.__id)
        self.store = Storage(request=self.req, account_id=self.__id)