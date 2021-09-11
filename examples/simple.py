#!/usr/bin/env python3

from CloudflareAPI import Cloudflare


def main():
    api = Cloudflare()
    print(api.account.list())
    print(api.user.details())
    print(api.worker.list())
    print(api.store.list())


if __name__ == "__main__":
    main()
