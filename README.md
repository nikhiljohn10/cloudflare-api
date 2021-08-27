# pycf
Python client for Cloudflare API v4

## Usage

Create a `secret.py` in the root directory with following content:
```
API_TOKEN = ""
ACCOUNT_ID = ""
```
The above variable need to be assigned with your own api token and account id from Cloudflare dashboard.

Then run the following command in terminal:
```
./test.py
```

## Available endpoints

### Worker Script

- [x] list - List all existing workers
- [x] upload - Upload a new worker with binding if given
- [x] download - Download an existing worker
- [x] delete - Delete an existing worker

### Workers KV

- [x] list - List all existing Namespaces
- [x] id - Find the namespace id of the namespace
- [x] create - Create a new namespace
- [x] rename - Rename an existing namespace
- [x] delete - Delete an existing namespace
