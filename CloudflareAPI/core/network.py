#!/usr/bin/env python3

import requests
from typing import Any, Dict, Optional, Union

from requests.models import Response
from CloudflareAPI.exceptions import CFError, APIError

CLOUDFLARE_API_ROOT_URI = "https://api.cloudflare.com/client/v4"


class Request:
    def __init__(self, token: str, path: str = "") -> None:
        if not token:
            raise CFError("Invalid api token")
        path = self.__fix_path(path)
        self.base_url = f"{CLOUDFLARE_API_ROOT_URI}{path}"
        self.session = requests.Session()
        self.session.headers.update({"Authorization": f"Bearer {token}"})

    def verify_token(self):
        verification_url = f"{CLOUDFLARE_API_ROOT_URI}/user/tokens/verify"
        if self.get(verification_url)["status"] != "active":
            raise CFError("Invalid api token")

    def __del__(self):
        if self.session:
            self.session.close()
            self.session = None

    def get_result(self, response: Response) -> Union[Dict[str, Any], bool]:
        data = response.json()
        if data["result"] is None:
            return data["success"]
        return data["result"]

    def parse_error(self, response: Response) -> None:
        data = response.json()
        keys = data.keys()
        if "error" in keys or "errors" in keys:
            if data["errors"]:
                raise APIError(data["errors"])
            if data["error"]:
                raise APIError(data["error"])
        raise CFError("Unkown error")

    def parse(self, response: Response) -> Union[Dict[str, Any], str, bool]:
        if not response.ok:
            self.parse_error(response)
        if "json" not in response.headers["content-type"]:
            return response.text
        return self.get_result(response)

    def __fix_path(self, path):
        if not path.startswith("/"):
            path = "/" + path
        return path

    def url(self, path: Optional[str] = None):
        if path is None:
            return self.base_url
        return self.base_url + self.__fix_path(path)

    def get(
        self,
        url: Optional[str] = None,
        params: Optional[Any] = None,
        data: Optional[Any] = None,
        headers: Optional[Any] = None,
    ):
        url = self.url() if url is None or not url else self.url(url)
        _res = self.session.get(url, params=params, data=data, headers=headers)
        return self.parse(_res)

    def post(
        self,
        url: str,
        params: Optional[Any] = None,
        data: Optional[Any] = None,
        json: Optional[Any] = None,
        headers: Optional[Any] = None,
        files: Optional[Any] = None,
    ):
        if json is not None:
            _res = self.session.post(
                url, params=params, json=json, headers=headers, files=files
            )
        else:
            if isinstance(data, (bytes, str)):
                _res = self.session.post(
                    url, params=params, data=data, headers=headers, files=files
                )
            else:
                _res = self.session.post(
                    url, params=params, json=data, headers=headers, files=files
                )
        return self.parse(_res)

    def put(
        self,
        url: str,
        params: Optional[Any] = None,
        data: Optional[Any] = None,
        json: Optional[Any] = None,
        headers: Optional[Any] = None,
        files: Optional[Any] = None,
    ):
        if json is not None:
            _res = self.session.put(
                url, params=params, json=json, headers=headers, files=files
            )
        else:
            if isinstance(data, (bytes, str)):
                _res = self.session.put(
                    url, params=params, data=data, headers=headers, files=files
                )
            else:
                _res = self.session.put(
                    url, params=params, json=data, headers=headers, files=files
                )
        return self.parse(_res)

    def delete(
        self,
        url: str,
        params: Optional[Any] = None,
        data: Optional[Any] = None,
        json: Optional[Any] = None,
        headers: Optional[Any] = None,
    ):
        if json is not None:
            _res = self.session.delete(url, params=params, json=json, headers=headers)
        else:
            if isinstance(data, (bytes, str)):
                _res = self.session.delete(
                    url, params=params, data=data, headers=headers
                )
            else:
                _res = self.session.delete(
                    url, params=params, json=data, headers=headers
                )
        return self.parse(_res)
