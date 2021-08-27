#!/usr/bin/env python3

import requests
from typing import Any, Optional, Union

from requests.models import Response
from CloudflareAPI.exceptions import CFError


class Request:
    def __init__(self, base: str, token: str) -> None:
        self.base_url = base
        self.session = requests.Session()
        self.session.headers.update({"Authorization": f"Bearer {token}"})

    def __del__(self):
        if self.session:
            self.session.close()
            self.session = None

    def parse(self, response: Response):
        return response.json()

    def get(
        self,
        url: Union[str, bytes],
        params: Optional[Any] = None,
        data: Optional[Any] = None,
        headers: Optional[Any] = None,
        *args,
        **kwargs
    ):
        _res = self.session.get(url, params=params, data=data, headers=headers, *args, **kwargs)
        data = self.parse(_res)
        keys = data.keys()
        if _res.ok:
            return data["result"]
        else:
            if "errors" in keys and data["errors"]:
                raise CFError.APIError(data["errors"])
            elif "error" in keys and data["error"]:
                raise CFError.APIError(data["error"])
            else:
                raise CFError.APIError("Unkown error")
