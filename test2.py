#!/usr/bin/env python3

from CloudflareAPI import Cloudflare, jsonPrint

from secret import API_TOKEN, ACCOUNT_ID

def main():
    cf = Cloudflare(token=API_TOKEN, account_id=ACCOUNT_ID)
    workers = cf.worker.list()
    store = cf.store.list()
    jsonPrint(workers, "Workers")
    jsonPrint(store, "Store")
    id = cf.store.id("todo")
    print("ID: ", id)
    if cf.store.create("my_kv"):
        print("New namespace 'my_kv' is created")
    if cf.store.delete("my_kv"):
        print("The namespace 'my_kv' is deleted")

if __name__ == "__main__":
    main()
