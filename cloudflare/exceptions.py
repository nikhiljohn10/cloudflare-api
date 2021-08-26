#!/usr/bin/env python3

from typing import Optional


class CloudflareError(Exception):
    def __init__(
        self, message: str = "Unknown Error found", code: Optional[str] = None
    ) -> None:
        self.message = message
        self.code = code
        super().__init__(self.message)

    def __str__(self) -> str:
        if self.code is not None:
            return f"Cloudflare Error {self.code}: {self.message}"
        return f"Cloudflare Error: {self.message}"


class OutputError(CloudflareError):
    ...


class InputError(CloudflareError):
    ...


class TokenError(CloudflareError):
    ...


class ZoneError(CloudflareError):
    ...


class NamespaceError(CloudflareError):
    ...
