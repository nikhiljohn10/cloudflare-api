#!/usr/bin/env python3

from typing import Dict
from dataclasses import dataclass

from .network import Request


@dataclass
class CFBase:
    request: Request
    account_id: str

    def build_url(self, path: str = "") -> str:
        url = self.request.base_url
        if not hasattr(self, "base_path"):
            if self.base_path.startswith("/"):
                url += self.base_path
            else:
                url += f"/{self.base_path}"
        if path is not None:
            if path.startswith("/"):
                url += path
            else:
                url += f"/{path}"
        return url

    def dict(self) -> Dict[str, str]:
        return self.__dict__
