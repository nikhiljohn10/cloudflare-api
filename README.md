# cloudflare-api
Python client for Cloudflare API v4

## Usage

### Python Package

```bash
pip install cloudflare-api
```

Sample code can be found inside [/test.py](https://github.com/nikhiljohn10/cloudflare-api/blob/main/test.py) 

### Source Code

```bash
git clone https://github.com/nikhiljohn10/cloudflare-api
cd cloudflare-api
```

Create a `secret.py` in the root directory with following content:
```python
API_TOKEN = ""
ACCOUNT_ID = ""
```
The above variable need to be assigned with your own api token and account id from Cloudflare dashboard.

Then run the following command in terminal:
```bash
make test
```

## Example

For this example, `poetry` is used for easy setup.
```bash
python3 -m pip install poetry
poetry new cloudflare-app
cd cloudflare-app
poetry add cloudflare-api
```

Copy the code below in to a new file `./cloudflare-app/__main__.py`. Then replace `API_TOKEN` & `ACCOUNT_ID` values with values obtained from Cloudflare dashboard.
```python
#!/usr/bin/env python3

from CloudflareAPI import Cloudflare, jsonPrint

API_TOKEN = ""
ACCOUNT_ID = ""

def main():
  cf = Cloudflare(token=API_TOKEN, account_id=ACCOUNT_ID)
  print(cf.worker.list())
  print(cf.store.list())
```

Now we can run our program using following command:
```
poetry run python cloudflare-app
```

## Available endpoints

### Worker Script

- [x] `list` - List all existing workers
- [x] `upload` - Upload a new worker with binding if given
- [x] `download` - Download an existing worker
- [x] `delete` - Delete an existing worker

### Workers KV

- [x] `list` - List all existing Namespaces
- [x] `id` - Find the namespace id of the namespace
- [x] `create` - Create a new namespace
- [x] `rename` - Rename an existing namespace
- [x] `delete` - Delete an existing namespace
