#!/usr/bin/env python3

import requests
from CloudflareAPI import Cloudflare, jsonPrint

from secret import API_TOKEN


def main():
    worker_name = "tester"

    cf = Cloudflare(token=API_TOKEN)

    # Account.list
    accounts = cf.account.list()
    jsonPrint(accounts, "Accounts")

    # Worker.list
    workers = cf.worker.list()
    jsonPrint(workers, "Workers")

    # Store.list
    store = cf.store.list()
    jsonPrint(store, "Store")

    # Store.create
    if cf.store.create("my_kv"):
        print("New namespace 'my_kv' is created")

    # Store.rename
    if cf.store.rename("my_kv", "my_new_kv"):
        print("New namespace 'my_kv' is renamed to 'my_new_kv'")

    ns_id = cf.store.get_id("my_new_kv")
    print("Namespace ID: ", ns_id)

    # Worker.upload
    if cf.worker.upload(
        name=worker_name, file="test.js", bindings=dict(name="my_new_kv", id=ns_id)
    ):
        print(f"Worker script {worker_name} is uploaded to cloudflare")

    # Worker.deploy
    if cf.worker.deploy(worker_name):
        print(f"Worker script {worker_name} is deployed to cloudflare network")

    # Worker.Subdomain.create
    # [ Raise error if subdomain exists for current account ]
    # subdomain = cf.worker.subdomain.create("test-subdomain")

    # Worker.Subdomain.get
    subdomain = cf.worker.subdomain.get()
    url = f"https://{worker_name}.{subdomain}.workers.dev"

    # Response from deployed worker
    print(f"{worker_name.title()} URL:", url)
    response = requests.get(url)
    if response.ok:
        print("URL Response:", response.text)

    # Worker.undeploy
    if cf.worker.undeploy(worker_name):
        print(f"Worker script {worker_name} is undeployed from cloudflare network")

    # Worker.download
    if cf.worker.download(worker_name):
        print(
            f"Worker script {worker_name} is downloaded and written in to {worker_name}.js"
        )

    # Worker.delete
    if cf.worker.delete(worker_name):
        print(f"Worker script {worker_name} is deleted from cloudflare")

    # Store.delete
    if cf.store.delete("my_new_kv"):
        print("The namespace 'my_new_kv' is deleted")


if __name__ == "__main__":
    main()
