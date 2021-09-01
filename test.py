#!/usr/bin/env python3

from secrets import token_urlsafe
from dataclasses import dataclass


class Request:
    def __init__(self, token) -> None:
        self.base_url = "https://localhost/client/api/v4/" + token

    def get(self, path):
        url = self.base_url + path
        return f"GET {url}"

    def put(self, data, path):
        url = self.base_url + path
        return f"PUT {url} <- {data}"


@dataclass
class Base:
    request: Request
    account_id: str


class Account(Base):
    def __init__(self) -> None:
        self.base_path = "/accounts"
        super().__init__(self.request, self.account_id)

    def details(self):
        return self.request.get(self.base_path + "/" + self.account_id)


class Store(Base):
    def __init__(self) -> None:
        self.base_path = "/store"

    def read(self, name):
        return self.request.get(self.base_path + "/" + name)

    def write(self, name, value):
        return self.request.put(value, self.base_path + "/" + name)


class Master(Base):
    def __init__(self, token) -> None:
        self.account_id = "thisisatestaccountid"
        self.request = Request(token)
        self.account = Account()
        self.store = Store()


m = Master(token_urlsafe(8))

print(m.account_id)
print(m.account.details())
print(m.store.write("hello", "world"))
print(m.store.read("hello"))
