#!/usr/bin/env python3

import sys

sys.path.append(".")

from CloudflareAPI import Cloudflare, Fetch, wait_result
from CloudflareAPI.exceptions import APIError, CFError


class MyApp(Cloudflare):
    def __init__(self, worker_name) -> None:
        self.worker_name = worker_name
        self.__current_namespace = None
        super().__init__()

    def show_info(self):
        # Account.list
        accounts = self.account.list()
        print("Accounts:", accounts)

        # Account.get_id
        account_id = self.account.get_id()
        print("Account ID: ", account_id)

        # Account.details
        details = self.account.details(formated=True)
        print("Account Details:", details)

        # User.details
        print("User Details:", self.user.details(formated=True))

        # Worker.list
        workers = self.worker.list(formated=True)
        print("Workers:", workers)

        # Store.list
        store = self.store.list()
        print("Stores:", store)

    def setup_namespace(self):
        ns = self.__current_namespace

        # Store.Namespace.write
        if ns.write("test", "this is a test value"):
            result = wait_result(ns.read, "test")
            print(f"\rWritten data to NS Key test: {result}")

        # Store.Namespace.Metadata
        nsmeta = ns.Metadata("metaTest", "This is meta of test")

        # Store.Namespace.write with metadata
        if ns.write("test2", "this is a test value 2", metadata=nsmeta):
            result = wait_result(ns.read, "test2")
            print(f"\rWritten data to NS Key test2: {result}")

        # Store.Namespace.NSBundler
        bundle = ns.NSBundler()

        # Store.Namespace.NSBundler.add
        bundle.add(
            "test3", "this is a test value 3", metadata=nsmeta, expiration_ttl=200
        )

        # Store.Namespace.NSBundler.add with base64 encoding
        bundle.add("test4", "dGhpcyBpcyBhIHRlc3QgdmFsdWUgNA==", base64=True)

        # Store.Namespace.bulk_write
        if ns.bulk_write(bundle=bundle):
            result = wait_result(ns.read, "test3")
            print(f"\rWritten data to NS Key test3: {result}")
            result = wait_result(ns.read, "test4")
            print(f"\rWritten data to NS Key test4: {result}")

        # Store.Namespace.keys
        print("Keys:", ns.keys())

    def prepare_store(self):
        try:
            # Store.create
            if self.store.create("my_kv"):
                print("New namespace my_kv is created")

            # Store.rename
            if self.store.rename("my_kv", "my_new_kv"):
                print("New namespace my_kv is renamed to my_new_kv")
        except APIError:
            pass

        try:
            # Store.get_ns
            self.__current_namespace = self.store.get_ns("my_new_kv")
        except CFError:
            # Store.create
            if self.store.create("my_new_kv"):
                print("New namespace my_new_kv is created")
                self.__current_namespace = self.store.get_ns("my_new_kv")

        print("Namespace:", self.__current_namespace)

        self.setup_namespace()

    def prepare_worker(self):
        ns = self.__current_namespace

        # Worker.Metadata
        metadata = self.worker.Metadata()

        # Worker.Metadata.add_binding
        metadata.add_binding("my_new_kv", ns.id)

        # Worker.Metadata.add_variable
        metadata.add_variable("my_new_var", "This is a new variable")

        # Worker.Metadata.add_secret
        metadata.add_secret("my_new_secret", "This is secret")

        print("Worker Metadata:", metadata)

        return metadata

    def deploy_worker(self):
        ns = self.__current_namespace
        metadata = self.prepare_worker()

        # Worker.upload
        if self.worker.upload(self.worker_name, "tests/test.js", metadata):
            print(f"Worker script {self.worker_name} is uploaded to cloudflare")

        # # Worker.deploy
        if self.worker.deploy(self.worker_name):
            print(f"Worker script {self.worker_name} is deployed to cloudflare network")

    def update_cron(self):
        # Worker.Cron.update (Run cron script every 12 hour)
        # ( Cron require ScheduledEvent )
        # https://developers.cloudflare.com/workers/runtime-apis/scheduled-event
        if self.worker.cron.update(
            self.worker_name, crons=["* */12 * * 2-6", "* 2 * * 1"]
        ):
            print(f"Cron for worker {self.worker_name} is updated successfully")

        # Worker.Cron.get
        print(f"The worker {self.worker_name} cron list:")
        for cron in self.worker.cron.get(self.worker_name):
            print(f"  [ {cron['cron']} ]")

    def check_worker(self):

        # # Worker.Subdomain.create
        # # [ Raise error if subdomain exists for current account ]
        # subdomain = self.worker.subdomain.create("test-subdomain")

        # Worker.Subdomain.get
        subdomain = self.worker.subdomain.get()

        # Response from deployed worker
        fetch = Fetch(f"https://{self.worker_name}.{subdomain}.workers.dev")

        # Get key-value pair in the MY_NEW_KV Namespace
        kv_response = fetch("/kv")
        print("\rKV Response:", kv_response)

        # Get environment variable from worker
        var_response = fetch("/var")
        print("\rVariable Response:", var_response)

        # Get secret variable from worker
        secret_response = fetch("/secret")
        print("\rSecret Response:", secret_response)

        # Worker.download
        if self.worker.download(self.worker_name):
            print(
                f"Worker script {self.worker_name} is downloaded as {self.worker_name}.js"
            )

    def clean_worker(self):

        # Worker.undeploy
        if self.worker.undeploy(self.worker_name):
            print(
                f"Worker script {self.worker_name} is undeployed from cloudflare network"
            )

        # Worker.delete
        if self.worker.delete(self.worker_name):
            print(f"Worker script {self.worker_name} is deleted from cloudflare")

    def clean_store(self):
        ns = self.__current_namespace

        # Store.Namespace.delete
        if ns.delete("test"):
            print("Deteled test key from namespace")

        # Store.Namespace.bulk_delete
        if ns.bulk_delete(["test2", "test3", "test4"]):
            print("Deteled test2, test3 & test4 key from namespace")

        # Store.delete
        if self.store.delete("my_new_kv"):
            print("The namespace my_new_kv is deleted")

    def clean(self):
        self.clean_worker()
        self.clean_store()


def main():

    # Cloudflare
    app = MyApp(worker_name="testing")

    app.show_info()
    app.prepare_store()
    app.deploy_worker()
    app.update_cron()
    app.check_worker()
    app.clean()

    print("Cloudflare API test completed successfully")


if __name__ == "__main__":
    main()
