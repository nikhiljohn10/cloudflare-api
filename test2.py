#!/usr/bin/env python3

from CloudflareAPI import Cloudflare, jsonPrint

from secret import API_TOKEN, ACCOUNT_ID


def main():
    cf = Cloudflare(token=API_TOKEN, account_id=ACCOUNT_ID)

    workers = cf.worker.list()
    jsonPrint(workers, "Workers")

    store = cf.store.list()
    jsonPrint(store, "Store")

    id = cf.store.id("todo")
    print("ID: ", id)

    if cf.store.create("my_kv"):
        print("New namespace 'my_kv' is created")
    if cf.store.rename("my_kv", "my_new_kv"):
        print("New namespace 'my_kv' is renamed to 'my_new_kv'")
    if cf.store.delete("my_new_kv"):
        print("The namespace 'my_new_kv' is deleted")

    if cf.worker.download("tester"):
        print(f"Worker script written in to tester.js")
    if cf.worker.upload(
        name="tester2", file="test.js", bindings=dict(name="todo", id=id)
    ):
        print("Worker script tester is uploaded to cloudflare")
    else:
        print("Unkown error while uploading worker script tester")


if __name__ == "__main__":
    main()
