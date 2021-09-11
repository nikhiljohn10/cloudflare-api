#!/usr/bin/env python3

from secrets import token_urlsafe
from CloudflareAPI import Cloudflare
from CloudflareAPI.exceptions import CFError


class ExampleWorker:
    WORKER_NS_NAME_KEY = "DEPLOYMENT_EXAMPLE_NS"
    WORKER_VARIABLE_KEY = "WEBSITE_TITLE"
    WORKER_SECRET_KEY = "SECRET_WEBSITE_TOKEN"

    def deploy(self, name: str, file: str):
        api = Cloudflare()
        token = token_urlsafe()
        print("Secret token generated:", token)

        try:
            namespace = api.store.get_ns(self.WORKER_NS_NAME_KEY)
            print("Namespace found")
        except CFError:
            namespace = api.store.create(self.WORKER_NS_NAME_KEY)
            print("Namespace created")

        namespace.write("greeting", "Hello World!")
        print("Secret written to namespace")

        metadata = api.worker.Metadata()
        metadata.add_binding(self.WORKER_NS_NAME_KEY, namespace.id)
        metadata.add_variable(self.WORKER_VARIABLE_KEY, "Greetings!")
        metadata.add_secret(self.WORKER_SECRET_KEY, token)
        print("Generated worker metadata")

        if api.worker.upload(name, file, metadata):
            print("Worker is uploaded")
            if api.worker.deploy(name):
                subdomain = api.worker.subdomain.get()
                url = f"https://{name}.{subdomain}.workers.dev"
                return url, f"{url}/{token}"

        raise CFError("Deployment failed")


def main():
    worker = ExampleWorker()
    url, secret_url = worker.deploy(
        name="test-worker", file="./examples/sample_data/worker.js"
    )
    print("Deployed successfully to", url)
    print("Your secret message is at", secret_url)


if __name__ == "__main__":
    main()
