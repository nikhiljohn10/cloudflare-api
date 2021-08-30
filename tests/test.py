#!/usr/bin/env python3

import sys

sys.path.append(".")

from CloudflareAPI import Cloudflare, jsonPrint, Fetch

from secret import API_TOKEN


def main():
    worker_name = "testing"

    # Cloudflare
    cf = Cloudflare(API_TOKEN)

    # Account.list
    accounts = cf.account.list()
    jsonPrint(accounts, "Accounts")

    # Account.get_id
    account_id = cf.account.get_id()

    # Account.details
    details = cf.account.details(account_id)
    jsonPrint(details, "Account Details:")

    # User.details
    jsonPrint(cf.user.details(), "User Details:")

    # Worker.list
    workers = cf.worker.list()
    jsonPrint(workers, "Workers")

    # Store.list
    store = cf.store.list()
    jsonPrint(store, "Store")

    # Store.create
    if cf.store.create("my_kv"):
        print("New namespace my_kv is created")

    # Store.rename
    if cf.store.rename("my_kv", "my_new_kv"):
        print("New namespace my_kv is renamed to my_new_kv")

    # Store.get_id
    ns_id = cf.store.get_id("my_new_kv")
    print("Namespace ID: ", ns_id)

    # Worker.Metadata
    metadata = cf.worker.Metadata()
    metadata.add_binding("my_new_kv", ns_id)
    metadata.add_variable("my_new_var", "This is a new variable")
    metadata.add_secret("my_new_secret", "This is secret")

    # Worker.upload
    if cf.worker.upload(worker_name, "tests/test.js", metadata):
        print(f"Worker script {worker_name} is uploaded to cloudflare")

    # Worker.deploy
    if cf.worker.deploy(worker_name):
        print(f"Worker script {worker_name} is deployed to cloudflare network")

    # Worker.Corn.update (Run corn script every 12 hour)
    # ( Corn require ScheduledEvent )
    # https://developers.cloudflare.com/workers/runtime-apis/scheduled-event
    cf.worker.corn.update(worker_name, corns=list(dict(corn="* */12 * * *")))

    # Worker.Corn.get
    corn = cf.worker.corn.get(worker_name)
    if corn:
        print(f"The worker {worker_name} corn is", corn["cron"])

    # Worker.Subdomain.create
    # [ Raise error if subdomain exists for current account ]
    # subdomain = cf.worker.subdomain.create("test-subdomain")

    # Worker.Subdomain.get
    subdomain = cf.worker.subdomain.get()

    # Response from deployed worker
    fetch = Fetch(f"https://{worker_name}.{subdomain}.workers.dev")

    # Set key-value pair in the MY_NEW_KV Namespace
    fetch("/set")

    # Get key-value pair in the MY_NEW_KV Namespace
    kv_response = fetch("/kv")
    print("\rKV Response:", kv_response)

    # Get environment variable from worker
    var_response = fetch("/var")
    print("\rVariable Response:", var_response)

    # Get secret variable from worker
    secret_response = fetch("/secret")
    print("\rSecret Response:", secret_response)

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
        print("The namespace my_new_kv is deleted")


if __name__ == "__main__":
    main()
