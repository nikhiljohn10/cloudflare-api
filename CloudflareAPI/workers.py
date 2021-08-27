#!/usr/bin/env python3

from pathlib import Path
from typing import Any, Dict, List, Optional
from CloudflareAPI.base import CFBase
from CloudflareAPI.network import Request


class Worker(CFBase):
    def __init__(self, request: Request, account_id: str) -> None:
        self.req = request
        self.base_path = f"/accounts/{account_id}/workers/scripts"
        super().__init__()

    def list(
        self, detailed: bool = False, params: Optional[Dict[str, Any]] = None
    ) -> List:
        url = self.build_url()
        workers = self.req.get(url, params=params)
        if detailed:
            wlist = [
                {
                    worker["id"]: [
                        {item["script"]: item["pattern"]} for item in worker["routes"]
                    ]
                }
                if worker["routes"] is not None
                else {worker["id"]: "No routes"}
                for worker in workers
            ]
        else:
            wlist = [worker["id"] for worker in workers]
        return wlist

    def download(self, name: str, directory: str = "./workers") -> int:
        url = self.build_url(name)
        data = self.req.get(url)
        directory = Path(directory)
        directory.mkdir(parents=True, exist_ok=True)
        file = directory / f"{name}.js"
        return file.write_text(data)
