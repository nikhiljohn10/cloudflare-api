#!/usr/bin/env python3

import sys

sys.path.append(".")

from CloudflareAPI import Cloudflare, Fetch, wait_result


def main():
    worker_name = "testing"

    # Cloudflare
    cf = Cloudflare()

    # Account.list
    accounts = cf.account.list()
    print("Accounts:", accounts)

    # Account.get_id
    account_id = cf.account.get_id()
    print("Account ID: ", account_id)

    # Account.details
    details = cf.account.details(formated=True)
    print("Account Details:", details)

    # User.details
    print("User Details:", cf.user.details(formated=True))

    # Worker.list
    workers = cf.worker.list(formated=True)
    print("Workers:", workers)

    # Store.list
    store = cf.store.list()
    print("Stores:", store)

    # Store.create
    if cf.store.create("my_kv"):
        print("New namespace my_kv is created")

    # Store.rename
    if cf.store.rename("my_kv", "my_new_kv"):
        print("New namespace my_kv is renamed to my_new_kv")

    # Store.get_id
    ns_id, ns1 = cf.store.get_ns("my_new_kv")

    print("Namespace:", ns1)

    # Store.Namespace.write
    if ns1.write("test", "this is a test value"):
        result = wait_result(ns1.read, "test")
        print(f"\rWritten data to NS Key test: {result}")

    # Store.Namespace.Metadata
    nsmeta = ns1.Metadata("metaTest", "This is meta of test")

    # Store.Namespace.write with metadata
    if ns1.write("test2", "this is a test value 2", metadata=nsmeta):
        result = wait_result(ns1.read, "test2")
        print(f"\rWritten data to NS Key test2: {result}")

    # Store.Namespace.NSBundler
    bundle = ns1.NSBundler()

    # Store.Namespace.NSBundler.add
    bundle.add("test3", "this is a test value 3", metadata=nsmeta, expiration_ttl=200)

    # Store.Namespace.NSBundler.add with base64 encoding
    bundle.add("test4", "dGhpcyBpcyBhIHRlc3QgdmFsdWUgNA==", base64=True)

    # Store.Namespace.bulk_write
    if ns1.bulk_write(bundle=bundle):
        result = wait_result(ns1.read, "test3")
        print(f"\rWritten data to NS Key test3: {result}")
        result = wait_result(ns1.read, "test4")
        print(f"\rWritten data to NS Key test4: {result}")

    # Store.Namespace.keys
    print("Keys:", ns1.keys())

    # Worker.Metadata
    metadata = cf.worker.Metadata()

    # Worker.Metadata.add_binding
    metadata.add_binding("my_new_kv", ns_id)

    # Worker.Metadata.add_variable
    metadata.add_variable("my_new_var", "This is a new variable")

    # Worker.Metadata.add_secret
    metadata.add_secret("my_new_secret", "This is secret")

    print("Worker Metadata:", metadata)

    # Worker.upload
    if cf.worker.upload(worker_name, "tests/test.js", metadata):
        print(f"Worker script {worker_name} is uploaded to cloudflare")

    # # Worker.deploy
    if cf.worker.deploy(worker_name):
        print(f"Worker script {worker_name} is deployed to cloudflare network")

    # Worker.Cron.update (Run cron script every 12 hour)
    # ( Cron require ScheduledEvent )
    # https://developers.cloudflare.com/workers/runtime-apis/scheduled-event
    if cf.worker.cron.update(worker_name, crons=["* */12 * * 2-6", "* 2 * * 1"]):
        print(f"Cron for worker {worker_name} is updated successfully")

    # Worker.Cron.get
    print(f"The worker {worker_name} cron list:")
    for cron in cf.worker.cron.get(worker_name):
        print(f"  [ {cron['cron']} ]")

    # # Worker.Subdomain.create
    # # [ Raise error if subdomain exists for current account ]
    # subdomain = cf.worker.subdomain.create("test-subdomain")

    # Worker.Subdomain.get
    subdomain = cf.worker.subdomain.get()

    # Response from deployed worker
    fetch = Fetch(f"https://{worker_name}.{subdomain}.workers.dev")

    # Get key-value pair in the MY_NEW_KV Namespace
    kv_response = fetch("/kv")
    print("\rKV Response:", kv_response)

    # Get environment variable from worker
    var_response = fetch("/var")
    print("\rVariable Response:", var_response)

    # Get secret variable from worker
    secret_response = fetch("/secret")
    print("\rSecret Response:", secret_response)

    # Store.Namespace.delete
    if ns1.delete("test"):
        print("Deteled test key from namespace")

    # Store.Namespace.bulk_delete
    if ns1.bulk_delete(["test2", "test3", "test4"]):
        print("Deteled test2, test3 & test4 key from namespace")

    # Worker.undeploy
    if cf.worker.undeploy(worker_name):
        print(f"Worker script {worker_name} is undeployed from cloudflare network")

    # Worker.download
    if cf.worker.download(worker_name):
        print(f"Worker script {worker_name} is downloaded as {worker_name}.js")

    # Worker.delete
    if cf.worker.delete(worker_name):
        print(f"Worker script {worker_name} is deleted from cloudflare")

    # Store.delete
    if cf.store.delete("my_new_kv"):
        print("The namespace my_new_kv is deleted")

    print("Cloudflare API test completed successfully")


if __name__ == "__main__":
    main()
