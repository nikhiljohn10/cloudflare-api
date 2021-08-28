#!/usr/bin/env python3

import secrets
import requests
from CloudflareAPI import Cloudflare, jsonPrint

from secret import API_TOKEN, ACCOUNT_ID


def main():
    worker_name = "tester"

    cf = Cloudflare(token=API_TOKEN, account_id=ACCOUNT_ID)

    accounts = cf.account.list()
    jsonPrint(accounts, "Accounts")

    workers = cf.worker.list()
    jsonPrint(workers, "Workers")

    store = cf.store.list()
    jsonPrint(store, "Store")

    if cf.store.create("my_kv"):
        print("New namespace 'my_kv' is created")

    if cf.store.rename("my_kv", "my_new_kv"):
        print("New namespace 'my_kv' is renamed to 'my_new_kv'")

    ns_id = cf.store.get_id("my_new_kv")
    print("Namespace ID: ", ns_id)

    if cf.worker.upload(
        name=worker_name, file="test.js", bindings=dict(name="my_new_kv", id=ns_id)
    ):
        print(f"Worker script {worker_name} is uploaded to cloudflare")

    if cf.worker.deploy(worker_name):
        print(f"Worker script {worker_name} is deployed to cloudflare network")

    subdomain = cf.worker.subdomain.get()
    url = f"https://{worker_name}.{subdomain}.workers.dev"
    print(f"{worker_name.title()} URL:", url)
    response = requests.get(url)
    if response.ok:
        print("URL Response:", response.text)

    if cf.worker.undeploy(worker_name):
        print(f"Worker script {worker_name} is undeployed from cloudflare network")

    if cf.worker.download(worker_name):
        print(
            f"Worker script {worker_name} is downloaded and written in to {worker_name}.js"
        )

    if cf.worker.delete(worker_name):
        print(f"Worker script {worker_name} is deleted from cloudflare")

    if cf.store.delete("my_new_kv"):
        print("The namespace 'my_new_kv' is deleted")


if __name__ == "__main__":
    main()
