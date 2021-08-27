#!/usr/bin/env python3

from typing import Any, Dict, List, Optional, Union
from CloudflareAPI.base import CFBase
from CloudflareAPI.network import Request


class Storage(CFBase):
    def __init__(self, request: Request, account_id: str) -> None:
        self.req = request
        self.base_path = f"/accounts/{account_id}/storage/kv/namespaces"
        super().__init__()

    def list(self, detailed: bool = False, params: Optional[Dict[str, Any]] = None) -> Any:
        url = self.build_url()
        nslist: Any = self.req.get(url, params=params)
        if not detailed:
            nslist = {ns["title"]: ns["id"] for ns in nslist}
        return nslist