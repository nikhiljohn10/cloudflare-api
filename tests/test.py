#!/usr/bin/env python3

import sys
from time import sleep

sys.path.append(".")

from CloudflareAPI import Cloudflare, Fetch, jsonPrint


def wait_result(func, *args, **kargs):
    while True:
        try:
            result = func(*args, **kargs)
            print(f"\r{result}")
        except:
            print("\rWaiting for result...", end="")
            sleep(0.1)
            continue
        break


def main():
    worker_name = "testing"

    # Cloudflare
    cf = Cloudflare()

    # # Account.list
    # accounts = cf.account.list()
    # jsonPrint(accounts, "Accounts")

    # # Account.get_id
    # account_id = cf.account.get_id()
    # print("Account ID: ", account_id)

    # # Account.details
    # details = cf.account.details()
    # jsonPrint(details, "Account Details:")

    # # User.details
    # jsonPrint(cf.user.details(), "User Details:")

    # # Worker.list
    # workers = cf.worker.list()
    # jsonPrint(workers, "Workers")

    # Store.list
    store = cf.store.list()
    print(store)

    # # Store.create
    # if cf.store.create("my_kv"):
    #     print("New namespace my_kv is created")

    # Store.rename
    if cf.store.rename("my_kv", "my_new_kv"):
        print("New namespace my_kv is renamed to my_new_kv")

    # Store.get_id
    ns_id, ns1 = cf.store.get_ns("my_new_kv")

    # print(ns1)
    # keys = ns1.keys()
    # print(keys)
    # for key in keys:
    #     print(ns1.read(key))
    #     break
    # if ns1.write("test", "this is a test value"):
    #     wait_result(ns1.read, "test")

    # nsmeta = ns1.Metadata("metaTest", "This is meta of test")
    # if ns1.write("test2", "this is a test value 2", metadata=nsmeta):
    #     wait_result(ns1.read, "test2")

    # bundle = ns1.NSBundler()
    # bundle.add("k1", "hello", metadata=nsmeta, expiration_ttl=200)
    # bundle.add("k2", "d29ybGQ=", metadata=nsmeta, base64=True)
    # if ns1.bulk_write(bundle=bundle):
    #     wait_result(ns1.read, "k1")
    #     wait_result(ns1.read, "k2")

    # keys = ns1.keys()
    # print(keys)

    # if ns1.delete("test"):
    #     print("Deteled test key from namespace")

    # if ns1.bulk_delete(["test2", "k1", "k2"]):
    #     print("Deteled test2, k1 & k2 key from namespace")

    # # Worker.Metadata
    # metadata = cf.worker.Metadata()
    # metadata.add_binding("my_new_kv", ns_id)
    # metadata.add_variable("my_new_var", "This is a new variable")
    # metadata.add_secret("my_new_secret", "This is secret")

    # # Worker.upload
    # if cf.worker.upload(worker_name, "tests/test.js", metadata):
    #     print(f"Worker script {worker_name} is uploaded to cloudflare")

    # # Worker.deploy
    # if cf.worker.deploy(worker_name):
    #     print(f"Worker script {worker_name} is deployed to cloudflare network")

    # # Worker.Cron.update (Run cron script every 12 hour)
    # # ( Cron require ScheduledEvent )
    # # https://developers.cloudflare.com/workers/runtime-apis/scheduled-event
    # if cf.worker.cron.update(worker_name, crons=["* */12 * * 2-6", "* 2 * * 1"]):
    #     print(f"Cron for worker {worker_name} is updated successfully")

    # # Worker.Cron.get
    # print(f"The worker {worker_name} cron list:")
    # for cron in cf.worker.cron.get(worker_name):
    #     print(f"  - {cron['cron']}")

    # # Worker.Subdomain.create
    # # [ Raise error if subdomain exists for current account ]
    # # subdomain = cf.worker.subdomain.create("test-subdomain")

    # # Worker.Subdomain.get
    # subdomain = cf.worker.subdomain.get()

    # # Response from deployed worker
    # fetch = Fetch(f"https://{worker_name}.{subdomain}.workers.dev")

    # # Set key-value pair in the MY_NEW_KV Namespace
    # fetch("/set")

    # # Get key-value pair in the MY_NEW_KV Namespace
    # kv_response = fetch("/kv")
    # print("\rKV Response:", kv_response)

    # # Get environment variable from worker
    # var_response = fetch("/var")
    # print("\rVariable Response:", var_response)

    # # Get secret variable from worker
    # secret_response = fetch("/secret")
    # print("\rSecret Response:", secret_response)

    # # Worker.undeploy
    # if cf.worker.undeploy(worker_name):
    #     print(
    #         f"Worker script {worker_name} is undeployed from cloudflare network")

    # # Worker.download
    # if cf.worker.download(worker_name):
    #     print(
    #         f"Worker script {worker_name} is downloaded and written in to {worker_name}.js"
    #     )

    # # Worker.delete
    # if cf.worker.delete(worker_name):
    #     print(f"Worker script {worker_name} is deleted from cloudflare")

    # # Store.delete
    # if cf.store.delete("my_new_kv"):
    #     print("The namespace my_new_kv is deleted")


if __name__ == "__main__":
    main()
