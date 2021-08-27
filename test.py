#!/usr/bin/env python3

from CloudflareAPI import Cloudflare, jsonPrint

from secret import API_TOKEN, ACCOUNT_ID


def main():
    cf = Cloudflare(token=API_TOKEN, account_id=ACCOUNT_ID)

    workers = cf.worker.list()
    jsonPrint(workers, "Workers")

    store = cf.store.list()
    jsonPrint(store, "Store")

    if cf.store.create("my_kv"):
        print("New namespace 'my_kv' is created")

    if cf.store.rename("my_kv", "my_new_kv"):
        print("New namespace 'my_kv' is renamed to 'my_new_kv'")

    ns_id = cf.store.id("my_new_kv")
    print("Namespace ID: ", ns_id)

    if cf.worker.upload(
        name="tester", file="test.js", bindings=dict(name="my_new_kv", id=ns_id)
    ):
        print("Worker script tester is uploaded to cloudflare")

    if cf.worker.download("tester"):
        print(f"Worker script tester is downloaded and written in to tester.js")

    if cf.worker.delete("tester"):
        print(f"Worker script tester is deleted from cloudflare")

    if cf.store.delete("my_new_kv"):
        print("The namespace 'my_new_kv' is deleted")


if __name__ == "__main__":
    main()
