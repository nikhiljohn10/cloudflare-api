#!/usr/bin/env python3

from json.decoder import JSONDecodeError
import requests
from typing import Any, Dict, Optional, Union

from requests.models import Response
from CloudflareAPI.exceptions import CFError, APIError


class Request:
    def __init__(self, base: str, token: str) -> None:
        self.base_url = base
        self.session = requests.Session()
        self.session.headers.update({"Authorization": f"Bearer {token}"})

    def __del__(self):
        if self.session:
            self.session.close()
            self.session = None

    def get_result(self, response: Response) -> Optional[Union[Dict[str, Any], bool]]:
        try:
            data = response.json()
            keys = data.keys()
        except JSONDecodeError:
            return None
        if response.ok:
            if data["result"] is None:
                return data["success"]
            return data["result"]
        else:
            if "errors" in keys and data["errors"]:
                raise APIError(data["errors"])
            elif "error" in keys and data["error"]:
                raise APIError(data["error"])
            else:
                raise CFError("Unkown error")

    def parse(self, response: Response):
        result = self.get_result(response)
        if result is None:
            return response.text
        else:
            return result

    def get(
        self,
        url: str,
        params: Optional[Any] = None,
        data: Optional[Any] = None,
        headers: Optional[Any] = None,
    ):
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
            if isinstance(data, str) or isinstance(data, bytes):
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
            if isinstance(data, str) or isinstance(data, bytes):
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
            if isinstance(data, str) or isinstance(data, bytes):
                _res = self.session.delete(
                    url, params=params, data=data, headers=headers
                )
            else:
                _res = self.session.delete(
                    url, params=params, json=data, headers=headers
                )
        return self.parse(_res)
