#!/usr/bin/env python3

from typing import Dict
from dataclasses import dataclass

from .network import Request
from .configuration import config


@dataclass
class CFBase:
    def props(self) -> Dict[str, str]:
        return self.__dict__

    def get_request(self, path: str):
        return Request(token=config.token(), path=path)
