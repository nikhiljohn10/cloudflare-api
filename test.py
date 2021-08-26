#!/usr/bin/env python3

from cloudflare import Cloudflare, Worker, Storage
from secret import API_TOKEN, ACCOUNT_ID

NAMESPACE = "todo"
WORKER_NAME = "tester"

cf = Cloudflare(
    key=API_TOKEN,
    id=ACCOUNT_ID,
    verbose=True,
)

store = Storage(cf)
worker = Worker(cf)

print("Storage: ", store.list())
store.create(NAMESPACE)
print("Storage: ", store.list())
todo_id = store.id(NAMESPACE)

print("Workers: ", worker.list())
worker.upload(
    name=WORKER_NAME,
    file="test.js",
    bindings=dict(name=NAMESPACE, id=todo_id)
)
print("Workers: ", worker.list())
