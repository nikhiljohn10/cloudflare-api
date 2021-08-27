#!/usr/bin/env python3

import requests
from json import dumps as jsonDumps
from json.decoder import JSONDecodeError
from requests.models import Response
from requests.exceptions import HTTPError, ConnectionError, Timeout, RequestException
from typing import Dict, List, Optional, Any, Union
from cloudflare.exceptions import OutputError, TokenError


def jprint(content: Dict[str, Any], title: Optional[str] = None) -> None:
    if title is not None:
        data = {title: content}
    else:
        data = content
    print(jsonDumps(data, indent=2))


class Cloudflare:
    def __init__(
        self,
        key: str,
        id: str,
        verbose: bool = False,
    ) -> None:
        self.account_id = id
        self.verbose = verbose
        self.headers = {"Authorization": f"Bearer {key}"}
        self.base_url = "https://api.cloudflare.com/client/v4"
        status = self.get("/user/tokens/verify")["status"]
        if status != "active":
            raise TokenError("Invalid token")

    def get_url(self, url: str) -> str:
        if not url.startswith("https") and url:
            if url.startswith("/"):
                return self.base_url + url
            else:
                return self.base_url + f"/{url}"
        return url

    def get_result(self, response: Response) -> Any:
        result = None
        try:
            data = response.json()
            keys = data.keys()

            if "errors" in keys:
                for err in data["errors"]:
                    raise OutputError(err["message"], err["code"])
            elif "error" in keys:
                raise OutputError(data["error"], data["code"])

            if "result" in keys and data["result"] is not None:
                return data["result"]
            elif "success" in keys:
                return data["success"]
        except JSONDecodeError:
            return response.text

        if not result or result is None:
            return response.status_code == 200

        return result

    def get(self, url: str, params: Dict[str, str] = {}, type: Optional[str] = None) -> Any:
        headers = {"Content-Type": "application/json"}
        headers.update(self.headers)
        if type is not None:
            headers["Content-Type"] = type
        response = requests.get(
            url=self.get_url(url),
            params=params,
            headers=headers,
        )
        return self.get_result(response)

    def post(
        self,
        url: str,
        data: Optional[Union[str, bytes]] = None,
        json: Optional[Dict[str, Any]] = None,
        params: Dict[str, str] = {},
        type: Optional[str] = None,
    ) -> Any:
        headers = {"Content-Type": "application/json"}
        headers.update(self.headers)
        if type is not None:
            headers["Content-Type"] = type
        response = requests.post(
            url=self.get_url(url),
            params=params,
            data=data,
            json=json,
            headers=headers,
        )
        return self.get_result(response)

    def put(
        self,
        url: str,
        data: Optional[Union[str, bytes]] = None,
        json: Optional[Dict[str, Any]] = None,
        files: Optional[Union[List[str], str]] = None,
        params: Dict[str, str] = {},
        type: Optional[str] = None,
    ) -> Any:
        headers = {"Content-Type": "application/json"}
        headers.update(self.headers)
        if files is not None:
            del headers["Content-Type"]
        elif type is not None:
            headers["Content-Type"] = type

        response = requests.put(
            url=self.get_url(url),
            params=params,
            data=data,
            json=json,
            files=files,
            headers=headers,
        )
        return self.get_result(response)

    def delete(self, url: str, params: Dict[str, str] = {}) -> Any:
        response = requests.delete(
            url=self.get_url(url),
            params=params,
            headers=self.headers,
        )
        return self.get_result(response)
