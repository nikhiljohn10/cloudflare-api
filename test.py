#!/usr/bin/env python3

from secrets import token_urlsafe


class Request:
    def __init__(self, token) -> None:
        self.base_url = "https://localhost/client/api/v4/" + token

    def get(self, path):
        url = self.base_url + path
        return f"GET {url}"

    def put(self, data, path):
        url = self.base_url + path
        return f"PUT {url} <- DATA: {data}"


class Config:
    def __init__(self, token=None, account_id=None) -> None:
        self.token = token
        self.account_id = account_id

    def load_request(self):
        return Request(token=self.token)


class Account:
    def __init__(self, config) -> None:
        self.config = config
        self.request = config.load_request()
        self.base_path = "/accounts"

    def details(self):
        return self.request.get(self.base_path + "/" + self.config.account_id)


class Store:
    def __init__(self, config) -> None:
        self.request = config.load_request()
        self.base_path = "/store"

    def read(self, name):
        return self.request.get(self.base_path + "/" + name)

    def write(self, name, value):
        return self.request.put(value, self.base_path + "/" + name)


class Master:
    def __init__(self, config: Config) -> None:
        if config.account_id and config.token:
            self.config = config
        else:
            raise ValueError("Invalid configuration")
        self.config.load_request()
        self.account = Account(self.config)
        self.store = Store(self.config)


c = Config(token_urlsafe(8), "thisisatestaccountid")
m = Master(c)

print("ID:", m.account.config.account_id)
print(m.account.details())
print(m.store.write("hello", "world"))
print(m.store.read("hello"))
